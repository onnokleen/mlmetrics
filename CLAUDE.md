# CLAUDE.md — Machine Learning for Econometricians

## Project overview

Open-source Quarto textbook: **Machine Learning for Econometricians**. Rendered as a website (`quarto render`), deployed via Github pages. Licensed CC BY-NC-SA 4.0.

**Author**: Onno Kleen, Assistant Professor, Erasmus University Rotterdam

---

## Target audience

Graduate students in econometrics (MSc Econometrics & Management Science level). Assume:

- **Strong foundations**: probability theory, mathematical statistics, MLE, OLS/WLS/GLS, HAC standard errors, GARCH, AR/ARMA processes, basic panel data methods
- **No ML assumed**: never assume prior exposure to neural networks, tree-based methods, or ML-specific concepts like cross-validation or regularization
- **Frame ML via econometrics**: when introducing ML concepts, connect them to econometric analogues the students already know (e.g., "gradient boosting builds on the idea of iterative residual fitting, similar to how you'd think about sequential OLS on residuals")

---

## Content philosophy

1. **Econometric data, always.** Examples and applications use financial time series, macroeconomic forecasting, panel data, cross-sectional economic data. Never cats-and-dogs image classification or similar.
2. **Non-iid is the norm.** Time series dependence, heteroskedasticity, and structural breaks are recurring themes throughout. Standard iid assumptions should be questioned explicitly when they appear.
3. **Theory + implementation balance.** Each chapter has mathematical foundations and Python implementations, but theory should be self-contained enough to understand without running code.
4. **Notation and rigor.** Use precise mathematical notation. Define terms before using them. Proofs and derivations should be step-by-step.

---

## Exercise requirements

Exercises must be suitable for a **3-hour handwritten exam**:

- **Pen-and-paper gradeable**: every exercise must be answerable with pen and paper. No "run this code and report" questions.
- **Concrete, well-scoped sub-parts**: break exercises into numbered parts (Part 1, Part 2, ...) with clear, bounded scope. Each part should be independently gradeable.
- **Flexible number of sub-parts**: use as many sub-parts as the exercise actually needs. Do not default mechanically to four parts; many good exercises will naturally have 2 or 3 parts, while 4 parts should be used only when the structure genuinely adds value.
- **No open-ended questions**: avoid "discuss the implications" or "what do you think about" style questions. Each part should have a definitive correct answer or derivation.
- **Gradual difficulty**: hints guide students through harder exercises; a strong student should be able to solve without hints, but hints make the exercise accessible to all.
- **Hints should be selective, not mechanical**: do not force one hint per sub-part. Add a hint only when it gives meaningful scaffolding, such as a useful intermediate step, a setup idea, or a warning about a common mistake. If a part is already direct and a hint would merely restate the question, omit the hint.
- **Difficulty annotation**: include an italic comment about exam suitability, e.g., `*Could be part of an exam if broken into sub-exercises with hints.*`

## Difficulty calibration

Exercises should be calibrated for **MSc econometrics students with strong statistics/econometrics training**. The goal is not merely to check whether students recognize notation, but whether they can work through a statistically meaningful argument under exam conditions.

- **Target time per sub-part**: as a default, each numbered sub-part should take roughly **5-10 minutes** for a well-prepared student. If a sub-part can be answered in 30-60 seconds by copying a formula from the notes, it is too short unless it is only scaffolding for a harder follow-up part.
- **Statistical substance**: each exercise should contain reasonably difficult statistical content. Prefer derivations, comparisons of estimators or loss functions, conditional-vs-unconditional reasoning, misspecification analysis, dependence/non-iid issues, identification, or interpretation of formal results.
- **Not just interpretation**: interpretation questions are useful, but they should usually come **after** a nontrivial derivation or formal step. Do not let an exercise consist mainly of short conceptual prompts with no mathematical work.
- **Not just notation drills**: avoid exercises that only ask students to restate a definition, copy a likelihood, verify a trivial positivity/probability constraint, or substitute symbols into a formula already given in the text. Such tasks are acceptable only as a first part that prepares a deeper second or third part.
- **Econometric framing**: whenever possible, at least one sub-part should connect the ML object to an econometric issue such as forecast evaluation, dependent data, heteroskedasticity, information sets, leakage, misspecification, or identification.
- **Bounded but nontrivial**: the exercise should still be solvable with pen and paper in exam conditions. Avoid long proofs, excessive algebra with little insight, or questions that require ideas not developed in the notes.

