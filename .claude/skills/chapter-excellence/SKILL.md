---
name: chapter-excellence
description: Multi-agent comprehensive review of one ML-book chapter (student lens + substance + exercises + proofread, plus TikZ conditionally). Use when user says "chapter excellence", "full chapter review", "review everything in this chapter", "pre-release chapter check", or before rendering/publishing a chapter. Fanout wrapper — for a single lens, use /mlbook-student-lens or /proofread directly.
argument-hint: "[chapter .qmd filename or stem] [--fast] [--out DIR] [--skip-exercises | --skip-substance | --skip-student]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "Task"]
context: fork
---

# Chapter Excellence Review

Run a comprehensive multi-dimensional review of one chapter of *Machine Learning for Econometricians*. Independent agents analyze the chapter in parallel; results reduce to one typed scorecard.

> **Which review do I want?**
>
> - **`/chapter-excellence`** (this skill) — multi-agent fanout: student lens + substance + exercises + proofread (+ TikZ conditionally). Best **pre-release**.
> - **`/mlbook-student-lens`** — single lens: pedagogy/consistency punch list. Also handles multi-chapter and regression-vs-last-year passes, which this skill does not.
> - **`/proofread`** — single lens: grammar/typos/terminology.
> - **`/mlbook-writing`** — applying fixes afterwards, not reviewing.

This orchestrator does **conditional dispatch** — it spawns only lenses that can produce useful output, keyed off the exemption flags the project `CLAUDE.md` defines (reference appendices, `chapter-type: empirical-illustration`, `exercises-required: false`).

**Review-only by design.** No fixer loop: unlike render-parity QA, textbook prose has no compile-or-not oracle, so fixes are applied deliberately afterwards (by hand or via `/mlbook-writing`), never by an unattended loop.

## Step 1: Resolve the Chapter

