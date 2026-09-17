# Panel Methods

Use this long-term reference when observations have cross-sectional and time dimensions, including country-year, firm-year, person-period, region-year, and market-period datasets. Pair it with `iv-causal-methods.md` when lagged outcomes, endogenous regressors, instruments, DiD, or explicit causal claims are involved.

## Table Of Contents

- Panel Data Setup
- Fixed Effects And Random Effects
- Static Fixed-Effect Estimators
- Random Effects, Variance Components, And GLS
- FE Versus RE, Mundlak, And Hausman
- Balanced And Unbalanced Panels
- Cross-Sectional Dependence
- Random Coefficient And Heterogeneous Slopes
- Dynamic Panels
- Panel Nonstationarity And Cointegration
- Nonlinear Trends And Polynomial Panels
- Binary Panel Models
- Time-Varying And Trending Panels
- Health Expenditure Application Template
- Method-Matched Robustness
- Claim Boundaries

## Panel Data Setup

Use panel methods when both unit and time variation matter.

Core families:

```text
Homogeneous panel: Y_it = X_it' beta + e_it
Heterogeneous panel: Y_it = X_it' beta_i + e_it
Dynamic panel: Y_it = beta_0' (Y_{i,t-1}, ..., Y_{i,t-d}) + e_it
Binary panel: Y_it = I[X_it' beta + e_it >= 0]
Nonlinear homogeneous panel:
Y_it = alpha + sum beta_j X_jit + sum gamma_kl X_jit X_kit + e_it
```

Methodology:

- Use common slopes when the paper's target is an average association or elasticity.
- Use heterogeneous slopes or random coefficients when unit-specific responses are substantive.
- Use dynamic panels when lagged outcomes are part of the economic process.
- Use binary panel models when the outcome is an indicator.
- Include nonlinear or interaction terms when the economic response is curved or depends on covariate levels.

Report:

- Define the unit `i`, time `t`, sample window, balanced/unbalanced status, and outcome.
- Explain why panel variation is needed rather than pooled cross-sections or separate time series.

## Fixed Effects And Random Effects

Core fixed-effect model:

```text
Y_it = X_it' beta + alpha_i + e_it
```

Two-way fixed-effect style model:

```text
Y_it = X_it' beta + alpha_i + gamma_t + epsilon_it
```

Decision rule:

- Use fixed effects when unobserved unit heterogeneity may be correlated with regressors.
- Use random effects only when unit effects are plausibly uncorrelated with regressors.
- Add time effects when common shocks, macro cycles, or aggregate trends affect all units.

Within estimation:

- Demean by unit to eliminate `alpha_i`.
- Demean by unit and time when using two-way effects.
- Estimate `beta` by OLS on transformed variables.
- For heterogeneous slopes, estimate within-unit slopes after removing unit effects.

Report:

- State FE or RE rationale.
- Report whether time effects are included.
- Avoid presenting fixed effects as a full endogeneity solution.

## Static Fixed-Effect Estimators

Use when the outcome depends on observed regressors and unit-specific omitted factors that may be correlated with regressors.

One-way fixed effects:

```text
Y_it = alpha_i + X_it' beta + u_it
```

Equivalent estimators:

