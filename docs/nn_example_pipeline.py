"""Reproduce SPY forecasts with annual sliding-window estimation.

The direct FNN uses 22 daily inputs; Simple RNN and LSTM use 756.
Every model is estimated on the most recent 756 training examples.

Data stay in the private TAQ directory. Run --all for all ten model/target
pairs; --assemble rebuilds the summary from completed per-model results.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

os.environ.setdefault("KERAS_BACKEND", "tensorflow")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "nn-example-mpl"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "nn-example-cache"))
os.environ.setdefault("TF_NUM_INTRAOP_THREADS", "2")
os.environ.setdefault("TF_NUM_INTEROP_THREADS", "1")

import numpy as np
import pandas as pd

INPUT_DAYS = 756
FNN_INPUT_DAYS = 22
ESTIMATION_EXAMPLES = 756
VALIDATION_START = pd.Timestamp("2022-01-01")
TEST_START = pd.Timestamp("2023-01-01")
TEST_END = pd.Timestamp("2024-12-31")
N_TRIALS = 20
MAX_EPOCHS = 30
SEED = 0
MODELS = ("HAR-OLS", "HAR-FNN", "FNN", "Simple RNN", "LSTM")
TARGETS = ("log(rv)", "rv")
ROOT = Path(__file__).resolve().parent


def load_data(path):
    data = pd.read_csv(path, parse_dates=["date"]).sort_values("date")
    data = data.loc[data.date <= TEST_END, ["date", "rv"]].reset_index(drop=True)
    if data.date.duplicated().any() or not data.date.is_monotonic_increasing:
        raise ValueError("Dates must be distinct and increasing.")
    if not np.isfinite(data.rv).all() or not (data.rv > 0).all():
        raise ValueError("Every observed trading-day RV must be finite and positive.")
    return data


def make_inputs(data, input_days=INPUT_DAYS):
    """One row per target date; all inputs end on its preceding trading day."""
    rv = data.rv.to_numpy(dtype=float)
    z = np.log(rv)
    targets = np.arange(input_days, len(data))
    lag_rv = np.stack([rv[t-input_days:t] for t in targets])
    har_rv = np.array([[rv[t-1], rv[t-5:t].mean(), rv[t-21:t].mean()]
                       for t in targets])
    return {
        "dates": data.date.iloc[targets].reset_index(drop=True),
        "target_positions": targets,
        "lag_log": np.log(lag_rv), "lag_rv": lag_rv,
        "har_log": np.log(har_rv), "har_rv": har_rv,
        "y_log": z[targets], "y_rv": rv[targets],
    }


def estimation_indices(dates, first_forecast_date, n_examples=ESTIMATION_EXAMPLES):
    """The last n_examples outcomes observed before this forecast target."""
    idx = np.flatnonzero(np.asarray(dates < first_forecast_date))
    if len(idx) < n_examples:
        raise ValueError("Not enough forecast-origin examples for the estimation window.")
    return idx[-n_examples:]


def arrays_for(panel, model_name, target):
    prefix = "har" if model_name.startswith("HAR") else "lag"
    suffix = "log" if target == "log(rv)" else "rv"
    X = panel[f"{prefix}_{suffix}"]
    if model_name == "FNN":
        X = X[:, -FNN_INPUT_DAYS:]
    return X, panel[f"y_{suffix}"]


def fit_scaler(X, y, model_name, target):
    """Fit only on the current estimation examples, including their inputs."""
    y_center, y_scale = float(y.mean()), float(y.std())
    if y_scale <= 0:
        raise ValueError("The estimation targets have zero variance.")
    if not model_name.startswith("HAR") and target == "log(rv)":
        x_center, x_scale = y_center, y_scale
    else:
        x_center, x_scale = X.mean(axis=0), X.std(axis=0)
        x_scale = np.where(x_scale > 0, x_scale, 1.0)
    return {"x_center": x_center, "x_scale": x_scale,
            "y_center": y_center, "y_scale": y_scale}


def transform(X, y, scaler, model_name):
    X_scaled = ((X-scaler["x_center"])/scaler["x_scale"]).astype("float32")
    y_scaled = ((y-scaler["y_center"])/scaler["y_scale"]).astype("float32")
    if model_name in ("Simple RNN", "LSTM"):
        X_scaled = X_scaled[..., np.newaxis]
    return X_scaled, y_scaled


def make_network(model_name, input_shape, width, learning_rate):
    import keras
    from keras import layers
    keras.backend.clear_session()
    keras.utils.set_random_seed(SEED)
    if model_name in ("FNN", "HAR-FNN"):
        hidden = layers.Dense(width, activation="softplus")
    elif model_name == "Simple RNN":
        hidden = layers.SimpleRNN(width, activation="tanh", stateful=False)
    elif model_name == "LSTM":
        hidden = layers.LSTM(width, activation="tanh", stateful=False)
    else:
        raise ValueError(model_name)
    model = keras.Sequential([keras.Input(shape=input_shape), hidden, layers.Dense(1)])
    # Clip the stacked raw gradient, following the recurrent-network chapter.
    model.compile(loss="mse", optimizer=keras.optimizers.Adam(
        learning_rate=learning_rate, global_clipnorm=1.0))
    return model


def tune_network(panel, model_name, target, trials=N_TRIALS, max_epochs=MAX_EPOCHS):
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    dates = panel["dates"]
    tr = estimation_indices(dates, VALIDATION_START)
    va = np.flatnonzero(np.asarray((dates >= VALIDATION_START) & (dates < TEST_START)))
    X, y = arrays_for(panel, model_name, target)
    scaler = fit_scaler(X[tr], y[tr], model_name, target)
    X_tr, y_tr = transform(X[tr], y[tr], scaler, model_name)
    X_va, y_va = transform(X[va], y[va], scaler, model_name)
    trial_rows = []

    def objective(trial):
        start = time.monotonic()
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-3, log=True),
            "batch_size": trial.suggest_int("batch_size", 16, 64, step=4),
            "width": trial.suggest_int("width", 16, 96, step=4),
        }
        model = make_network(model_name, X_tr.shape[1:], params["width"], params["learning_rate"])
        history = model.fit(X_tr, y_tr, validation_data=(X_va, y_va),
                            epochs=max_epochs, batch_size=params["batch_size"],
                            shuffle=False, verbose=0)
        losses = np.asarray(history.history["val_loss"], dtype=float)
        if not np.isfinite(losses).all():
            raise FloatingPointError("Nonfinite validation loss; investigate before using results.")
        best_epoch = int(np.argmin(losses))+1
        best_loss = float(losses[best_epoch-1])
        trial.set_user_attr("best_epoch", best_epoch)
        trial.set_user_attr("parameters", model.count_params())
        row = dict(trial=trial.number, **params, best_epoch=best_epoch,
                   validation_loss=best_loss, parameters=model.count_params(),
                   seconds=round(time.monotonic()-start, 2))
        trial_rows.append(row)
        print(json.dumps({"stage": "trial", "model": model_name, "target": target, **row}), flush=True)
        return best_loss

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=1))
    study.optimize(objective, n_trials=trials)
    best = dict(study.best_params, **study.best_trial.user_attrs,
                validation_loss=float(study.best_value))
    return best, trial_rows


def score_forecasts(rv_true, rv_hat):
    rv_true, rv_hat = np.asarray(rv_true), np.asarray(rv_hat)
    if not np.isfinite(rv_hat).all():
        raise FloatingPointError("Nonfinite forecast.")
    nonpositive = int(np.count_nonzero(rv_hat <= 0))
    if nonpositive:
        rmse_log = mae_log = qlike = None
    else:
        log_error = np.log(rv_hat)-np.log(rv_true)
        ratio = rv_true/rv_hat
        rmse_log = float(np.sqrt(np.mean(log_error**2)))
        mae_log = float(np.mean(np.abs(log_error)))
        qlike = float(np.mean(ratio-np.log(ratio)-1))
    return {"rmse_log_rv": rmse_log, "mae_log_rv": mae_log,
            "rmse_rv": float(np.sqrt(np.mean((rv_hat-rv_true)**2))),
            "mae_rv": float(np.mean(np.abs(rv_hat-rv_true))), "qlike": qlike,
            "nonpositive_rv_forecasts": nonpositive}


def annual_forecasts(panel, model_name, target, params):
    """Refit once per test year on a sliding window; freeze within the year."""
    from sklearn.linear_model import LinearRegression
    dates = panel["dates"]
    X, y = arrays_for(panel, model_name, target)
    predictions, records = [], []
    for year in sorted(dates.loc[dates >= TEST_START].dt.year.unique()):
        te = np.flatnonzero(np.asarray((dates >= TEST_START) & (dates.dt.year == year)))
        first_date = dates.iloc[te[0]]
        tr = estimation_indices(dates, first_date)
        if model_name == "HAR-OLS":
            model = LinearRegression().fit(X[tr], y[tr])
            target_hat = model.predict(X[te])
        else:
            scaler = fit_scaler(X[tr], y[tr], model_name, target)
            X_tr, y_tr = transform(X[tr], y[tr], scaler, model_name)
            X_te, _ = transform(X[te], y[te], scaler, model_name)
            model = make_network(model_name, X_tr.shape[1:], params["width"], params["learning_rate"])
            model.fit(X_tr, y_tr, epochs=params["best_epoch"], batch_size=params["batch_size"],
                      shuffle=False, verbose=0)
            target_hat = model.predict(X_te, verbose=0).ravel()*scaler["y_scale"]+scaler["y_center"]
        rv_hat = np.exp(target_hat) if target == "log(rv)" else target_hat
        with np.errstate(invalid="ignore", divide="ignore"):
            z_hat = np.where(rv_hat > 0, np.log(rv_hat), np.nan)
        for j, index in enumerate(te):
            predictions.append({"date": dates.iloc[index].strftime("%Y-%m-%d"),
                                "rv": float(panel["y_rv"][index]),
                                "forecast_rv": float(rv_hat[j]),
                                "forecast_log_rv": float(z_hat[j]) if np.isfinite(z_hat[j]) else None})
        records.append({"year": int(year), "estimation_examples": len(tr),
                        "estimation_start": dates.iloc[tr[0]].strftime("%Y-%m-%d"),
                        "estimation_end": dates.iloc[tr[-1]].strftime("%Y-%m-%d"),
                        "first_test_target": first_date.strftime("%Y-%m-%d"),
                        "last_test_target": dates.iloc[te[-1]].strftime("%Y-%m-%d"),
                        "forecasts": len(te)})
    frame = pd.DataFrame(predictions)
    return score_forecasts(frame.rv, frame.forecast_rv), predictions, records


def slug(model, target):
    return model.lower().replace(" ", "-")+"_"+("log" if target == "log(rv)" else "level")


def configuration(data_path, panel):
    dates=panel["dates"]
    tr=estimation_indices(dates,VALIDATION_START)
    return {"input_days": INPUT_DAYS, "fnn_input_days": FNN_INPUT_DAYS,
            "estimation_examples": ESTIMATION_EXAMPLES,
            "validation_start": str(VALIDATION_START.date()),
            "validation_end": str((TEST_START-pd.Timedelta(days=1)).date()),
            "validation_scheme": "one full calendar year with one annual fit",
            "first_validation_target": str(dates.loc[dates>=VALIDATION_START].iloc[0].date()),
            "first_test_target": str(dates.loc[dates>=TEST_START].iloc[0].date()),
            "test_start": str(TEST_START.date()), "test_end": str(TEST_END.date()),
            "tuning_estimation_start": str(dates.iloc[tr[0]].date()),
            "tuning_estimation_end": str(dates.iloc[tr[-1]].date()),
            "tuning_examples": len(tr),
            "validation_examples": int(((dates>=VALIDATION_START)&(dates<TEST_START)).sum()),
            "test_examples": int((dates>=TEST_START).sum()),
            "n_trials": N_TRIALS, "max_epochs": MAX_EPOCHS,
            "seed": SEED, "optuna_seed": 1, "global_clipnorm": 1.0,
            "tf_intraop_threads": int(os.environ["TF_NUM_INTRAOP_THREADS"]),
            "tf_interop_threads": int(os.environ["TF_NUM_INTEROP_THREADS"]),
            "refit_frequency": "annual", "estimation_scheme": "sliding",
            "data_sha256": hashlib.sha256(Path(data_path).read_bytes()).hexdigest(),
            "pipeline_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "versions": {p: importlib.metadata.version(p) for p in
                         ["numpy", "pandas", "keras", "tensorflow", "optuna", "scikit-learn"]}}


def run_one(args):
    data=load_data(args.data); panel=make_inputs(data)
    params, trials = (None, []) if args.model == "HAR-OLS" else tune_network(panel,args.model,args.target)
    metrics, predictions, refits = annual_forecasts(panel,args.model,args.target,params)
    result={"model": args.model, "target": args.target, "config": configuration(args.data,panel),
            "selected": params, "trials": trials, "metrics": metrics,
            "refits": refits, "predictions": predictions,
            "provenance": {"execution_pipeline_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           "reused_unaffected_run": False}}
    path=args.output_dir/(slug(args.model,args.target)+".json")
    path.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"stage":"complete","model":args.model,"target":args.target,**metrics}),flush=True)


def assemble(args):
    results=[json.loads((args.output_dir/(slug(m,t)+".json")).read_text()) for t in TARGETS for m in MODELS]
    config=results[0]["config"]
    assert all(r["config"]==config for r in results)
    assert all(r["refits"]==results[0]["refits"] for r in results)
    assert all([p["date"] for p in r["predictions"]]==[p["date"] for p in results[0]["predictions"]] for r in results)
    summary={"config":config,"refits":results[0]["refits"],
             "results":[{k:r[k] for k in ["model","target","selected","metrics","provenance"]} for r in results]}
    (args.output_dir/"summary.json").write_text(json.dumps(summary,indent=2,allow_nan=False)+"\n")
    records=[]
    for r in results:
        records.extend(dict(model=r["model"],target=r["target"],**p) for p in r["predictions"])
    pd.DataFrame(records).to_csv(args.output_dir/"forecasts.csv",index=False)
    trial_rows=[dict(model=r["model"],target=r["target"],**v) for r in results for v in r["trials"]]
    pd.DataFrame(trial_rows).to_csv(args.output_dir/"trials.csv",index=False)
    print(json.dumps(summary,indent=2),flush=True)


def run_all(args):
    pending=[(m,t) for t in TARGETS for m in MODELS]
    active=[]
    while pending or active:
        while pending and len(active)<args.jobs:
            model,target=pending.pop(0)
            name=slug(model,target)
            if (args.output_dir/(name+".json")).exists():
                saved = json.loads((args.output_dir/(name+".json")).read_text())
                current = configuration(args.data, make_inputs(load_data(args.data)))
                if saved["config"] != current:
                    raise ValueError(f"Stale result for {name}; use a fresh output directory.")
                print("Resume: completed "+name,flush=True); continue
            log=(args.output_dir/(name+".log")).open("w")
            command=[sys.executable,"-u",str(Path(__file__).resolve()),"--model",model,"--target",target,
                     "--data",str(args.data),"--output-dir",str(args.output_dir)]
            process=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT)
            active.append((process,log,name))
            print("Started "+name,flush=True)
        for item in active[:]:
            process,log,name=item
            status=process.poll()
            if status is not None:
                log.close(); active.remove(item)
                if status:
                    for other,handle,_ in active: other.terminate(); handle.close()
                    raise RuntimeError(f"{name} failed, see its log")
                print("Completed "+name,flush=True)
        if active: time.sleep(2)
    assemble(args)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data",type=Path,default=ROOT/"data/taq_spy/SPY_daily_measures.csv")
    parser.add_argument("--output-dir",type=Path,default=ROOT/"data/taq_spy/nn_example_756")
    parser.add_argument("--model",choices=MODELS)
    parser.add_argument("--target",choices=TARGETS)
    parser.add_argument("--all",action="store_true")
    parser.add_argument("--assemble",action="store_true")
    parser.add_argument("--jobs",type=int,default=4)
    args=parser.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    if args.all: run_all(args)
    elif args.assemble: assemble(args)
    elif args.model and args.target: run_one(args)
    else: parser.error("Choose --all, --assemble, or --model and --target.")


if __name__ == "__main__":
    main()
