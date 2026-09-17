# Economics Table Recipes

Select the structure that matches the evidence. A single universal regression-table layout is not appropriate for every design.

## Main regression table

Use a left-to-right specification progression readers can narrate:

1. parsimonious/baseline specification;
2. pre-specified controls;
3. fixed effects or trends;
4. preferred inference/sample;
5. a small number of targeted alternatives.

Keep the focal coefficient at the top in every column. Place controls/FE/sample facts in a separated lower block. Include `N`, clusters when relevant, and the appropriate fit statistic. If columns have different outcomes rather than accumulating specifications, use outcome spanners and make the column logic explicit.

Do not infer that labels such as `baseline`, `controls`, and `FE` are cumulative. Inspect the fitted formulas/specification metadata. If `FE` could mean either FE-only or controls-plus-FE and the objects do not resolve it, ask before constructing the column plan.

Avoid a kitchen-sink main table. Put extensive robustness in the appendix or a coefficient/forest figure.

## Descriptive statistics

Choose statistics based on the data and comparison:

- Standard continuous variables: `N`, `Mean`, `SD`.
- Skewed variables: `Mean`, `SD`, `p10`, `Median`, `p90`, as in the Wang sample.
- Matched/reweighted sample comparison: `P25`, `Mean`, `P75` for each sample, as in Kleven.
- Multiple samples: repeat a compact statistic set under sample spanners rather than adding a sample row for every variable.

Group rows into substantive panels and include the observation unit in each panel heading, such as `Panel B. Rural development (household)`. Put units or transformations in row labels. For binary variables, report means as shares and say so. Do not mix raw currency units, thousands, logs, and indices without labels.

## Balance table

Default columns:

`Variable | Treated mean | Control mean | Difference | SE or p-value | Standardized difference`

- Put SDs below group means and the SE below the difference only if the note makes the differing parentheses explicit.
- Prefer standardized differences for balance diagnostics; p-values alone depend strongly on sample size.
- Identify whether balance is raw, matched, weighted, or regression-adjusted and state the clustering/inference method for the difference.
- Do not use balance-test significance to select controls after seeing the results unless the design explicitly calls for it.

## Difference-in-differences and policy effects

- Put the treatment×post or policy coefficient first.
- Label the comparison and omitted period/group clearly.
- Include unit/group and period fixed effects or other design-specific effects in the lower block rather than printing absorbed coefficients.
- For staggered adoption or alternative estimators, label the estimator by column; do not call every specification `TWFE`. State the comparison group, cohort/event-time support, aggregation or weighting convention, endpoint bins, and whether reported uncertainty is pointwise or simultaneous when relevant.
- Include clustering level and any weighting. A pre-trend/joint-test p-value belongs in a labeled diagnostic row when reported.

## Event-study summary table

Use this when a figure contains many dynamic coefficients but the paper needs compact quantitative summaries.

- Define windows ex ante, for example `Panel A. Short run (event times 0–5)` and `Panel B. Long run (event times 6–10)`.
- Keep outcome columns identical across panels.
- For group comparisons, use `Group A`, `Group B`, and `Difference` rows with SEs, following the Kleven structure.
- State whether summaries are averages, weighted averages, linear combinations, or separate regressions and how their SEs were computed.

Do not replace the full event-study diagnostic with only a summary table when pre-trends and dynamics are substantively important.

## Heterogeneity and interaction table

- Start with the common/main effect when it has a meaningful interpretation.
- Organize modifiers into theory-driven panels such as `Panel A. Primary mechanism` and `Panel B. Alternative explanations`.
- Show the interaction or subgroup contrast, and report the linear-combination estimate when readers care about the effect for the non-reference group.
- Include the equality/interaction p-value. Never treat different star patterns as a test of difference.
- Keep reference categories and coding visible in row labels or notes.
- When many outcomes repeat the same two interaction rows, use stacked outcome panels with repeated concise headers; move repeated controls/FE to the note, as in the compact CLL appendix tables.

If the table becomes a long list of subgroup estimates, use a companion forest plot via `$econfigure` when that skill is available, while retaining exact tests in the table or appendix.

## Robustness table

- Column 1 should reproduce the preferred baseline.
- Change one clearly identified design feature per subsequent column whenever possible.
- Put changing features—matching radius, minimum observations, sample restriction, controls, estimator, SE method—in the lower specification block.
- Keep the focal coefficient(s), units, and inference comparable. If a check changes the estimand, separate it into a panel or different table.
- For more than about eight one-coefficient checks, prefer a robustness forest figure and a concise table of exact values/diagnostics in the appendix.

## Instrumental variables

Use explicit panels or spanners:

- `Panel A. Reduced form`
- `Panel B. First stage`
- `Panel C. Second stage`

Report the instrument coefficient and outcome first, then the structural estimate. Include a named weak-instrument diagnostic matched to the covariance structure, number of instruments, number of endogenous regressors, and estimator; do not report a generic or homoskedastic first-stage F when clustered/heteroskedastic inference calls for another statistic. Label LIML, 2SLS, JIVE, or other estimators accurately. When identification may be weak, report design-appropriate weak-ID-robust tests or confidence sets, such as Anderson–Rubin or CLR where applicable, rather than relying only on conventional Wald inference. Do not report an ordinary first-stage `R²` as a substitute for weak-instrument diagnostics.

## Multiple outcomes and outcome families

- Use top-level spanners for outcome families and second-level labels for specific outcomes.
- Put one common model progression under each family when the specifications repeat.
- If eight columns approach the readability limit, use stacked panels with the same column numbers rather than squeezing more columns.
- State any family-wise error rate, false discovery rate, sharpened q-value, or standardized outcome index construction in a dedicated row/note.

## Mechanisms, mediation, and channels

- Separate `Ex ante` characteristics from `Ex post` outcomes with top-level spanners when the conceptual timing differs.
- Separate reduced-form channel evidence from formal mediation; do not label a regression `mediation` unless the estimand and assumptions justify it.
- For controlled direct effects or decomposition results, state the method, scale, and comparison. Include `Size relative to main effect` only when numerator and denominator are commensurate and uncertainty is handled appropriately.
- Put joint effects or linear combinations and their p-values immediately below the component coefficients, not hidden in the note.

## Nonlinear and transformed outcomes

- Label log outcomes as `Log outcome` or state the transformation in the spanner.
- For log-point coefficients, do not label the raw coefficient as an exact percentage effect when the approximation is poor. Compute and label an exact transformation if that is what the table reports.
- For logits/probits/count models, state whether cells contain index coefficients, odds ratios, incidence-rate ratios, or average marginal effects.
- Keep marginal effects and structural coefficients in separate panels/tables when their scales differ.

## Appendix compression

Compress repetition, not meaning:

- move identical control definitions to one note;
- repeat concise headers for each outcome panel;
- keep the two or three focal rows plus `N` when the purpose is to document a large grid of heterogeneity results;
- use landscape or continuation for genuinely wide evidence;
- never reduce the table to unreadable type or omit inference details merely to fit one page.
