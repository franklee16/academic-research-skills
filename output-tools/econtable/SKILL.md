---
name: econtable
description: Create, revise, or audit journal-ready economics tables and export code from descriptive statistics or estimation results, including main regressions, experiments, RD, balance, IV, robustness, event-study summaries, mechanisms, and heterogeneity. Use when producing or assessing a research table; pair with econfigure for mixed table-and-figure requests.
---

# Econtable

Produce compact, self-contained economics tables whose numerical content is generated from data or stored model objects and whose hierarchy remains readable at final journal size. Preserve the user's estimand, inference, model order, language, and journal template unless a change is necessary and disclosed.

## Start with the table's argument

Identify or infer:

- whether the table is descriptive, diagnostic, main-result, mechanism, heterogeneity, robustness, or appendix evidence;
- the observation unit, sample period/restrictions, outcome units/transformation, treatment/reference category, and weights;
- the sequence of models or outcomes and what changes from one column to the next;
- the standard-error or confidence-interval construction, clustering level, hypothesis tests, and multiple-testing adjustment;
- the target manuscript system, text width, and journal convention.

Do not invent or transcribe estimates manually. Do not recompute a different model merely to make an export package work. Retrieve values from the fitted objects or their reproducible result files.

When creating a table, changing values, or numerically validating results, pause if no data/model object or complete result extract is available and request the minimum missing input rather than manufacturing numbers. A visual/structural audit of an existing PDF, image, or table may proceed without models, but must state that numerical accuracy and inference cannot be verified. For a final table, do not guess outcome units, treatment coding, model progression, weights, inference, language, or page width and do not ship unresolved placeholders. Resolve output language in this order: explicit user choice, target manuscript/journal, established project labels, then prompt language; ask when those signals conflict materially.

## Route to the detailed guidance

- Read [references/table-system.md](references/table-system.md) for every table. It defines the sample-derived hierarchy, rules, typography, numeric formatting, notes, width, and QA defaults.
- Read [references/table-recipes.md](references/table-recipes.md) for the requested table family.
- Read [references/implementation-recipes.md](references/implementation-recipes.md) when writing or revising R, Stata, Python, LaTeX, Word, or spreadsheet export code.
- Read [references/sample-derived-decisions.md](references/sample-derived-decisions.md) only when matching the supplied papers closely, explaining provenance, or selecting between alternative layouts.

## Working sequence

1. Inspect the model/data objects and nearby analysis code. If a target journal is named, check its current official author/style guide before choosing layout or significance conventions. Reuse established variable labels, model names, sample definitions, and export paths when sound.
2. Build a column plan before formatting: column groups, model order, coefficients/contrasts, specification rows, diagnostics, and notes. Each adjacent column should have a clear reason to exist.
3. Extract numbers programmatically. Confirm coefficient identity, transformation, reference group, inference method, sample size, clusters, fit statistics, and any linear-combination tests.
4. Apply the table system. Use semantic spanners and panels rather than a flat wall of numbered columns. Split a table before shrinking it below readable size.
5. Render the actual output in its target medium. Inspect page fit, line breaks, decimal alignment, note wrapping, and consistency with the surrounding manuscript.
6. Cross-check the rendered table against the underlying objects and report the checks performed.

## Statistical reporting constraints

- Put the estimate on the first line and its standard error in parentheses on the next line by default. If reporting confidence intervals, use brackets and state the confidence level.
- State the exact inference method and clustering level. The word `robust` alone is insufficient.
- Keep one inferential convention within a table. Do not mix standard errors, confidence intervals, bootstrap intervals, and p-values across columns without explicit headers or panel labels.
- Significance stars are optional. Absent a user or current journal policy, use `* p<0.10`, `** p<0.05`, `*** p<0.01` for two-sided tests and define them exactly once in the notes. A journal profile may prohibit or redefine stars and always takes precedence. Never bold significant coefficients.
- For subgroup comparisons, include the interaction, difference, or equality-test p-value. Do not infer heterogeneity by comparing whether separate subgroup coefficients have stars.
- For nonlinear models or transformed outcomes, label the reported object accurately: coefficient, marginal effect, elasticity, percent effect, or back-transformed quantity.
- Preserve the model's actual sample by column. If `N` changes, make the reason discoverable in a specification row or note.
- Never use `0` to represent a coefficient that was not estimated or data that are missing.

## Delivery contract

When creating or editing a table, return or save:

- executable export code tied to stored data/model objects;
- the manuscript-native table file, normally LaTeX, Word, or an editable spreadsheet/HTML table as requested;
- a rendered PDF/image preview for visual verification when layout matters;
- a concise note block that fully describes sample, units, specification, inference, and significance conventions;
- a short QA statement covering numerical and visual checks.

Keep full-precision numbers in the analytical objects and round only at presentation time. Do not deliver a screenshot as the sole table artifact.
