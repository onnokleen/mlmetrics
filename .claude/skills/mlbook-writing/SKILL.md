---
name: mlbook-writing
description: Draft or revise prose for the "Machine Learning for Econometricians" Quarto textbook (Book_ML_Econometrics). Trigger when writing or reworking chapter text — overviews, roadmaps, definitions, transitions, callouts, figure discussions — or when the user types /mlbook-writing. Skip for whole-chapter audits (use mlbook-student-lens), for research-paper prose (econometrics-writing / finance-writing), and for code-only or build-only changes.
---

# ML-Book Writing

Prose discipline for the textbook *Machine Learning for Econometricians*. The book is a **lecture script**: a graduate student should be able to read a chapter linearly, weeks after the previous one, and never stumble over a term, symbol, or claim that assumes something they have not yet been given. Two modes: **refine** (surgical edits with rationale) and **draft** (new prose in the book's register).

Relationship to the project `CLAUDE.md`: `CLAUDE.md` governs *structure* (chapter skeleton, heading depth, callout types, figure policy, exercise design). This skill governs the *prose layer* — sequencing, terminology, notation timing, antecedents, register, citations. Where they overlap, `CLAUDE.md` wins.

## The core discipline: the reader's information set

The book teaches that a forecast is honest only if it is measurable with respect to the forecast-origin information set. Apply the same standard to the prose. The reader at position $p$ of chapter $N$ knows exactly:

1. **The prerequisites** listed in `CLAUDE.md`: probability theory, mathematical statistics, MLE, OLS/WLS/GLS, HAC standard errors, GARCH, AR/ARMA, basic panel methods. **No ML concepts** — not cross-validation, not regularization, not neural networks, not trees.
2. **Chapters strictly before $N$** in the render order (`grep href _quarto.yml` gives the order; the YAML `number-offset` gives the chapter number).
3. **Everything earlier in chapter $N$** — and nothing later in it.

Every term, abbreviation, symbol, and coined label used at $p$ must be resolvable from this set. Using a term before its definition is **term leakage**, and it is the book's most damaging regression class: the LLM-assisted revisions know the whole book at once and silently assume the reader does too.

**Before writing or revising, build the ledger.** For a revision inside chapter $N$: skim the chapter from the top down to the edit site and list what has been defined so far (terms, acronyms, symbols, coined labels). For new sections: also check which chapters precede $N$. Write against the ledger, not against your own knowledge of the material.

## How to operate

**Step 1 — Identify mode.** Existing prose to improve → `refine`. Bullet points, a sketch, or "add a section on X" → `draft`. If ambiguous, ask once.

**Step 2 — Locate the text in the book.** Which chapter number, which section, what precedes it. Establish the reader's information set (above). For Overview/Roadmap edits, remember these are read *before* the chapter — their information set is chapters $1..N-1$ only.

**Step 3 — Load `principles.md`.** The rule database, tagged `[B-*]`. Scan to the relevant sections; do not work from memory.

**Step 4 — Apply the mode protocol.**

## Refine mode

Surgical edits, not rewriting. Preserve the author's voice — the target register is the measured lecture-script tone of the pre-existing text, not generic textbook prose.

1. Read the passage against the ledger and `principles.md`.
2. For each issue, cite the specific rule (e.g. `[B-S4] roadmap uses chapter-internal label without gloss`).
3. Output a per-edit list: verbatim before / verbatim after / rule / severity. No silent rewrites.
4. Then one clean revised block with the edits applied.
5. Judgement calls go in as `[taste]` — let the author decide.

## Draft mode

Prose the author could commit after light editing.

1. Confirm the inputs: what is the section supposed to teach, what figure/code does it wrap, where does it sit in the chapter? Ask once if something load-bearing is missing.
2. Build the ledger first; expand every abbreviation at first use; gloss any coined label that first appears in an Overview or Roadmap.
3. Self-check against `principles.md` before delivering — in particular: any term used before defined? any acronym expanded twice? any sentence- or bullet-initial bare pronoun? any forecast object without explicit origin-and-target timing? any imported result without a citation at the claim site?
4. Deliver the prose, then a short rule-trace note.

## Output format

Mirrors `econometrics-writing`. Stable IDs so the user can reply "apply E1, E3; skip E2".

```
## Summary
Edits: <N> (Essential: <k1>, Style: <k2>, Taste: <k3>)
Rules invoked: <[B-S1]: 3, [B-A1]: 2, ...>

## Edits

### E1 — [B-T2] second expansion of MAE
- **Before:** "It generalizes the Mean Absolute Error (MAE) to probabilistic forecasts."
- **After:** "The CRPS generalizes the MAE to probabilistic forecasts."
- **Severity:** Essential
- **Why:** MAE was expanded at its chapter-first use in §3.3; re-expanding signals a new object. Bare "It" after a figure violates [B-A1].

## Revised block
<one clean copy-pasteable block>
```

- **Verbatim before/after** — suitable for find-and-replace on the `.qmd` source.
- **One issue per item**; compound problems split.
- **Severity values:** `essential` (a student stumbles or is misled), `style` (rule-driven improvement), `taste` (author's call), `blocked` (needs input; name what).
- Draft mode: prose first, rule trace after, choices flagged with IDs.

## Files in this skill

- `principles.md` — the tagged rule database (sequencing, terminology, antecedents, notation/timing, precision, citations, register, cross-chapter linking), plus worked before/after regressions taken from the book itself.

## Calibration notes

- **The regression watchlist.** These are the documented failure modes that crept in relative to the previous year's script (hosted at onnokleen.com/ml/): acronyms used before definition (LogS, CRPS, KL in a roadmap); chapter-internal jargon in roadmaps ("honest workflow", "invalidates the estimate"); dangling "It" after figures; duplicate acronym expansions; examples relying on later chapters (learning rate in the CV chapter, three chapters before neural nets); timing-ambiguous forecast notation ($u_t = F_t(y_{t+1})$); literature results imported without a citation at the claim site. Check every edit against this list.
- **Author's own work.** When a chapter touches density-forecast evaluation, scoring rules, volatility, GARCH-MIDAS, or high-frequency data, check `references-local.bib` and onnokleen.com for the author's own relevant papers (e.g. `Kleen2024` on scaling and measurement-error sensitivity of scoring rules) — an uncited own result the chapter uses is an `essential` citation gap.
- **Bibliography policy.** New entries go in `references-local.bib` (the repo must be self-contained), style `apalike`, cite as `@AuthorYear`.
- **Exercises.** Exercise design and difficulty are fully specified in `CLAUDE.md`; this skill only polishes exercise *prose* (sequencing, notation, antecedents) and defers everything else.
