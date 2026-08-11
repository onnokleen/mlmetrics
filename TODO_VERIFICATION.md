# TODO Verification Report

Verification pass for the essential (`[E]`) items in `TODO.md`, performed against the current repository state. Status labels:

- `confirmed`: the TODO claim is supported by source inspection, rendered HTML, local computation, or cited literature.
- `confirmed (duplicate)`: same issue appears elsewhere in `TODO.md`.
- `source-confirmed`: local text is as described and the external/source-dependent part checks out.

Scope: essential items only. Style, taste, bridge, and exercise-quality notes without `[E]` were not exhaustively verified in this pass.

External sources used:

- Bates, Hastie, and Tibshirani, "Cross-validation: what does it estimate and how well does it do it?" arXiv: https://arxiv.org/abs/2104.00673
- Arlot and Celisse, "A survey of cross-validation procedures for model selection" arXiv: https://arxiv.org/abs/0907.4728
- Chen, Pelger, and Zhu, "Deep Learning in Asset Pricing" arXiv: https://arxiv.org/abs/1904.00745
- Barber, Candes, Ramdas, and Tibshirani, "Predictive inference with the jackknife+" arXiv: https://arxiv.org/abs/1905.02928
- Barber, Candes, Ramdas, and Tibshirani, "The limits of distribution-free conditional predictive inference" arXiv: https://arxiv.org/abs/1903.04684

## Summary

All 57 essential TODO claims were checked. I found no essential false positives. Several claims are duplicates or chapter-local repeats of global items, but they are still valid.

Counts:

- `confirmed`: 49
- `source-confirmed`: 6
- `confirmed (duplicate)`: 2
- `false positive`: 0

## Verified Essential Items

