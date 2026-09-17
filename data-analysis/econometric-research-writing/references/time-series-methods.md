# Time-Series Methods

Use this long-term reference when the task involves a single aggregate series, multiple interacting time series, nonstationarity, thresholds, nonlinear dynamics, time-varying coefficients, or forecasting. Pair it with `method-selection.md` for model choice and `empirical-workflow.md` for execution and reporting.

## Table Of Contents

- Linear AR Estimation
- Unit Root And Nonstationarity
- Threshold And Structural Change
- Kernel And Nonparametric Regression
- Cointegration
- Granger Predictive Causality
- VAR Models
- Time-Varying VAR And Coefficients
- Dynamic Wild Bootstrap
- Semiparametric And Localized Neural Networks
- Method-Matched Robustness
- Claim Boundaries

## Linear AR Estimation

Use for a stationary single series, forecasting baseline, or benchmark before threshold, nonlinear, VAR, or nonstationary extensions.

Core equations:

```text
AR(1): X_t = phi_1 X_{t-1} + Z_t
AR(p): X_t - phi_1 X_{t-1} - ... - phi_p X_{t-p} = Z_t
```

Methodology:

- Estimate AR coefficients by OLS, minimizing sample squared one-step prediction errors.
- For AR(1), use the lagged cross-product over lagged squares estimator.
- Estimate innovation variance from the residual sum of squares.
- For AR(p), use Yule-Walker equations by multiplying the AR equation by lagged values and solving autocovariance moments.
- Use maximum likelihood when a full innovation distribution is imposed; under independent Gaussian innovations, simple AR ML coincides with OLS for coefficients.

Report:

- State the stationarity assumption.
- Report order selection, residual diagnostics, and innovation variance.
- Do not use a linear AR model as the final method when the research question is about regimes, parameter instability, or nonstationarity.

## Unit Root And Nonstationarity

Use before estimating models in levels when persistence, stochastic trends, or macro/financial variables are plausible.

DF/ADF logic:

```text
y_t = rho y_{t-1} + u_t
Delta y_t = gamma y_{t-1} + u_t, gamma = rho - 1
H0: gamma = 0  (unit root / nonstationary)
H1: gamma < 0  (stationary)
```

Methodology:

- Estimate the differenced regression by OLS.
- Use the t-statistic for `gamma`, recognizing that the null distribution is non-standard.
- Add lagged differences for ADF when residual serial correlation is likely.
- Use PP tests for non-i.i.d. errors and KPSS as a complementary stationarity-null test.
- Include no deterministic term, intercept, or intercept plus trend according to the data-generating story.

Report:

- Report the deterministic specification.
- Distinguish trend stationarity from difference stationarity.
- Phrase non-rejection carefully: "evidence consistent with nonstationarity," not proof of a unit root.

## Threshold And Structural Change

Use when dynamics or covariate effects differ across regimes, thresholds, or structural break periods.

Core model:

```text
y_t = x_t' beta_1 I[z_t in A] + x_t' beta_2 I[z_t in B] + e_t
B = A^c
```

Common cases:

- `x_t = y_{t-1}` and `z_t = y_{t-1}` for threshold autoregression.
- External `z_t` for economically defined regimes.
- `z_t = t` for structural change or time split.

Methodology:

- For a fixed threshold, estimate regime coefficients by OLS inside each regime.
- If the threshold is unknown, search candidate thresholds and minimize residual sum of squares.
- Use trimming rules to avoid very small regimes.
- For threshold AR, use differenced forms when discussing persistence or unit-root behavior.

Report:

- Define the threshold variable and economic interpretation of regimes.
- Report search range, trimming rule, and regime sizes.
- Treat threshold evidence as conditional dynamics, not causal identification.

## Kernel And Nonparametric Regression

Use when a parametric conditional mean, variance, or density is too restrictive and sample size supports local estimation.

Density and conditional density:

```text
f_hat(y, x) = average product kernels in y and x
f_hat(y | x) = f_hat(y, x) / f_hat(x)
```

Conditional mean and variance:

```text
m_hat(x) = sum K((x_t - x)/b) y_t / sum K((x_t - x)/b)
sigma_hat^2(x) = weighted residual variance around m_hat(x)
```

Methodology:

- Choose kernel and bandwidth.
- Estimate local means, variances, or densities through kernel-weighted averages.
- For smooth time trends, set `x_t = t` or `tau_t = t/T`.
- Always run bandwidth sensitivity because the shape can depend on smoothing.

Report:

- State kernel, bandwidth, and effective local sample size.
- Discuss boundary behavior.
- Use plots and confidence bands when the estimated function is central.

## Cointegration

