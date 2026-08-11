# ML-Book prose principles

Rule database for *Machine Learning for Econometricians*. Tags are stable; cite them in every edit (`[B-S1]`, `[B-N2]`, ...). The same tags are used by `mlbook-student-lens`.

Throughout, "the reader's information set at position $p$" means: the `CLAUDE.md` prerequisites + chapters strictly before this one in `_quarto.yml` render order + everything earlier in this chapter. Overviews and Roadmaps have the smaller set: earlier chapters only.

---

## S — Sequencing and self-containedness

**B-S1 — Define before use.** No term, acronym, symbol, or coined label appears before its definition unless it is in the reader's information set. This holds *within* callouts and figure captions too — a callout placed early in the chapter may not name objects defined later (an "Evaluation Workflow" box that says "LogS and CRPS address the first task, PIT histograms the second" before any of the three is defined must move below the definitions, or gloss each name inline).

**B-S2 — Forward references are signposts, never load-bearing.** "We return to nested cross-validation in @sec-x" is fine if the current sentence stands on its own. Using a later concept's *properties* in an argument is not. Test: delete the forward-referenced clause — if the surrounding argument breaks, the material is out of order.

**B-S3 — Examples respect chapter order.** An illustrative example may not require machinery from a later chapter. "Hyperparameters such as the learning rate" in Chapter 2 fails when neural networks arrive in Chapter 5; "such as the polynomial degree, the ridge penalty, or the number of folds" draws on what the reader has. When only a later-chapter example is natural, name it with an explicit pointer and a gloss ("the learning rate, a step-size constant we introduce with neural networks in [Chapter 5](feed_forward_nns.qmd)") — and only if nothing earlier serves.

**B-S4 — Overview and Roadmap speak plain language.** These sections are read before the chapter; their information set is previous chapters only. A chapter-internal coined label may appear there only with an inline gloss: "the **honest workflow** — the discipline of separating data used for fitting, tuning, and final evaluation —". Test each Roadmap item: would it carry meaning for a student who just finished the previous chapter? "Explain how leakage inside folds invalidates the estimate" fails (which estimate? what is leakage?); "explain why information slipping from the held-out data into the training step makes the estimated performance too optimistic" passes.

**B-S5 — Definitions appear where the object first matters, not where drafting happened to place them.** If a term's first substantive use and its definition have drifted apart (common after chapter reorganizations), move the definition to the first use — do not patch with a forward reference.

---

## T — Terminology and abbreviations

**B-T1 — Every chapter is self-contained: expand every abbreviation at chapter-first use.** "ordinary least squares (OLS)", "the logarithmic score (LogS)", "the continuous ranked probability score (CRPS)", "the Kullback–Leibler (KL) divergence". No whitelist: this applies to prerequisite-level abbreviations (OLS, MLE, MSE, CDF) exactly as to ML-specific ones, and it applies even when an earlier chapter already expanded the term — chapters are read weeks apart and must stand alone.

**B-T2 — Expand exactly once per chapter.** After the chapter-first expansion, use the short form. A second parenthetical expansion — "the Mean Absolute Error (MAE)" reappearing mid-chapter — signals lost bookkeeping and makes the student wonder whether a new object was introduced. Self-containedness is *per chapter*: the count restarts at each chapter, never within one. One exemption: **section headings** may carry the parenthetical ("## The Logarithmic Score (LogS)") without counting toward the limit — headings are navigational anchors read from the table of contents.

**B-T3 — One primary term per object.** Pick one name at the definition site, list synonyms there once ("**distribution forecast** (also called a density forecast or predictive distribution)"), then use only the primary term. Do not drift between synonyms across sections.

**B-T4 — Bold marks the definition site only.** Bold face signals "this is being defined here". Do not bold later uses, and do not bold a term whose definition is elsewhere.

**B-T5 — One meaning per symbol per chapter.** Keep a symbol ledger. $F$ as a predictive CDF and $\mathcal{F}_t$ as an information set may coexist because they are visually distinct and both defined; reusing plain $F$ for both is a defect. If an earlier chapter fixed a symbol's meaning, do not silently repurpose it (see B-X2).

---

## A — Antecedents and pronouns

**B-A1 — No bare pronoun after a break.** A sentence or bullet that follows a figure, code block, display equation, table, or callout may not begin with "It", "This", "These", "They". The visual break severs the antecedent; restate the noun ("The CRPS generalizes ...", not "It generalizes ...").

**B-A2 — "This" takes a noun.** "This shrinks the estimate" → "This contamination shrinks the estimate". Applies everywhere, not only after breaks.

**B-A3 — List items name their subject.** Under a run-in label like "**Intuition**:" or "**Properties**:", either the label line names the object ("**Properties of the LogS**:") or each bullet is a full sentence with an explicit subject. A bullet list where every item silently refers to something two paragraphs up fails.

