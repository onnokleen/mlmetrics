# claude-agents.md — Reusable Agent Prompts

Agent prompts for common authoring tasks on this textbook. Use with the Agent tool in Claude Code.

---

## chapter-review

> Reviews a chapter for flow, clarity, econometric framing, and adherence to project conventions.

```
Review the chapter at /Users/onnokleen/Research-ML/Book_ML_Econometrics/CHAPTER.qmd.

Read CLAUDE.md first for project conventions.

Evaluate the chapter on these dimensions:

1. **Flow and structure**: Does it follow the expected skeleton (Overview → Roadmap → Core content → Summary → Exercises)? Is the progression logical?

2. **Econometric framing**: Are ML concepts introduced with connections to econometric methods the students already know? Are examples drawn from economic/financial data, not image classification?

3. **Audience calibration**: Does it assume too much or too little ML knowledge? Does it respect the students' strong econometrics/probability background?

4. **Non-iid awareness**: When iid assumptions appear (e.g., in cross-validation, bootstrap), are they flagged and discussed in the context of time series or heteroskedastic data?

5. **Notation and rigor**: Are all terms defined before use? Is notation consistent within the chapter and with other chapters?

6. **Callout usage**: Are the right callout types used (definitions in callout-definition, not callout-note; hints in collapsible callout-warning, etc.)?

7. **Cross-references**: Do all @sec-*, @fig-*, and @citation references point to valid targets?

8. **Commented-out or dead content**: Flag any HTML comments, stubs, or duplicate content that should be cleaned up.

Report findings organized by dimension. For each issue, reference the specific line or section.
```

---

## exercise-review

> Reviews exercises for exam-suitability and formatting.

```
Review the exercises in /Users/onnokleen/Research-ML/Book_ML_Econometrics/CHAPTER.qmd.

Read CLAUDE.md first, especially the "Exercise requirements" section.

For each exercise, evaluate:

1. **Pen-and-paper feasibility**: Can every part be answered with pen and paper in a reasonable time under exam conditions (3-hour handwritten exam)? Flag any part that requires running code, looking up values, or open-ended discussion.

2. **Scope and gradeability**: Is each sub-part well-bounded with a definitive answer? Could a teaching assistant grade it with a clear rubric?

3. **Hint quality**: Are hints progressive (not giving away the answer, but providing the right nudge)? Is there a hint for each non-trivial part?

4. **Solution completeness**: Does the solution fully answer every part of the question? Does the derivation match what a student would write?

5. **Difficulty annotation**: Is there an italic comment about exam suitability?

6. **Format compliance**: Does the exercise follow the callout format (statement in callout-note, hints in collapsible callout-warning, solution in collapsible callout-tip)?

7. **Coverage**: Are the exercises representative of the chapter's key concepts? Are there important topics not covered by any exercise?

Report findings per exercise, then give an overall assessment of the exercise set.
```

---

## math-check

> Verifies mathematical derivations step-by-step.

```
Check all mathematical derivations in /Users/onnokleen/Research-ML/Book_ML_Econometrics/CHAPTER.qmd.

For each derivation (in the main text and in exercise solutions):

1. Verify each algebraic step. Flag sign errors, missing terms, or unjustified steps.
2. Check that stated results (e.g., "the entropy is 1/2 log(2*pi*e*sigma^2)") match the derivation that precedes them.
3. Verify that assumptions are stated (e.g., "assuming p and q have the same support").
4. Check that notation is consistent (e.g., H vs h for discrete vs continuous entropy).
5. For inequalities, verify the direction and the conditions for equality.

Report each issue with the specific equation or line reference and the correction needed.
```

---

## consistency-check

> Cross-chapter consistency audit.

```
Perform a consistency audit across all chapters in /Users/onnokleen/Research-ML/Book_ML_Econometrics/.

Read CLAUDE.md and _quarto.yml first.

Check:

1. **Notation consistency**: Is the same symbol used for the same concept across chapters? (e.g., H for entropy, theta for parameters, etc.) Flag conflicts.

2. **Cross-reference validity**: For each @sec-*, @fig-*, and inter-chapter link (e.g., [Section 5](feed_forward_nns.qmd)), verify the target exists.

3. **Chapter numbering**: Do the number-offset values in each chapter's YAML frontmatter match their position in _quarto.yml?

4. **Structural consistency**: Does every chapter follow the Overview → Roadmap → Core content → Summary → Exercises skeleton? Which chapters deviate?

5. **Callout conventions**: Are callout types used consistently (definitions always in callout-definition, not mixed with callout-note, etc.)?

6. **Dead content**: Flag commented-out sections, empty stubs, or TODO markers across all chapters.

Report findings grouped by issue type. Prioritize issues that would confuse students.
```

---

## new-exercise

> Generates a new pen-and-paper exercise for a given topic.

```
Read CLAUDE.md in /Users/onnokleen/Research-ML/Book_ML_Econometrics/ for exercise conventions.

Then read the chapter at /Users/onnokleen/Research-ML/Book_ML_Econometrics/CHAPTER.qmd to understand the content and existing exercises.

Generate a new exercise on the topic: TOPIC

Requirements:
- Follow the exact exercise format from CLAUDE.md (callout-note statement, callout-warning hints, callout-tip solution)
- Must be answerable with pen and paper under exam conditions
- Break into 2-4 numbered parts with increasing difficulty
- Provide one hint per non-trivial part
- Write a complete, step-by-step solution
- Include an exam-suitability annotation in italics
- Number it as Exercise X.Y where X matches the chapter and Y follows the last existing exercise
- Use econometric/financial data context where possible
- Do not require running code or looking up numerical values

Output the complete exercise block in Quarto markdown, ready to paste into the chapter.
```