Use when multiple series appear nonstationary but may share a stable long-run relation.

Residual-based workflow:

```text
c_t = alpha + beta i_t + u_t
or after detrending:
u_t = c_t^* - alpha - beta i_t^*
```

Methodology:

- Motivate or test nonstationarity in individual series.
- Estimate the long-run relation by OLS.
- Test residuals for stationarity using residual unit-root checks.
- Use Engle–Granger or residual-cointegration critical values, not ordinary DF/ADF critical values, because the residual is generated by an estimated first-stage relation.
- For Johansen trace or maximum-eigenvalue rank tests, match critical values to the deterministic specification and lag structure; consider small-sample corrections or bootstrap rank inference when supported.
- For ARDL bounds testing, use case-specific lower and upper critical bounds and treat statistics between them as inconclusive. Standard bounds procedures do not permit `I(2)` variables.
- If residuals are stationary while variables are nonstationary, interpret the result as evidence of a long-run equilibrium relation.

Report:

- Separate individual series unit-root evidence from residual stationarity evidence.
- Name the cointegration test, deterministic terms, lag choice, and critical-value family used.
- Do not treat cointegration alone as structural causality.

## Granger Predictive Causality

Use for predictive precedence, not structural causality.

Core comparison:

```text
Restricted AR: y_t = rho_0 + rho_1 y_{t-1} + ... + rho_p y_{t-p} + e_t
Augmented AR:  add gamma_1 x_{t-1} + ... + gamma_q x_{t-q}
```

Methodology:

- Fit the restricted autoregression for `y_t`.
- Fit the augmented model with lagged `x_t`.
- Test whether lagged `x_t` coefficients jointly add predictive information.
- If feedback is plausible, test both directions.

Report:

- Say "`x` Granger-causes `y`" only in the predictive sense.
- Report lag choices and joint significance tests.

## VAR Models

Use for multiple endogenous time series that interact dynamically.

Core model:

```text
Y_t = nu + A_1 Y_{t-1} + ... + A_p Y_{t-p} + epsilon_t
epsilon_t is vector white noise with covariance Sigma_epsilon
```

Methodology:

- Specify lag order `p`.
- Estimate by multivariate least squares or equation-by-equation OLS.
- Check stability using roots of `det(I_K - A_1 z - ... - A_p z^p) = 0`; stability requires roots outside the unit circle.
- For stable VARs, use the infinite MA representation for propagation and forecasting.
- Select lag order using residual diagnostics, residual ACF, Ljung-Box tests, and information criteria.

Report:

- Report variables, lag order, stability, and residual diagnostics.
- Emphasize forecasting and dynamic dependence unless structural restrictions are justified.
- Avoid treating reduced-form VAR coefficients as structural mechanisms.

## Time-Varying VAR And Coefficients

Use when coefficients evolve smoothly over time.

Univariate time-varying regression:

```text
y_t = X_{t-1}' beta_t + e_t
```

TV-VAR:

```text
y_t = a(tau_t) + sum_{j=1}^p A_j(tau_t) y_{t-j} + eta_t
tau_t = t/T
```

Local constant TV-VAR estimator:

```text
vec[A_hat(tau)] =
[sum Z_{s-1} Z_{s-1}' K_h(tau_s - tau)]^{-1}
 sum Z_{t-1} y_t K_h(tau_t - tau)
```

Methodology:

- Rewrite the model as local regression in normalized time `tau`.
- Estimate coefficient matrices with kernel weights at each time point.
- Estimate local innovation covariance from weighted residuals.
- Test coefficient constancy with restrictions such as `C beta(tau) = c`.
- Use integrated weighted squared deviation statistics for constancy tests.
- Use simulation-assisted or dynamic wild bootstrap inference when finite-sample inference is fragile.

Report:

- Plot coefficient paths with uncertainty bands.
- Report bandwidth and lag choices.
- Interpret paths as evolving associations or transmission patterns unless a structural design is added.

## Dynamic Wild Bootstrap

Use when nonparametric smoothing and time dependence make analytic inference unreliable.

Methodology:

- Estimate the smooth mean or coefficient function, often with an over-smoothing bandwidth.
- Obtain residuals.
- Generate bootstrap residuals by multiplying residuals by a dependent wild process with mean zero, unit variance, and serial dependence controlled by a kernel/tuning parameter.
- Re-estimate the smooth function on bootstrap samples.
- Use bootstrap quantiles for confidence intervals or test statistics.

Report:

- State bootstrap repetitions, bandwidths, and dependence tuning.
- Present bootstrap intervals as finite-sample support, not exact proof.

## Semiparametric And Localized Neural Networks

