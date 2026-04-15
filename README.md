# MLmetrics: Machine Learning for Econometricians

MLmetrics is an open textbook on machine learning for graduate students in econometrics.

The book is written for readers with a strong background in probability, statistics, and econometrics who want a treatment of machine learning that takes econometric structure seriously. Instead of presenting ML in clean i.i.d. toy settings, the book focuses on the problems econometricians actually face: time dependence, real-time information sets, leakage from invalid validation schemes, heteroskedasticity, tail risk, and predictive distributions.

## Scope

The book covers:

- cross-validation and model comparison under dependence
- predictive distributions and forecast evaluation
- feed-forward, recurrent, and LSTM neural networks
- decision trees, random forests, and gradient boosting
- hyperparameter optimization, conformal prediction, and foundation models for economic text

It does not aim to replace a full course in econometrics or time-series econometrics. ARIMA, GARCH, state-space models, causal inference, and asymptotic theory are treated as background rather than as primary topics.

## Repository Layout

- `index.qmd`: website landing page
- `*.qmd`: chapter sources
- `_quarto.yml`: Quarto site configuration
- `docs/`: rendered website output
- `data/`: data files used in examples
- `figures/`: saved figures and graphics assets

## Build Locally

You need Quarto and a Python environment with the packages used in the chapters.

To render the book locally:

```sh
quarto render
```

The rendered website is written to `docs/`.

## Feedback

Suggestions, typo reports, and issue reports are welcome through GitHub:

- Repository: <https://github.com/onnokleen/mlmetrics>
- Issues: <https://github.com/onnokleen/mlmetrics/issues>

## Author

Onno Kleen is an Assistant Professor of Econometrics at Erasmus University Rotterdam and a fellow at the Tinbergen Institute.

## License

The book is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International CC BY-NC-SA 4.0.