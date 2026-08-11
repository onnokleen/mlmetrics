# Student-lens audit checklist

Dimensions, detection recipes, and mechanical backstops. Rule tags `[B-*]` are defined in `../mlbook-writing/principles.md`. The linear read with a ledger (SKILL.md Step 3) is the primary instrument; the greps below only backstop it.

---

## 1. Sequencing / self-containedness — [B-S1..B-S5]

**Ledger check (primary).** During the linear read, record every first use of a term/acronym/symbol/coined label and every definition site. Findings:
- first use strictly before definition site, and term not in the information set → `[B-S1]` blocking;
- Overview/Roadmap uses a chapter-internal label without an inline gloss → `[B-S4]` blocking;
- an example requires a later chapter's machinery → `[B-S3]` blocking;
- a forward reference that is load-bearing (delete the clause and the argument breaks) → `[B-S2]`.

**Mechanical backstop — acronym first-use scan.** List acronym occurrences in file order and eyeball whether the first hit for each is its expansion site:

```bash
grep -on '\b[A-Z][A-Za-z]*[A-Z][A-Za-z]*\b' chapter.qmd | sort -t: -k2 -u
```

(Catches LogS, CRPS, MAE, PIT, KL, OOB, GDP, ... — filter out code-chunk hits only.) The scan must cover **math mode** — `\stackrel{\text{iid}}{\sim}`, `\operatorname{MSPE}`, `\widehat{\mathrm{CV}}_K` are first uses too — and **exercise, hint, and solution text**, where acronyms like MSPE or AR(1) often first appear. Coined letter-symbols count as abbreviations: $\widehat{\mathrm{CV}}_K$ needs one prose tie to its term ("the cross-validation (CV) estimate"). Every acronym's first occurrence must be its expansion site, and there is **no whitelist** — prerequisite-level abbreviations (OLS, MLE, MSE, i.i.d.) need a chapter-first expansion like everything else.

**Roadmap scan.** Read Overview + Roadmap in isolation, pretending the rest of the chapter does not exist. Any bolded or technical term not covered by prerequisites or earlier chapters must carry an inline gloss.

**Back-reference verification.** Every sentence that leans on another chapter's content — "as discussed in the previous chapter", "recall from", "the same data used in the X chapters" — must be checked against that chapter's actual text:

```bash
grep -n 'previous chapter\|as discussed\|[Rr]ecall from\|earlier chapter\|same .* chapter' chapter.qmd
```

For each hit, grep the referenced file for the claimed content. A back-reference to material that is not actually there is `[B-X1]` blocking — the attentive student flips back and finds nothing. Never trust the sentence; a ledger-only pass misses these because the claim sounds plausible.

## 2. Terminology hygiene — [B-T1..B-T5]

- Acronym expanded **zero** times in the chapter (even if an earlier chapter expanded it) → `[B-T1]` blocking. Chapters are self-contained: prerequisite-level abbreviations (OLS, MLE, MSE, CDF, ...) need a chapter-first expansion too.
- Acronym expanded **twice or more** → `[B-T2]` friction. Grep backstop: `grep -c '(MAE)' chapter.qmd` style counts for each acronym found in the scan above, or search for the spelled-out form recurring.
- Synonym drift ("distribution forecast" / "density forecast" / "predictive distribution" alternating outside the definition site) → `[B-T3]` friction.
- Bold on a non-definition use → `[B-T4]` polish.
- Symbol reused with a second meaning within the chapter → `[B-T5]` blocking.

## 3. Antecedents — [B-A1..B-A3]

**Mechanical backstop:**

```bash
grep -n '^\s*[-*]\s*\(It\|This\|These\|They\)\b' chapter.qmd
grep -n '^\(It\|This\|These\|They\)\s' chapter.qmd
```

Then check each hit's context: does a figure, code chunk, display equation, table, or callout sit between the pronoun and its antecedent? → `[B-A1]` blocking. Bare "this/these" without a noun anywhere → `[B-A2]` friction. Bullet lists whose items have no explicit subject and whose run-in label does not name the object → `[B-A3]` friction.

