# Econometric Data Analysis Workflow

Use this long-term reference when the user provides a dataset, variable list, codebook, result table, or asks for data analysis before writing an economics/management empirical paper. This reference adapts common high-quality data-analysis skill patterns--automatic profiling, quality checks, visualization, structured reports, and verification loops--to professional econometric research, where variables have economic meaning and causal roles.

When the user requests grilling or a mock defense, read `research-grilling.md` first. Treat profiling and focused diagnostics as temporary evidence gathering until the user explicitly authorizes implementation; do not start the formal analysis runner during the grilling phase.

## Table Of Contents

- What Generic Data Analysis Skills Do Well
- Econometric Upgrade
- Intake And Variable Semantics
- Data Structure Audit
- Data Quality And Measurement
- Variable Construction
- Causal And Mechanism Map
- Descriptive And Diagnostic Analysis
- Model-Ready Dataset Checks
- Output Contract
- Failure Modes

## What Generic Data Analysis Skills Do Well

Reuse these strengths:

- Start with an automatic data profile: rows, columns, types, missingness, ranges, duplicates, date coverage, category levels, and basic distributions.
- Produce visual and tabular summaries early, before modeling.
- Detect obvious anomalies: impossible values, outliers, date gaps, duplicate keys, constant variables, high missingness, and inconsistent units.
- Generate structured outputs: data profile, quality report, analysis narrative, chart list, and reproducibility artifacts.
- Use verification loops: after each analysis step, check whether the result answers the question and whether assumptions still hold.

Do not copy the weak parts:

- Do not treat every correlation as an insight.
- Do not rank variables only by predictive power when the task is causal or structural.
- Do not ignore units, timing, measurement construction, or economic interpretation.
- Do not select charts mechanically without a research question.

## Econometric Upgrade

For economics/management empirical work, every analysis must separate:

- Outcome `Y`: the dependent variable or target construct.
- Treatment/main regressor `D` or `X`: the economic exposure, policy, price, shock, or strategic variable.
- Controls `W`: pre-determined or plausibly exogenous covariates used for comparability.
- Fixed effects: unit, time, industry, region, firm, product, or cohort effects.
- Mechanisms `M`: variables on the causal path from `D` to `Y`.
- Moderators `Z`: variables that change the strength or direction of the effect.
- Instruments `Z_iv`: variables used only through an exclusion restriction.
- Colliders/bad controls: variables affected by both treatment and outcome determinants, or post-treatment controls that block part of the effect.

Default rule: data analysis should produce a model-ready research map, not just an EDA report.

## Data Acquisition and Decoupling

Rather than hardcoding specific database clients or APIs (like World Bank, FRED, or AkShare) into the writing skill, leverage the Model Context Protocol (MCP) or external fetching scripts as an abstract retrieval interface:

- **Data Acquisition Boundary**: Use available data-fetching MCP tools or write temporary Python scripts to download macroeconomic, financial, or micro-level variables, saving them into a standard CSV, XLSX, or DTA dataset in the local workspace.
- **Profiling Decoupling**: Once the data file is generated, pass it to `scripts/profile_econ_dataset.py` for deterministic structure and quality profiling: column summaries, missingness, panel checks for explicitly assigned keys, regressor diagnostics, and transformation warnings. The profiler does not assign semantic roles from column-name keywords. The agent must inspect names and observed values together with the research question and any codebook, record its decisions in `roles.json`, and rerun the profile with that file. The profiler does **not** run unit-root or stationarity tests; run those separately after confirming frequency, deterministic terms, lag structure, and relevant variables.

## Intake And Variable Semantics

Before modeling, build a variable dictionary with:

- Variable name and plain-language label.
- Unit of measurement and scale.
- Timing: contemporaneous, lagged, cumulative, pre-treatment, post-treatment.
- Level: individual, firm, country, market, product, region, industry, or aggregate.
- Transformation candidates: log, growth rate, first difference, standardized index, winsorized value, share, per-capita value.
- Economic role: outcome, main regressor, control, mechanism, moderator, instrument, fixed effect, clustering unit, weight, or sample flag.
- Measurement risk: survey error, accounting definition change, currency/inflation issue, coding change, top-coding, censoring, selection.

The agent decides roles from the joint evidence in variable names, observed values and distributions, units, timing, research design, and any codebook. It must record the decision in a reviewed `roles.json`; deterministic scripts must not silently convert name hints into outcome, treatment, control, unit, or time roles. If the evidence is ambiguous, ask targeted questions or label the agent decision as provisional.

A standard executable role specification can include:

```json
{
  "outcome": "revenue",
  "treatment": "subsidy",
  "controls": ["assets", "employment"],
  "unit": "firm_id",
  "time": "year",
  "fixed_effects": ["firm_id", "year"],
  "cluster": "firm_id",
  "event_time": "event_time",
  "event_reference": -1,
  "event_window": [-4, 4]
}
```

## Data Structure Audit

Classify the dataset:

- Cross-section: one row per unit.
- Repeated cross-sections: repeated time periods but not the same units.
- Panel: repeated observations for the same units.
- Time series: one aggregate unit over time.
- Event-study panel: units observed around an event or treatment date.
- Transaction-level data: many rows per unit-time requiring aggregation.

For panel data:

- Identify unit key and time key.
- Check duplicate unit-time rows.
- Check balanced versus unbalanced panel.
- Report `N`, `T`, total observations, min/max observations per unit, and date coverage.
- Check whether treatment varies within units over time; fixed effects cannot estimate a fully time-invariant treatment.

For time series:

- Check date frequency, gaps, seasonality, trends, and persistence.
- Flag variables that need deflation, log transformation, differencing, or unit-root checks.

## Data Quality And Measurement

Run these checks before substantive interpretation:

- Missingness by variable and by key groups/time periods.
- Impossible or economically nonsensical values: negative prices, rates outside `[0,1]` when stored as shares, invalid dates, zero denominators, impossible ages or firm sizes.
- Outliers by raw scale and transformed scale.
- Duplicates on the proposed analysis key.
- Unit inconsistencies: thousands versus units, percentages versus fractions, nominal versus real values, local currency versus USD.
- Structural breaks in definitions, data source changes, or policy coding.
- Sample selection: who enters the data, who is excluded, and whether missingness is related to treatment or outcome.

Report whether each issue is a cleaning issue, a modeling issue, or a limitation.

## Variable Construction

Construct variables to match economic meaning:

- Logs for positive scale variables when elasticity or proportional change is meaningful.
- Growth rates or first differences when trends dominate levels.
- Per-capita, per-employee, or per-asset normalization when size mechanically drives levels.
- Real terms after deflating nominal money variables.
- Lagged regressors when simultaneity or timing requires prior-period exposure.
- Treatment indicators and event time variables for DiD/event-study designs.
- Mechanism variables only after deciding whether they are mediators, controls, or outcomes in separate mechanism models.

Document every transformation with formula, source variable, timing, and sample consequences.

## Causal And Mechanism Map

Before regression, write a compact pathway map:

```text
Main path: D -> Y
Mechanism path: D -> M -> Y
Confounding path: C -> D and C -> Y
Reverse path: Y -> D
Selection path: S affects sample inclusion and may relate to D/Y
Measurement path: observed D or Y may differ from latent construct
```

Use the map to decide:

- Which variables are controls versus mechanisms.
- Which controls must be pre-treatment.
- Whether lagging variables improves timing credibility.
- Whether a fixed effect absorbs the relevant omitted factor.
- Whether an instrument or treatment design is needed.
- Which robustness checks correspond to each threat.

Do not put mediators and confounders in the same "controls" bucket without stating what estimand changes.

## Descriptive And Diagnostic Analysis

Minimum descriptive outputs:

- Table 1: sample size, mean, standard deviation, selected percentiles, missingness, and unit of measurement.
- Correlation table for variables that are theoretically connected, not every numeric column.
- Treatment/control balance or exposure distribution when causal design is present.
- Time trend plot for outcome, treatment, and key covariates when time exists.
- Within/between variation summary for panel regressors.
- Missingness and sample selection summary by treatment/time/unit group.

After the agent reviews `roles.json`, run:

```bash
python3 scripts/run_empirical_analysis.py data.csv --roles-json roles.json --output-dir results
```

The deterministic runner produces focused descriptive-statistics tables, a baseline OLS/fixed-effect design with clustered standard errors when a cluster role exists (HC3 otherwise), a progression of robustness specifications, and an event-study coefficient table plus PNG/PDF figure when `event_time` is defined. These are statistical outputs, not automatic causal identification; the agent must still justify the design and interpret estimates within its assumptions.

Multicollinearity diagnostics must be based on agent-declared treatment/main regressors and controls. Exclude unit IDs, time keys, clustering variables, and absorbed fixed effects. Report top correlations with a sample-adaptive threshold, VIF, standardized design-matrix condition number, and rank deficiency rather than relying on a fixed pairwise-correlation cutoff.

Diagnostics by data type:

- Panel: within variation, duplicate unit-time keys, unbalancedness, cross-sectional dependence, clustering unit.
- Time series: stationarity, lag order, seasonality, breaks.
- IV: first-stage relationship and instrument balance/exclusion risks.
- DiD/event study: pre-treatment outcome trends and treatment timing distribution.
- Synthetic counterfactual: pre-treatment fit and donor pool contamination.

## Model-Ready Dataset Checks

Before estimating a baseline model, confirm:

- The analysis sample is fixed and reproducible.
- `Y`, main regressor, controls, fixed effects, cluster variables, and weights are defined.
- Timing is coherent: treatment/exposure precedes or is contemporaneous with the outcome as intended.
- There is identifying variation after fixed effects.
- Missingness does not silently change the sample across columns.
- Transformations do not create infinite values or drop economically important zeros without explanation.
- Table shells are known before running many specifications.

## Output Contract

When analyzing data for this skill, produce:

1. Data profile: structure, keys, variable types, missingness, duplicates, coverage.
2. Variable dictionary: economic role, unit, timing, transformation, measurement risk.
3. Causal/mechanism map: main path, confounders, mechanisms, reverse causality, selection.
4. Descriptive tables/figures: focused on the research question.
5. Model-readiness memo: baseline specification, required diagnostics, and unresolved issues.
6. Reproducibility note: input files, scripts run, generated outputs, and temporary artifacts.

For Word paper deliverables, convert the final descriptive and regression tables to three-line tables and keep chart captions tied to the empirical claim.

## Failure Modes

- Reporting "strong correlation" without economic role, timing, or omitted-variable discussion.
- Using post-treatment variables as controls without explaining the estimand change.
- Treating high predictive importance as causal importance.
- Ignoring unit changes, inflation, deflators, sample selection, or data source breaks.
- Running FE models when the main regressor has no within-unit variation.
- Running panel regressions without checking duplicate unit-time keys.
- Running event studies without event-time support or pre-period observations.
- Reporting many visuals but no model-ready conclusion.

## See Also

- [Method Selection](method-selection.md)
- [Empirical Workflow](empirical-workflow.md)
- [Tables and Figures Style](tables-figures-style.md)
