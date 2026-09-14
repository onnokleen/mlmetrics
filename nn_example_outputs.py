"""Build public aggregate tables and the figure from private SPY forecasts.

Run after nn_example_pipeline.py --all. Daily observations and forecasts remain
under data/taq_spy; only aggregate results and the figure are public outputs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

MODELS = ("HAR-OLS", "HAR-FNN", "FNN", "Simple RNN", "LSTM")
ROOT = Path(__file__).resolve().parent


def number(value, digits=4):
    return "undefined" if value is None else f"{value:.{digits}f}"


def performance_table(summary):
    lines = ["| Target fit | Model | RMSE log RV | RMSE RV | QLIKE | Nonpositive |",
             "|---|---|---:|---:|---:|---:|"]
    for r in summary["results"]:
        m = r["metrics"]
        lines.append(f"| `{r['target']}` | {r['model']} | " + " | ".join(
            number(m[k]) for k in ("rmse_log_rv", "rmse_rv", "qlike"))
            + f" | {m['nonpositive_rv_forecasts']} |")
    return "\n".join(lines)


def tuning_table(summary):
    lines = ["| Target fit | Model | Width | Parameters | Learning rate | Batch size | Epochs | Validation loss |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for r in summary["results"]:
        p = r["selected"]
        if r["model"] == "HAR-OLS":
            continue
        lines.append(f"| `{r['target']}` | {r['model']} | {p['width']} | {p['parameters']:,} | "
                     f"{p['learning_rate']:.6f} | {p['batch_size']} | {p['best_epoch']} | {p['validation_loss']:.4f} |")
    return "\n".join(lines)


def performance_figure(summary, forecasts, output):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    colors = {"HAR-OLS": "#777777", "HAR-FNN": "#8c564b", "FNN": "#4c78a8",
              "Simple RNN": "#d9791c", "LSTM": "#2e8540"}
    fig, axes = plt.subplots(2, 1, figsize=(11, 8.8), height_ratios=[1.1, 1], layout="constrained")
    ax = axes[0]
    observed = forecasts.loc[(forecasts.model == "HAR-OLS") & (forecasts.target == "log(rv)")]
    ax.plot(pd.to_datetime(observed.date), np.log(observed.rv), color="black", lw=.9, alpha=.65, label="Observed")
    for model in MODELS:
        f = forecasts.loc[(forecasts.model == model) & (forecasts.target == "log(rv)")]
        ax.plot(pd.to_datetime(f.date), f.forecast_log_rv, label=model, color=colors[model], lw=1)
    ax.axvline(pd.Timestamp("2024-01-02"), color="0.4", ls=":", lw=1)
    ax.set(title="Log-target forecasts; dotted line marks the 2024 refit", ylabel="Log realized variance")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(ncol=3, loc="upper center", fontsize=9)
    ax.grid(axis="y", alpha=.2)
    ax = axes[1]
    locations = np.arange(len(MODELS))
    maximum = max(r["metrics"]["rmse_log_rv"] or 0 for r in summary["results"])
    for target, shift, color, label in [("log(rv)", -.19, "#4c78a8", "Fit on log RV"), ("rv", .19, "#d9791c", "Fit on RV")]:
        values = {r["model"]: r["metrics"]["rmse_log_rv"] for r in summary["results"] if r["target"] == target}
        for j, model in enumerate(MODELS):
            value = values[model]
            x = locations[j]+shift
            if value is None:
                ax.plot(x, .03*maximum, marker="x", color=color, ms=8)
                ax.text(x, .075*maximum, "undefined", ha="center", va="bottom", rotation=90, fontsize=9, color=color)
            else:
                ax.bar(x, value, width=.36, color=color, label=label if j == 0 else None)
                ax.text(x, value+.025*maximum, f"{value:.3f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(locations, MODELS)
    ax.set_ylim(0, maximum*1.18)
    ax.set(ylabel="Test RMSE on log RV", title="One test period, two target-and-normalization pipelines")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=.2)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def update_outputs(private_dir, root=ROOT):
    # Importing the pipeline loads no TensorFlow until a network is actually fit.
    from nn_example_pipeline import score_forecasts
    summary = json.loads((private_dir/"summary.json").read_text())
    config = summary["config"]
    if config["pipeline_sha256"] != hashlib.sha256((root/"nn_example_pipeline.py").read_bytes()).hexdigest():
        raise ValueError("Results do not match the current forecasting pipeline.")
    data_path = root/"data/taq_spy/SPY_daily_measures.csv"
    if config["data_sha256"] != hashlib.sha256(data_path.read_bytes()).hexdigest():
        raise ValueError("Results do not match the current input data.")
    forecasts = pd.read_csv(private_dir/"forecasts.csv")
    for r in summary["results"]:
        rows = forecasts.loc[(forecasts.model == r["model"]) & (forecasts.target == r["target"])]
        if len(rows) != config["test_examples"] or rows.date.duplicated().any():
            raise ValueError("Wrong test-forecast count.")
        actual = score_forecasts(rows.rv, rows.forecast_rv)
        for key, expected in r["metrics"].items():
            if expected is None:
                assert actual[key] is None
            else:
                np.testing.assert_allclose(actual[key], expected, rtol=1e-10, atol=1e-12)
    (root/"results").mkdir(exist_ok=True)
    (root/"results/nn-example-756.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n")
    performance_figure(summary, forecasts, root/"figures/nn-example-performance.png")
    print(performance_table(summary))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-dir", type=Path, default=ROOT/"data/taq_spy/nn_example_756")
    args = parser.parse_args()
    update_outputs(args.private_dir)


if __name__ == "__main__":
    main()