Project root: the directory containing `_quarto.yml` (this file's `../../..`). Chapters are root-level `.qmd` files.

Parse `$ARGUMENTS` for the target (first non-flag token). Accept a filename (`decision_trees.qmd`) or a stem (`decision_trees`). Resolve against root-level `.qmd` files only — never `_archive/`, `_book/`, `docs/`, `prototypes/`. Zero matches → say so and stop. Multiple → list and ask.

```bash
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
FILE="$ROOT/${ARG%.qmd}.qmd"
STEM="$(basename "$FILE" .qmd)"
REPORT_DIR="${OUT_DIR:-$ROOT/quality_reports}"
mkdir -p "$REPORT_DIR"
```

Work in absolute paths from here on — subagents do not inherit your resolution.

## Step 2: Pre-flight — Detect Conditions

```bash
# Front-matter exemption flags (CLAUDE.md machine-checkable exemptions)
chapter_type=$(sed -n '/^---$/,/^---$/p' "$FILE" | grep '^chapter-type:' | awk '{print $2}')
exercises_required=$(sed -n '/^---$/,/^---$/p' "$FILE" | grep '^exercises-required:' | awk '{print $2}')

# Chapter number = number-offset[0] + 1
offset=$(sed -n '/^---$/,/^---$/p' "$FILE" | grep 'number-offset' | grep -o '[0-9]*' | head -1)

# Structural probes
has_exercises=$(grep -c '^## Exercises' "$FILE")
has_reflection=$(grep -c 'Question for Reflection' "$FILE")

# TikZ figures: chapters compile figures/*.tex via R chunks
tikz_files=$(grep -o 'figures/[A-Za-z0-9_]*\.tex' "$FILE" | sort -u)

# Reference appendix? (CLAUDE.md: datasets.qmd and any future reference-style appendix)
is_reference=false
[ "$STEM" = "datasets" ] && is_reference=true
```

Decide the lens set:

| Lens | Condition |
|---|---|
| A. Student lens | teaching chapters only — skip if `is_reference` (exempt from skeleton, visual pedagogy, self-reflection) |
| B. Substance | always |
| C. Exercises | skip if `is_reference` or `exercises-required: false`; if neither exemption holds and `has_exercises == 0`, do NOT spawn — record an orchestrator CRITICAL finding ("required `## Exercises` section missing") directly |
| D. Proofread | always |
| E. TikZ | only if `tikz_files` non-empty |

Report the detection before spawning:

```
Chapter:      /abs/path/decision_trees.qmd  (Chapter 10)
Type:         teaching | empirical-illustration | reference appendix
Reports →     /abs/path/quality_reports/
Exercises:    required, present (4) | exempt (exercises-required: false) | MISSING → CRITICAL
Reflection:   3 questions
TikZ figures: figures/lstm_cells.tex, ... | none
Lenses:       [A, B, C, D] (skipped: E [no TikZ])
```

**De-duplication:** if a lens skill already ran on this chapter in the current session (e.g. `/mlbook-student-lens` just finished), ask whether to reuse that report or re-run. Default: reuse.

## Step 3: Run Review Agents in Parallel

Spawn all selected agents **in one message**. Every prompt must be self-contained: absolute chapter path, absolute report path, chapter number, and the pointers below — subagents see none of this conversation.

- **Agent A: Student Lens** (`general-purpose` agent)
  Prompt: *"Read `$ROOT/.claude/skills/mlbook-student-lens/SKILL.md` and its `checklist.md`, then execute that skill exactly on the single chapter `$FILE` (Chapter N). Save the report to `$REPORT_DIR/${STEM}_student_lens.md`. After the report's Summary, append the typed findings/scorecard YAML block per `~/.claude/references/orchestration-schemas.md`, mapping severities: blocking → MAJOR (CRITICAL if the student is misled into believing something false), friction → MINOR, polish → report-only (excluded from the scorecard counts). Do not edit any source files."*

- **Agent B: Substance Review** (`domain-reviewer`)
  Prompt: *"Review `$FILE` (Chapter N of the Quarto textbook at `$ROOT`; the reader knows only earlier chapters per `$ROOT/_quarto.yml` order). Rule database: `~/.claude/skills/econometrics-methods/checklist.md`. Project conventions: `$ROOT/CLAUDE.md`. Bibliography: `$ROOT/references-local.bib`; PDF library: `~/Research-ML/Literature/`. Code chunks are Python. Save report to `$REPORT_DIR/${STEM}_substance_review.md` and append the typed findings/scorecard YAML."*

- **Agent C: Exercise Review** (`general-purpose` agent)
  Prompt: *"Read `$ROOT/.claude/agents/exercise-reviewer.md` and execute it exactly on `$FILE` (Chapter N). Rulebook: `$ROOT/CLAUDE.md`. Save report to `$REPORT_DIR/${STEM}_exercise_review.md`."*

- **Agent D: Proofreading** (`proofreader`)
  Prompt: *"Proofread `$FILE` (Quarto textbook chapter, HTML output — ignore Beamer/overflow checks; check grammar, typos, terminology consistency, citation format, academic register). Save report to `$REPORT_DIR/${STEM}_proofread_report.md` and append the typed findings/scorecard YAML per `~/.claude/references/orchestration-schemas.md`."*

- **Agent E: TikZ Review** (`tikz-reviewer`) — conditional
  Prompt: *"Review these TikZ sources used by chapter `$FILE`: [absolute paths from `$tikz_files`]. Measurement-based collision audit. Save report to `$REPORT_DIR/${STEM}_tikz_review.md` and append the typed findings/scorecard YAML."*

`--fast`: instead of the fanout, spawn ONE `general-purpose` agent that reads the chapter plus `$ROOT/CLAUDE.md` and produces a single combined report covering all applicable dimensions at reduced depth. Cheaper (~8k vs ~40–60k tokens), less thorough.

## Step 4: Reduce — Typed Scorecard

Fan-out → reduce per `~/.claude/rules/orchestrator-protocol.md`: stack the YAML scorecards; do not re-review by eye. Dedup findings across lenses on `(location, finding)` — the student lens and exercise lens both look at exercises; the student lens and substance lens both look at citations. Keep the more specific lens's version.

Verdict is the deterministic gate predicate: `sum(CRITICAL) > 0 → BLOCK`, else `sum(MAJOR) > 0 → REVISE`, else `PASS`. A skipped lens contributes no findings, not zeros to average.

```markdown
# Chapter Excellence Review: [STEM].qmd (Chapter N)

**Type:** [teaching / empirical-illustration / reference appendix]
**Lenses run:** [A, B, C, D] (skipped: E [no TikZ])
**Verdict:** [PASS / REVISE / BLOCK]

| Lens | Critical | Major | Minor |
|------|----------|-------|-------|
| Student lens | | | |
| Substance | | | |
| Exercises | | | |
| Proofread | | | |
| TikZ (if ran) | | | |
| **Total (deduped)** | | | |

### Critical issues (fix before release)
### Major issues (next revision)
### Recommended next steps
[Point at /mlbook-writing for prose fixes; individual reports in quality_reports/ carry the details and stable finding IDs.]
```

## Step 5: Report Budget

Print an estimate after completion: agents spawned, approximate token usage, and the reminder that single-lens runs (`/mlbook-student-lens`, `/proofread`) are the cost-conscious alternative.

## Flag Reference

| Flag | Effect |
|---|---|
| `--fast` | One synthesis agent instead of the fanout. ~8k vs ~40–60k tokens. |
| `--out DIR` | Reports to `DIR` instead of `<root>/quality_reports/`. |
| `--skip-exercises` / `--skip-substance` / `--skip-student` | Drop that lens (the missing-Exercises CRITICAL check still runs). |

## Quality Score Rubric

| Verdict | Meaning |
|---|---|
| PASS | Ready to render and publish |
| REVISE | Publishable after addressing MAJORs; no student-misleading content |
| BLOCK | Contains wrong math/code, a broken exercise, or a missing required section |