Use for flexible nonlinear response surfaces or high-dimensional predictors when a report needs more than a parametric regression.

Partially linear model:

```text
y = alpha z + g(x) + epsilon
z = I(m(x) - eta >= 0)
```

Residualized estimator:

```text
y_t - g1_hat(x_t) approx (z_t - g2_hat(x_t)) alpha + epsilon_t
alpha_hat = [sum z_tilde^2]^{-1} sum z_tilde y_tilde
```

Localized neural network:

```text
y_t = g(x_t) + epsilon_t
```

Methodology:

- Estimate nuisance functions `E[y|x]` and `E[z|x]`.
- Residualize `y` and `z`, then estimate the low-dimensional parameter by OLS on residuals.
- For localized neural networks, partition the covariate domain into local cubes and approximate `g(x)` with local shallow-network components.
- Use out-of-sample performance, RMSE, coverage, or simulation evidence for validation.

Report:

- Emphasize nonlinear prediction or flexible association.
- Do not claim causal identification without separate identifying restrictions.

## Method-Matched Robustness

- AR: residual whiteness, lag order, alternative estimators.
- Unit root: ADF/PP/KPSS and deterministic-specification sensitivity.
- ARCH/GARCH: ARCH effects, standardized residual diagnostics, distributional assumptions, volatility forecast performance, and alternative volatility specifications.
- Markov switching: number of regimes, transition probability stability, regime classification uncertainty, and robustness to starting values.
- Threshold: threshold range, trimming, regime sizes, alternative threshold variables.
- Kernel/nonparametric: bandwidth and kernel sensitivity.
- Cointegration: residual stationarity and break sensitivity.
- Granger: lag order and reverse-direction tests.
- VAR: stability roots, residual ACF/Ljung-Box, information criteria, forecast performance.
- TV-VAR/time-varying coefficients: bandwidth, constancy tests, bootstrap confidence bands, out-of-sample comparison.
- Semiparametric/neural methods: nuisance fit, sample splitting where relevant, out-of-sample validation, bootstrap inference.

## Claim Boundaries

- Granger causality means predictive content, not structural causality.
- Cointegration indicates a stable long-run relation, not a causal mechanism.
- Reduced-form VAR dynamics are endogenous interactions unless structural restrictions are imposed.
- Nonparametric and time-varying models show flexible heterogeneity or evolving associations by default.

## ARCH And GARCH Volatility Models

Use when volatility clustering, risk dynamics, or conditional variance forecasting is central, especially for financial returns, exchange rates, inflation uncertainty, or commodity prices.

ARCH(q):

```text
r_t = mu + epsilon_t
epsilon_t = sigma_t z_t
sigma_t^2 = omega + sum_{i=1}^q alpha_i epsilon_{t-i}^2
```

GARCH(1,1):

```text
sigma_t^2 = omega + alpha epsilon_{t-1}^2 + beta sigma_{t-1}^2
```

Extensions:

- EGARCH or GJR-GARCH for asymmetric volatility responses.
- GARCH-in-mean when risk affects expected returns.
- Multivariate GARCH only when covariance dynamics are central and the sample supports the parameter count.

Workflow:

1. Model or remove mean dynamics first.
2. Test residual ARCH effects.
3. Estimate conditional variance model with an appropriate innovation distribution.
4. Check standardized residual autocorrelation and remaining ARCH effects.
5. Report persistence `alpha + beta` and volatility half-life when meaningful.
6. Evaluate out-of-sample volatility forecasts if forecasting is a goal.

Writing boundary:

- GARCH explains conditional variance, not necessarily the conditional mean.
- Do not use volatility persistence as evidence of a causal mechanism without an identification design.

## Markov-Switching Models

Use when regimes are latent and the data may switch probabilistically between states such as expansion/recession, high/low volatility, or tight/loose policy.

Two-regime mean model:

```text
y_t = mu_{s_t} + phi_{s_t} y_{t-1} + epsilon_t
s_t in {1, 2}
Pr(s_t = j | s_{t-1} = i) = p_ij
```

Workflow:

1. Define which parameters switch: intercept, variance, autoregressive slope, or transition probabilities.
2. Estimate with maximum likelihood or filtering/smoothing routines.
3. Report transition probabilities and expected regime durations.
4. Plot smoothed regime probabilities against economically meaningful events.
5. Test whether additional regimes are justified by fit and interpretability.

Writing boundary:

- Regimes are model-implied latent states, not directly observed categories.
- Label regimes by estimated behavior, not by desired narrative.

## See Also

- [Method Selection](method-selection.md)
- [Panel Methods](panel-methods.md)
- [IV and Causal Methods](iv-causal-methods.md)
