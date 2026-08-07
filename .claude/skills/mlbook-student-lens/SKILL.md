---
name: mlbook-student-lens
description: Audit a chapter of the "Machine Learning for Econometricians" textbook as a naive-but-attentive MSc student who knows only the earlier chapters. Trigger when the user asks whether a chapter reads well, asks for a pedagogy/consistency check, wants regressions found relative to the previous year's script, or types /mlbook-student-lens. Produces a structured punch list (term leakage, notation timing, antecedents, citations, register, structure conformance) with verbatim quotes and stable IDs. Skip for line-level rewriting (use mlbook-writing) and for checking mathematical correctness of derivations (use econometrics-methods).
---

# ML-Book Student Lens

Inverts the book's target reader into an audit tool. The reviewer is the **naive but attentive student** from `CLAUDE.md`: an MSc econometrics student with strong statistics training and *zero* ML background, who reads the chapter linearly, notices every imprecise word, and has read only the chapters that come before this one — weeks ago.

The output is not a rewrite — it is a punch list of every place this student stumbles, structured so the fixes can be applied afterwards (by hand or via `mlbook-writing`).

## When this skill fires

- "Does this chapter read well / hold up?"
- "Check evaluating_distributions.qmd for regressions"
- "Audit chapter N before I re-render"
- "Compare this chapter against last year's version"
- Explicit `/mlbook-student-lens`

Do **not** use for:
- Applying fixes or polishing prose → `mlbook-writing`
- Verifying that derivations, proofs, or estimator claims are mathematically correct → `econometrics-methods`
- Repo/build issues (render errors, search.json staleness) — those are covered in `CLAUDE.md`

## Inputs

1. The chapter file(s) — one `.qmd`, several, or "the whole book".
2. Optional: a reference version to compare against. The previous academic year's script is hosted at onnokleen.com/ml/ — if the user asks for a regression check, fetch the corresponding page there and flag places where the current text is *less* clear than the old one (new material is not automatically suspect; only degraded pedagogy is).

If the user gives no scope, ask which chapters; a full-book pass is expensive and should be deliberate.

## How to operate

**Step 1 — Fix the reader's information set.** Get the chapter order from `_quarto.yml` (`grep href _quarto.yml`); the chapter number is `number-offset + 1`. The student knows: the `CLAUDE.md` prerequisites (probability, mathematical statistics, MLE, OLS/WLS/GLS, HAC, GARCH, AR/ARMA, basic panel — **no ML concepts whatsoever**), plus chapters strictly before this one, plus nothing. For the Overview and Roadmap, not even the current chapter's later sections exist yet.

**Step 2 — Load `checklist.md`.** It contains the audit dimensions, detection recipes (including mechanical greps), and the output template. Do not audit from memory. The rule tags `[B-*]` are defined in `../mlbook-writing/principles.md`; consult it when a tag's exact scope matters.

**Step 3 — Linear read with a ledger.** Read the chapter top to bottom *once, in order*, maintaining a running ledger of defined terms, expanded abbreviations, coined labels, and symbols with their meanings and timing conventions. Every time the text uses something not yet in the ledger (and not in the information set), that is a finding. Every time the text re-defines something already in the ledger, that is a finding. This single pass catches the largest defect class (term leakage) and cannot be replaced by grepping.

**Step 4 — Run the dimension checks** from `checklist.md`: sequencing/self-containedness, terminology hygiene, antecedents, notation & timing, precision, citations, register, structure conformance (against `CLAUDE.md`), and exercises (against the `CLAUDE.md` exercise self-check). Use the mechanical greps to backstop the linear read, not to replace it.

**Step 5 — Verify each finding before reporting.** For a "used before defined" claim, confirm the term really is absent from the information set (search earlier chapters if in doubt — a term defined in Chapter 1 is fair game in Chapter 3, though it may still need re-expansion per [B-T1]). For a citation-gap claim, confirm the reference is not present elsewhere in the chapter. Drop anything that does not survive.

**Step 6 — Produce the report** in the fixed format below, most severe first within each dimension.

## Severity calibration

- **blocking** — the student cannot parse the sentence, is misled, or must read ahead to understand: term leakage, mixed timing clocks, wrong/ambiguous antecedent, undefined jargon in Overview/Roadmap, uncited imported result presented as established.
- **friction** — the student gets through but pays a cost: duplicate expansions, synonym drift, slide-style bullet cascades, vague evaluative claims, figure not discussed in text.
- **polish** — worth fixing, no real cost: bold on a non-definition use, mildly wordy transitions.

Be fair, not signal-jamming: do not inflate polish items into blocking ones, and credit passages that already do it right. The goal is an honest mirror, and the fix list must be worth its length.

## Output format

Stable IDs so the user can reply "fix F1, F3, F7; skip the rest" — and so the list can be handed to `mlbook-writing` or a fix pass directly.

```
# Student-lens report: <chapter file> (Chapter <N>)
Information set: prerequisites + chapters <1..N-1> (<names>)

## Verdict by dimension
- Sequencing / self-containedness: Pass / Borderline / Fail — <one sentence>
- Terminology: ...
- Antecedents: ...
- Notation & timing: ...
- Precision: ...
- Citations: ...
- Register: ...
- Structure (CLAUDE.md): ...
- Exercises (CLAUDE.md self-check): ...

## Findings (<k>)

### F1 — [B-S1] blocking — LogS used before definition
- **Quote:** "LogS and CRPS address the first task. PIT histograms address the second."
- **Location:** §3.3, "Evaluation Workflow" callout
- **Problem:** All three names are defined only in §3.4–3.8; the student meets them cold.
- **Fix:** Move the callout below the definitions, or gloss each name inline.
- **Effort:** low

[...]

## Summary
- blocking: <k1>, friction: <k2>, polish: <k3>
- Top three fixes by payoff: F1, F4, F9
- <one-sentence overall assessment>
```

- **Verbatim quotes** with section/heading location — enough for find-and-replace on the `.qmd`.
- **One issue per finding**; recurring patterns (e.g. the same acronym leaked in five places) get one finding with all locations listed.
- **Rule tag mandatory**, from `principles.md`; `[ad-hoc]` only with an explanation.
- **Effort marker** `low` / `medium` / `high` (low = string replacement; medium = a paragraph rewritten or moved; high = section restructuring).
- No prose outside the structured blocks; the Summary closes the report.

For multi-chapter or full-book passes, emit one report per chapter plus a final cross-chapter section (notation clashes across chapters [B-X2], synonym drift between chapters, broken or missing cross-links, `?@sec-` artifacts in `docs/`).

## Files in this skill

- `checklist.md` — audit dimensions, detection recipes, mechanical greps, report template

## Calibration notes

- The known regression pattern: LLM-assisted revisions see the whole book at once and silently assume the reader does too. Term leakage, jargon-laden roadmaps, dangling pronouns after inserted figures, duplicate expansions, and timing-ambiguous notation are the documented classes — weight them highest.
- The author's own papers are part of citation coverage: chapters touching density-forecast evaluation, scoring rules, volatility, GARCH-MIDAS, or high-frequency data must cite the relevant Kleen papers (e.g. @Kleen2024 for measurement-error sensitivity of scoring rules). Check `references-local.bib` and onnokleen.com.
- This lens judges *pedagogy and consistency*, not mathematical truth. If a derivation looks wrong, flag it as `[ad-hoc]` with a pointer to `econometrics-methods`, and do not attempt the verification here.
