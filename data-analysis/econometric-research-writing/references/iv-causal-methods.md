# IV And Causal Methods

Use this long-term reference when the task involves endogeneity, causal interpretation, instruments, dynamic-panel IV, policy/treatment designs, DiD/event studies, or careful claim boundaries. Pair it with `panel-methods.md` for panel structure and `time-series-methods.md` for dynamic or nonstationary series.

## Table Of Contents

- Causal Framing
- IV And 2SLS
- Dynamic Panel IV
- Exogenous Covariates In Dynamic Panels
- Difference-In-Differences And Event Studies
- Panel Treatment Effects And Synthetic Counterfactuals
- Granger, VAR, Cointegration, And Causal Language
- Robustness And Validity Checks
- Writing Templates
- Claim Boundaries

## Causal Framing

Before using causal language, identify:

- Treatment or endogenous regressor.
- Outcome.
- Unit and time.
- Counterfactual comparison.
- Source of variation.
- Threat: omitted variables, reverse causality, simultaneity, selection, measurement error, anticipation, spillovers, nonstationarity, or common shocks.

Use causal claims only when an identification strategy addresses the main threat. Otherwise write association, prediction, dynamic relation, or long-run relation.

## IV And 2SLS

Use when a regressor is endogenous and a defensible instrument is available.

Structural equation:

```text
Y_i = beta X_i + W_i' gamma + u_i
```

First stage:

```text
X_i = pi Z_i + W_i' delta + v_i
```

Second stage:

```text
Y_i = beta X_hat_i + W_i' gamma + error_i
```

Core assumptions:

- Relevance: `Z_i` predicts the endogenous regressor conditional on controls.
- Exclusion: `Z_i` affects `Y_i` only through `X_i`.
- Independence/as-good-as-random assignment: `Z_i` is not correlated with unobserved determinants of `Y_i`.
- Monotonicity when interpreting LATE.

Methodology:

- Estimate the first stage and report instrument strength.
- Estimate the second stage using fitted endogenous variation.
- Cluster standard errors at the treatment, assignment, or sampling level when dependence is plausible.
- Use overidentification checks only as partial diagnostics; they do not prove exclusion.
- Match the strength diagnostic to the covariance assumptions. A conventional first-stage F and Stock–Yogo critical values belong to the homoskedastic Cragg–Donald setting; under heteroskedasticity or clustering, report a robust Kleibergen–Paap-type statistic or an appropriate effective-F diagnostic.
- For multiple endogenous regressors, report conditional first-stage diagnostics such as Sanderson–Windmeijer statistics rather than one omnibus F alone.
- When identification may be weak, report Anderson–Rubin or conditional likelihood-ratio confidence sets/tests where supported and use LIML or Fuller-type estimates as sensitivity checks. Do not apply a universal `F > 10` rule mechanically.

Report:

- State why OLS is likely biased.
- State the instrument, relevance channel, and exclusion restriction in words.
- Report first-stage coefficient and F-statistic or equivalent weak-instrument diagnostic.
- Report partial first-stage fit, excluded-instrument and endogenous-regressor counts, and the weak-identification-robust procedure used when conventional 2SLS inference is unreliable.
- Interpret IV as local to the variation induced by the instrument when appropriate.

## Dynamic Panel IV

Use when fixed effects and lagged dependent variables coexist.

Core model:

```text
Y_it = beta Y_{i,t-1} + alpha_i + epsilon_it
```

Differenced version:

```text
Delta Y_it = beta Delta Y_{i,t-1} + Delta epsilon_it
```

Why IV is needed:

- Differencing removes `alpha_i`.
- The differenced lagged dependent variable can remain correlated with the differenced error.
- Lagged levels or lagged differences can serve as instruments under assumptions on serial correlation and predeterminedness.

Lecture IV form:

```text
beta_hat_IV =
[sum_i sum_t (Y_{i,t-1} - Y_{i,t-2}) V_it]^{-1}
 sum_i sum_t (Y_it - Y_{i,t-1}) V_it
```

Common instruments:

```text
V_it = Y_{i,t-2}
V_it = Delta Y_{i,t-2}
```

Methodology:

- Difference the equation to remove fixed effects.
- Choose lagged levels or lagged differences as instruments.
- Check whether the instrument timing is valid under the assumed error process.
- Compare alternative lag depths and instrument sets.
- For Arellano-Bond-style GMM, stack all available moment conditions of the form `E[W_i' Delta u_i] = 0`, choose a weighting matrix, and keep instrument count controlled relative to `N`.
- Difference GMM uses lagged levels as instruments for transformed equations. System GMM additionally stacks level equations instrumented by lagged differences and therefore requires extra initial-condition or mean-stationarity restrictions; state and defend those restrictions rather than treating system GMM as automatically preferable.
- Report AR(1) and AR(2) tests in differenced residuals. First-order correlation is commonly induced by differencing, whereas second-order correlation threatens the usual lagged-level instruments.
- Report one-step robust inference and, when reporting two-step GMM, finite-sample-corrected two-step standard errors such as the Windmeijer correction. Uncorrected two-step standard errors are often downward biased in finite samples.
- Limit instrument proliferation with prespecified lag windows, collapsed instruments, or both. Report instrument count relative to the number of units and sensitivity to a smaller instrument set; a high Hansen p-value with many instruments is not reassuring by itself.
- For forward orthogonal deviations, transform each observation by subtracting the average of future observations; this can be useful in unbalanced panels and preserves orthogonality under the same underlying timing assumptions.
- For likelihood or QMLE dynamic panels, explicitly model the initial condition or use a conditional-mean approximation; otherwise likelihood estimates can be driven by unmodeled initial conditions.

Report:

- State the instrument set and timing.
- Explain relevance and exclusion/exogeneity.
- Report serial-correlation diagnostics in differenced residuals and whether lagged instruments remain valid.
- Report instrument count, lag windows, and any instrument-collapsing rule when using GMM.
- Report the transformation, one-step/two-step weighting choice, Windmeijer or other finite-sample covariance correction, AR(1)/AR(2), Hansen/Sargan diagnostics, and difference-in-Hansen tests for additional system-GMM moment subsets when relevant.
- Avoid saying IV "solves endogeneity"; write "under the maintained instrument validity assumptions."

## Exogenous Covariates In Dynamic Panels

Dynamic panel with exogenous covariates:

```text
Y_it = beta Y_{i,t-1} + delta' X_it + alpha_i + epsilon_it
```

Methodology:

- Difference to remove fixed effects.
- Instrument the differenced lagged dependent variable.
- Include differenced exogenous covariates directly only when their exogeneity assumptions are credible.
- Estimate the stacked parameter vector by IV-based OLS or the locally appropriate GMM variant.

Report:

- Separate assumptions for lagged outcomes and other regressors.
- Report robustness to alternative instruments and lag depth.

## Difference-In-Differences And Event Studies

Use when policy or treatment adoption creates treated and comparison groups over time.

Two-way fixed-effect DiD baseline:

```text
Y_it = alpha_i + gamma_t + beta Treat_i Post_t + X_it' delta + epsilon_it
```

Event-study form:

```text
Y_it = alpha_i + gamma_t + sum_{k != -1} beta_k 1[event_time_it = k] + X_it' delta + epsilon_it
```

Methodology:

- Define treated group, control group, treatment date, and event time.
- Check pre-trends with event-study leads.
- Use designs/estimators appropriate for staggered timing if treatment effects may be heterogeneous.
- Cluster at the treatment-assignment or unit level when shocks are serially correlated.

Report:

- State the parallel-trends assumption.
- Interpret pre-period estimates as design diagnostics, not definitive proof.
- Discuss anticipation, spillovers, and composition changes.

## Panel Treatment Effects And Synthetic Counterfactuals

Use when the paper evaluates a policy, intervention, shock, reform, or program using panel data and needs an explicit untreated counterfactual.

Potential-outcome setup:

```text
Individual effect: Delta_i = Y_i(1) - Y_i(0)
Observed outcome:  Y_i = D_i Y_i(1) + (1 - D_i) Y_i(0)
ATE: E[Y_i(1) - Y_i(0)]
TT/ATT: E[Y_i(1) - Y_i(0) | D_i = 1]
```

Core identification issue:

- The treated unit's untreated outcome is never observed after treatment.
- Selection can be on observables, unobservables, or both.
- Panel data help because pre-treatment histories reveal persistent unobserved heterogeneity and cross-sectional dependence.

Synthetic-counterfactual workflow:

1. Define treated unit(s), donor pool, treatment date, and pre/post periods.
2. Use only untreated donor units and pre-treatment outcomes/covariates to construct the counterfactual.
3. Fit a weighted or regression-based predictor for the treated unit's pre-treatment outcome path.
4. Predict the treated unit's post-treatment untreated outcome.
5. Estimate the treatment-effect path as actual minus counterfactual, then summarize ATT or average post-treatment effects.

Generic model:

```text
Y_1t(0) = f(Y_2t, ..., Y_Nt, X_t) + eta_t
Treatment effect at t: tau_t = Y_1t - Y_hat_1t(0)
Average post-treatment effect: tau_bar = average_t tau_t
```

Methodology:

- Treat the method as constructing a counterfactual, not as a black-box prediction exercise.
- Require strong pre-treatment fit; poor pre-treatment fit undermines post-treatment effects.
- Allow effect heterogeneity and time-varying treatment effects by reporting `tau_t`, not only one average.
- Use prediction uncertainty or placebo distributions to quantify uncertainty.
- Avoid donor contamination: controls must not be treated, indirectly affected, or mechanically tied to the outcome of the treated unit after treatment.

Report:

- Report donor pool, pre-treatment fit, treatment date, post-treatment window, and effect path.
- Plot actual versus synthetic counterfactual and the gap.
- Provide placebo tests, leave-one-out sensitivity, alternative donor pools, and alternative predictor windows.
- State whether results are interpreted as ATT for treated units, not a universal ATE.

## Granger, VAR, Cointegration, And Causal Language

These methods often use "causality" language in legacy econometrics but should be bounded in writing.

- Granger causality: predictive precedence; it does not establish structural causality.
- Reduced-form VAR: dynamic dependence among endogenous variables; causal interpretation requires structural identification.
- Cointegration: stable long-run relation among nonstationary variables; not a causal mechanism by itself.
- Threshold/time-varying models: heterogeneous or evolving associations unless paired with identification.

Recommended phrasing:

- "predicts future changes in"
- "is associated with"
- "the evidence is consistent with"
- "under the maintained identification assumptions"
- "the instrument-induced variation suggests"

Avoid:

- "proves"
- "fully identifies"
- "solves endogeneity"
- "confirms the causal effect" unless the design and assumptions have been explicitly defended.

## Modern Staggered DiD

Use this section when treatment adoption occurs in different periods across units and treatment effects may vary across cohorts or event time.

Problem:

- A single two-way fixed-effects coefficient can be a weighted average of many 2x2 comparisons.
- With staggered timing and heterogeneous effects, some comparisons use already-treated units as controls.
- Negative or unintuitive weights can make the TWFE coefficient hard to interpret.

Preferred workflow:

1. Define treatment cohorts by first treatment date.
2. Identify never-treated or not-yet-treated comparison groups.
3. Estimate group-time average treatment effects when possible.
4. Aggregate effects by cohort, calendar time, or event time only after checking support.
5. Plot event-time effects with pre-treatment coefficients.
6. Report whether the estimand is ATT for treated cohorts, not a universal ATE.

Recommended estimator families:

- Callaway and Sant'Anna style group-time ATT estimators.
- Sun and Abraham style interaction-weighted event studies.
- Imputation or stacked-event designs when the assumptions and sample structure fit.
- TWFE may be reported as a descriptive benchmark, but not as the only causal estimate under heterogeneous staggered adoption.

Checks:

- Cohort composition and treatment timing table.
- Number of treated and comparison units by event time.
- Pre-trend coefficients for each supported pre-period window.
- Sensitivity to comparison group: never-treated versus not-yet-treated.
- Sensitivity to anticipation windows and treatment reversals.
- Clustering at the treatment assignment level.

Writing template:

```text
Because treatment timing is staggered, I do not interpret a single TWFE coefficient as the main causal estimand. Instead, I estimate cohort-by-time treatment effects using [estimator], comparing treated cohorts with [never-treated/not-yet-treated] units. I then aggregate the supported group-time effects into an event-time profile. This approach targets the average effect for treated cohorts under parallel trends within the chosen comparison set and no anticipation before treatment.
```

## Robustness And Validity Checks

- OLS baseline: sign, magnitude, and known omitted-variable direction.
- IV: first-stage strength, reduced form, alternative instruments, exclusion discussion, weak-instrument sensitivity.
- Dynamic panel IV: alternative lag depths, instrument count, serial correlation, sensitivity to instrument set.
- DiD/event study: pre-trends, placebo dates, placebo groups, alternative windows, clustering, treatment-timing robustness.
- Staggered DiD: cohort support, not-yet-treated versus never-treated comparisons, anticipation windows, treatment reversals, and heterogeneity-robust estimators.
- Synthetic counterfactuals: pre-treatment fit, donor-pool sensitivity, placebo/permutation tests, leave-one-out checks, post-treatment contamination, alternative predictor windows.
- Panel FE causal claims: time-varying controls, unit trends, common shocks, cross-sectional dependence.
- Time-series causal claims: stationarity, lag order, reverse direction, structural restrictions, break sensitivity.

## Writing Templates

Empirical strategy paragraph:

```text
The baseline specification relates [outcome] to [main regressor] while absorbing [unit] and [time] fixed effects. This design compares changes within the same [unit] over time, net of common shocks. The identifying interpretation requires that, conditional on these controls, remaining changes in [main regressor] are not driven by unobserved time-varying determinants of [outcome].
```

IV paragraph:

```text
To address potential endogeneity in [X], I instrument [X] with [Z]. The relevance condition requires [Z] to shift [X], which is supported by the first-stage estimates. The exclusion restriction requires [Z] to affect [Y] only through [X], conditional on [controls/fixed effects]. Therefore, the IV estimate should be interpreted as the effect induced by the variation in [X] generated by [Z].
```

Dynamic panel paragraph:

```text
Because current [Y] depends on its lag and unit fixed effects, a within estimator may be biased. I difference the equation to remove fixed effects and use lagged [Y] as instruments for the differenced lagged dependent variable. The interpretation depends on the absence of serial correlation that would invalidate these lag instruments.
```

DiD paragraph:

```text
The difference-in-differences specification compares changes in [Y] for treated units before and after [policy] with contemporaneous changes among comparison units. The causal interpretation relies on parallel trends: absent the policy, treated and comparison units would have followed similar outcome trajectories.
```

Synthetic-counterfactual paragraph:

```text
I construct the untreated counterfactual for [treated unit] using the pre-treatment relationship between [treated outcome] and outcomes/covariates from untreated donor units. The estimated treatment effect at each post-treatment date is the gap between the observed outcome and the predicted untreated counterfactual. This design requires that the donor pool is not affected by the intervention and that the pre-treatment fit captures the relevant untreated outcome dynamics.
```

## Claim Boundaries

- Use "effect" only after stating the identification strategy and assumptions.
- Use "association" for fixed-effect, VAR, threshold, or nonparametric estimates without causal design.
- Use "predictive content" for Granger causality.
- Use "long-run relation" for cointegration.
- Use "instrument-induced variation" for IV.
- Use "treatment effect under parallel trends" for DiD/event studies.
- Use "group-time ATT under staggered-adoption assumptions" for modern staggered DiD.
- Use "gap relative to the constructed untreated counterfactual" for synthetic-counterfactual designs.

## See Also

- [Method Selection](method-selection.md)
- [Panel Methods](panel-methods.md)
- [RDD and Matching Methods](rdd-matching-methods.md)
- [Time-Series Methods](time-series-methods.md)