## 4. Notation & timing — [B-N1..B-N5]

For every forecasting object in the chapter ($\hat y$, $F$, $u$, scores, errors):
- Is the issuance time and target time explicit — either two-index notation ($F_{t+1\mid t}$) or a stated single-subscript convention held fixed all chapter? Missing/ambiguous → `[B-N1]` blocking.
- Do derived sequences run on the target clock ($u_{t+1} = F_{t+1\mid t}(y_{t+1})$, not $u_t = F_t(y_{t+1})$)? Mixed clocks in one identity → `[B-N2]` blocking.
- Is the information set stated when the forecast is defined (contents, publication lags, vintage)? → `[B-N3]`.
- Does the code index time the same way as the math? Check pandas `shift` calls against the prose; unstated mapping → `[B-N4]` friction.
- Any index letter with two roles → `[B-N5]`.

## 5. Precision — [B-P1..B-P4]

- Evaluative claims ("more robust", "unstable", "often better") without criterion, conditions, or citation in the same or adjacent sentence → `[B-P1]`/`[B-P4]` friction (blocking if the claim drives a recommendation).
- Statements true only under an unstated condition → `[B-P2]` blocking.
- Intuition presented as exact statement → `[B-P3]` friction.

In scope for this dimension: claims that contradict the chapter's *own* definitions (e.g. calling train–validation dependence "leakage" after defining leakage as an information-set violation); stated results missing a needed condition (a strict inequality without a nondegeneracy assumption — check exercise statements too); statistical quantities presented as something they are not (fold-score dispersion as an "uncertainty estimate"). Out of scope: verifying novel derivations — route to `econometrics-methods`.

## 6. Citations — [B-C1..B-C3]

- Result imported from the literature with no citation at the claim site → `[B-C1]` blocking if presented as established fact.
- Comparison tables / property lists: each non-obvious row needs a source. Cross-check the author's own papers for their fields (density-forecast evaluation, scoring rules, volatility, GARCH-MIDAS, high-frequency): `grep -i kleen references-local.bib` and onnokleen.com. Chapter uses an own-paper result without citing it → `[B-C2]` blocking.
- New citations must resolve: every `@Key` in the chapter exists in `references-local.bib`:

```bash
grep -o '@[A-Za-z][A-Za-z0-9]*' chapter.qmd | sort -u   # compare against bib keys
```

## 7. Register — [B-R1..B-R4]

- Conceptual development delivered as headed bullet cascades ("**Definition**: ... **Properties**: ... **Intuition**: ...") instead of connected paragraphs → `[B-R1]` friction; note the sections, do not rewrite here.
- Marketing adjectives, past tense, "you will learn" framing → `[B-R2]` polish.
- Figure appears without an introducing sentence before it or interpretation after → `[B-R3]` friction.
- Section opens with a definition dump, no connective first sentence → `[B-R4]` polish.
- A running example or worked model class introduced without motivation — no statement of what the reader already knows about it (its econometric anchor) or why it is the right laboratory for the chapter's concepts → `[B-R5]` friction.

## 8. Structure conformance (CLAUDE.md)

Check against the project `CLAUDE.md` directly (do not restate it here): chapter skeleton (Overview, Roadmap, `##`-only sections, Summary with Key Takeaways, Exercises), no `###` or deeper, no one-paragraph `##` sections, callout-type table respected, figure chunks labeled `fig-*` with captions, self-reflection prompt format, `number-offset` consistent with the chapter's position in `_quarto.yml`.

Check captions in **both directions**: a generic caption ("Illustration of Time Series Cross-Validation Methods.") violates the self-containment rule — panels, axes, colors, markers, and construction must be defined; a caption that carries the substantive interpretation violates the interpretation-in-main-text rule. Both are findings.

**Cross-file reference check** (this is a Quarto *website*: cross-file `@sec-` breaks silently):

