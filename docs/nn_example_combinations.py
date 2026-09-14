"""Reproduce the exploratory HAR + neural log-RV forecast combinations.

After nn_example_pipeline.py and nn_example_outputs.py, run --fit-weights to
fit and freeze all weights using 2022, then --evaluate for 2023-2024 results.
These years were inspected before this extension was proposed; the results
are exploratory. Daily data and forecasts remain in the private directory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
MODELS = ("HAR-FNN", "FNN", "Simple RNN", "LSTM")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def convex_weight(y, har, neural):
    """Least-squares weight on the neural forecast, constrained to [0, 1]."""
    y, har, neural = (np.asarray(v, dtype=float) for v in (y, har, neural))
    if y.ndim != 1 or y.shape != har.shape or y.shape != neural.shape:
        raise ValueError("Validation targets and forecasts must be aligned vectors.")
    if not all(np.isfinite(v).all() for v in (y, har, neural)):
        raise ValueError("Validation targets and forecasts must be finite.")
    difference = neural-har
    denominator = float(difference@difference)
    if denominator == 0:
        return 0.0  # Identical forecasts; retain HAR.
    return float(np.clip(difference@(y-har)/denominator, 0, 1))


def fingerprints(root):
    return {"combination_module_sha256": digest(__file__),
            "pipeline_sha256": digest(root/"nn_example_pipeline.py"),
            "base_results_sha256": digest(root/"results/nn-example-756.json"),
            "data_sha256": digest(root/"data/taq_spy/SPY_daily_measures.csv")}


def fit_weights(root, private_dir):
    import nn_example_pipeline as base
    from sklearn.linear_model import LinearRegression
    path = private_dir/"weights.json"
    if path.exists():
        raise ValueError("Weights are already frozen; use a fresh output directory to refit.")
    original = json.loads((root/"results/nn-example-756.json").read_text())
    hashes = fingerprints(root)
    assert original["config"]["pipeline_sha256"] == hashes["pipeline_sha256"]
    assert original["config"]["data_sha256"] == hashes["data_sha256"]
    data = base.load_data(root/"data/taq_spy/SPY_daily_measures.csv")
    panel = base.make_inputs(data.loc[data.date < base.TEST_START].copy())
    dates = panel["dates"]
    tr = base.estimation_indices(dates, base.VALIDATION_START)
    va = np.flatnonzero(np.asarray(dates >= base.VALIDATION_START))
    assert len(tr) == 756 and len(va) == 251 and dates.max().year == 2022
    x_har, y = base.arrays_for(panel, "HAR-OLS", "log(rv)")
    har = LinearRegression().fit(x_har[tr], y[tr]).predict(x_har[va])
    rows, validation = [], []
    for name in MODELS:
        specification = next(r for r in original["results"]
                             if r["model"] == name and r["target"] == "log(rv)")
        params = specification["selected"]
        x, y = base.arrays_for(panel, name, "log(rv)")
        scaler = base.fit_scaler(x[tr], y[tr], name, "log(rv)")
        xt, yt = base.transform(x[tr], y[tr], scaler, name)
        xv, _ = base.transform(x[va], np.zeros(len(va)), scaler, name)
        network = base.make_network(name, xt.shape[1:], params["width"], params["learning_rate"])
        network.fit(xt, yt, epochs=params["best_epoch"], batch_size=params["batch_size"],
                    shuffle=False, verbose=0)
        neural = network.predict(xv, verbose=0).ravel()*scaler["y_scale"]+scaler["y_center"]
        weight = convex_weight(y[va], har, neural)
        combined = (1-weight)*har+weight*neural
        row = {"model": name, "neural_weight": weight,
               "validation_rmse_log_rv": float(np.sqrt(np.mean((combined-y[va])**2)))}
        rows.append(row)
        validation.extend({"model": name, "date": dates.iloc[i].strftime("%Y-%m-%d"),
                           "log_rv": float(y[i]), "har": float(har[j]), "neural": float(neural[j])}
                          for j, i in enumerate(va))
        print(json.dumps(row), flush=True)
    record = {"fingerprints": hashes, "weights": rows,
              "validation_year": 2022, "evaluation_years": [2023, 2024],
              "weight_rule": "Convex least squares on 2022; fixed in both evaluation years.",
              "component_models": "Original single-seed log-target fits; annual sliding refits.",
              "evaluation_status": "Exploratory: 2023-2024 results were inspected before proposing combinations."}
    private_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(validation).to_csv(private_dir/"validation.csv", index=False)
    path.write_text(json.dumps(record, indent=2)+"\n")


def combination_table(summary):
    lines = ["| Neural component | Neural weight | Alone: RMSE log RV | With HAR: RMSE log RV |",
             "|---|---:|---:|---:|"]
    for r in summary["results"]:
        lines.append(f"| {r['model']} | {r['neural_weight']:.4f} | "
                     f"{r['neural_metrics']['rmse_log_rv']:.4f} | {r['combined_metrics']['rmse_log_rv']:.4f} |")
    return "\n".join(lines)


def combination_figure(summary, destination):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 4.2), layout="constrained")
    benchmark = summary["har_metrics"]["rmse_log_rv"]
    ax.axvline(benchmark, color="0.4", ls="--", lw=1.3,
               label=f"HAR-OLS: {benchmark:.4f}")
    for i, r in enumerate(summary["results"]):
        alone = r["neural_metrics"]["rmse_log_rv"]
        combined = r["combined_metrics"]["rmse_log_rv"]
        ax.plot([alone, combined], [i, i], color="0.75", lw=2, zorder=1)
        ax.scatter(alone, i, color="#4c78a8", s=55, label="Neural alone" if i == 0 else None, zorder=2)
        ax.scatter(combined, i, color="#2e8540", marker="D", s=45,
                   label="Combined with HAR" if i == 0 else None, zorder=3)
        ax.annotate(f"{alone:.4f}", (alone, i), xytext=(0, 9), textcoords="offset points",
                    ha="center", fontsize=9, color="#245b87")
        ax.annotate(f"{combined:.4f}", (combined, i), xytext=(0, -16), textcoords="offset points",
                    ha="center", fontsize=9, color="#216331")
    ax.set_yticks(range(len(summary["results"])), [r["model"] for r in summary["results"]])
    ax.set_ylim(len(summary["results"])-.5, -.5)
    ax.set_xlim(.568, .635)
    ax.set_xlabel("2023–2024 RMSE on log RV (lower is better)")
    ax.set_title("Can the neural forecast complement HAR?")
    ax.grid(axis="x", alpha=.15)
    ax.legend(loc="lower right", fontsize=9)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, dpi=180)
    plt.close(fig)


def evaluate(root, base_dir, private_dir):
    import nn_example_pipeline as base
    weights_path = private_dir/"weights.json"
    frozen = json.loads(weights_path.read_text())
    assert frozen["fingerprints"] == fingerprints(root), "Stale weights or source results."
    original = json.loads((root/"results/nn-example-756.json").read_text())
    source = pd.read_csv(base_dir/"forecasts.csv")
    source = source.loc[source.target == "log(rv)"].copy()
    har = source.loc[source.model == "HAR-OLS"].sort_values("date")
    assert len(har) == 502 and har.date.is_unique
    assert har.date.iloc[0] == "2023-01-03" and har.date.iloc[-1] == "2024-12-31"
    har_metrics = base.score_forecasts(har.rv, har.forecast_rv)
    original_har = next(r for r in original["results"]
                        if r["model"] == "HAR-OLS" and r["target"] == "log(rv)")
    for key, value in har_metrics.items():
        np.testing.assert_allclose(value, original_har["metrics"][key], rtol=1e-10, atol=1e-12)
    rows, predictions = [], []
    for weight in frozen["weights"]:
        name = weight["model"]
        neural = source.loc[source.model == name].sort_values("date")
        assert neural.date.tolist() == har.date.tolist()
        np.testing.assert_array_equal(neural.rv.to_numpy(), har.rv.to_numpy())
        metrics = base.score_forecasts(neural.rv, neural.forecast_rv)
        old = next(r for r in original["results"] if r["model"] == name and r["target"] == "log(rv)")
        for key, value in metrics.items():
            np.testing.assert_allclose(value, old["metrics"][key], rtol=1e-10, atol=1e-12)
        w = weight["neural_weight"]
        combined = (1-w)*har.forecast_log_rv.to_numpy()+w*neural.forecast_log_rv.to_numpy()
        rows.append(dict(weight, neural_metrics=metrics,
                         combined_metrics=base.score_forecasts(har.rv, np.exp(combined))))
        predictions.extend({"model": "HAR + "+name, "date": d, "forecast_log_rv": float(z),
                            "forecast_rv": float(np.exp(z))} for d, z in zip(har.date, combined))
    summary = {"protocol": frozen, "frozen_weights_sha256": digest(weights_path),
               "har_metrics": har_metrics, "results": rows}
    pd.DataFrame(predictions).to_csv(private_dir/"forecasts.csv", index=False)
    (private_dir/"summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    (root/"results/nn-example-combinations.json").write_text(json.dumps(summary, indent=2)+"\n")
    combination_figure(summary, root/"figures/nn-example-combinations.png")
    print(combination_table(summary))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--base-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--fit-weights", action="store_true")
    action.add_argument("--evaluate", action="store_true")
    args = parser.parse_args()
    # Allow a staged module to use the book's unchanged original pipeline.
    import sys
    sys.path.insert(0, str(args.root))
    base_dir = args.base_dir or args.root/"data/taq_spy/nn_example_756"
    private_dir = args.output_dir or args.root/"data/taq_spy/nn_example_combinations"
    if args.fit_weights:
        fit_weights(args.root, private_dir)
    else:
        evaluate(args.root, base_dir, private_dir)


if __name__ == "__main__":
    main()
