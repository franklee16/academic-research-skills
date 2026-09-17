# Method Selection

Use this reference when the user asks what model to use, how to frame an empirical strategy, or whether a proposed method fits the data.

## Intake Checklist

Identify:

- Unit: person, firm, country, region, asset, market, product, or aggregate series.
- Time: none, short panel, long panel, single time series, event window, repeated cross-sections.
- Outcome: continuous, binary, count, share, index, rate, log level, growth rate.
- Main regressor: policy, treatment, price, GDP, exposure, lagged outcome, instrumented variable, latent factor.
- Variable roles: controls, mechanisms, moderators, instruments, fixed effects, clustering unit, sample flags, and bad controls.
- Target interpretation: prediction, association, elasticity, dynamic response, treatment effect, long-run relation, heterogeneity.
- Main threat: omitted variables, reverse causality, simultaneity, nonstationarity, serial correlation, cross-sectional dependence, selection, measurement error.

## Selection Rules

- Use OLS/cross-sectional regression when the outcome is continuous, units have no meaningful time dimension, and the target is association or prediction.
- Use fixed effects panel models when unobserved time-invariant unit heterogeneity is central and panel data are available.
- Use two-way fixed effects only when time shocks also matter; avoid causal language unless treatment timing/design assumptions are credible.
- Use random effects only when unit effects are plausibly uncorrelated with regressors.
- Use Mundlak-style correlated random effects when the report needs an explicit bridge between FE and RE or a direct test of correlation between regressors and unit effects.
- Use random coefficient or heterogeneous-slope models when unit-specific elasticities are the object of interest.
- Use dynamic panel IV/GMM when lagged outcomes are regressors and fixed effects create correlation after demeaning/differencing; use QMLE/conditional-mean approaches when the initial condition and regressor process assumptions are defensible.
- Use IV/2SLS when a regressor is endogenous and a defensible instrument is available.
- Use DiD/event study when there is a policy/treatment event with treated and control groups and credible parallel trends.
- Use modern staggered DiD estimators when treatment timing differs across cohorts and effects may be heterogeneous; do not rely only on a TWFE coefficient in that setting.
- Use RDD when treatment assignment changes discontinuously at a known cutoff in a running variable and continuity around the cutoff is credible.
- Use matching, IPW, or doubly robust weighting when selection on observables is the best defensible design and overlap/balance can be demonstrated.
- Use PSM-DiD or IPW-DiD when both observable imbalance and before-after treatment timing matter; parallel trends remains required after matching or weighting.
- Use panel synthetic counterfactual methods when one or more treated units have rich pre-treatment panels and the goal is a treatment-effect path relative to a constructed untreated outcome.
- Use time-series AR/ARIMA when a single series has persistence and forecasting is central.
- Use ADF/PP/KPSS and cointegration tools when series may be nonstationary.
- Use VAR when multiple endogenous time series interact and the goal is forecasting or dynamic dependence.
- Use structural VAR only if the identifying restrictions are explicitly justified.
- Use ARCH/GARCH-family models when conditional volatility, volatility clustering, or risk dynamics are central.
- Use Markov-switching models when regimes are latent and relationships change probabilistically across states.
- Use threshold/structural-change models when relationships change across regimes or candidate break points.
- Use kernel/nonparametric methods when the functional form is unknown and sample size supports local estimation.
- Use time-varying coefficient or TV-VAR methods when coefficient paths are central to the research question.
- Use binary panel/logit/probit when the outcome is an indicator.

## Model Choice Output

When recommending a method, provide:

1. Baseline model equation.
2. Why the method matches the data and question.
3. Key identifying or interpretation assumptions.
4. Required diagnostics.
5. Robustness checks.
6. What the method cannot claim.

## Red Flags

- A causal claim with no treatment design, instrument, or credible identification story.
- A levels regression with nonstationary time series and no unit-root/cointegration discussion.
- A dynamic panel estimated by naive OLS after fixed effects without discussing Nickell bias/endogeneity.
- A random-effects estimate reported without considering whether regressors are correlated with unit effects; use Hausman or Mundlak logic.
- A synthetic-counterfactual estimate with poor pre-treatment fit, contaminated donor units, or no placebo/sensitivity checks.
- A staggered-adoption DiD design reported only as a TWFE coefficient without cohort/time heterogeneity checks.
- A matching or IPW estimate with no overlap and balance diagnostics.
- An RDD estimate without running-variable plots, manipulation checks, bandwidth sensitivity, or covariate continuity checks.
- A GARCH estimate interpreted as a mean effect rather than volatility dynamics.
- A threshold or time-varying model with no bandwidth/threshold sensitivity.
- A panel model that ignores cross-sectional dependence when units share macro shocks.
- Tables of coefficients with no economic magnitude interpretation.

## See Also

- [Time-Series Methods](time-series-methods.md)
- [Panel Methods](panel-methods.md)
- [IV and Causal Methods](iv-causal-methods.md)
- [RDD and Matching Methods](rdd-matching-methods.md)
- [Data Analysis Workflow](data-analysis-workflow.md)