```bash
grep -n '@sec-' chapter.qmd            # each hit must resolve within the same file
grep -o '?@sec-[a-z0-9-]*' docs/*.html # after a render: must return nothing
```

## 9. Exercises (CLAUDE.md self-check)

Run the `CLAUDE.md` "Final exercise self-check" per exercise: 5–10 minutes per sub-part; at least one nontrivial derivation; beyond formula recall; solution reveals understanding; pen-and-paper answerable; hints selective; exam-level annotation present; format block correct.

Two sub-rules are the most-missed — check them by name: (i) **hint selectivity**: count hints against sub-parts; one hint per part across the board is mechanical, and any hint that restates the question or hands over the asked-for operation gets cut; (ii) **conditions in exercise claims**: a stated result carries the assumptions it needs (a strict inequality needs a nondegeneracy condition even when the solution quietly adds it). Report failures as findings tagged `[ad-hoc]` with a pointer to the specific CLAUDE.md requirement. Do not redesign exercises inside the lens.

### Question–answer round trip — [B-Q1..B-Q4]

Inventory every student-facing question, including reflection callouts, exercise parts, hints, suggested answers, and solutions. For each prompt, read forward through its answer and then backward from the answer to the prompt:

- **Determinate answer [B-Q1]:** Does the prompt state the conditions needed for the intended answer, or does the answer add a moment condition, timing convention, null hypothesis, or comparison benchmark that the student was never given?
- **Coupled artifacts [B-Q2]:** Does the hint use the prompt's notation and assumptions? Does the answer address every requested task and no different one? Does either conflict with the preceding chapter text?
- **Comparison precision [B-Q3]:** Does the question distinguish the target from sensitivity to realizations, and the optimizer from the attained criterion value or irreducible uncertainty? Treat false dichotomies such as "only the mean matters" as findings.
- **Subpart load [B-Q4]:** Can a prepared student complete the task cluster in 5–10 minutes? Split calculations, numerical specializations, economic explanations, and cross-section applications when they do not form one immediate chain.

Backstop the inventory mechanically, but inspect the surrounding callout rather than treating each grep hit independently:

```bash
grep -n 'Question for Reflection\|Suggested Answer\|^## Exercise\|^## Hint\|^## Solution\|?' chapter.qmd
```

---

## Cross-chapter checks (multi-chapter passes only)

- Symbol or term defined differently in two chapters without acknowledgment → `[B-X2]` blocking.
- Concept re-taught at length instead of reminded-and-linked → `[B-X1]` friction.
- Markdown cross-links point to existing files/anchors:

```bash
grep -on '](\([a-z_]*\.qmd[^)]*\))' chapter.qmd   # verify targets exist
```

- Same object named differently across chapters (terminology drift at book level) → `[B-T3]` friction, reported in the cross-chapter section.

---

## Severity guardrails

The classes are defined in SKILL.md; these worked calls keep reports comparable across runs:

- Term leakage in an Overview/Roadmap, a false back-reference, a mixed-clock identity, an uncited own-paper result presented as established → **blocking**.
- A bare "This"/"It" whose antecedent is recoverable from the previous sentence → **friction**, never blocking; it reaches blocking only when a figure/display/callout severs the antecedent *and* multiple candidates compete.
- A missing expansion of a prerequisite-level acronym → **friction**.
- A factually wrong side statement (an API claim, an implementation note) → **friction**, unless it misleads the chapter's statistical teaching — then blocking.
- Mechanical hints, generic captions, synonym drift → **friction**; re-bolding, wordy connectives → **polish**.
- Sanity check on the finished report: a distribution like "9 blocking, 0 polish" almost always means inflation; "0 blocking" on a chapter with known regressions almost always means leniency. Recalibrate before reporting.

## Report template

Use the exact structure from SKILL.md ("Output format"): header with information set, verdict-by-dimension block (Pass / Borderline / Fail + one sentence each), findings with stable IDs `F1..Fk` (tag, severity, verbatim quote, location, problem, fix, effort), closing summary with counts and top-three fixes. One report per chapter; cross-chapter section last.
