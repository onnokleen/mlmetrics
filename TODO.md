# Book audit TODO (July 2026)

Complete line-numbered findings from the full-book audit (all 16 teaching chapters read in full; every exercise solution recomputed; empirical code executed where relevant; rendered HTML checked). Line numbers refer to the state of the files on 2026-07-02 and will drift as edits land — use the quoted anchors to relocate.

Tags: **[E]** essential (false/misleading statement, broken output, or submission-level defect) · **[S]** style (rule-driven improvement) · **[T]** taste (judgement call). Lenses: **A** = methods rigor, **B** = writing precision, **C** = structure/CLAUDE.md conventions.

Verified clean (no action): bibliography (all 89 entries in `references-local.bib` cited, no dangling keys) · no `###` headings anywhere · all `number-offset` values correct · chapter skeletons complete (one exception: `nn_example.qmd`, see below).

---

## Global — production and publishing

- [ ] **[E]** Draft chapters render publicly: `autoencoders.qmd`, `hidden.qmd`, `reinforcement_learning.qmd`, `decision_trees_full.qmd` are built into `docs/` and deployed (reachable via site search) because `_quarto.yml` renders `*.qmd`. Exclude them in the render list or move drafts out of the root.
- [ ] **[E]** `adv_tree_based_methods.qmd:2` — only teaching chapter with a YAML `title:`; produces two `<h1>` elements in the built HTML (verified). Delete line 2. Check `datasets.qmd` (same YAML-title + `#`-heading pattern).
- [ ] **[E]** `index.qmd:65,67` — `Coqueret and Guida @CoqueretGuida2020` / `James et al. @JamesWittenHastieTibshirani2013` render the author names twice; use bracketed citations.
- [ ] **[E]** Broken list rendering (missing blank line before bullets; verified in built HTML): `information_theory.qmd:184-187`, `information_theory.qmd:247-250`, `evaluating_distributions.qmd:527-529` (also "notion" → "notions"/"notation").
- [ ] **[S]** `#| echo: false` on figure chunks against the foldable-code convention: `information_theory.qmd:121,275,428`; `cross_validation.qmd:41,226,330`; `decision_trees.qmd:116,158,257`; `random_forests.qmd:130,230`; `gradient_boosting.qmd:125,360`. Switch to `echo: true` (global `code-fold` handles folding).
- [ ] **[S]** Stale YAML comments "`# This makes sections 2.1, 2.2, etc.`" in `evaluating_distributions.qmd:3`, `feed_forward_nns.qmd:3`, `optimization.qmd:3`, `lstm_neural_networks.qmd:3` (and the draft files).
- [ ] **[S]** Lecture-register leftovers: `feed_forward_nns.qmd:719` "in the lecture"; `recurrent_neural_networks.qmd:48` "For this course"; `lstm_neural_networks.qmd:289` "We do not cover GANs in class". A book should say "in this book/chapter".
- [ ] **[T]** Repo hygiene: `deep-research-report.md`, `deep-research-report-5.md`, `notes.tex`, `test.tex`, `texput.log`, `rnn_diagram.log`, `_quarto_backup.yml`, `_quarto_clean.yml`, `_old_references.bib` in root — delete or move.

## Global — cross-chapter notation harmonization

- [ ] **[S]** Loss symbol: $L$ / $\ell$ / $\mathcal{L}$ / $l$ across chapters; in Ch 5, $L$ is simultaneously loss and layer count (both meanings in one formula at `feed_forward_nns.qmd:560`). Suggest book-wide: $\ell$ per observation, $L$ sample average.
- [ ] **[E]** Ch 6 vs Ch 7 state contradictory Jacobians for the same object (`recurrent_neural_networks.qmd:233` transposed vs `lstm_neural_networks.qmd:141` correct). Fix Ch 6 (see chapter section).
- [ ] **[S]** Four weight-naming schemes across Ch 5–7: Ch 6 main text $W_{hh},W_{xh},W_{hy}$; Ex 6.1 $W_h,W_x$; Ex 6.2 $W_{ih},W_{hh},W_{ho}$ (undefined in text); Ch 7 recap $W_h,W_x$. Also concatenation convention $W_f\cdot[h_{t-1},x_t]$ vs sum form never reconciled ($W_f=[W_{f,h}\;W_{f,x}]$ sentence fixes it).
- [ ] **[S]** Hidden state bold $\mathbf{h}_t$ (Ch 6) vs non-bold $h_t$ (Ch 7); input dimension $p$ (Ch 5) vs $D$ (Ch 6/7).
- [ ] **[S]** $\sigma$ collision in Ch 13: Gaussian scale and logistic function two bullets apart (`adv_tree_based_methods.qmd:214,265,267`); Ch 12 uses $\sigma$ = logistic only. Rename scale $s(x)$ or use $\Lambda(\cdot)$ for logistic.
- [ ] **[S]** $F$ overload: forecast CDF vs true CDF (Ch 3, flips at `evaluating_distributions.qmd:225/486/508` and Ex 3.2); ensemble $F_m$ (Ch 12); Fisher info $F(\theta)$ vs CDF $\hat F(y|x)$ (Ch 13). Use $\mathcal{I}(\theta)$ for Fisher information (audience knows it from MLE).
- [ ] **[S]** Ch 11 is the only chapter using $\mathbb{V}$; every other chapter uses $\operatorname{Var}$.
- [ ] **[S]** Loss argument order flips between Ch 12 $\ell(y_i,F(x_i))$ and Ch 13 $\ell(\theta;y)$ — standardize or flag the switch.
- [ ] **[S]** "Gate" overload: Ch 5 backprop calls $g'(z)$ the "local gate" (`feed_forward_nns.qmd:577-581,605`); Ch 7 defines gates as sigmoid units. Rename in Ch 5.
- [ ] **[S]** Sigmoid range: Ch 5:180 correctly $(0,1)$; Ch 7:133 claims $[0,1]$.
- [ ] **[S]** QRF naming drift in Ch 13: "Quantile Random Forest(s)" vs Meinshausen's "quantile regression forests" — pick one.
- [ ] **[S]** Exam-annotation style: bare "*Exam level*" (`hpo.qmd:661,753,823`; `lstm_neural_networks.qmd:356`) vs descriptive annotations elsewhere — harmonize toward descriptive.
- [ ] **[S]** Solution label format: "**Part k:** Title" (standard) vs "**Part k.**" (`foundation_models.qmd:651,720,802,913`) vs "Task k" (LSTM Ex 7.1) vs solutions split across three callouts (RNN Ex 6.1, `recurrent_neural_networks.qmd:310-391`).
- [ ] **[E]** Ch 5–7 contain **no Python implementation** (Ch 5 chunks only plot; Ch 6/7 only build TikZ figures) despite CLAUDE.md's "Theory + implementation balance." Add a minimal fit/forecast example to Ch 6/7 or explicit forward pointers to Ch 8.

