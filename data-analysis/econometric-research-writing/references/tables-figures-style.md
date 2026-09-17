# Tables And Figures Style

Use this reference when producing or revising tables, regression output, descriptive statistics, robustness tables, coefficient plots, event-study figures, trend plots, mechanism diagrams, or Word/PDF-ready visual material for economics, finance, management, or applied econometrics papers.

## Style Basis

Default to an economics/management top-journal style inspired by AEA/JEL, QJE, Journal of Finance, Review of Financial Studies, and Academy of Management conventions:

- Use restrained black-and-white table design with horizontal rules only.
- Keep three-line tables as the default for empirical Word outputs: top rule, header-bottom rule, and bottom rule.
- Prefer author-year references in text unless the target journal or user requires numeric superscript citations.
- Use figure and table captions/legends to make empirical objects self-contained without turning notes into mini-method sections.
- Keep tables and figures claim-driven: each object should support a specific empirical point in the surrounding text.

## Table Rules

Use these defaults unless the user provides a journal template:

- Number tables consecutively with Arabic numerals for general economics/management papers: Table 1, Table 2, etc.
- For finance papers following Journal of Finance style, use Roman numerals for tables if explicitly requested: Table I, Table II, etc.
- Put table titles above the table.
- Use only horizontal lines; do not use vertical lines, grid boxes, shading, or decorative fills.
- Keep tables in portrait orientation when possible.
- Keep empirical tables narrow: no more than 8-9 columns including row labels unless a landscape appendix table is justified.
- Use `Panel A`, `Panel B`, etc. for sections inside a table.
- Do not abbreviate column headings unless the abbreviation is standard and defined in the note.
- Place a leading zero before decimals: `0.357`, not `.357`.
- Put standard errors in parentheses below coefficients, or t-statistics if the project explicitly uses them.
- Do not add significance stars by default. If the user or course requires stars, define the thresholds in the note.
- Put sample size, fixed effects, controls, clustering, and standard-error type in visible rows.
- Put `Notes:` and `Source:` below the table, outside the table grid.
- Define every non-obvious variable, transformation, panel, sample restriction, and estimation convention in the note or variable-definition appendix.
- Place source notes after other notes.
- Include full citations for data or reused table content in the references.

## Empirical Table Types

### Descriptive Statistics

Include variables that matter to the empirical strategy:

- Outcome, main regressor/treatment, mechanism variables, moderators, instruments, core controls, and sample flags.
- Mean, standard deviation, median, min/max or percentiles, and nonmissing count.
- Units and transformations, especially logs, percentages, winsorization, lags, or differences.

Avoid dumping every numeric column from the dataset.

### Correlation Tables

Use correlation tables only for theoretically connected variables. Do not interpret a high correlation as a causal pathway.

Flag:

- Mechanical correlations caused by construction.
- Variables that are alternative measures of the same construct.
- Potential multicollinearity among controls.
- Treatment-mechanism-outcome correlations that require model-based checks before interpretation.

### Regression Tables

Use a stable column progression:

1. Baseline with minimal controls.
2. Add core controls.
3. Add fixed effects.
4. Add full controls or preferred specification.
5. Add robustness/mechanism/heterogeneity column only if it answers a stated threat.

Keep the main coefficient in the same row across columns. If the outcome changes, separate tables are often clearer.

### Mechanism And Heterogeneity Tables

Label mechanism columns by construct, not only by regression number. Distinguish:

- Mechanism outcome specifications.
- Mediation-style conditioning.
- Heterogeneity interactions.
- Subsample splits.

State whether conditioning on a post-treatment variable changes the estimand.

## Figure Rules

Use figures when the visual pattern is more informative than exact numbers:

- Trends before and after a shock or treatment.
- Event-study coefficients and confidence intervals.
- Coefficient paths across horizons, lags, quantiles, or bandwidths.
- Distributional comparisons, binned scatterplots, and residual diagnostics.
- Mechanism diagrams when the variable path is part of the argument.

Default figure style:

- Use vector formats when possible for final figures: PDF, SVG, EPS, or editable PPT/EMF when compatible with the output.
- Use 300 dpi or higher for raster images.
- Label every axis with variable name and unit.
- Use readable text at final Word/PDF size.
- Use colorblind-safe palettes; ensure the figure still works in grayscale.
- Remove unnecessary chart borders, background fills, and heavy gridlines.
- Use light horizontal reference lines only when they improve interpretation.
- Show uncertainty intervals when plotting estimates.
- Label multi-panel figures with `A`, `B`, `C`, etc., and keep panel order consistent with the prose.
- Put figure captions/legends below the figure unless a target journal template says otherwise.
- Put source notes after other figure notes.

## Econometric Figure Types

### Event-Study Figures

- Show point estimates and confidence intervals.
- Mark the omitted reference period.
- Add a vertical line at treatment/event timing when applicable.
- Do not crop pre-period coefficients in a way that hides pre-trend evidence.
- State the fixed effects, controls, and clustering in the note or caption.

### Coefficient Plots

- Sort coefficients by conceptual order, not by statistical significance unless explicitly analyzing ranking.
- Use a zero reference line for effect estimates.
- Plot confidence intervals and state the confidence level.
- Keep variable labels readable and consistent with table row names.

### Time-Series And Panel Trends

- Show sample coverage and major policy/event dates when relevant.
- Avoid dual y-axes unless the scales and interpretation are unmistakable.
- For raw trends, do not imply treatment effects without a credible counterfactual.

### Binned Scatterplots

- State residualization controls, binning rule, and weights if used.
- Use binned means plus fitted line when appropriate.
- Do not overinterpret as causal unless identification is justified elsewhere.

## Placement And Callouts

- Every table and figure must be cited in the text before or near where it appears.
- Each callout should tell readers what to look for, not only say "see Table 2."
- For course reports and Word papers, place tables/figures near first substantive mention unless the user requests an end-of-manuscript journal layout.
- For AOM-style management submissions, group references, appendices, tables, and figures at the end and insert placement markers in the text if requested.

## Table/Figure Prose

Use this pattern:

1. Name the object: `Table 2 reports the baseline estimates.`
2. Identify the key comparison: `Columns (1)-(3) progressively add controls and fixed effects.`
3. State magnitude and uncertainty: `The preferred estimate implies...`
4. Bound interpretation: `Under the maintained fixed-effects specification...`

Avoid:

- Repeating every number in prose.
- Explaining formatting choices in the paper body.
- Treating control coefficients as central findings without theory.

## QA Checklist

Before final delivery:

- Tables use three-line style unless explicitly overridden.
- No vertical borders, shading, or full grid tables in empirical outputs.
- Notes define variables, standard errors, clustering, sample restrictions, and sources.
- Figures have axis labels, units, captions, readable text, and uncertainty intervals where needed.
- Every table/figure is called out in the text.
- Every source note has a matching reference-list entry when applicable.
- Word rendering has no clipped tables, missing images, unreadable labels, or caption separation from the object.
