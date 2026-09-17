# Empirical Workflow

Use this reference to run or plan an econometric analysis from model-ready data to final paper tables. For initial dataset profiling, variable semantics, data quality, and causal/mechanism mapping, read `data-analysis-workflow.md` first. For final table/figure style and Word layout rules, read `tables-figures-style.md`.

## Analysis Pipeline

1. Define the research question as a testable relationship.
2. Build the analysis sample and record every filter.
3. Create a variable dictionary that assigns economic roles: outcome, main regressor, controls, mechanisms, moderators, instruments, fixed effects, clustering unit, and bad controls.
4. Create variables with explicit formulas, units, logs, lags, differences, and winsorization rules.
5. Produce descriptive statistics and sample coverage tables.
6. Diagnose data structure: missingness, balance, outliers, stationarity, serial correlation, cross-sectional dependence, and identifying variation after fixed effects.
7. Map the likely pathway from main regressor to outcome and match robustness checks to each threat.
8. Estimate the baseline model.
9. Estimate alternative specifications that answer specific threats.
10. Run robustness checks matched to the method.
11. Convert estimates to economic magnitudes.
12. Produce final tables/figures with self-contained notes, source notes, and text callouts.
13. Write interpretation with limitations and citation-backed claims.

For standard linear and event-study work after the agent has reviewed semantic roles, `scripts/run_empirical_analysis.py` implements steps 5 and 8-10 as reproducible CSV/Markdown tables and PNG/PDF figures. Its default robustness progression separates minimal, controlled, preferred fixed-effect, and alternative-inference specifications; replace or extend these only when the added specification targets a stated threat.

## Reproducibility Contract

- Keep raw data read-only.
- Save cleaned data separately.
- Save scripts that transform raw to clean and clean to results.
- Save final tables/figures under stable names.
- Save verified citation/reference metadata when literature is used.
- Record package versions when possible.
- Do not overwrite final outputs without creating a formal archive or noting the authority change.

## Baseline Table Plan

Typical empirical paper tables should use clean economics-style three-line formatting in Word outputs unless the user requests a different journal/class template:

- Table 1: sample construction or descriptive statistics.
- Table 2: baseline estimates.
- Table 3: mechanism, heterogeneity, or dynamic response.
- Table 4: robustness and sensitivity.
- Figure 1: raw trend, event-study path, coefficient path, or key model visualization.

## Robustness Menu

Choose only checks that target real threats:

- Alternative dependent variable definitions.
- Alternative main regressor definitions.
- Additional fixed effects or time controls.
- Alternative clustering/standard errors.
- Lagged regressors or lagged outcome controls.
- Sample restrictions and influential-unit exclusion.
- Placebo outcomes or placebo timing.
- Pre-trend checks for event designs.
- Bandwidth/threshold sensitivity for nonparametric and threshold methods.
- Instrument set sensitivity for IV/dynamic panel.
- Lag order and stability diagnostics for VAR/time series.

## Results Interpretation

For every main coefficient:

1. State sign and statistical evidence.
2. Translate magnitude into the original economic unit or elasticity.
3. Compare with baseline mean or plausible benchmark.
4. State whether the estimate is robust across key specifications.
5. State the interpretation boundary.

Avoid reading too much into controls. Controls are often included to improve comparability or reduce omitted-variable concerns; they are not automatically substantive findings.

For mechanism variables, state whether the estimate is a separate mechanism test, a mediation-style specification, or a changed estimand after conditioning on a post-treatment variable.

## Table Writing Rules

- Put the main coefficient in the same row across columns.
- Use clear column labels, not only model numbers.
- Report sample size and fixed effects.
- Report standard-error type and clustering.
- Keep notes concise and specific.
- Keep source notes below other table notes.
- Avoid significance stars unless the user/course/journal requires them; if used, define thresholds.
- Do not bury important sample restrictions in prose only.

## Failure Modes

- Analysis has many specifications but no baseline.
- Robustness checks are unrelated to the threat model.
- Result interpretation repeats statistical significance but never explains economic magnitude.
- The paper claims causality while the design only supports association.
- Generated Word/PDF outputs are not rendered and visually checked.

## See Also

- [Data Analysis Workflow](data-analysis-workflow.md)
- [Method Selection](method-selection.md)
- [Tables and Figures Style](tables-figures-style.md)
