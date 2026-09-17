# RDD And Matching Methods

Use this reference for regression discontinuity designs, propensity-score methods, inverse probability weighting, matching-based robustness checks, and combined PSM-DiD or IPW-DiD designs.

## Regression Discontinuity Design

Use RDD when treatment assignment changes discontinuously at a known cutoff in a running variable.

Sharp RDD:

```text
D_i = I(R_i >= c)
Y_i = alpha + tau D_i
    + beta_- (R_i - c)(1-D_i) + beta_+ (R_i - c)D_i + epsilon_i
```

Equivalently, use separate local functions on the two sides of the cutoff. The interaction or side-specific functions are essential: imposing a common slope through the cutoff can turn curvature into a false discontinuity.

Fuzzy RDD:

```text
First stage: D_i = pi_0 + pi_1 Z_i + g_-(R_i-c)(1-Z_i) + g_+(R_i-c)Z_i + v_i
Reduced form: Y_i = gamma_0 + gamma_1 Z_i + f_-(R_i-c)(1-Z_i) + f_+(R_i-c)Z_i + u_i
Wald estimand: tau_FRD = gamma_1 / pi_1
```

where `R_i` is the running variable, `c` is the cutoff, and `Z_i = I(R_i >= c)` is cutoff eligibility.

### Design Checks

- Confirm the cutoff rule is institutional, not chosen after inspecting outcomes.
- Plot treatment probability against the running variable.
- Plot outcome means around the cutoff with transparent binning.
- Check covariate continuity at the cutoff.
- Test for manipulation or sorting in the running variable.
- Report bandwidth selection and sensitivity to narrower/wider bandwidths.
- Prefer local linear specifications near the cutoff; avoid high-order global polynomials as the main result.
- Use robust bias-corrected confidence intervals when available.
- Check placebo cutoffs and outcomes when credible.

### Interpretation

- Sharp RDD estimates the local treatment effect at the cutoff.
- Fuzzy RDD estimates a local effect for compliers whose treatment status changes at the cutoff.
- Do not generalize to units far from the cutoff without evidence.

RDD writing template:

```text
The assignment rule creates a discontinuity in treatment probability at [cutoff] of [running variable]. I estimate local linear regressions on both sides of the cutoff and interpret the discontinuity in [outcome] as a local treatment effect for observations near the threshold. This interpretation requires that potential outcomes and predetermined covariates evolve smoothly through the cutoff and that units cannot precisely manipulate the running variable.
```

## Propensity Score Matching

Use matching when treatment is not randomized but selection on observables is a defensible approximation. Treat matching as design support, not as automatic causal identification.

Propensity score:

```text
p(X_i) = Pr(D_i = 1 | X_i)
```

ATT after matching:

```text
ATT = E[Y_i(1) - Y_j(0) | D_i = 1, j in matched controls]
```

### Matching Workflow

1. Define treatment before looking at outcomes.
2. Choose pre-treatment covariates that jointly affect treatment and outcome.
3. Estimate propensity scores with logit/probit or flexible models.
4. Check common support and trim unsupported observations.
5. Match with nearest neighbor, radius/caliper, kernel, or stratification.
6. Report balance before and after matching using standardized mean differences.
7. Estimate treatment effects on the matched sample.
8. Run sensitivity checks for caliper, matching ratio, replacement, and covariate set.

### Limits

- Matching only addresses observed confounding.
- Do not match on post-treatment variables, mechanisms, or colliders.
- Good balance is necessary but not sufficient for causal interpretation.
- Report the estimand clearly: usually ATT for the matched treated population.

## IPW And Doubly Robust Designs

Use inverse probability weighting when the goal is to reweight the comparison group to resemble the target population.

ATE weights:

```text
w_i = D_i / p(X_i) + (1 - D_i) / [1 - p(X_i)]
```

ATT weights:

```text
w_i = D_i + (1 - D_i) p(X_i) / [1 - p(X_i)]
```

Checks:

- Inspect propensity-score overlap.
- Stabilize or trim extreme weights.
- Report effective sample size when weights are highly variable.
- Use robust or bootstrap inference matched to the weighting procedure.
- Consider doubly robust estimators when both outcome and treatment models can be specified.

## PSM-DiD And IPW-DiD

Use combined designs when treatment and comparison groups differ observably before treatment and panel or repeated outcome data support a difference-in-differences comparison.

Workflow:

1. Estimate propensity scores using pre-treatment covariates only.
2. Match or weight treated and comparison units.
3. Check pre-treatment covariate balance and outcome trends.
4. Estimate DiD/event-study models on the matched or weighted sample.
5. Report whether results change relative to unmatched/unweighted DiD.

Interpretation:

- Matching/weighting improves comparability on observables.
- DiD still requires parallel trends after reweighting or matching.
- The estimand applies to the overlap population, not necessarily the original full sample.

## Reporting Checklist

- Treatment definition and timing.
- Covariate set and why each covariate is pre-treatment.
- Common support or overlap diagnostics.
- Balance table before and after matching/weighting.
- Main estimand: ATE, ATT, local RDD effect, fuzzy RDD complier effect, or overlap-population effect.
- Sensitivity to bandwidth, caliper, weights, trimming, and matching method.
- Explicit statement that unobserved confounding remains a threat unless the design adds a credible source of exogenous variation.

## See Also

- [Method Selection](method-selection.md)
- [Panel Methods](panel-methods.md)
- [IV and Causal Methods](iv-causal-methods.md)