- Least-squares dummy-variable estimator: include one unit dummy per unit, subject to the usual normalization.
- Within/covariance estimator: premultiply each unit's equation by `Q = I_T - (1/T) ee'` and run OLS on demeaned data.
- The within estimator identifies `beta` from deviations around each unit's time mean and does not estimate coefficients on time-invariant regressors.

Estimator logic:

```text
beta_hat_within =
[sum_i sum_t (X_it - X_i_bar)'(X_it - X_i_bar)]^{-1}
 sum_i sum_t (X_it - X_i_bar)'(Y_it - Y_i_bar)
```

Report:

- State whether the estimator is LSDV or within; they estimate the same slope under the same specification.
- Explain that FE uses within-unit variation and absorbs all time-invariant unit heterogeneity.
- Note that intercept/unit-effect estimates are incidental to the main slope estimate when `N` is large and `T` is short.

## Random Effects, Variance Components, And GLS

Use when unit effects are treated as draws from a population and are plausibly uncorrelated with regressors.

Variance-components model:

```text
Y_it = alpha + X_it' beta + a_i + u_it
E(a_i | X_i) = 0
E(u_it | X_i, a_i) = 0
Var(a_i) = sigma_a^2
Var(u_it) = sigma_u^2
```

Methodology:

- Estimate variance components for the unit effect and idiosyncratic error.
- Use feasible GLS or quasi-demeaning, subtracting a fraction of each unit mean from `Y_it` and `X_it`.
- Interpret RE GLS as an intermediate weighted combination of within variation and between variation.
- When the RE weight collapses toward the within estimator, between variation is effectively down-weighted; when it collapses toward pooled OLS, unit effects matter less.

Report:

- State the assumed exogeneity of `a_i` with respect to regressors.
- Report variance components or intra-class correlation when they help explain the RE choice.
- Do not use RE only because it is more efficient; efficiency is relevant only after the RE exogeneity assumption is credible.

## FE Versus RE, Mundlak, And Hausman

Use this section when choosing between fixed effects and random effects, or when the paper needs a formal bridge between them.

Decision logic:

- FE allows arbitrary correlation between `alpha_i` and time-varying regressors.
- RE is more parsimonious and can estimate time-invariant regressors, but requires no correlation between unit effects and regressors.
- The key empirical issue is not only efficiency; it is whether the model treats unit heterogeneity as conditional on the sample or drawn from a population.

Mundlak correlated-random-effects formulation:

```text
alpha_i = X_i_bar' theta + omega_i
Y_it = X_it' beta + X_i_bar' theta + omega_i + u_it
```

Methodology:

- Add unit-level means of time-varying regressors to the RE specification.
- Test whether the coefficients on unit means are jointly zero.
- If the unit-mean coefficients are nonzero, regressors are correlated with unit effects and plain RE is misspecified.
- Use Mundlak as a transparent way to preserve time-invariant regressors while modeling correlated unit effects.

Hausman logic:

```text
H = (beta_FE - beta_RE)' [Var(beta_FE) - Var(beta_RE)]^{-1} (beta_FE - beta_RE)
```

Methodology:

- Compare an estimator consistent under both null and alternative, usually FE, with an estimator efficient under the RE null, usually RE.
- Under the null, both are consistent and coefficient differences should be small.
- Under the alternative, RE is inconsistent and FE remains the safer slope estimator.

Report:

- If using RE, state the exogeneity assumption and whether Mundlak/Hausman evidence supports it.
- If using FE, state what is sacrificed: time-invariant regressors and between-unit interpretation.
- If Hausman covariance differences are not positive definite or the test is unstable, prefer substantive exogeneity reasoning and Mundlak-style diagnostics over mechanical decisions.

## Balanced And Unbalanced Panels

Use explicit handling when units have unequal observation counts.

Methodology:

- For balanced panels, each unit has the same `T`.
- For unbalanced panels, use each unit's available `T_i` in demeaning, sums, and diagnostics.
- Check whether missingness is random or related to outcomes/treatments.
- Avoid silently dropping many observations without describing the sample change.

Report:

- State the number of units, time periods, and observations.
- Report whether the main sample is balanced or unbalanced.
- If a balanced subsample is used for robustness, describe what is lost.

## Cross-Sectional Dependence

Use when units may share common shocks, supply chains, regional spillovers, or macro trends.

Methodology:

- Inspect pairwise residual correlations after fitting the baseline model.
- Use tests based on summed pairwise residual correlations when `N` panels may not be independent.
- Cluster at the level of independent assignment or sampling. Unit clustering permits arbitrary heteroskedasticity and serial dependence within units but does not address common shocks across units.
- Use two-way or multiway clustering when errors may co-move along more than one non-nested dimension, such as firm and calendar time. Require enough independent clusters in every dimension and inspect sparse intersection cells; a large observation count does not replace cluster count.
- With few clusters, conventional cluster-robust asymptotics can over-reject. Report cluster counts and balance, and use a justified CR2/CR3-type correction, randomization inference, or wild-cluster bootstrap-t procedure. For the bootstrap, state whether the null is imposed, the weight distribution, repetitions, and the cluster level.
- Add time effects or common factors when common shocks affect outcomes. Changing the covariance estimator alone does not repair slope inconsistency from omitted common factors correlated with regressors.
- Use Driscoll–Kraay-type inference only when the time dimension is sufficiently long for its cross-sectional-and-serial-dependence asymptotics. Report kernel and bandwidth choices; do not present it as a remedy for short panels or latent-factor endogeneity.

Report:

- State whether common shocks are controlled.
- Report clustering dimensions, cluster counts, finite-sample corrections, and why they match the assignment and dependence structure.
- Avoid overconfident standard errors when cross-sectional dependence is plausible.

## Random Coefficient And Heterogeneous Slopes

Use when the distribution of unit-specific effects or elasticities is central.

Core model:

```text
Y_it = X_it' beta_i + alpha_i + epsilon_it
```

Methodology:

- Estimate each `beta_i` by within-unit OLS after eliminating `alpha_i`.
- Estimate the average coefficient by averaging unit-level slope estimates.
- Avoid multiple intercept-like terms in addition to `alpha_i`.
- When variables are log-transformed, interpret `beta_i` as unit-specific elasticity.

Report:

- Report the distribution, quantiles, range, or plots of `beta_i`, not only the average.
- Compare heterogeneous estimates with the homogeneous fixed-effect model.

## Dynamic Panels

Use when the lagged dependent variable is economically necessary.

Core model:

```text
Y_it = beta Y_{i,t-1} + alpha_i + epsilon_it
```

Differenced form:

```text
Delta Y_it = beta Delta Y_{i,t-1} + Delta epsilon_it
```

Methodology:

- Recognize that demeaning or differencing with lagged outcomes creates endogeneity because transformed lagged outcomes are correlated with transformed errors.
- Use differenced IV, Arellano-Bond-style GMM, forward orthogonal deviations, QMLE, or conditional-mean approaches depending on assumptions and panel dimensions; see `iv-causal-methods.md` for IV/GMM details.
- Include exogenous covariates only under explicit exogeneity assumptions.

Estimator menu:

- Differenced IV: difference the equation to remove `alpha_i`, then instrument `Delta Y_{i,t-1}` with valid lagged levels such as `Y_{i,t-2}` under no serial correlation in the original error.
- Arellano-Bond GMM: stack differenced equations and exploit multiple lag moment conditions, weighting the sample moments by a suitable matrix.
- Forward orthogonal deviations: transform each observation by subtracting the average of future observations, preserving sample size in unbalanced panels and keeping transformed errors orthogonal under suitable conditions.
- Random-effects likelihood/QMLE: model the covariance structure implied by the unit effect and lagged outcome; efficient when distribution and initial-condition assumptions are credible.
- Conditional mean approach: model the conditional mean of the individual effect and initial observation as functions of regressor histories, then estimate the resulting level system by GLS/QMLE.

Report:

- State why dynamics are needed.
- State the estimator and instrument set.
- State how the initial condition `Y_i0` is handled when using likelihood or conditional-mean approaches.
- Report serial-correlation checks and instrument-count discipline when using GMM.
- Avoid naive fixed-effect OLS as the final dynamic-panel estimator unless the bias is addressed or justified as negligible.

## Panel Nonstationarity And Cointegration

Use when panel variables are persistent and may contain unit roots.

Dynamic panel unit-root logic:

```text
Levels AR form:
Y_it = mu_i + delta_i t + phi_i Y_{i,t-1} + epsilon_it
H0: phi_i = 1

Equivalent ADF form with optional augmenting lags:
Delta Y_it = mu_i + delta_i t + rho_i Y_{i,t-1}
             + sum_j gamma_ij Delta Y_{i,t-j} + epsilon_it
rho_i = phi_i - 1; H0: rho_i = 0
```

Panel cointegration:

```text
Y_it = X_it' beta + alpha_i + epsilon_it
Panel cointegration: Y_it - X_it' beta is stationary even if Y_it and X_it are nonstationary.
```

Methodology:

- Estimate unit-specific persistence parameters when heterogeneity matters.
- Match the null to the equation: test `phi_i=1` in the levels AR form or `rho_i=0` in the ADF form. Do not test a coefficient on `Delta Y_{i,t-1}` against one.
- Choose deterministic terms and augmenting lags before testing, and use panel-test-specific nonstandard critical values or p-values rather than ordinary normal or t critical values.
- State whether the panel test imposes a common persistence parameter or allows heterogeneous alternatives, and address cross-sectional dependence with an appropriate second-generation procedure when common factors are plausible.
- Estimate fixed-effect cointegrating relations, then test residual persistence.

Report:

- Separate unit-root evidence from cointegration evidence.
- Discuss whether stationarity/cointegration appears homogeneous across units.
- Do not interpret panel cointegration as causal proof.

## Nonlinear Trends And Polynomial Panels

Use when time trends are substantive or nonlinear trends are needed as controls.

Linear trend panel:

```text
Y_it = mu + beta t + e_it
e_it = alpha_i + epsilon_it
```

Nonlinear trend panel:

```text
Y_it = X_it' beta + g_t + alpha_i + epsilon_it
```

Examples:

```text
Polynomial trend: theta_0 + theta_1 t + ... + theta_p t^p
Periodic trend: sin(2 pi t)
```

Methodology:

- Use time effects or demeaning when the trend is a nuisance control.
- Estimate the trend explicitly when it is the substantive object.
- Choose polynomial order conservatively.
- Plot the trend when it carries the empirical result.

## Binary Panel Models

Use when the dependent variable is an indicator.

Latent-index setup:

```text
Y_it = I[X_it' beta_i + alpha_i - epsilon_it >= 0]
P(Y_it = 1 | X_it, alpha_i) = F(X_it' beta_i + alpha_i)
```

Methodology:

- Choose homogeneous `beta` or heterogeneous `beta_i`.
- Specify a link/CDF such as logistic or normal.
- Construct the likelihood from Bernoulli probabilities.
- Estimate fixed effects and slopes by maximum likelihood.

Report:

- Interpret marginal effects or probability changes, not raw coefficients alone.
- Discuss fixed-effect complications when `T` is short.

## Time-Varying And Trending Panels

Use when panel coefficients evolve smoothly over time and the evolution is central.

Nonparametric time-varying coefficient panel:

```text
Y_it = f_t + X_it' beta_t + alpha_i + e_it
f_t = f(t/T), beta_t = beta(t/T)
sum_i alpha_i = 0
```

Local linear approximation:

```text
Y_it approx X_it^*' beta^*(tau)
      + X_it^*' beta^{*'}(tau) (tau_t - tau)
      + alpha_i + e_it
```

Semiparametric trending panel:

```text
Y_it = X_it' beta + f_t + alpha_i + e_it
```

Factor-augmented time-varying panel:

```text
y_it = x_it' beta_i(tau_t) + lambda_i' F_t + epsilon_it
x_it = g_i(tau_t) + gamma_i' G_t + eta_it
```

Methodology:

- Impose an identification restriction on fixed effects, such as `sum_i alpha_i = 0`.
- Estimate coefficient paths by local linear dummy-variable estimation.
- Use kernel weights around each `tau`.
- For trending panels, profile out the smooth trend and then estimate constant slopes.
- For factor-augmented panels, estimate common factors/loadings by PCA or iterative least squares, then estimate time-varying coefficients conditional on factors.

Report:

- Make coefficient paths the central empirical object.
- Report bandwidth and sensitivity.
- State whether fixed effects, common trends, or factors are controlled.

## Health Expenditure Application Template

Use as a reusable applied panel-paper template when the topic resembles health expenditure, macro panels, country panels, or expenditure elasticities.

Baseline individual fixed-effect model:

```text
lnHE_it = beta_1 lnGDP_it + beta_2 pop65_it
        + beta_3 pop14_it + beta_4 public_it + alpha_i + u_it
```

Methodology:

- Inspect the probabilistic structure and persistence of regressors.
- Run unit-root or panel unit-root checks when variables are persistent.
- Model A: homogeneous fixed-effect panel slope by within OLS.
- Model B: heterogeneous country-specific slopes by within OLS.
- Compare panel and time-series formulations:

```text
Panel:      Y_it = alpha_i + X_it' beta_i + epsilon_it
Time series: y_t = alpha + x_t' beta + epsilon_t
```

Report:

- Report homogeneous and heterogeneous estimates separately.
- Plot country-specific intercepts or slopes when heterogeneity matters.
- Interpret GDP elasticity carefully and avoid causal wording without an identification design.

## Method-Matched Robustness

- FE/RE panels: fixed versus random effects rationale, time effects, clustering, cross-sectional dependence.
- Mundlak/Hausman: correlated-random-effects terms, Hausman statistic, and substantive exogeneity reasoning.
- Heterogeneous slopes: distribution of unit estimates and comparison with homogeneous slopes.
- Dynamic panels: alternative instruments, lag depth, instrument count, first-difference versus forward-orthogonal-deviation transformation, QMLE versus GMM sensitivity, finite-sample sensitivity, serial correlation checks.
- Nonstationary panels: panel unit-root alternatives and residual cointegration checks.
- Binary panels: link function, marginal effects, fixed-effect treatment.
- Panel VAR: lag order, stability, impulse-response uncertainty, ordering or structural restrictions, and cross-sectional dependence.
- Spatial panels: spatial weights definition, alternative weights, spatial spillover interpretation, and direct/indirect effect decomposition.
- Time-varying panels: bandwidth sensitivity, coefficient-path confidence bands, common-factor controls.

## Claim Boundaries

- Fixed effects control time-invariant unit heterogeneity, not simultaneity or time-varying omitted variables.
- Random effects require uncorrelated unit effects and regressors.
- Dynamic panel estimates depend on valid instruments and lag structure.
- Mundlak and Hausman diagnostics test compatibility with RE assumptions; they do not create exogeneity.
- Time-varying panel models show evolving associations unless paired with credible identification.
- Panel cointegration indicates a stable long-run relation, not causality.

## Panel VAR

Use when multiple panel variables are jointly endogenous and the research question concerns dynamic feedback across variables.

Basic PVAR:

```text
y_it = A_1 y_{i,t-1} + ... + A_p y_{i,t-p} + alpha_i + lambda_t + epsilon_it
```

Workflow:

1. Define the endogenous variable vector before estimating.
2. Choose lag order using information criteria and substantive timing.
3. Remove fixed effects with an appropriate transformation.
4. Estimate using GMM or bias-corrected approaches when `T` is short.
5. Check stability of the companion matrix.
6. Report impulse responses with confidence intervals.
7. Explain identification assumptions if interpreting shocks structurally.

Writing boundary:

- Reduced-form PVAR shows dynamic association and feedback.
- Causal shock interpretation requires ordering restrictions, external instruments, sign restrictions, or another identification strategy.

## Spatial Panel Models

Use when outcomes or shocks spill across geographic, product, firm-network, or market-neighbor units.

Spatial lag panel:

```text
Y_it = rho W Y_it + X_it' beta + alpha_i + lambda_t + epsilon_it
```

Spatial error panel:

```text
Y_it = X_it' beta + alpha_i + lambda_t + u_it
u_it = rho W u_it + epsilon_it
```

Spatial Durbin panel:

```text
Y_it = rho W Y_it + X_it' beta + W X_it' theta + alpha_i + lambda_t + epsilon_it
```

Workflow:

1. Justify the spatial weights matrix `W` before seeing results.
2. Row-standardize or otherwise normalize `W` transparently.
3. Test or motivate spatial dependence.
4. Include unit and time effects when panel structure supports them.
5. Report direct, indirect, and total effects rather than only raw coefficients when spatial feedback is present.
6. Test sensitivity to alternative plausible weights matrices.

Writing boundary:

- Spatial correlation does not by itself establish spillover causality.
- The definition of neighbors is part of the identifying argument and must be defensible.

## See Also

- [Method Selection](method-selection.md)
- [IV and Causal Methods](iv-causal-methods.md)
- [RDD and Matching Methods](rdd-matching-methods.md)