---

## N — Notation and timing

**B-N1 — Forecast objects carry origin and target.** Default convention: $\hat y_{t+1\mid t}$, $F_{t+1\mid t}$ — issued at $t$, targeting $t+1$. Single-subscript shorthand ($F_t$) is allowed only if the sentence introducing it states the convention explicitly ("we write $F_t$ for the predictive CDF constructed at origin $t$ for the outcome $y_{t+1}$") and the convention is held fixed for the entire chapter. Never let the reader infer the timing from context.

**B-N2 — Derived sequences run on the target clock.** PITs, scores, and forecast errors are indexed by the date of the outcome they involve: $u_{t+1} = F_{t+1\mid t}(y_{t+1})$, $e_{t+1} = y_{t+1} - \hat y_{t+1\mid t}$. Mixing clocks in one identity — $u_t = F_t(y_{t+1})$ — leaves the reader unsure which index the sequence runs on and breaks statements like "the $u_t$ are i.i.d. Uniform".

**B-N3 — State the information set when a forecast is defined.** What is in $\mathcal{F}_t$, when predictors are observed (publication lags, revisions), and when the outcome realizes. Real-data applications say which vintage is used and flag the real-time caveat if final-vintage data stand in for real-time data.

**B-N4 — Math and code share one timing convention.** If the code's indexing differs from the math (e.g. a pandas `shift(-1)` makes row $t$ hold $y_{t+1}$), state the mapping in the surrounding text or a code comment. A reader cross-checking prose against code must not find $y_t$ meaning two different dates.

**B-N5 — Index roles are fixed per chapter.** $t$ for time, $i$ for cross-sectional units, $k$ for folds, and so on, declared implicitly by first use and never reassigned within the chapter.

---

## P — Precision

**B-P1 — Evaluative claims name their criterion.** "More robust", "unstable", "better calibrated", "often preferable" must say: under which loss/score, against which alternative, under which conditions. If the honest answer is a citation, give the citation at the claim site.

**B-P2 — Conditions are explicit.** If a statement holds only under an extra condition (finite first moment, continuity, correct specification, one-step-ahead horizon), state the condition in the same sentence or the immediately adjacent one. (Mirrors `CLAUDE.md` writing conventions.)

**B-P3 — Intuition is flagged as intuition.** "Heuristically, ...", "As a first intuition, ..." — and the exact statement appears nearby or is pointed to.

**B-P4 — No unresolved vagueness.** "Often", "in practice", "can be unstable", "tends to" need a reason, an example, or a citation within the sentence or the next one. If none exists, the claim is decoration — cut it.

---

## Q — Questions, hints, and solutions

**B-Q1 — The stated conditions determine the intended answer.** Every reflection question and exercise part must specify enough of the data-generating process, conditioning information, comparison object, and maintained assumptions for the intended answer to be defensible. Do not let the solution quietly add a condition absent from the prompt. For example, skewness alone does not determine a PIT shape unless location and dispersion behavior are also fixed.

**B-Q2 — Prompt, hint, and answer form one coupled unit.** Read each question forward into its hint and suggested answer or solution, then backward from the answer to the prompt. The answer must address exactly what was asked, the hint must use the same assumptions and notation, and neither may contradict the preceding chapter text. When one element changes, inspect and update the entire unit, including part numbering and exam-level annotations.

**B-Q3 — Comparison questions separate target, criterion, optimizer, and attained value.** State which object a loss or score evaluates, which feature determines its optimizer, and which other features still affect the attained expected loss. Tail sensitivity is not the same as targeting a tail event; under MSE the conditional mean determines the optimal point forecast, but conditional variance still affects the minimum expected MSE.

**B-Q4 — One subpart contains one coherent task cluster.** A calculation followed by its immediate interpretation may stay together. Split a subpart that also asks for a numerical specialization, a new economic explanation, and an application to another section, especially when the combined work exceeds the `CLAUDE.md` target of 5–10 minutes per subpart.

---

## C — Citations

**B-C1 — Cite at the claim site.** Every result imported from the literature carries its citation where the claim is made, not only in a "further reading" list at the chapter end.

**B-C2 — Coverage check for summarized literature.** Comparison tables and property lists compress literature results; each non-obvious row or claim needs a source. Specifically check the author's own papers when the chapter touches their fields (density-forecast evaluation, scoring rules, volatility, GARCH-MIDAS, high-frequency data): a table row on measurement-error sensitivity of scoring rules is @Kleen2024 and must cite it. Check `references-local.bib`, `../Literature/`, and onnokleen.com.