| TODO line | Status | Verification |
|---:|---|---|
| 13 | confirmed | `_quarto.yml` renders `*.qmd`, and `docs/autoencoders.html`, `docs/hidden.html`, `docs/reinforcement_learning.html`, and `docs/decision_trees_full.html` exist. |
| 14 | confirmed | `adv_tree_based_methods.qmd` has YAML `title:` plus `#` heading; rendered HTML has two H1s. `datasets.qmd` has the same pattern and also renders two H1s. |
| 15 | confirmed | `index.qmd` uses `Coqueret and Guida @...` and `James et al. @...`; rendered HTML duplicates author names. |
| 16 | confirmed | The cited bullet lists render as single paragraphs in `docs/information_theory.html` and `docs/evaluating_distributions.html`; `notion` typo is present. |
| 25 | confirmed | Ch 6 uses `W_hh^T diag(g')`; Ch 7 uses `diag(g') W_h`. The Ch 6 display is the transposed/backward-adjoint form for the stated forward Jacobian. |
| 37 | confirmed | Ch 5 Python chunks are plotting/diagrams, while Ch 6/7 are R/TikZ/Mermaid diagrams; no fit/forecast Python implementation appears in Ch 5-7. |
| 57 | confirmed | Shared support only avoids support-violation infinity. Example: Cauchy truth vs Gaussian model has common support but infinite KL because the Gaussian log-density contributes an infinite second moment under Cauchy tails. |
| 58 | confirmed | Equal Gaussian variances make KL symmetric for all mean differences, so the text's "only if equal variance and equal mean" statement is false. |
| 59 | confirmed | The Jensen proof sums `q` only over `supp(p)`, giving `<= 1`; equality also forces no `q` mass outside `supp(p)`. |
| 60 | confirmed | `H(Y|X) <= H(Y)` is an average statement. A realized condition `X=x` can have higher entropy than unconditional `Y`. |
| 61 | confirmed | The Bernoulli entropy example and definition callouts are verbatim duplicates. |
| 73 | source-confirmed | The local text says CV approximates `R(fhat)` for the fitted model. Bates-Hastie-Tibshirani distinguish this from the average error of the fitting procedure over hypothetical training sets. |
| 74 | source-confirmed | The local text gives an unqualified bias/variance tradeoff for `K`. The variance direction is not safely stated that way; cross-validation variance behavior depends on the setting. |
| 75 | confirmed | Ex 2.3 solution uses `E[xi_t | F_t] = 0`; the statement only gives unconditional mean zero and independence of `u`, not the needed innovation assumption for `xi_t`. |
| 76 | confirmed | The forecast-origin definition includes "outcomes" observed by time `t`, which is impossible for the validation outcome being forecast. |
| 77 | confirmed | The overview sentence reverses the analogy: pretest/specification-search bias is the econometric analogue; nested validation is the ML remedy. |
| 90 | confirmed | Re-running the PIT skew simulation gives a low first bin, a left-of-center peak, and only a modest right-edge rise, not a simple upward slope. |
| 91 | confirmed | The application ranks raw average LogS/CRPS with no DM/HAC test. Re-running the scoring loop gives 63 test quarters and large COVID-quarter score shares, especially RF in-sample LogS. |
| 92 | confirmed | If the criterion is the miss indicator/lower miss rate, always-infinite intervals dominate; the described gaming example only fits a target-coverage criterion. |
| 93 | source-confirmed | PIT uniformity is conventionally probabilistic calibration, not marginal calibration. Marginal calibration refers to matching the unconditional outcome distribution by the average forecast distribution. |
| 94 | confirmed | The chapter writes `u_t = F_t(y_t)` while conditioning on `F_t`; for a one-step forecast the outcome should be shifted, e.g. `F_t(y_{t+1})`. |
| 95 | confirmed | Strict propriety domains are not stated: LogS needs densities and CRPS is standard on distributions with finite first moment; the CRPS sample/kernel representation also needs integrability. |
| 96 | confirmed (duplicate) | Same broken-list issue as line 16, localized to Ch 3. |
| 106 | confirmed | Momentum defines `g_t` at `theta^(t-1)` but updates `theta^(t+1)` from `theta^t`, skipping the matching update index. |
| 107 | confirmed | Ex 4.2 Part 2 solution invokes the SRSWOR variance formula rather than deriving it, so the proof is circular. |
| 108 | confirmed | Convergence claims are unconditional; the chapter's own quadratic exercise shows step-size restrictions are necessary. |
| 109 | confirmed | Adam bias correction uses expectations over a gradient process even though the paragraph just said mini-batches were omitted from notation. |
| 110 | confirmed | Nonconvex optimizer figure uses different learning rates by optimizer in code; text/caption do not disclose the adaptive-scale rationale. |
| 121 | confirmed | A sign-varying cross-partial does not by itself rule out PSD Hessians; off-diagonal Hessian elements may be positive or negative in PSD matrices. |
| 122 | confirmed | The chapter defines `L` as total layers including output, but the parameter-count formula treats `H^(1),...,H^(L)` as hidden widths plus an added output layer. |
| 123 | confirmed | The output-layer delta formula assumes elementwise activation; softmax is vector-valued and needs the Jacobian or the softmax-cross-entropy simplification. |
| 124 | confirmed | Standardization advice does not say to fit scaling constants on training data only, and the Common Pitfalls box omits this leakage case. |
| 134 | confirmed | Same Jacobian issue as line 25, localized to Ch 6. |
| 135 | confirmed | Direct calculation gives `dh2/dx1 ≈ 0.384`, so Ex 6.2 Part 4's "essentially no memory" answer is wrong for the stated values. |
| 147 | source-confirmed | Chen-Pelger-Zhu state 46 firm characteristics, 178 macro series, 1967-2016, and a no-arbitrage/GMM/adversarial-moment objective; the chapter's 94/1957/MSE framing is incorrect. |
| 148 | confirmed | The only LSTM exercise is a mechanical forward-pass substitution exercise and lacks the required derivation/comparison/diagnostic structure. |
| 161 | confirmed | Tuning returns `min(val_loss)` across 30 epochs, but final models train 100 epochs on train+valid with no matching early-stopping/best-epoch protocol. |
| 162 | confirmed | Log-target forecasts are back-transformed as `exp(z_hat)`, which is a geometric/median-style back-transform; RV-scale MSE/QLIKE target mean-type behavior without a lognormal correction. |
| 173 | confirmed | Ch 9 uses an 80/20 train+test split named `X_trva`, hard-codes 32 units, `1e-3`, and 200 epochs, and has no validation block or stated provenance. |
| 187 | confirmed | Cost-complexity pruning is stated without the subtree domain `T subset T0` or weakest-link/nested-subtree result. |
| 188 | confirmed | Recursive binary splitting is described without a base stopping rule. |
| 198 | confirmed | The forest-weight formula ignores bootstrap multiplicities; exactness requires multiplicity weights or a subsampling/distinct-observation convention. |
| 199 | confirmed | Random forests Ch 11 forward-references "constrained boosting" before Ch 12. |
| 212 | confirmed | The AdaBoost equivalence requires base learners returning class labels/signs; as written it overstates equivalence for regression trees with real-valued outputs. |
| 223 | confirmed | Pooled-neighbor empirical quantiles match forest weights only under equal leaf-size/weight conditions; otherwise the unweighted pooled sample is not equivalent. |
| 224 | confirmed (duplicate) | Same duplicate-H1 issue as line 14, localized to Ch 13. |
| 225 | confirmed | NGBoost has no explicit iterative update with iteration index, learning rate, or parameter function update. |
| 251 | source-confirmed | Barber et al. give jackknife+ worst-case coverage at `1 - 2 alpha` under exchangeability/symmetric algorithm, not a generic `1 - alpha` finite-sample marginal guarantee. |
| 252 | confirmed | Exact code split gives 149/47/53 observations, but date cutoffs end at Q3; `1999-12-01` and `2011-12-01` are in `macro` but in no subsample. |
| 253 | confirmed | With `n_cal=47`, the conformal order statistic has level `44/48 = 91.7%`; observed test coverage is `50/53 = 94.3%`, so discreteness alone does not explain it. |
| 254 | confirmed | CQR correction is additive: lower minus `qhat`, upper plus `qhat`. The caption's "widening is largest where the band is already wide" is false for the conformal correction. |
| 255 | source-confirmed | The chapter only gives a heteroskedastic constant-width example. The general impossibility of meaningful distribution-free conditional coverage is supported by Vovk/Lei-Wasserman and Barber et al. |
| 256 | confirmed | Ex 15.3 Part 1 reuses the exact `n=4`, predictions, residuals, sorted bounds, and interval from the in-text jackknife+ worked example. |
| 270 | confirmed | Stationarity of `W_t` alone does not make `E[-log p_theta(W_t|W_1:t-1)]` independent of `t` when the conditioning history grows from the sequence start; a rate/Cesaro formulation is needed. |
| 271 | confirmed | The caption says `d4` was published before `t` but cites material after `t`, which is impossible as a property of that physical document; the figure code marks it admissible. |
| 272 | confirmed | Recalculation gives log-probability sum `-17.6097505`, average NLL `2.2012188`, and PPL `9.0360200`; the displayed `-17.6096` and `9.038` are off. |
| 286 | confirmed (duplicate) | Same citation-syntax issue as line 15, repeated under Ch 17/front matter. |

## Local Computations Performed

- Ch 3 skew-PIT simulation reproduced the non-monotone skew-mismatch histogram.
- Ch 3 empirical density-forecast loop reproduced 63 test quarters and COVID-quarter score dominance.
- Ch 6 derivative check produced `dh2/dx1 = 0.3843932011517108`.
- Ch 15 FRED-QD conformal split reproduced `149/47/53` observations and confirmed the Q4 gaps.
- Ch 15 conformal empirical block reproduced coverage `0.9434`, high-VIX coverage `0.8182`, `qhat = 6.8348`, and discreteness level `44/48 = 0.9167`.
- Ch 16 perplexity exercise recalculation produced PPL `9.0360200`.