## Global — missed econometric bridges (one-paragraph additions each)

- [ ] Ch 2: expanding/rolling window = recursive/rolling pseudo-out-of-sample schemes (West 1996; Clark–McCracken) — never named. Also qualify "K-fold unsuitable for time series" with Bergmeir–Hyndman–Koo (2018).
- [ ] Ch 4: AdaGrad's accumulator $\sum g g^\top$ = OPG/BHHH information estimator; adaptive scaling = quasi-Newton/Fisher-scoring preconditioning (`optimization.qmd:180-189`). Overview promises the MLE connection; this is where it lives.
- [ ] Ch 5: MSE fitting of $f(x;\theta)$ = nonlinear least squares (never named); NN-as-sieve literature (White 1990; Chen 2007); cite ridge at the weight-decay bullet (:721).
- [ ] Ch 6: hidden state = *filtered* state (Kalman recursion) / observation-driven models (Cox 1981), not the latent state itself (`recurrent_neural_networks.qmd:48,182`).
- [ ] Ch 9: the Gaussian NLL at :82 *is* the GARCH quasi-likelihood with the recursion replaced by $g_{\phi_\sigma}(\mathbf{x}_t)$; Bollerslev–Wooldridge QMLE remark.
- [ ] Ch 10: tree = regressogram with data-chosen bins (sets up Ch 11's kernel-weights analogy at `random_forests.qmd:123`).
- [ ] Ch 12: componentwise L2-boosting = shrunken forward-stagewise regression (Bühlmann–Yu 2003) — the "sequential OLS on residuals" analogy named in CLAUDE.md is absent from the book.
- [ ] Ch 12↔13: Bernoulli Newton leaf step (÷ $\sum p_i(1-p_i)$ = Bernoulli Fisher info) = one-parameter Fisher scoring = Ch 13's natural gradient. One cross-reference sentence in §13.6.
- [ ] Ch 13: NGBoost can minimize CRPS (already defined in Ch 3) — unmentioned.
- [ ] Ch 15: classical regression prediction interval as opening contrast; normalized score at :526 = GARCH standardized-residual logic; Christoffersen coverage tests for §15.6's empirical coverage check.
- [ ] Ch 16: cite Loughran–McDonald (2011), Gentzkow–Kelly–Taddy (2019), Baker–Bloom–Davis (2016) at :15/:454/:502 (add to `references-local.bib`).

---

## Ch 1 — information_theory.qmd

- [ ] **[E/A]** :336 — "share support … Then $D_{\text{KL}}(p_0\|p_\theta)<\infty$" — false (Cauchy vs Gaussian counterexample: common support, infinite KL). Fix: shared support only rules out the support-violation $+\infty$; add $\mathbb{E}_{p_0}|\log(p_0/p_\theta)|<\infty$.
- [ ] **[E/A]** :266 — "symmetric only if $\sigma_0^2=\sigma_1^2$ and $\mu_0=\mu_1$" — false and contradicted by own Ex 1.5 (equal variances alone give symmetry).
- [ ] **[E/A]** :715,724-726 — Ex 1.3 solution gap: $\mathbb{E}_p[q/p]=\sum_{\mathrm{supp}(p)}q\le 1$, not $=1$; correct chain $D\ge-\log(\sum_{\mathrm{supp}(p)}q)\ge 0$; equality needs Jensen equality AND $\sum_{\mathrm{supp}(p)}q=1$; ":726 unconstrained outside support" misleading (equality forces $q=0$ there).
- [ ] **[E/A]** :406-408 — "learning about one variable can only reduce uncertainty" — only on average; $\mathbb{H}(Y|X{=}x)>\mathbb{H}(Y)$ possible (Cover–Thomas flag this). Also :406 understates the discrete iff for equality.
- [ ] **[E/C]** :106-116 — verbatim duplicate Bernoulli-entropy callouts (Example + Definition) — delete one.
- [ ] **[S/A]** :425-499 — fig-mi-example presents a k-NN MI *estimate* on n=100 as the population quantity; continuous MI never defined (chapter defines MI for discrete only); caption not self-contained. Consider ARCH example ($r_t,r_{t-1}$ uncorrelated, MI > 0) per "econometric data, always".
- [ ] **[S/B]** :84 — "generalized variance" analogy: term of art for $\det(\Sigma)$; entropy is relabeling-invariant so ignores outcome values — contrast with variance instead.
- [ ] **[S/A]** :334-361 — MLE–KL section iid-only; add forward link to conditional log score/KL for dependent data (AR/GARCH factorization). :343 continuous-case empirical-KL caveat; :354 White limit needs "under regularity conditions (unique KL minimizer)".
- [ ] **[S/B]** :208 — $\text{NLL}(q,X)$ used but never defined; $\mathbb{H}(\theta)$ overloads $\mathbb{H}(X)$; $I(x)$ (self-info) vs $\mathbb{I}(X;Y)$ visually adjacent; Ex 1.5 switches to capital $P,Q$.
- [ ] **[S/C]** — 16 hints for 16 sub-parts, mechanical; Ex 1.1 P2 hint states the answer; cut roughly half.
- [ ] **[T/A]** Ex 1.4 — "invertible" needs continuously differentiable, non-vanishing derivative (also :257 main text).
- [ ] **[T/B]** :221-226 reflection uses KL before introduced; :214 "log-score difference" before log score defined; :77 exclamation + scare quotes; :363-387 commented-out image-augmentation block (would violate content philosophy if restored); `***…***` pseudo-headings :242,260,268; "the figure above" instead of `@fig-` refs.
- [ ] **Exercises**: 6, all other algebra verified correct. Ex 1.1 P2 below bar (hint gives answer); Ex 1.5 P2–3 light back-to-back. **No dependence/non-iid exercise in the chapter** — add conditional-KL or AR(1) likelihood-factorization exercise.

## Ch 2 — cross_validation.qmd

- [ ] **[E/A]** :117 — "The whole point of CV is to approximate $R(\hat f)$" — conflates conditional risk with the CV estimand (expected risk of the procedure at training size $n(K-1)/K$; Bates–Hastie–Tibshirani 2023). Add estimand paragraph after :212.
- [ ] **[E/A]** :216 — "higher $K$ → less bias … lower $K$ → higher variance" — bias w.r.t. what unstated; variance direction reverses the usual claim and is setting-dependent (Arlot–Celisse 2010). State the training-size bias mechanism; drop or qualify variance sentence.
- [ ] **[E/A]** :914-916 — Ex 2.3: solution uses $\mathbb{E}[\xi_t|\mathcal{F}_t]=0$ but the statement assumes only unconditional mean zero. Add "$\{\xi_t\}$ iid innovations" (or independence from $\{z_s\}_{s\le t-1}$).
- [ ] **[E/A]** :281 — measurability definition requires the validation *outcome* to be $\mathcal{F}_t$-measurable — impossible. Restrict condition to predictors + training data; the outcome is the subsequently realized target.
- [ ] **[E/B]** :12 — "Nested validation … is the econometric analogue of what this chapter formalizes" — inverted; the econometric analogue is pretest/specification-search bias; nested validation is the ML answer.
- [ ] **[S/B]** :275-394 — name recursive/rolling pseudo-OOS schemes (see bridges); :284 qualify blanket "K-fold not suitable for time series" (Bergmeir–Hyndman–Koo 2018).
- [ ] **[S/A]** :535 — fold std is not a valid SE (folds share training data; Bengio–Grandvalet 2004) — add one sentence; students will t-test fold scores otherwise.
- [ ] **[S/A]** :785-789 — Ex 2.2 P2 strict inequality needs non-degeneracy (solution :862 quietly adds it) — put in the statement.
- [ ] **[S/C]** :185-188 — reflection question answered verbatim in the callout directly above — replace with a discriminating prompt (e.g., winsorizing at fixed vs full-sample percentile thresholds).
- [ ] **[S/C]** — hints mechanical (4+4+4); drop content-free ones (2.1 P4, 2.2 P2/P4, 2.3 P3/P4).
- [ ] **[S/C]** :41,226,330 echo:false; :403-404 `nn-cv-tuning` label lacks `fig-` prefix (not cross-referenceable); :329 caption not self-contained; purged/embargoed CV (:300) deserves a third panel in @fig-timeseries-cv; :398 hardcoded "[Section 5]" → `@sec-` ref, and it's a chapter.
- [ ] **[S/A]** :542 — nested CV estimates the performance of the tuning-plus-fitting *procedure* (selected HPs differ across outer folds) — one clarifying sentence.
- [ ] **[T]** Notation: $\Delta_j$ ≡ $z_j^{\text{honest}}$ duplication (:606-608); $R$ overloaded (functional, scalar, estimates); unremarked $n$→$T$ switch in Ex 2.1.
- [ ] **Exercises**: 3, all algebra verified correct. 2.2 P1–2 light (scaffolding OK); 2.3 solution P4 heading mislabeled ("Why Random CV Becomes Infeasible" — the *forecast* is infeasible).

## Ch 3 — evaluating_distributions.qmd

- [ ] **[E/A]** :376 and :709 — "upward-sloping PIT histogram" description of skew mismatch contradicts the chapter's own figure (replicated: deficit near 0, hump left of center, only modest uptick at 1). Rewrite both.
- [ ] **[E/A]** :698 — models ranked by raw average LogS/CRPS over 63 quarters, no DM/HAC test, LogS gap driven by 2020Q2 — while :112/:517 teach exactly this. Add DM-type comparison with HAC on the score-difference series, or a caveat noting the single-observation dominance.
- [ ] **[E/A]** :135 — interval-gaming example inconsistent with the miss-indicator criterion at :133 (under it, always-infinite intervals dominate). Restate criterion as $|\text{coverage}-0.90|$ or change the gaming strategy.
- [ ] **[E/A]** :369 — "marginal calibration (PIT uniform)" — clashes with GBR/Gneiting–Katzfuss terminology (that is *probabilistic* calibration; marginal calibration = average forecast CDF matches unconditional distribution). Rename; cite `GneitingKatzfuss2014` (already in bib, uncited); consider stating "maximize sharpness subject to calibration".
- [ ] **[E/B]** :369 — $u_t=F_t(y_t)$ index clash (conditional on $\mathcal{F}_t$, $y_t$ known); use $F_t(y_{t+1})$ or shift index; add one-step-ahead clause to DGT iid-U(0,1) result.
- [ ] **[E/A]** :335, :282 — strict-propriety classes unspecified (CRPS: finite first moment, $\mathcal{P}_1$; LogS: densities); kernel representation at :282 needs finite first moment. Cosmetic: $CRPS$ italic → $\text{CRPS}$.
- [ ] **[E/C]** :527-529 — broken bullet rendering (verified in built HTML) + "notion" typo.
- [ ] **[S/B]** :225 vs :486 vs :508 — $F$'s forecast/true role flips inside the CRPS material and again in Ex 3.2 — reserve $F$ for the forecast, or flag the callout-local convention and fix :508.
- [ ] **[S/A]** :503 — $\int(F-G)^2dz$ is the **Cramér distance**, not Cramér–von Mises (which integrates against $dF$).
- [ ] **[S/A]** :678,:700 — 15 bins on 63 test quarters (~4.2 obs/bin), no uniformity bands, test-window size never stated in text; :449 promises serial-dependence PIT diagnostics never shown. State $n=63$, use ~8 bins, add bands or caveat.
- [ ] **[S/C]** :16-22 Roadmap omits the empirical application; :512-519 "Beyond LogS and CRPS" is a one-callout section — fold in; :3 stale YAML comment; :523 link FRED-QD description to `datasets.qmd`.
- [ ] **[S/C]** :539,:653 — captions carry heavy interpretation (move to prose); :342 "Measurement Error Sensitivity: High/Low" table row asserted with zero supporting text — explain or cut.
- [ ] **Exercises**: 3, all algebra verified correct. 3.1 P1 scaffolding, P4 below bar, hints mechanical (P1 restates, P4 gives answer); 3.1 P3 note criterion diverges at boundary (so FOC is the min); 3.2 a.e.-vs-everywhere equality clause + Tonelli parenthetical; **no dependence/forecast-comparison-testing exercise** — add HAC-on-score-differences or PIT-uniformity≠independence part.

## Ch 4 — optimization.qmd

- [ ] **[E/A]** :163 vs :170-171 — momentum off-by-one: $g_t$ evaluated at $\theta^{(t-1)}$ but update maps $\theta^{(t)}\to\theta^{(t+1)}$ (gradient two iterates stale). Rewrite as $\theta^{(t)}=\theta^{(t-1)}-\eta v_t$ (AdaGrad/RMSprop/Adam already consistent).
- [ ] **[E/A]** :971-990 — Ex 4.2 P2 solution is circular (cites the SRSWOR variance formula the part asks to show). Derive via inclusion probabilities $\pi_i=b/N$, $\pi_{ij}=b(b-1)/(N(N-1))$.
- [ ] **[E/A]** :71, :85 — convergence claims with no conditions (batch GD "stable and direct"; Robbins–Monro "recovers convergence"). Add short formal box: convex + $L$-smooth + $\eta\le 1/L$ ⇒ $O(1/t)$; nonconvex smooth ⇒ $\|\nabla L\|\to 0$ only. GD diverges on the chapter's own Ex 4.1 quadratic if $\eta>2/a$.
- [ ] **[E/A]** :231 — Adam bias-correction takes expectation over mini-batch randomness explicitly assumed away at :163 — one sentence reinstating the probability space.
- [ ] **[E/A-B]** :690-695 vs :518,:523 — nonconvex comparison figure uses lr 0.01/0.001/0.3 across optimizers, undisclosed (first figure discloses its exception at :265). State the adaptive-scale rationale in text and caption.
- [ ] **[S/B]** :120-123 — dependence reflection answer too vague; name the actual mechanisms: unbiasedness of the minibatch gradient survives dependence (linearity), variance changes, real dangers are stateful/sequence models and preprocessing leakage.
- [ ] **[S/C]** :785-1111 — no econometric-diagnostic part in the exercise set. Cheapest fix: Ex 4.2 Part 4 on contiguous time-block vs random batches under serial correlation (formalizes the :115 reflection).
- [ ] **[S/A]** :168 — Hessian-PSD equivalence needs twice differentiability (ReLU next chapter is the non-smooth case); move convexity definition to a Definition callout near first use (:85 already needed it).
- [ ] **[S/C]** :125-150 — Epoch definition in `callout-tip` → `callout-note` per callout table; algorithm notation drift ($n_{e,b}$ duplicates $J$; $T$ not in Input; $L_j$ computed but unused).
- [ ] **[S/B]** :24-56 — $\eta$, $\nabla$, loss used before `## Notation` defines them; :32 $l$ vs :35 $L$ vs $\ell_i$ — three loss symbols; move Notation up; rename the 2D demo function (:262, also axes labeled $\theta_1,\theta_2$ while defined in $(x,y)$).
- [ ] **[T/C]** :269,:523 captions not self-contained (panels/paths/markers undefined); :1003-1005 chapter-boundary callout sits between Ex 4.2 and 4.3 — move above `## Exercises`; :3 stale YAML comment.
- [ ] **Exercises**: 3, all verified except the circular 4.2 P2 solution. 4.1 P1 hint restates; 4.2 fixed-partition (main text) vs SRSWOR (exercise) mismatch worth a sentence; 4.3 exemplary (Schur–Cohn/AR(2) verified) but uses $\theta_t$ vs chapter's $\theta^{(t)}$.

## Ch 5 — feed_forward_nns.qmd

- [ ] **[E/A]** :623 — invalid non-convexity inference (sign-varying cross-partial is compatible with PSD Hessians). Replace with a negative 2×2 principal minor at a specific point, or the sign-flip symmetry argument (two distinct minimizers whose midpoint has $w_2=0$).
- [ ] **[E/A]** :76 vs :155-160 — layer-count convention contradiction: parameter-count formula treats $L$ as hidden layers + extra output layer, against the declared convention (layer $L$ *is* the output). Pick one.
- [ ] **[E/A]** :91,:199,:560 — output-layer $\delta^{(L)}$ formula holds only for element-wise activations, yet softmax is recommended; give the softmax+CE result $\delta^{(L)}=\hat{\mathbf p}-\mathbf y$ (mirroring Ex 5.3's sigmoid case).
- [ ] **[E/A]** :696 — standardization advice never says "fit the scaler on the training split only" — the canonical leakage vector; also missing from the Common Pitfalls box (:747 catches shuffling only).
- [ ] **[S/A]** :637 — "$\mathbb{E}[Y|X=x]=f(x;\theta)$" asserts correct specification ("we model/approximate"); :36 single-index/GLM hierarchy inverted.
- [ ] **[S/B]** :549,:560,:621,:1095 — symbol overloads: $L$ loss vs layer count in one formula; $H_{jk}$ Hessian vs $H$ width; Ex 5.3 reuses $L(\theta)$ for the likelihood.
- [ ] **[S/B]** :587-591 — callout conflates optimizer's parameter iterate with the network's data input; per-example-then-average gradient convention never stated.
- [ ] **[S/A]** :723 — dropout: units dropped independently w.p. $1-p$ ($p$ = retention), not a fixed fraction; test-time rescaling unmentioned.
- [ ] **[S/C]** :28-649 — "Basic Architecture" spans ~620 lines and swallows roadmap items 2–4; split into `##` sections so the TOC matches the roadmap.
- [ ] **Exercises**: 3, all algebra verified correct (ReLU representation, gradients, $g'\le 1/4$ bound, $\partial\mathcal{L}/\partial z=p-y$). Ex 5.2 P2 wording implies the uniform bound explains saturation (solution prose handles it — align wording); hints mechanical (P1 hints of 5.2/5.3 restate setup).

## Ch 6 — recurrent_neural_networks.qmd

- [ ] **[E/A]** :233 — Jacobian transposed: $\partial\mathbf h_i/\partial\mathbf h_{i-1}=\operatorname{diag}(g'(\mathbf z_i))\,\mathbf W_{hh}$, not $\mathbf W_{hh}^\top\operatorname{diag}(g')$ (that is the backward adjoint); product order unstated (descending $J_tJ_{t-1}\cdots J_{k+1}$). Contradicts Ch 7:141 (correct).
- [ ] **[E/A]** :452-454 (premise :411) — **Ex 6.2 P4 model answer wrong**: $\partial h_2/\partial x_1=(W_{hh}\tanh'(z_2))(W_{ih}\tanh'(z_1))\approx 0.38$ — substantial memory; solution conflates near-zero state *value* with loss of dependence and contradicts its own $\le 0.8$/step bound. A student computing correctly would be marked wrong. Rewrite around geometric decay vs cancellation-by-new-inputs.
- [ ] **[S/A]** — exploding gradients absent (Ch 7's table presupposes them); add paragraph after :242 incl. clipping.
- [ ] **[S/A]** — no window construction / truncated BPTT / batching of overlapping sequences / stationarity-as-justification for parameter sharing (:154) — the missing applied core for this book.
- [ ] **[S/B]** :48,:182,:177 — analogue should be *filtered* state / observation-driven models (Cox 1981), not the latent state; "structural interpretation" of GARCH $\sigma_t^2$ misuses "structural".
- [ ] **[S/C]** :310-391 — Ex 6.1 solutions split across three callout-tips; hint titles nonstandard; :293 Hint 1 hands over the formula P1 asks to derive.
- [ ] **[S/B]** :226 — output $\mathbf y_T$ vs target $y_T$ same letter, bold-only distinction.
- [ ] **[S/B]** :134 vs :278 vs :400-404 — three weight-naming schemes in one chapter; $W_{ih}$, $W_{ho}$ never defined.
- [ ] **[T/B]** :37 vs :53 near-verbatim duplication; fig-rnn-side-by-side caption doesn't explain node/arrow semantics; Ex 6.2's image (:396) has no caption/label/discussion.
- [ ] **Exercises**: 2. 6.1 meets bar (spectral-norm extension correct); 6.2 P1–3 arithmetic verified, P4 wrong (above); no comparison-across-models part.

## Ch 7 — lstm_neural_networks.qmd

- [ ] **[E/A]** :216-220, :289 — Chen–Pelger–Zhu case study misdescribed (verified against the paper, Mgmt Sci 2024): (i) 46 characteristics + 178 macro series, not 94; (ii) 1967–2016, not 1957; (iii) objective is the no-arbitrage GMM moment condition $E[M_{t+1}R^e_{t+1,i}g(I_t,I_{t,i})]=0$ with adversarial test assets, **not** MSE — the paper argues prediction-objective ML can underperform; ":289 GAN adjusts the objective beyond MSE" inverts the message. Quoted Sharpe/R² numbers are correct. Either present MSE framing as Gu–Kelly–Xiu and CPZ as the no-arbitrage alternative, or rewrite Steps 1–3 around the moment condition.
- [ ] **[E/C]** :328-356 — the chapter's only exercise is pure substitution into equations printed 40 lines earlier (disallowed by CLAUDE.md); no derivation/comparison/diagnostic anywhere. Add: derive $\partial C_T/\partial C_t|_{\text{gates fixed}}=\prod f_k$, compare to RNN bound $|W_h|^{T-t}$ (Ex 6.1), explain why the gates-fixed caveat matters.
- [ ] **[S/A]** :135 — "gradient magnitude depends only on forget gates, not weights" — overclaim (true only for the gates-fixed cell-state path; forget gates are weight-dependent); the :169 Scope note corrects it — qualify in place.
- [ ] **[S/A]** :28 — forget gate not in Hochreiter–Schmidhuber (1997); added by Gers–Schmidhuber–Cummins (2000) — one attribution clause.
- [ ] **[S/A]** :209 — "Linear Factor Models" label over a linear *characteristics* regression (Fama–MacBeth style) — label/equation mismatch.
- [ ] **[S/B]** :133 — sigmoid range is $(0,1)$, so $f_t=1$ unattainable — gradients always attenuated, just controllably slowly (:162 narrative).
- [ ] **[S/C]** :178 — "$O(H^2)$ vs $O(4H^2)$" meaningless; say $4H(H+D)+4H$ ≈ 4× an RNN cell.
- [ ] **[S/C]** :228-240,:77,:252 — mermaid NN1 diagram has no label/fig-cap; one-line captions far from self-contained (TikZ gate symbols unexplained).
- [ ] **[T/C]** :3 stale YAML comment; :84-93,:259-267 `if (TRUE)` guards force TikZ rebuild every render (copy Ch 6's mtime pattern); :16 blog post as primary intuition pointer.
- [ ] **Exercises**: 1; all six values verified correct; "Task k" labels; the σ/tanh numerical values live in Hint 3 but are required data — move into the statement; bare annotation.
- [ ] **[T]** Chapter is the thinnest in substance (case study + figure code dominate); needs new material (BPTT-for-LSTM or estimation discussion) more than edits.

## Ch 8 — nn_example.qmd

- [ ] **[E/A]** :463 vs :541 — tuning certifies configs by best epoch within 30 (implicit early stopping); final model trains 100 epochs on train+valid with no early stopping — selected HPs never evaluated under the deployed protocol. Record and reuse best epoch, or EarlyStopping in both stages; at minimum disclose.
- [ ] **[E/A]** :549,:572 — $\exp(\hat z)$ is a conditional-median estimate of $RV$; MSE/QLIKE reward the conditional mean — log-target models handicapped without the $\exp(\sigma^2/2)$-type correction (identity stated at `distributions_via_nns.qmd:305`). Acknowledge or correct.
- [ ] **[S/A]** :615 — per-period SD of squared-error differences conflated with the SE of the mean loss differential (HAC-adjusted, smaller by $\sqrt{n_{\text{test}}}\approx 15$–20); ":roughly 0.01" asserted without derivation. Fix both.
- [ ] **[S/A-C]** :202-287 vs :488-491,:590-594 — dead level-target arrays (`X_lag_rv_*` etc.) never used; `tune_model` closes over log-target globals, so level-target rows aren't reproducible from shown code (text disclosure at :570 exists). Show an `eval: false` level-pipeline chunk or delete the arrays.
- [ ] **[S/B]** :619 — "scale-equivariant" → scale-*invariant* (homogeneity of degree zero). (Adjacent underprediction-penalty claim is correct.)
- [ ] **[S/B]** :572 vs :574 — $n$ vs $n_{\text{test}}$ in RMSE vs QLIKE in the same paragraph.
- [ ] **[S/C]** :4-6 — self-invented YAML fields (`chapter-type`, `exercises-required: false`) exempt the chapter from `## Exercises`; codify an empirical-illustration exception in CLAUDE.md or add 1–2 pen-and-paper exercises (QLIKE invariance/asymmetry; SE of a loss differential under dependence; HAR lookahead check).
- [ ] **[T/B]** :611 — caption garbled ("test-period realized log realized variance"); enumerate plotted series. :41 vs :574 forecast time-index convention shifts ($\hat z_{t+1|t}$ → $\widehat{RV}_t$) — one defining clause.
- [ ] Verified sound (keep): chronological split with origins formed pre-split; train-only scaling; HAR averages lookahead-free; fair HAR-OLS refit on train+valid (disclosed); shuffle=False; test block touched once; quoted 0.0003 LSTM–HAR gap matches table.

## Ch 9 — distributions_via_nns.qmd

- [ ] **[E/A]** :232-235,:275,:292-295 — empirical application has no validation block; hyperparameters (32 units, lr 1e-3, 200 epochs) have no stated provenance; `X_trva` named "train+valid" but nothing validated — contradicts Ch 8's discipline on the same data/split. State a-priori fixing or carve out a validation block; also one clause on why scaling on 80% (vs Ch 8's 64%) is fine here.
- [ ] **[S/B]** :80-82 vs :435 — "up to constants": the displayed $\ell_t$ is 2×Gaussian NLL − $\log 2\pi$ (positive affine, not additive constant); inconsistent with Ex 9.1's correct ½ factors — harmonize.
- [ ] **[S/B]** :155 — "$K$ indexes the mixture components" — $k=1,\dots,K$ indexes; $K$ is the count.
- [ ] **[S/C]** :14-20 — Roadmap omits the empirical application; item 5 wrong about what closes the chapter.
- [ ] **[S/C]** :101 — hemisphere-network fig-cap not self-contained (boxes/core/heads undefined).
- [ ] **[S/B-C]** :331 — caption carries interpretation + "breathes" register + factor-1.6 claim (prose at :357 already covers it) — move to text.
- [ ] **[S/B]** :75-94 — add GARCH-QMLE bridge (see global bridges).
- [ ] **[T/A]** :61-65 — models condition on finite $\mathbf x_t$, not $\mathcal{F}_{t-1}$: the training sum is a partial/quasi-likelihood — one clause.
- [ ] **[T/A]** :401 — score difference read without noting it is untested (DM cross-ref clause).
- [ ] **[T/B]** — quantile-regression networks (pinball loss, crossing) absent from a "distributional NNs" chapter — one-sentence pointer preempts the question.
- [ ] **Exercises**: 2, all algebra verified correct (9.1 minimizer $e^2$, $\max\{e^2,c\}$ matches the chapter's own `VAR_FLOOR` code; 9.2 mixture variance and density limits). 9.1 P2–3 both 1–3 min — consider merging; hints mechanical (9.2 P2 hint *is* the answer; 9.1 P1 restates).

## Ch 10 — decision_trees.qmd

- [ ] **[E/A]** :334-342 — cost-complexity objective has no optimization domain (subtrees $T\subseteq T_0$ by collapsing internal nodes) and no weakest-link/nested-sequence result (BFOS) — as written, ill-posed and infeasible. Two sentences + tie $\alpha$ tuning to the :346 warning.
- [ ] **[E/A]** :111 — recursion has no stopping rule (never terminates as described). State base termination (pure node / min size / no improving split), then pre-pruning tightens it.
- [ ] **[S/A]** :304-317 — bias-variance display: $\varepsilon_0$ and bias target undefined; posit $Y_0=f(x_0)+\varepsilon_0$, independence, expectation over new draw + training sample.
- [ ] **[S/B]** :10 — "Regreesion" typo; monograph title is "Classification and Regression *Trees*".
- [ ] **[S/A]** :111 — "guarantees a local optimum" — no topology in which that's true; say myopically optimal given prior splits.
- [ ] **[S/C]** :116,:158,:257 echo:false; :157 (and :115) captions not self-contained (fill/scatter colors, missing colorbar).
- [ ] **[T/B]** — regressogram bridge (see global); :149,:190 "The figure shows…" → `@fig-` refs; Ex 10.1 hints P1/P4 restate the task.
- [ ] **Exercises**: 2 (9 sub-parts), all arithmetic verified (stump SSE 5.1875; split SSEs 3.5/3.625/0.5; crossover α = 4.6875; entropies/Ginis; threshold 0.2). 10.2 P1–4 substitution-heavy, P4 a read-off — acceptable as scaffolding for P5, but consider tightening.

## Ch 11 — random_forests.qmd

- [ ] **[E/A]** :111-121 — forest-weights identity stated as exact but inexact under bootstrap multiplicity (distinct-observation weights vs bootstrap-sample leaf means). Weight by multiplicity $m_{ib}$ or state the convention under which it is exact.
- [ ] **[E/C]** :317 — "same as in constrained boosting" forward-references Ch 12 material; make self-contained here, dedupe the near-identical `monotonic_cst` block across chapters.
- [ ] **[S/A]** :43-69 — variance formula: state the probability space (randomization conditional on sample vs joint) and $\rho\ge 0$ for the lower-bound reading (formula valid for $\rho\ge -1/(B-1)$).
- [ ] **[S/A]** :306 — $p/3$, $\sqrt p$ defaults misattributed to @Breiman2001RandomForests (his Forest-RI uses $m=1$, $\lfloor\log_2 p+1\rfloor$); cite Liaw–Wiener (2002) — new entry in `references-local.bib`.
- [ ] **[S/A]** :202 — "approximately honest" uses the Wager–Athey term informally; say "approximately out-of-sample" (the exercise solution at :715 already does).
- [ ] **[S/A-B]** :362 — conflates (i) iid resampling destroying dependence in training with (ii) OOB evaluation leakage (post-$t$ trees predicting date $t$); also mention block bootstrap/subsampling as a resampling-side remedy.
- [ ] **[S/C]** :517-533,:652 — Ex 11.1 P2 hint hands over the full derivation (whose target formula is printed in the body); 11.2 P2 is a 30-second multiplication. Trim hint to $\text{Cov}=\rho\sigma^2$; merge 11.2 P1–2; add one harder part (heterogeneous correlations, or finite-$B$ gap as MC error).
- [ ] **[S/C]** :130,:230 echo:false; fig-oob-convergence caption must say data are simulated iid (that's *why* OOB tracks test MSE there).
- [ ] **[T/B]** :39,:111 — $L$ subsample size vs $L_b(x)$ leaf collision (rename $\ell$ or $s$); subagging uncited; permutation-importance off-support pathology sentence (:375-383).
- [ ] **Exercises**: 2, all verified (1.872; 79.2%; $e^{-1}$; 184). Set below the difficulty bar overall; 11.2 P4 (real-time reasoning) is strong.
- [ ] Noted correct (keep): "forests cannot overfit" folklore handled properly at :296 ($B$ = Monte Carlo error; complexity in leaf size/depth).

## Ch 12 — gradient_boosting.qmd

- [ ] **[E/A]** :267 — least-squares-to-pseudo-residuals ⟺ weighted classification holds only if the base learner outputs $\pm 1$ — stated for $y_i$, not for $h$; false for the regression trees used elsewhere. Add the condition; one clause that the AdaBoost correspondence covers the weighting, not the step size $\alpha_m$.
- [ ] **[S/C]** :723 — Ex 12.2 titled "…and Early Stopping" but no part touches early stopping; and the chapter's exercise set has no econometric-diagnostic part. Add Part 4: why choosing $M$ by random K-fold on an AR-dependent target biases validation loss downward vs a time-ordered split (ties to the :499-503 warning) — or retitle.
- [ ] **[S/B]** :58-104 — add the componentwise-L2-boosting/forward-stagewise paragraph (global bridges; CLAUDE.md's flagship analogy).
- [ ] **[S/C]** :125-126,:360-361 — echo:false + non-self-contained captions (define panels, red line, scatter, synthetic DGP; fig-gb-fredqd at :433 is the model to copy).
- [ ] **[S/A]** :299 — "halving $\nu$ approximately doubles optimal $M$ [@ZhangYu2005]" — they prove consistency of early-stopped boosting, not this reciprocal; mark as empirical regularity (Friedman 2001) and move the citation.
- [ ] **[T/B]** :238 — the contrast is probability scale vs *log-odds* scale (where $F$ lives), which is why the Newton step at :240 is needed — reword.
- [ ] **[T/B]** :524 — "flexible loss functions" strength claim vs only squared/Bernoulli/exponential derived; one sentence on quantile/Huber losses + subgradients at kinks, connecting to Ch 13.
- [ ] **Exercises**: 2, all arithmetic verified to the last digit (12.1 SSE chain; 12.2 $F_0=\log 3$, pseudo-residuals). 12.1 P1 is 2-min recall (scaffolding).

## Ch 13 — adv_tree_based_methods.qmd

- [ ] **[E/A]** :97 — pooled-neighbor view claimed "equivalent" to the weight representation — exact only when the leaf containing $x$ has equal size in every tree (Ex 13.1 silently satisfies it: all leaves size 3). Say "approximately; exactly when…"; optionally new Ex 13.1 part deriving when the views coincide.
- [ ] **[E/C]** :2 — YAML `title:` → duplicate `<h1>` in built HTML (verified). Delete.
- [ ] **[E/A]** :257 — NGBoost update never displayed (no iteration index, no $\nu$, no $\theta^{(m)}(x)=\theta^{(m-1)}(x)-\nu\hat h_m(x)$, no early stopping). One display + carry-over sentence cross-referencing @sec-gb-regularization / @sec-gb-early-stopping.
- [ ] **[S/B]** :214,:265,:267 — $\sigma(x)$ = Gaussian scale and logistic within one list (see global notation).
- [ ] **[S/A]** :99-103 — Wager–Athey consistency callout omits the **iid sampling** assumption (the caveat this book most needs); add Meinshausen's own QRF consistency clause.
- [ ] **[S/C]** — only one figure in the chapter; add (i) NLL contours in $(\mu,\log\sigma)$ with ordinary vs natural gradient steps, (ii) step-function $\hat F(y|x)$ from Ex 13.1's pooled sample.
- [ ] **[S/C]** :338-366,:479 — hints: 13.1 P5 hint *is* the answer, P1 nearly; 13.2 P3 hint restates the definition. Delete.
- [ ] **[S/C]** :461-462 — 13.2 P3 (30–60 s) and P4 (1–2 min) below bar — merge; add reparameterization-vs-Fisher-scaling part ($\partial\ell/\partial\theta=\lambda y-1$ under $\theta=\log\lambda$ = natural gradient ÷ $\lambda$).
- [ ] **[T/B]** :61 — "estimates something like $\mathbb{E}[Y|X=x]$" — precisely the prohibited suggestive phrasing; state the estimator.
- [ ] **[T/C]** :28-40 — §13.2 re-derives weights from `random_forests.qmd:109` (@sec-rf-weights, which forward-links here) without a back-reference — open with "Recall from @sec-rf-weights…".
- [ ] **Exercises**: 2, all arithmetic verified (pooled CDF, median 12, P25 = 11; Poisson natural gradient 0.08).

## Ch 14 — hpo.qmd

- [ ] **[S/A]** :321,:331 — EI incumbent defined as the noisy min $c_{\min,t}=\min_j\hat c_j$ right after the chapter proves that min is optimistically biased; acknowledge and give the plug-in alternative $\min_j m_t(\lambda_j)$.
- [ ] **[S/C]** :732,:744-750 — Ex 14.2 P1 recall (1–2 min), P3 read-off (30 s); no derivation part in 14.2 or 14.3. Replace P1 with deriving the EI closed form from $\mathbb{E}[\max\{c_{\min}-C,0\}]$; give P3 content (TPE's EI increasing in $\ell/g$).
- [ ] **[S/C]** :664-686,:756-778,:826-848 — 12 hints for 12 parts; keep ~3 with scaffolding value.
- [ ] **[S/C]** :661,:753,:823 — bare "*Exam level*" → descriptive annotations (match foundation_models style).
- [ ] **[S/A]** :49-63 — prose claims optimism vs the *selected* configuration but the display proves it vs $\min_j c_j$; add the $\mathbb{E}[c_{\hat\jmath}]\ge\min_j c_j$ sentence.
- [ ] **[S/B]** :513-519 — $B$ uninterpreted (per-bracket budget in Li et al.; total ≈ $(s_{\max}+1)B$).
- [ ] **[T/A]** :552-556 — schematic bracket counts [27,9,3,1]/[9,3,1]/[3,1] don't satisfy the $n_s$ formula displayed above (true values 27,12,6,4) and budgets are unequal — reconcile or flag the simplification in text.
- [ ] **[T/B]** :428,:436 — $y$ and $\gamma$ each defined twice (unmerged edit); delete the second clause.
- [ ] **[T/A]** :656 — Ex 14.1 needs non-degenerate noise for the strict inequality (used at :701).
- [ ] **[T]** :77,:355 — `import math` lives in the wrong chunk (session-shared; breaks standalone).
- [ ] **Exercises**: 3; all solutions verified numerically (EI 0.0300 vs 0.0307; SH 324 vs 2187 = 6.75×; min-identity + induction). 14.1 exemplary (ideal derivation/comparison/diagnostic mix); 14.2/14.3 below bar (above).

## Ch 15 — conformal_prediction.qmd

- [ ] **[E/A]** :1022 — jackknife+ "finite-sample marginal coverage result" — level never stated: Barber et al. (2021) prove ≥ **1−2α** (CV+ ≥ 1−2α−min(…)), requiring a *symmetric* fitting algorithm; interval targets 1−α so students infer the wrong guarantee. State both.
- [ ] **[E/A]** :649-651,:754,:762 — prose says calibration spans 2000Q1–2011Q4; FRED-QD dates quarters by final month, so the code's `<= 10-01` cutoffs end at Q3 and **1999Q4/2011Q4 fall into no subsample** (verified by execution). Fix cutoffs to `12-01` or correct the prose (incl. fig caption :762).
- [ ] **[E/A]** :754 — overcoverage explained by finite-sample discreteness — wrong: with $n_{\text{cal}}=47$, discreteness caps expected coverage at 44/48 ≈ 91.7% < observed 94.3%. Correct explanation: test-window sampling noise ($n=53$, binomial SE ≈ 4pp) + calibration-draw variability (Beta$(k,n{+}1{-}k)$) + non-exchangeability.
- [ ] **[E/A-B]** :601 — fig-cqr-recalibration caption: "widening is largest where the band is already wide" — false; the conformal correction adds constant $2\hat q$ everywhere; adaptivity comes from the initial band. Rewrite caption.
- [ ] **[E/A]** :416-423,:465 — chapter proves only the heteroskedasticity example; add the general distribution-free conditional-coverage impossibility remark + citations (Vovk 2012; Lei–Wasserman 2014; Foygel Barber–Candès–Ramdas–Tibshirani 2021) — new bib entries. Key Takeaway 5 otherwise invites "better score restores conditional validity".
- [ ] **[E/C]** :1419-1444 — Ex 15.3 P1 numerically identical to the in-text "Jackknife+ by Hand" worked example (:921-977). Change numbers; make $(1-\alpha)(n+1)$ non-integer to exercise the ceiling logic. Also P3/P4 near-identical answers.
- [ ] **[S/A]** :1057 — ACI described only verbally; add $\alpha_{t+1}=\alpha_t+\gamma(\alpha-\text{err}_t)$ and its *deterministic* long-run guarantee ($|T^{-1}\sum\text{err}_t-\alpha|=O(1/(\gamma T))$, no distributional assumption — the flagship result for the book's theme); one sentence on weighted/nex conformal (Barber et al. 2023).
- [ ] **[S/A]** :98 — "inductive" introduced without its contrast; add a short full-(transductive)-conformal paragraph (refit on augmented data per candidate $y$; cost) — completes the efficiency ladder for §15.10.
- [ ] **[S/A]** :435,:449-450,:463 — "continuous CDF ⇒ strictly increasing on its support" false (disconnected support); symmetry assumed but never used. Assume everywhere-positive density; drop or use symmetry.
- [ ] **[S/B]** :554-593 — three hatted $q$'s collide ($\hat q_{\text{low}},\hat q_{\text{high}}$ functions vs conformal scalar $\hat q$); rename $\hat q_{\text{cal}}$; state which levels the initial quantile models target (α/2, 1−α/2) and that validity holds for any fixed band while efficiency depends on the choice.
- [ ] **[S/B]** :12,:526,:756 — econometric anchors (see global bridges: prediction interval / GARCH / Christoffersen).
- [ ] **[S/A]** :756 — high-VIX subgroup is 9/11 = 81.8%, binomial SE ≈ 12pp; "exactly the lesson from the theory" overclaims — report $n=11$ in prose, soften to "consistent with".
- [ ] **[S/B]** :272 — exchangeability "slightly weaker" than iid → *strictly* weaker + one exchangeable-but-dependent example (equicorrelated Gaussians / de Finetti).
- [ ] **[S/A]** :393 — "iid infinitesimal perturbation" undefined; use $U_i\sim\text{Unif}(0,\delta)$ with $\delta$ below the minimal score gap, or auxiliary-uniform rank tie-breaking.
- [ ] **[T/C]** :22-29 — Roadmap omits the real-data section; ordering of item 5 misleads. Future-split seam: §15.8 (time series) is the natural place if ACI content grows.
- [ ] **Exercises**: 4; all arithmetic verified (15.1 $k=18$, q̂=1.8, exact 18/20; 15.2 [28,52]; 15.4 covariances). 15.2 P4 reproduces the :568-593 derivation verbatim (recall); 15.4 best exercise ("such as ρ=0" → "iff ρ=0"). Missing exercise content: coverage-bound algebra, ties, jackknife+ level, CQR-vs-symmetric width.

## Ch 16 — foundation_models.qmd

- [ ] **[E/A]** :61 (and :53) — "under stationarity the RHS does not depend on $t$" — false in general (conditioning history grows; finite-context transformer is neither fixed-order Markov nor a stationary function of the infinite past). Define $H(p^\star,p_\theta)$ as a Cesàro rate, state the condition on $p_\theta$ or flag as heuristic; a.s. convergence needs generalized SMB (Algoet–Cover 1988; Barron 1985), not Cover–Thomas Ch. 4.
- [ ] **[E/B]** :406 — "$d_4$ … published before $t$ but cites material produced after $t$" — temporally impossible; intended point is retriever-side contamination (figure code marks $d_4$ admissible). Rewrite.
- [ ] **[E/A]** :659,:666 — Ex 16.1: sum is $-17.6098$ (not $-17.6096$); PPL $=\exp(2.2012)=9.036$ (not 9.038). Part 3's numbers correct.
- [ ] **[S/C]** :74,:202,:278,:405 — four of six figures (`fig-fm-nextoken`, `fig-fm-attention`, `fig-fm-attenuation`, `fig-fm-timeline`) never referenced in prose — add one interpreting `@fig-` sentence each.
- [ ] **[S/C]** :634 — Ex 16.1 P1–2 not pen-and-paper answerable (no $\ln$ values supplied, unlike 14.2's Φ/φ table); supply values or ask for exact expressions.
- [ ] **[S/C]** :651,:720,:802,:913 — "**Part k.**" → "**Part k: Title**"; also `---` rules between exercises (:675,:769,:841) inconsistent with hpo.
- [ ] **[S/A]** :454,:502,:610 — dictionary baseline required three times, canonical anchors uncited (Loughran–McDonald; Gentzkow–Kelly–Taddy; Baker–Bloom–Davis) — add to bib + cite.
- [ ] **[S/B]** :510 — collinearity + ΔR² = 0.08 + "high R² ⟹ overfitting noise" internally inconsistent — rewrite the statistical explanation around overfitting noise in $z_t$ (large $k_z$/short sample).
- [ ] **[S/B]** :369 vs :448 — $x_t^{\text{text}}=G(D_t)$ then $z_t=G(D_t)$ — same object, two names; $H$ (cross-entropy vs persona distribution) and $h$ (horizon vs persona weight) overloads — unify/rename or flag explicitly (hpo :521 shows the pattern).
- [ ] **[T/B]** :387 — "all documented empirical examples run in this direction" — unsupported universal; soften or cite. :259 — "unordered discrete label" misfires (hawkish/neutral/dovish is ordered).
- [ ] **Exercises**: 4; 16.2 (EIV incl. non-classical cross-term $\rho\sigma_s\sigma_u(\sigma_u^2-\sigma_s^2)$) and 16.4 (bias decomposition; 0.7·3.3+0.3·5.3=3.9) verified exact — both exemplary; 16.1 P1–2 weak scaffolding redeemed by P3.

## Ch 17 — datasets.qmd + front matter

- [ ] **[S/C]** `datasets.qmd:2,7` — YAML `title:` + `#` heading: check for the same duplicate-h1 rendering as adv_tree_based_methods (fixed there by deleting the YAML title).
- [ ] **[T/B]** `datasets.qmd:127,134` — "Realized variance, sum of squared 5-minute log returns in percent" — unit ambiguity (%² vs %); one clarifying clause.
- [ ] **[E/B]** `index.qmd:65,67` — citation syntax (listed under Global; kept here for chapter-sweep completeness).
