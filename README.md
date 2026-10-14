# MLmetrics

This is the repository for [mlmetrics.org](https://mlmetrics.org), an open textbook on machine learning for econometricians by [Onno Kleen](https://onnokleen.com/).

The book is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). The website is rendered using [Quarto](https://quarto.org/).

## Reproducible rendering

The checked environment uses Quarto 1.7.32, Python 3.13.5, and R 4.5.2. Python package versions are pinned in `requirements.txt`; the R packages called directly by the chapters are recorded in `requirements-r.txt`. Code chunks never install packages during a render.

Create and activate a Python virtual environment, install the pinned packages, and point Quarto to that interpreter:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
QUARTO_PYTHON=.venv/bin/python quarto render
```

Install the R packages listed in `requirements-r.txt` before rendering. The R chapters also require a working LaTeX installation because several figures are generated from repository-owned TikZ sources. A missing dependency now produces an explicit error instead of changing the local R library during execution.

Quarto execution caching is enabled in `_quarto.yml`. For a clean verification run, remove only the chapter-specific cache directories you intend to rebuild, then run the same render command; do not treat cached output as evidence that a newly created environment is complete.

## Website analytics

The shared HTML include `includes/goatcounter.html` integrates the free hosted [GoatCounter](https://www.goatcounter.com/) service. The account dashboard is at [mlmetrics.goatcounter.com](https://mlmetrics.goatcounter.com/).

The configured endpoint is `https://mlmetrics.goatcounter.com/count`. This URL is public; no password or API key belongs in the repository. Set `endpoint` to an empty string to disable analytics. Keep individual-pageview recording disabled in the account settings and keep the dashboard private. The [privacy notice](privacy.qmd) describes the hosted setup.

The include runs only on `mlmetrics.org` and `www.mlmetrics.org`, respects Do Not Track and Global Privacy Control, and sends page paths and referral origins without query strings or fragments. It does not collect custom click events. Local previews and other copies of the site do not load the analytics script.

After changing the include, render the HTML site with `quarto render --to html` and publish the updated `docs/` through the usual GitHub Pages workflow. Confirm new visits in the GoatCounter dashboard after publication; visits with a blocking browser extension or privacy signal will not appear.