## Default exercise mix

Unless the chapter genuinely does not support it, aim for exercises with this profile:

- **one derivation-oriented part** that requires real algebra or likelihood/scoring-rule manipulation
- **one comparison or implication part** that asks what changes across objectives, models, or assumptions
- **one econometric-diagnostic part** that surfaces a pitfall involving dependence, uncertainty, identification, or misspecification

## Final exercise self-check

Before keeping an exercise, check:

- Would a strong student need around **5-10 minutes** for each sub-part?
- Does at least one sub-part require a nontrivial statistical derivation or argument?
- Does the exercise go beyond formula recall?
- Would the solution reveal whether the student actually understands the chapter?

## Exercise format

```markdown
:::{.callout-note}
## Exercise X.Y: Descriptive Title
[Exercise statement with numbered parts]

*Exam-level annotation in italics.*
:::

:::{.callout-warning collapse="true"}
## Hint for Part 1
[Progressive hint]
:::

:::{.callout-warning collapse="true"}
## Hint for Part 2
[Progressive hint]
:::

:::{.callout-tip collapse="true"}
## Solution
**Part 1: [Title]**
[Full derivation/solution]

**Part 2: [Title]**
[Full derivation/solution]
:::
```

Hints do not need to appear for every numbered part. Use only the hint boxes that materially help.

---

## Writing conventions

Write with a naive but attentive student in mind:

- Assume the reader will notice and stumble over any imprecise wording, skipped condition, overloaded notation, or hidden assumption.
- If a statement is true only under an additional condition, state that condition explicitly rather than leaving it implicit.
- If a theorem or algorithm uses a convention, such as a sample split, a tie-breaking rule, positivity of a scale parameter, or a training-only estimation step, spell it out.
- Avoid phrases that are heuristically suggestive but mathematically ambiguous when a more precise formulation is available.
- When simplifying for intuition, signal clearly that you are giving intuition rather than the exact formal statement.
- Prefer one extra clarifying sentence over a formulation that a literal-minded student could misread.

## Chapter structure

Each pedagogical chapter follows this skeleton:

1. **YAML frontmatter**: `number-sections: true`, `number-offset: [N, 0]` (where N = chapter number - 1)
2. **`# Chapter Title`** (top-level heading)
3. **`## Overview`** — what the chapter covers and why it matters for econometricians
4. **`## Roadmap`** — numbered list previewing the section flow
5. **Core content sections** (`##` only). Do not use `###` or deeper headings in chapter files; use bold run-in labels, lists, or callouts for local structure inside a section.
6. **`## Summary`** — contains a Key Takeaways callout (`callout-important`) and, when useful, a Common Pitfalls callout (`callout-warning`). Both live under this single heading.
7. **`## Exercises`** — pen-and-paper exercises with hints and solutions

**Reference appendix exception.** `datasets.qmd` is a reference appendix, not a teaching chapter. It documents the file-backed datasets shipped with the repo so other chapters can link to it instead of re-describing each source. It is exempt from the Overview/Roadmap/Summary/Exercises skeleton, the visual-pedagogy rule, and the self-reflection prompts. Keep it short and factual: source and citation, file path, unit of observation, frequency, any file-layout quirks, a table of the variables actually used, and one canonical loading snippet. Any future reference-style appendix should follow the same pattern.

Additional section-depth rule:

- Chapters should have only one numbered section depth below the chapter title. In practice this means: after `# Chapter Title`, use `##` headings for numbered sections and avoid `###` / `####`.
- Do not create a `##` section for only one short paragraph. If a local topic is that small, fold it into the surrounding section using a bold run-in label, a list item, or a callout title.
- Use callout titles for exercise hints and solutions, but do not use nested section headings merely for visual spacing.

Visual pedagogy rule:

- Chapters should contain enough figures or diagrams to help readers conceptualize the central ideas rather than only reading definitions and formulas.
- As a default, include multiple visuals across the chapter when the concepts are structural, geometric, sequential, or otherwise easier to understand graphically.
- Prefer simple explanatory figures made in the repo over decorative visuals.
- Every figure should have a clear teaching purpose and should be explicitly discussed in the surrounding main text rather than inserted without interpretation.
- Figure captions should be as self-contained as possible: define what is shown, what the axes, colors, panels, or markers represent, and any special construction needed to read the figure.
- Keep interpretation in the main text. Captions should describe the figure clearly, but the substantive lesson, econometric meaning, and model comparison should be explained in the surrounding prose.

## Summary section

- Each chapter has a single `## Summary` heading that contains one or two callout boxes.
- The **Key Takeaways** callout (`.callout-important` with `## Key Takeaways` title) always appears first, with a numbered list. It is styled green via `styles.css`.
- An optional **Common Pitfalls** callout (`.callout-warning` with `## Common Pitfalls` title) follows when there are predictable misunderstandings, implementation mistakes, or exam traps. Include it when useful, omit when it would be artificial.

## Self-reflection questions

- Use short self-reflection prompts throughout chapters when they help students pause on an econometric interpretation, modeling tradeoff, or conceptual pitfall.
- These prompts may be more reflective than final exam exercises, but they should still have a clear teaching point and should not be vague opinion questions.
- Format each prompt as `:::{.callout-note title="Question for Reflection"}` followed immediately by a collapsed answer using `:::{.callout-tip collapse="true" title="Suggested Answer"}`.
- Keep suggested answers concise. They should explain the intended reasoning, not become full exercise solutions.
- Suggested answers should be answerable from material already introduced in the book. Do not introduce new scoring rules, risk measures, model classes, or terminology unless the surrounding chapter has already explained them or explicitly points to where they are introduced.
- Avoid prompts whose main answer is a personal preference or "it depends." When asking about a model choice, specify the criterion or diagnostic evidence students should use.

```markdown
:::{.callout-note title="Question for Reflection"}

[Short reflection question tied to the surrounding section.]
:::

:::{.callout-tip collapse="true" title="Suggested Answer"}

[Concise answer explaining the intended reasoning.]
:::
```

## Callout types

| Type | Role | Collapsible? |
|------|------|-------------|
| `callout-note` | Key properties, notation, exercise statements, reflection questions, formal definitions with `title="Definition: ..."` | No |
| `callout-warning` | Exercise hints, cautions, common pitfalls | Usually yes (`collapse="true"`); no for chapter-level `Common Pitfalls` boxes |
| `callout-tip` | Exercise solutions, suggested answers to reflection questions, practical advice, worked examples with `title="Example: ..."` | Yes (`collapse="true"` for solutions and suggested answers; usually no for examples) |
| `callout-important` | Critical econometric interpretations, "why this matters", boxed key takeaways | No |

## Code chunks

- Python is the primary language for code examples
- Display figures should normally keep the generating code foldable: use `#| echo: true`, `#| label: fig-descriptive-name`, and `#| fig-cap: "Caption"` so readers can expand the code if they want to inspect it.
- Use `#| echo: false` for figure chunks only when showing the code is genuinely not feasible or would materially hurt readability.
- Instructional code: `#| echo: true`
- Global settings: `code-fold: true` (readers click "Show the code"), `cache: true`

## Cross-references

- Section anchors: `# Title {#sec-shortname}`
- Reference sections: `@sec-shortname`, figures: `@fig-name`, citations: `@AuthorYear`

## Python stack

Core: `numpy`, `matplotlib`, `scipy`, `sklearn`. Additional as needed: `pandas`, `properscoring`, `seaborn`. Don't add new dependencies without discussion.

---

## Build and deploy

- **Render**: `quarto render` (output to `docs/`)
- **Deploy**: manual SFTP upload
- **Bibliography**: `~/Dropbox (Personal)/library.bib`, style: `apalike`, rendered as hover citations/footnotes

---

## What NOT to do

- Don't change `_quarto.yml` structure or chapter ordering without discussion
- Don't create new chapter files without discussion
- Don't add Python dependencies beyond the core stack without asking
- Don't modify `styles.css` or the Quarto theme
- Don't write exercises that require running code to answer
- Don't use image classification examples (MNIST, CIFAR, cats vs dogs, etc.)