**B-C3 — Bibliography mechanics.** New entries go in `references-local.bib` (repo must be self-contained; never `library.bib`), keys in `AuthorYear` form, style `apalike`. Prefer archival sources — journal articles, books, handbook chapters, established working-paper series. Lecture notes or slides enter the bibliography only in a form the author supplies or approves (e.g. `hinton2012rmsprop` for RMSprop, citing Hinton's own slides with a URL — not a secondhand course attribution); do not invent such entries on your own, and never use a bare "(Author, year)" parenthetical that mimics a citation without a bib entry behind it.

---

## R — Register: the lecture-script voice

**B-R1 — Prose teaches; bullets enumerate.** Conceptual development — why a score behaves as it does, what a diagnostic reveals, how two estimators differ — belongs in connected paragraphs. Bullets are for genuine enumerations: lists of applications, algorithm steps, properties already argued in prose. A cascade of headed bullet blocks ("**Definition**: ... **Properties**: ... **Intuition**: ...") is slide style, not script style; rewrite as paragraphs with bold run-in labels only where `CLAUDE.md` structure calls for them.

**B-R2 — "We", present tense, no marketing.** First-person plural, present tense ("we now derive"), direct address to the student sparingly. No emotional adjectives about the material ("striking", "powerful", "elegant") — show the property instead.

**B-R3 — Figures are wrapped in prose.** Introduce every figure before it appears (what to look for) and interpret it after (what it showed); captions describe, main text interprets. (Mirrors `CLAUDE.md`; enforce at the sentence level.)

**B-R4 — Sections open with a connection, not a definition dump.** The first sentence of a section says why the section follows from what came before, then the machinery starts.

**B-R5 — Running examples justify themselves.** When a chapter builds on a running example or worked model class, motivate the choice at its introduction: say what the reader already knows about it (its econometric anchor — "fitting a degree-$d$ polynomial is just OLS on the regressors $x, x^2, \dots, x^d$") and why it is the right laboratory for the chapter's concepts (typically: the simplest setting the audience fully commands in which the phenomenon arises in full, with a visible flexibility dial). An unmotivated example reads as arbitrary to a reader with no ML background; an anchored one lets the new concept carry all the novelty. One or two sentences suffice, and the same standard applies wherever a model class is drafted in as a vehicle (ridge as the penalization example, logistic regression for classification losses, stumps for boosting).

---

## X — Cross-chapter linking

**B-X1 — Remind and link; do not re-teach.** When an earlier chapter's concept is needed, give a one-line reminder plus a markdown link: "Recall the forecast-origin information set $\mathcal{F}_t$ from the [Cross Validation chapter](cross_validation.qmd#sec-cv-time-series)." Never a page of re-derivation, and never a bare name with no reminder. Cross-file references use markdown links only — a cross-file `@sec-` renders as literal `?@sec-...`.

**B-X2 — Notation is consistent across chapters.** Do not redefine an earlier chapter's fixed symbol to mean something else; if a clash is unavoidable, say so explicitly at the definition site.

---

## Worked regressions (before → after)

Real examples from the book's own revision history; use them as calibration.

1. **[B-T1, B-S4] Roadmap acronyms.**
   Before: "We study the two most important univariate scoring rules in practice: **LogS** and **CRPS**."
   After: "We study the two most important univariate scoring rules in practice: the **logarithmic score (LogS)** and the **continuous ranked probability score (CRPS)**."

2. **[B-A1, B-T2] Dangling pronoun + duplicate expansion.**
   Before (bullet, after a figure): "It generalizes the Mean Absolute Error (MAE) to probabilistic forecasts."
   After: "The CRPS generalizes the MAE to probabilistic forecasts." (MAE was expanded earlier in the chapter.)

3. **[B-N1, B-N2] Mixed clocks in the PIT.**
   Before: "the PIT sequence $u_t = F_t(y_{t+1})$ should be i.i.d. Uniform(0,1)"
   After: "writing $F_{t+1\mid t}$ for the predictive CDF issued at origin $t$ for the outcome $y_{t+1}$, the PIT sequence $u_{t+1} = F_{t+1\mid t}(y_{t+1})$ should be i.i.d. Uniform(0,1)"

4. **[B-S3] Forward-dependent example.**
   Before (Chapter 2): "hyperparameters such as learning rate or regularization strength"
   After: "hyperparameters such as the polynomial degree in a series regression or the strength of a regularization penalty"

5. **[B-S4] Jargon in the Roadmap.**
   Before: "We introduce the **honest workflow** ... and explain how leakage inside folds invalidates the estimate."
   After: "We introduce the **honest workflow** — keeping the data used for fitting, tuning, and final evaluation separate — ... and explain why information slipping from held-out observations into the training step makes the estimated performance too optimistic."

6. **[B-C2] Uncited own result.**
   Before (table row): "**Measurement Error Sensitivity** | High | Low"
   After: same row plus a sentence at the table: "The measurement-error row summarizes @Kleen2024, who shows that LogS rankings are substantially more sensitive than CRPS rankings when the evaluation target is observed with error."
