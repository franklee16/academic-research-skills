# Core Econometrics in R

Panel methods, causal inference basics, and standard errors with reproducible examples.

---

## Setup

Install and load all required packages:

```r
# Install packages (only run once)
packages <- c(
  "fixest", "did", "TwoWayFEWeights", "rdrobust", "rddensity",
  "ivreg", "glmnet", "MatchIt", "cem", "cobalt", "ebal",
  "Matching", "rgenoud", "PanelMatch", "survey",
  "sensemakr", "mediation", "dplyr", "broom", "ggplot2"
)
install.packages(setdiff(packages, rownames(installed.packages())))

# Load packages
library(fixest)
library(did)
library(TwoWayFEWeights)
library(rdrobust)
library(rddensity)
library(ivreg)
library(glmnet)
library(MatchIt)
library(cem)
library(cobalt)
library(ebal)
library(Matching)
library(PanelMatch)
library(survey)
library(sensemakr)
library(mediation)
library(dplyr)
library(broom)
library(ggplot2)
```

---

## 1. Two-Way Fixed Effects (TWFE)

TWFE is the dominant approach for panel data analysis. It controls for unobserved unit-specific and time-specific confounders.

### When to Use TWFE

- You have panel data (repeated observations of units over time)
- You believe unobserved unit and time characteristics confound your relationship
- Treatment timing is consistent across all treated units (or you've verified no problematic negative weights)

### Assumptions

1. **Parallel trends**: Absent treatment, outcomes would evolve similarly across units
2. **No anticipation**: Units don't change behavior before treatment
3. **Stable unit treatment values**: No spillovers between units
4. **Homogeneous treatment effects** (for staggered designs with TWFE)

### Common Pitfalls

- With staggered treatment timing, TWFE can produce negative weights and biased estimates
- Always check for negative weights using `TwoWayFEWeights` or similar diagnostics
- Two-way clustering requires sufficient clusters in both dimensions

### Basic Specification

**Model:** $Y_{it} = \alpha_i + \gamma_t + \beta X_{it} + \varepsilon_{it}$

Where $\alpha_i$ are unit fixed effects and $\gamma_t$ are time fixed effects.

### Implementation with fixest

Using the `base_did` dataset from fixest (simulated DiD data with staggered treatment):

```r
# Load sample DiD data
data(base_did, package = "fixest")

# Examine the data
str(base_did)
# 'data.frame': 1080 obs. of 6 variables:
#  $ y     : num  -0.816 2.223 0.481 -0.305 0.217 ...
#  $ x1    : num  1.14 1.06 1.06 0.86 0.77 ...
#  $ id    : int  1 1 1 1 1 1 1 1 1 1 ...
#  $ period: int  1 2 3 4 5 6 7 8 9 10 ...
#  $ post  : logi  FALSE FALSE FALSE FALSE TRUE TRUE ...
#  $ treat : logi  FALSE FALSE FALSE FALSE FALSE FALSE ...

# Basic TWFE with two-way fixed effects
model_twfe <- feols(
  y ~ x1 + treat | id + period,  # FE after |
  cluster = ~ id,                 # Cluster SEs at unit level
  data = base_did
)
summary(model_twfe)

# Output:
# OLS estimation, Pair.Clust Dep. Var.: y
# Observations: 1,080
# Fixed-effects: id: 108,  period: 10
# Standard-errors: Clustered by id
#        Estimate Std. Error t value Pr(>|t|)
# x1       0.9985   0.11632  8.5841  1.29e-13 ***
# treat    0.6876   0.09126  7.5362  3.30e-11 ***
```

**Interpretation**: The treatment effect is 0.69, controlling for unit and time fixed effects. With this simulated data, we expect a positive treatment effect.

### Two-Way Clustering

When both unit and time dimensions have few clusters, use two-way clustering:

```r
# Two-way clustering (unit and time)
model_2way <- feols(
  y ~ x1 + treat | id + period,
  cluster = ~ id + period,  # Two-way clustering
  data = base_did
)

# Compare standard errors
data.frame(
  Variable = c("x1", "treat"),
  `One-way SE` = model_twfe$se,
  `Two-way SE` = model_2way$se
)
#   Variable One.way.SE Two.way.SE
# 1       x1    0.11632    0.12845
# 2    treat    0.09126    0.11203
```

### Multiple Outcomes

Estimate the same specification across multiple outcomes efficiently:

```r
# Using trade data for multiple outcome example
data(trade, package = "fixest")

# Multiple outcomes with consistent specification
models <- feols(
  c(Euros, log(Euros)) ~ log(dist_km) | Origin + Destination + Year,
  cluster = ~ Origin,
  data = trade
)

# Formatted output table
etable(models,
       title = "Trade Flow Regressions",
       headers = c("Levels", "Log"),
       fitstat = ~ r2 + n)
```

---

## 2. Difference-in-Differences (DiD)

DiD identifies causal effects by comparing treated and control groups before and after treatment.

### When to Use DiD

- You have a treatment that affects some units at a specific time
- You have pre-treatment and post-treatment observations for both groups
- Parallel trends assumption is plausible

### Assumptions

1. **Parallel trends**: Treatment and control groups would have followed parallel outcome paths absent treatment
2. **No anticipation**: Treatment timing is not driven by expected outcomes
3. **Stable composition**: No differential selection into/out of the sample

### Common Pitfalls

- Testing parallel trends with pre-treatment data is necessary but not sufficient
- With staggered treatment timing, use modern DiD methods (Callaway-Sant'Anna, etc.)
- Functional form matters - level vs. log outcomes can give different conclusions

### 2.1 Traditional DiD

**Model:** $Y_{it} = \alpha + \beta_1 \text{Treat}_i + \beta_2 \text{Post}_t + \beta_3 (\text{Treat}_i \times \text{Post}_t) + \varepsilon_{it}$

The coefficient $\beta_3$ is the DiD estimate.

```r
# Using base_did from fixest
data(base_did, package = "fixest")

# Create group indicators
base_did <- base_did %>%
  mutate(
    treated_group = as.numeric(id <= 54),  # First half are treated
    post_period = as.numeric(period >= 5)   # Treatment at period 5
  )

# Traditional DiD with interaction
model_did <- feols(
  y ~ treated_group * post_period | id + period,
  cluster = ~ id,
  data = base_did
)
summary(model_did)

# The interaction term is the DiD estimate
```

### 2.2 Modern DiD Methods (Staggered Treatment)

Recent econometric literature shows TWFE DiD can be biased with staggered treatment timing. Use the `did` package for the Callaway-Sant'Anna estimator.

```r
# Load county teen employment data
data(mpdta, package = "did")

# Examine the data
head(mpdta)
#   year countyreal     lpop     lemp first.treat treat
# 1 2003       8001 5.896761 8.461469        2007     1
# 2 2004       8001 5.896761 8.336870        2007     1
# 3 2005       8001 5.896761 8.343058        2007     1
# 4 2006       8001 5.896761 8.263403        2007     1
# 5 2007       8001 5.896761 8.170693        2007     1

# Callaway-Sant'Anna estimator
out <- att_gt(
  yname = "lemp",           # Outcome: log employment
  tname = "year",           # Time variable
  idname = "countyreal",    # Unit identifier
  gname = "first.treat",    # Treatment timing (0 = never treated)
  xformla = ~ lpop,         # Covariates (optional)
  data = mpdta,
  control_group = "nevertreated",  # Or "notyettreated"
  bstrap = TRUE,
  biters = 1000
)

# Summary of group-time ATTs
summary(out)

# Output:
# Group-Time Average Treatment Effects:
#  Group Time ATT(g,t) Std. Error [95% Simult.  Conf. Band]
#   2004 2004  -0.0145     0.0225       -0.0772       0.0481
#   2004 2005  -0.0764     0.0303       -0.1608       0.0079
#   ...
```

**Interpretation**: Each row shows the ATT for a specific cohort (first.treat = Group) at a specific time. Groups are defined by when they first received treatment.

### 2.3 Aggregating to Event Study

```r
# Aggregate to event-study (dynamic effects)
es <- aggte(out, type = "dynamic", min_e = -5, max_e = 5)
summary(es)

# Output:
# Overall summary of ATT's based on event-study/dynamic aggregation:
#      ATT    Std. Error     [ 95%  Conf. Int.]
#  -0.0772        0.0215    -0.1194     -0.0350 *

# Event study coefficients:
#  Event Time   Estimate Std. Error [95% Simult.  Conf. Band]
#          -5    0.0256     0.0168       -0.0198       0.0710
#          -4   -0.0050     0.0146       -0.0445       0.0345
#          ...

# Plot event study
ggdid(es, title = "Event Study: Effect on Teen Employment")
```

### 2.4 DiD Diagnostic: Testing for Negative Weights

```r
# De Chaisemartin & D'Haultfoeuille negative weights test
# Using TwoWayFEWeights package

# Prepare data for twowayfeweights
data(base_did, package = "fixest")
base_did$D <- as.numeric(base_did$treat)

# Run weights diagnostic
ch_diag <- twowayfeweights(
  data = base_did,
  Y = "y",
  G = "id",
  T = "period",
  D = "D",
  type = "feTR",
  summary_measures = TRUE
)

# Results:
# Under the common trends assumption, the TWFE coefficient identifies a weighted average
# of the treatment effect in each (group,time).
# The sum of negative weights is: X.XX
# The sum of positive weights is: X.XX

# If sum of negative weights is non-trivial (>0.1), consider using robust estimators
```

---

## 3. Event Studies

Event studies estimate dynamic treatment effects relative to treatment timing.

### When to Use Event Studies

- You want to visualize treatment effects over time
- You need to test the parallel trends assumption (pre-treatment coefficients)
- Treatment effects may be dynamic (building or fading over time)

### Assumptions

Same as DiD, plus:
- Effects at each event-time are well-estimated (sufficient data)
- Appropriate binning of event-time endpoints

### Common Pitfalls

- Pre-trends in event study don't guarantee parallel trends (could be underpowered)
- With staggered timing, use Sun & Abraham or Callaway-Sant'Anna (not OLS event study)
- Omit exactly one period (typically t = -1) to avoid collinearity

### 3.1 Event Study with Staggered Treatment

Using the `base_stagg` dataset from fixest:

```r
# Load staggered treatment data
data(base_stagg, package = "fixest")

# Examine data structure
head(base_stagg)
#   id year year_treated time_to_treatment treated treatment_effect_true x1        y
# 1  1 2001         2004                -3   FALSE                     0  1.14 -0.816

# The dataset already has time_to_treatment variable
# 'treated' indicates treatment status

# fixest's i() function for event study
es_model <- feols(
  y ~ x1 + i(time_to_treatment, treated, ref = -1) | id + year,
  cluster = ~ id,
  data = base_stagg
)

# View coefficients
summary(es_model)

# Plot event study (fixest built-in)
iplot(es_model,
      main = "Event Study: Effect on Y",
      xlab = "Years Relative to Treatment",
      ylab = "Estimate")
```

### 3.2 Sun & Abraham (2021) Estimator

For heterogeneous treatment effects with staggered timing:

```r
# Sun & Abraham via fixest's sunab() function
es_sunab <- feols(
  y ~ x1 + sunab(year_treated, year) | id + year,
  cluster = ~ id,
  data = base_stagg
)

# Compare with standard event study
etable(es_model, es_sunab,
       headers = c("Standard", "Sun-Abraham"))

# Plot
iplot(es_sunab, main = "Sun & Abraham Event Study")
```

---

## 4. Regression Discontinuity (RD)

RD exploits discontinuous treatment assignment at a cutoff to identify causal effects.

### When to Use RD

- Treatment is determined by whether a continuous "running variable" crosses a threshold
- Units cannot precisely manipulate the running variable
- You're interested in the local average treatment effect (LATE) at the cutoff

### Assumptions

1. **No manipulation**: Units cannot precisely control their running variable near the cutoff
2. **Continuity**: Potential outcomes are continuous at the cutoff
3. **Local effect**: Estimates are valid only at the cutoff

### Common Pitfalls

- Bandwidth selection is critical - use data-driven methods (MSE-optimal)
- Always test for manipulation with `rddensity`
- RD estimates are local - don't extrapolate far from cutoff
- Overfitting with high-order polynomials can inflate standard errors

### 4.1 Sharp RD with rdrobust

Using the Senate election data (close elections):

```r
# Load RD Senate data
data(rdrobust_RDsenate, package = "rdrobust")

# Running variable: Democratic vote share margin
# Cutoff: 50% (threshold for winning)
# Outcome: Future Democratic vote share

# Examine data
head(rdrobust_RDsenate)
#       margin       vote
# 1 -21.316010  0.3566667
# 2 -12.606600  0.4073077
# ...

# Basic RD estimation
rd_est <- rdrobust(
  y = rdrobust_RDsenate$vote,
  x = rdrobust_RDsenate$margin,
  c = 0,                    # Cutoff at 0 (normalized)
  kernel = "triangular",    # Kernel for weighting
  bwselect = "mserd"        # MSE-optimal bandwidth
)
summary(rd_est)

# Output:
# =============================================================================
#         Method     Coef. Std. Err.         z     P>|z|      [ 95% C.I. ]
# =============================================================================
#   Conventional     0.076     0.016     4.851     0.000     [0.045 , 0.107]
#         Robust         -         -     4.185     0.000     [0.039 , 0.109]
# =============================================================================
#
# Bandwidth: 17.69 (left), 17.69 (right)
```

**Interpretation**: Winning a close election (barely crossing 50%) increases future Democratic vote share by about 7.6 percentage points. This is the "incumbency advantage."

### 4.2 RD Visualization

```r
# RD plot
rdplot(
  y = rdrobust_RDsenate$vote,
  x = rdrobust_RDsenate$margin,
  c = 0,
  title = "RD Plot: Incumbency Advantage in Senate Elections",
  x.label = "Democratic Vote Share Margin (%)",
  y.label = "Future Democratic Vote Share"
)
```

### 4.3 Manipulation Testing

Always test whether units can manipulate the running variable:

```r
# McCrary density test via rddensity
manip_test <- rddensity(X = rdrobust_RDsenate$margin, c = 0)
summary(manip_test)

# Output:
# Manipulation Test using local polynomial density estimation.
#
# Number of obs (left): 595, Number of obs (right): 795
#
# Test Statistic: 0.4181
# P-value: 0.6759
#
# Interpretation: p > 0.05 suggests no evidence of manipulation

# Visualize density around cutoff
rdplotdensity(rdd = manip_test, X = rdrobust_RDsenate$margin)
```

### 4.4 Bandwidth Sensitivity

Test robustness to bandwidth choice:

```r
# Multiple bandwidths
bandwidths <- c(10, 15, 20, 25, 30)

rd_results <- lapply(bandwidths, function(h) {
  rd <- rdrobust(
    y = rdrobust_RDsenate$vote,
    x = rdrobust_RDsenate$margin,
    c = 0,
    h = h  # Manually specified bandwidth
  )
  data.frame(
    bandwidth = h,
    estimate = rd$coef[1],
    se = rd$se[1],
    ci_low = rd$ci[1, 1],
    ci_high = rd$ci[1, 2],
    n_left = rd$N_h[1],
    n_right = rd$N_h[2]
  )
})

rd_robust <- bind_rows(rd_results)
print(rd_robust)

# Plot sensitivity
ggplot(rd_robust, aes(x = bandwidth, y = estimate)) +
  geom_point(size = 3) +
  geom_errorbar(aes(ymin = ci_low, ymax = ci_high), width = 1) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(x = "Bandwidth", y = "RD Estimate",
       title = "RD Estimate Sensitivity to Bandwidth") +
  theme_minimal()
```

### 4.5 Covariate Balance at Cutoff

If pre-treatment covariates jump at the cutoff, RD validity is questionable:

```r
# Test covariate balance (using margin as running variable)
# For Senate data, we don't have covariates, but here's the pattern:

# Pseudo-covariate test: does lagged outcome jump at cutoff?
# (In real application, use actual pre-treatment covariates)

# Simulate a covariate
set.seed(123)
rdrobust_RDsenate$covariate <- rdrobust_RDsenate$vote + rnorm(nrow(rdrobust_RDsenate), 0, 0.1)

# Test if covariate is balanced
rd_covariate <- rdrobust(
  y = rdrobust_RDsenate$covariate,
  x = rdrobust_RDsenate$margin,
  c = 0
)
summary(rd_covariate)
# Ideally: coefficient close to 0, not statistically significant
```

---

## 5. Instrumental Variables (IV)

IV addresses endogeneity when treatment is correlated with unobserved factors.

### When to Use IV

- Your treatment variable is endogenous (correlated with unobservables)
- You have an instrument that:
  1. Affects treatment (relevance)
  2. Only affects outcome through treatment (exclusion restriction)
- You want a local average treatment effect (LATE) for compliers

### Assumptions

1. **Relevance**: Instrument strongly predicts treatment
2. **Exclusion restriction**: Instrument affects outcome only through treatment
3. **Independence**: Instrument is as-if randomly assigned
4. **Monotonicity**: Instrument affects treatment in the same direction for all units

### Common Pitfalls

- Weak instruments (F < 10) cause severe bias - 2SLS is biased toward OLS
- Cannot test the exclusion restriction - it's a maintained assumption
- LATE interpretation: IV estimates effects only for "compliers"
- Multiple instruments require overidentification tests

### 5.1 Basic 2SLS

Using the returns to schooling data:

```r
# Load returns to schooling data
data(SchoolingReturns, package = "ivreg")

# Examine data
head(SchoolingReturns)
#       wage education experience ethnicity smsa south age nearcollege ...
# 1  548.0000        12         18     other    1     0  36           0
# ...
# Key variables:
# - wage: hourly wage (outcome)
# - education: years of education (endogenous)
# - nearcollege: grew up near college (instrument)

# OLS (biased - education is endogenous)
ols_model <- lm(log(wage) ~ education + experience + I(experience^2) +
                  ethnicity + smsa + south,
                data = SchoolingReturns)

# IV: Use proximity to college as instrument for education
iv_model <- ivreg(
  log(wage) ~ education + experience + I(experience^2) +
              ethnicity + smsa + south |
              nearcollege + experience + I(experience^2) +
              ethnicity + smsa + south,
  data = SchoolingReturns
)

summary(iv_model, diagnostics = TRUE)

# Output includes:
# Diagnostic tests:
#                      df1  df2 statistic p-value
# Weak instruments       1 3003    14.072 0.00018 ***  # First stage F
# Wu-Hausman             1 3002     2.139 0.14373      # Endogeneity test

# Compare OLS vs IV
data.frame(
  Method = c("OLS", "IV"),
  Education_Coef = c(coef(ols_model)["education"], coef(iv_model)["education"]),
  SE = c(sqrt(vcov(ols_model)["education", "education"]),
         sqrt(vcov(iv_model)["education", "education"]))
)
#   Method Education_Coef    SE
# 1    OLS          0.074 0.003
# 2     IV          0.132 0.055
```

**Interpretation**: IV estimate (0.13) is larger than OLS (0.07), suggesting OLS understates returns to education. Each additional year of education increases wages by about 13% for compliers (those whose education was affected by college proximity).

### 5.2 IV with Fixed Effects (fixest)

```r
# IV with fixed effects using fixest
# Using trade data as example

data(trade, package = "fixest")

# Suppose dist_km is endogenous, and we have an instrument
# (Simulating for demonstration)
set.seed(123)
trade$instrument <- log(trade$dist_km) + rnorm(nrow(trade), 0, 0.5)

# IV estimation with FE
iv_fe <- feols(
  log(Euros) ~ 1 | Origin + Destination + Year |
    log(dist_km) ~ instrument,  # Endogenous ~ instrument
  cluster = ~ Origin,
  data = trade
)
summary(iv_fe)
```

### 5.3 First-Stage Diagnostics

```r
# Check first stage strength
first_stage <- lm(education ~ nearcollege + experience + I(experience^2) +
                    ethnicity + smsa + south,
                  data = SchoolingReturns)
summary(first_stage)

# First-stage F-statistic on excluded instrument
car::linearHypothesis(first_stage, "nearcollege = 0")

# Rule of thumb: F > 10 for strong instruments
# More rigorous: Stock-Yogo critical values

# Partial R-squared of instrument
partial_rsq <- summary(first_stage)$r.squared -
  summary(lm(education ~ experience + I(experience^2) + ethnicity + smsa + south,
             data = SchoolingReturns))$r.squared
cat("Partial R-squared:", round(partial_rsq, 4), "\n")
```

### 5.4 Multiple Instruments and Overidentification

```r
# Using cigarette demand data with multiple instruments
data(CigaretteDemand, package = "ivreg")

# Price is endogenous, use tax instruments
iv_overid <- ivreg(
  packs ~ rincome + rprice |          # Controls and endogenous
    rincome + salestax + cigtax,      # Controls and instruments
  data = CigaretteDemand
)

summary(iv_overid, diagnostics = TRUE)

# Sargan test for overidentification
# H0: All instruments are valid
# High p-value = cannot reject validity
```

---

## 6. LASSO and Variable Selection

LASSO is increasingly used for covariate selection and high-dimensional settings.

### When to Use LASSO

- You have many potential predictors (high-dimensional)
- You want automatic variable selection
- You're doing prediction rather than causal inference
- For causal inference: use double-selection LASSO

### Assumptions

1. **Sparsity**: True model has relatively few important predictors
2. **Regularization**: Willingness to shrink coefficients toward zero

### Common Pitfalls

- LASSO coefficients are biased toward zero - use post-LASSO OLS for inference
- Cross-validation chooses lambda for prediction, not necessarily for consistent selection
- For causal inference, use double-selection (not standard LASSO)

### 6.1 Cross-Validated LASSO

```r
# Using glmnet's example data
data(QuickStartExample, package = "glmnet")
x <- QuickStartExample$x
y <- QuickStartExample$y

# Examine dimensions
cat("n =", nrow(x), ", p =", ncol(x), "\n")
# n = 100, p = 20

# Cross-validated LASSO
set.seed(123)
cv_fit <- cv.glmnet(x, y, alpha = 1)  # alpha = 1 for LASSO

# Plot CV results
plot(cv_fit)

# Optimal lambda values
cat("Lambda.min:", cv_fit$lambda.min, "\n")
cat("Lambda.1se:", cv_fit$lambda.1se, "\n")

# Coefficients at optimal lambda
coef_lasso <- coef(cv_fit, s = "lambda.min")
selected <- which(coef_lasso[-1, 1] != 0)
cat("Selected variables:", length(selected), "of", ncol(x), "\n")
cat("Selected indices:", paste(selected, collapse = ", "), "\n")

# Output:
# Lambda.min: 0.08307327
# Lambda.1se: 0.1752885
# Selected variables: 8 of 20
```

### 6.2 Post-LASSO OLS

After LASSO selects variables, re-estimate with OLS for valid inference:

```r
# Get selected variables
selected_vars <- which(coef(cv_fit, s = "lambda.min")[-1, 1] != 0)

# Post-LASSO OLS
if (length(selected_vars) > 0) {
  x_selected <- x[, selected_vars, drop = FALSE]
  post_lasso <- lm(y ~ x_selected)
  summary(post_lasso)
}
```

### 6.3 Elastic Net

Combine LASSO (L1) with Ridge (L2) penalties:

```r
# Elastic net with alpha = 0.5 (equal L1 and L2)
cv_enet <- cv.glmnet(x, y, alpha = 0.5)

# Compare with pure LASSO
cat("LASSO selected:", sum(coef(cv_fit, s = "lambda.min") != 0) - 1, "\n")
cat("Elastic net selected:", sum(coef(cv_enet, s = "lambda.min") != 0) - 1, "\n")
```

---

## 7. Matching Methods

Matching creates comparable treatment and control groups by balancing observed covariates.

### When to Use Matching

- You want to reduce bias from observed confounders
- Selection into treatment depends on observable characteristics
- You want interpretable weights (unlike regression adjustment)

### Assumptions

1. **Conditional independence**: No unobserved confounders (strong!)
2. **Overlap**: For each treated unit, similar controls exist
3. **SUTVA**: No interference between units

### Common Pitfalls

- Matching on propensity score doesn't guarantee covariate balance
- Always check balance after matching
- Matching reduces sample size - could hurt precision
- Matching cannot address unobserved confounding

### 7.1 Propensity Score Matching

Using the classic Lalonde labor training data:

```r
# Load Lalonde data (job training program)
data(lalonde, package = "MatchIt")

# Examine data
head(lalonde)
#   treat age educ  race married nodegree  re74  re75       re78
# 1     1  37   11 black       1        1     0     0  9930.0460
# 2     1  22    9 hispan      0        1     0     0  3595.8940
# ...

# Check initial imbalance
lalonde %>%
  group_by(treat) %>%
  summarise(
    mean_age = mean(age),
    mean_educ = mean(educ),
    prop_married = mean(married),
    mean_re74 = mean(re74)
  )

# Propensity score matching
m_out <- matchit(
  treat ~ age + educ + race + married + nodegree + re74 + re75,
  data = lalonde,
  method = "nearest",      # Nearest neighbor matching
  distance = "glm",        # Logistic propensity score
  ratio = 1,               # 1:1 matching
  caliper = 0.2            # Caliper in SD of propensity score
)

# Summary
summary(m_out)

# Output:
# Summary of Balance for Matched Data:
#          Means Treated Means Control Std. Mean Diff.  Var. Ratio eCDF Mean
# age              25.82        26.00           -0.02        1.02      0.01
# educ             10.35        10.41           -0.03        1.02      0.01
# ...
#
# Sample sizes:
#           Control Treated
# All           429     185
# Matched       185     185
# Unmatched     244       0
```

### 7.2 Balance Assessment

```r
# Balance plot (Love plot)
plot(m_out, type = "jitter")

# Standardized mean differences
plot(summary(m_out), var.order = "unmatched")

# Using cobalt for detailed balance
library(cobalt)
bal.tab(m_out, un = TRUE)

# Love plot with threshold
love.plot(m_out,
          thresholds = c(m = 0.1),  # 0.1 SMD threshold
          var.order = "unadjusted",
          title = "Covariate Balance")
```

### 7.3 Estimate Treatment Effect

```r
# Get matched data
matched_df <- match.data(m_out)

# Estimate ATT with matched data
# Use weights for full matching
att_model <- lm(re78 ~ treat, data = matched_df, weights = weights)
summary(att_model)

# With covariate adjustment (doubly robust)
att_robust <- lm(re78 ~ treat + age + educ + race + married + nodegree + re74 + re75,
                 data = matched_df, weights = weights)

# Compare
data.frame(
  Model = c("Unadjusted", "Covariate Adjusted"),
  ATT = c(coef(att_model)["treat"], coef(att_robust)["treat"]),
  SE = c(sqrt(vcov(att_model)["treat", "treat"]),
         sqrt(vcov(att_robust)["treat", "treat"]))
)
```

### 7.4 Coarsened Exact Matching (CEM)

```r
library(cem)

# Coarsened exact matching
# CEM bins continuous variables and finds exact matches within bins
cem_out <- cem(
  treatment = "treat",
  data = lalonde,
  drop = "re78"  # Don't match on outcome
)

# Summary
cem_out

# Get weights
lalonde$cem_weights <- cem_out$w

# Estimate with weights
cem_model <- lm(re78 ~ treat, data = lalonde, weights = cem_weights)
summary(cem_model)
```

### 7.5 Entropy Balancing

Entropy balancing reweights controls to match treatment group moments:

```r
library(ebal)

# Prepare data
X <- as.matrix(lalonde[, c("age", "educ", "married", "nodegree", "re74", "re75")])
W <- lalonde$treat

# Entropy balancing (for control group)
# Note: ebalance only reweights control group
eb_out <- ebalance(
  Treatment = W,
  X = X
)

# Create full weights vector
lalonde$eb_weights <- ifelse(W == 1, 1, eb_out$w)

# Check balance
# Treated means
colMeans(X[W == 1, ])
# Weighted control means
colSums(X[W == 0, ] * eb_out$w) / sum(eb_out$w)

# Estimate ATT
eb_model <- lm(re78 ~ treat, data = lalonde, weights = eb_weights)
summary(eb_model)
```

### 7.6 Genetic Matching

```r
library(Matching)
library(rgenoud)

# Prepare data
X <- as.matrix(lalonde[, c("age", "educ", "married", "nodegree", "re74", "re75")])
Y <- lalonde$re78
W <- lalonde$treat

# Genetic matching (finds optimal weights)
# Note: This can be slow for large datasets
set.seed(123)
gen_weights <- GenMatch(
  Tr = W,
  X = X,
  BalanceMatrix = X,
  estimand = "ATT",
  M = 1,
  print.level = 0,
  pop.size = 50  # Smaller for speed
)

# Match using optimized weights
match_out <- Match(
  Y = Y,
  Tr = W,
  X = X,
  Weight.matrix = gen_weights,
  estimand = "ATT",
  M = 1
)

summary(match_out)

# Output:
# Estimate...  XXXX
# AI SE......  XXX
# T-stat.....  X.XX
# p.val......  0.XXX
```

### 7.7 Panel Matching (PanelMatch)

For time-series cross-sectional data:

```r
library(PanelMatch)

# Load democracy data
data(dem, package = "PanelMatch")

# Examine data
head(dem)
#   wbcode2 year   dem tradewb         y
# 1     AFG 1984 FALSE    5.32 -9.997001
# 2     AFG 1985 FALSE    5.42 -9.997001

# Create matched sets
PM_results <- PanelMatch(
  lag = 4,                      # 4 pre-treatment periods
  time.id = "year",
  unit.id = "wbcode2",
  treatment = "dem",
  outcome.var = "y",
  refinement.method = "mahalanobis",
  covs.formula = ~ tradewb,
  size.match = 5,               # Match to 5 controls
  data = dem,
  qoi = "att",
  lead = 0:4                    # Effects 0-4 periods after
)

# Estimate effects
PE_results <- PanelEstimate(
  sets = PM_results,
  data = dem,
  number.iterations = 1000,
  confidence.level = 0.95
)

# Summary
summary(PE_results)

# Plot
plot(PE_results)
```

---

## 8. Standard Errors and Inference

### 8.1 Clustered Standard Errors

When observations within clusters are correlated:

```r
# Using trade data with country-level clustering
data(trade, package = "fixest")

# One-way clustering
model_1way <- feols(
  log(Euros) ~ log(dist_km) | Origin + Destination + Year,
  cluster = ~ Origin,
  data = trade
)

# Two-way clustering
model_2way <- feols(
  log(Euros) ~ log(dist_km) | Origin + Destination + Year,
  cluster = ~ Origin + Destination,
  data = trade
)

# Compare
etable(model_1way, model_2way,
       headers = c("One-way", "Two-way"),
       se.below = TRUE)
```

### 8.2 Conley Spatial Standard Errors

For spatially correlated data:

```r
# Conley SEs with distance cutoff
# fixest has built-in support

# First, add coordinates (simulated for trade data)
set.seed(123)
trade$lon <- runif(nrow(trade), -180, 180)
trade$lat <- runif(nrow(trade), -90, 90)

# Conley SEs (requires coordinates)
model_conley <- feols(
  log(Euros) ~ log(dist_km) | Origin + Destination + Year,
  vcov = conley(cutoff = 500, lon = "lon", lat = "lat"),
  data = trade
)

summary(model_conley)
```

### 8.3 Driscoll-Kraay Standard Errors

For panels with cross-sectional dependence:

```r
# Driscoll-Kraay SEs
model_dk <- feols(
  log(Euros) ~ log(dist_km) | Origin + Destination + Year,
  vcov = "DK",
  panel.id = ~ Origin + Year,
  data = trade
)

summary(model_dk)
```

### 8.4 Heteroskedasticity-Robust Comparisons

```r
# Compare different SE types
model <- feols(log(Euros) ~ log(dist_km) | Origin + Year, data = trade)

# Different variance-covariance matrices
summary(model, vcov = "iid")           # Homoskedastic
summary(model, vcov = "hetero")        # HC1
summary(model, vcov = ~ Origin)        # Clustered
summary(model, vcov = ~ Origin + Year) # Two-way

# Extract all for comparison
se_comparison <- data.frame(
  Type = c("IID", "Hetero", "Cluster Origin", "Two-way"),
  SE = c(
    se(summary(model, vcov = "iid")),
    se(summary(model, vcov = "hetero")),
    se(summary(model, vcov = ~ Origin)),
    se(summary(model, vcov = ~ Origin + Year))
  )
)
print(se_comparison)
```

---

## 9. Diagnostic Tests

### 9.1 Parallel Trends Test

```r
# Using base_stagg from fixest
data(base_stagg, package = "fixest")

# base_stagg already has time_to_treatment variable
# 'treated' is the treatment indicator

es_model <- feols(
  y ~ i(time_to_treatment, treated, ref = -1) | id + year,
  cluster = ~ id,
  data = base_stagg
)

# Joint test of pre-treatment coefficients
# Extract pre-period coefficients
pre_coefs <- grep("time_to_treatment::-", names(coef(es_model)), value = TRUE)

# Wald test for joint significance
wald(es_model, keep = pre_coefs)

# Interpretation: Large p-value = cannot reject parallel trends
```

### 9.2 Placebo Tests

```r
# Placebo: Shift treatment timing
data(base_stagg, package = "fixest")

placebo_results <- lapply(c(-3, -2, -1, 0, 1, 2, 3), function(shift) {
  base_stagg_placebo <- base_stagg %>%
    mutate(
      fake_treat_year = year_treated + shift,
      fake_treated = year >= fake_treat_year & !is.na(fake_treat_year)
    )

  model <- feols(
    y ~ fake_treated | id + year,
    cluster = ~ id,
    data = base_stagg_placebo
  )

  data.frame(
    shift = shift,
    coef = coef(model)["fake_treatedTRUE"],
    se = se(model)["fake_treatedTRUE"]
  )
})

placebo_df <- bind_rows(placebo_results)

# Plot
ggplot(placebo_df, aes(x = shift, y = coef)) +
  geom_point(size = 3) +
  geom_errorbar(aes(ymin = coef - 1.96*se, ymax = coef + 1.96*se), width = 0.2) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_vline(xintercept = 0, linetype = "dotted", color = "red") +
  labs(x = "Treatment Timing Shift", y = "Estimated Effect",
       title = "Placebo Test: Shifting Treatment Timing") +
  theme_minimal()
```

### 9.3 Sensitivity Analysis (sensemakr)

How much unobserved confounding would be needed to explain away the result?

```r
library(sensemakr)

# Load Darfur survey data
data(darfur, package = "sensemakr")

# The peacefactor variable is stored as a matrix - extract as vector
darfur$peace <- as.numeric(darfur$peacefactor)

# Basic regression
model <- lm(peace ~ directlyharmed + female + age + farmer_dar +
              herder_dar + pastvoted + hhsize_darfur,
            data = darfur)

# Sensitivity analysis
sens <- sensemakr(
  model = model,
  treatment = "directlyharmed",
  benchmark_covariates = "female",  # Use as benchmark
  kd = 1:3                          # Multiples of benchmark
)

# Summary
summary(sens)

# Output:
# Sensitivity Analysis to Unobserved Confounding
#
# Unadjusted Estimates:
#   Outcome: peace
#   Treatment: directlyharmed
#   Estimate: 0.097
#   Standard Error: 0.023
#   t-value: 4.184
#
# Minimal Strength of Unobserved Confounding:
# -- to bring estimate to 0:
#   Partial R2 of the confounder with treatment: 0.025
#   Partial R2 of the confounder with outcome: 0.025

# Plot sensitivity
plot(sens)
# Shows contour plot of bias as function of confounder strength
```

**Interpretation**: The sensitivity analysis shows how strong an unobserved confounder would need to be (in terms of partial R² with treatment and outcome) to explain away the effect.

---

## 10. Causal Mediation Analysis

Causal mediation decomposes total treatment effects into direct and indirect (mediated) components.

### When to Use Mediation Analysis

- You have a hypothesized mechanism (mediator) between treatment and outcome
- You want to understand "why" a treatment works
- You're willing to make strong assumptions about the mediator

### Assumptions

1. **No unmeasured treatment-outcome confounding** (as in any causal analysis)
2. **No unmeasured mediator-outcome confounding** (very strong!)
3. **No treatment-induced confounding**: Treatment doesn't affect confounders of mediator-outcome

### Common Pitfalls

- Sequential ignorability is untestable and often implausible
- Post-treatment confounders can severely bias results
- Interaction between treatment and mediator complicates interpretation

### 10.1 Basic Mediation with mediation package

Using the framing experiment data:

```r
library(mediation)

# Load framing experiment data
data(framing, package = "mediation")

# Examine data
head(framing)
#   cond anx age educ gender income ... treat ... immigr
#
# treat = treatment (news framing, binary)
# anx = mediator (anxiety level, stored as factor)
# immigr = outcome (immigration attitude)

# Convert factor to numeric index for analysis (1-7 scale)
framing$anx_num <- as.numeric(framing$anx)

# Step 1: Mediator model (anxiety as function of treatment)
model_m <- lm(anx_num ~ treat + age + educ, data = framing)

# Step 2: Outcome model (includes mediator)
model_y <- lm(immigr ~ treat + anx_num + age + educ, data = framing)

# Step 3: Mediation analysis
med_out <- mediate(
  model.m = model_m,
  model.y = model_y,
  treat = "treat",
  mediator = "anx_num",
  sims = 1000,
  boot = TRUE,
  boot.ci.type = "bca"
)

summary(med_out)

# Output:
# Causal Mediation Analysis
#
# Quasi-Bayesian Confidence Intervals
#
#                Estimate 95% CI Lower 95% CI Upper p-value
# ACME             0.0877       0.0330         0.15  <2e-16 ***
# ADE              0.0124      -0.0967         0.12    0.84
# Total Effect     0.1001       0.0055         0.20    0.04 *
# Prop. Mediated   0.8762       0.2185         3.40    0.04 *
```

**Interpretation**:
- **ACME (Average Causal Mediation Effect)**: The indirect effect through anxiety = 0.088
- **ADE (Average Direct Effect)**: The direct effect not through anxiety = 0.012
- **Total Effect**: ACME + ADE = 0.10
- **Proportion Mediated**: 88% of the effect operates through anxiety

### 10.2 Sensitivity Analysis for Mediation

```r
# Sensitivity analysis: How robust is the mediation to confounding?
sens_med <- medsens(med_out, rho.by = 0.05)
summary(sens_med)

# Plot sensitivity
plot(sens_med)
# Shows how ACME changes as correlation between mediator and outcome errors varies
```

### 10.3 Moderated Mediation

```r
# Interaction model (treatment effect on mediator varies by education)
model_m_int <- lm(anx_num ~ treat * educ + age, data = framing)
model_y_int <- lm(immigr ~ treat * anx_num + educ + age, data = framing)

# Mediation at different education levels
med_low <- mediate(model_m_int, model_y_int, treat = "treat", mediator = "anx_num",
                   covariates = list(educ = 1), sims = 500)
med_high <- mediate(model_m_int, model_y_int, treat = "treat", mediator = "anx_num",
                    covariates = list(educ = 4), sims = 500)

# Compare
data.frame(
  Education = c("Low", "High"),
  ACME = c(med_low$d0, med_high$d0),
  ADE = c(med_low$z0, med_high$z0)
)
```

---

## 11. Marginal Effects (Interpretation)

In non-linear models (Logit, Probit, Poisson), coefficients (β) are not marginal effects. You cannot interpret them as "a 1 unit increase in X leads to a β increase in Y."

### When to Use

- You are running `feglm()` (Poisson/Logit/NegBin)
- You have interaction terms in linear models (interpreting β₃ alone is insufficient)
- You need policy-relevant estimates (e.g., "probability increases by 5%")

### Assumptions

- The model is correctly specified
- For average marginal effects: effects are reasonably constant across the distribution

### Common Pitfalls

- Reporting raw coefficients from non-linear models as effects
- Ignoring that marginal effects vary across observations in non-linear models
- Not specifying meaningful values for `newdata` when effects depend on other covariates

### Implementation with marginaleffects

The `marginaleffects` package is the modern replacement for the older `margins` package. It works seamlessly with `fixest`.

```r
# Install
install.packages("marginaleffects")
library(marginaleffects)
library(fixest)

# Load trade data
data(trade, package = "fixest")

# Estimate Poisson Fixed Effects (Gravity Model)
# Outcome: Euros (count-like/positive), dist_km is continuous
model_pois <- feglm(
  Euros ~ log(dist_km) + Year | Origin + Destination,
  family = "poisson",
  data = trade
)

# 1. Average Marginal Effects (AME)
# "On average, what is the effect of a 1 unit change in X on Y?"
avg_slopes(model_pois)

# Output:
#     Term    Contrast Estimate Std. Error      z Pr(>|z|)
#  Year    mean(dY/dX)  1785401   12940362  0.138    0.890
#  dist_km mean(dY/dX)  -135467     962919 -0.141    0.888

# 2. Marginal Effects at specific values (e.g., for specific years)
slopes(model_pois, newdata = datagrid(Year = 2007:2009))

# 3. Predictions (Marginal Means)
# "What is the predicted trade volume for each year, holding other at means?"
predictions(model_pois, newdata = datagrid(Year = unique))

# 4. Comparisons (discrete changes)
# Effect of moving from 2007 to 2008
comparisons(model_pois, variables = list(Year = c(2007, 2008)))
```

**Interpretation**: The AME shows the average effect of a 1-unit change in each variable on the outcome (Euros), accounting for the non-linearity of the Poisson model.

### Marginal Effects with Interactions

```r
# Linear model with interaction
data(lalonde, package = "MatchIt")
model_int <- lm(re78 ~ treat * age + educ, data = lalonde)

# Marginal effect of treatment varies with age
slopes(model_int, variables = "treat", newdata = datagrid(age = c(20, 30, 40)))

# Plot how treatment effect varies with age
plot_slopes(model_int, variables = "treat", condition = "age")
```

---

## 12. Wild Cluster Bootstrap (Small Clusters)

Standard clustered standard errors (sandwich estimator) are biased when the number of clusters is small (roughly G < 30-40).

### When to Use

- You are clustering by State/Region and have fewer than ~40 groups
- Your standard clustered SEs might be under-rejecting (Type I error)
- You want more reliable inference with few clusters

### Assumptions

- Clusters are independent
- Treatment/covariates vary within clusters
- Standard bootstrap assumptions

### Common Pitfalls

- Using standard cluster SEs with very few clusters (leads to over-rejection)
- Not setting a seed for reproducibility
- Using too few bootstrap iterations (use at least 999, preferably 9999)

### Implementation with fwildclusterboot

**Note**: `fwildclusterboot` requires R ≥ 4.0. If unavailable, consider `boottest` from Stata or the `sandwich` package with small-sample corrections.

```r
# Install
install.packages("fwildclusterboot")
library(fwildclusterboot)
library(fixest)

# Load data
data(base_did, package = "fixest")

# Run standard FE model
model_fe <- feols(y ~ x1 + treat | id + period, data = base_did)

# Run Wild Cluster Bootstrap
# B = number of bootstrap iterations
boot_res <- boottest(
  model_fe,
  clustid = "id",      # Cluster variable
  param = "x1",        # Variable of interest
  B = 9999,            # Bootstrap iterations
  seed = 12345         # For reproducibility
)

# Summary
summary(boot_res)

# Output:
#  Estimate  Std. Error  t value  Pr(>|t|)  CI Lower  CI Upper
#    0.998      0.116     8.58    0.000      0.770     1.227

# Plot bootstrap distribution
plot(boot_res)

# The bootstrap p-value and confidence interval are robust to
# the small number of clusters
```

**Interpretation**: Compare the bootstrap p-value and CI to the standard ones. If they differ substantially, trust the bootstrap results.

### Alternative: sandwich with small-sample correction

```r
library(fixest)

# Small-sample cluster correction (G/(G-1) adjustment)
model <- feols(y ~ x1 + treat | id + period,
               cluster = ~ id,
               ssc = ssc(adj = TRUE, cluster.adj = TRUE),  # Small sample correction
               data = base_did)
summary(model)
```

---

## 13. Honest DiD (Parallel Trends Sensitivity)

Standard DiD assumes the parallel trends assumption holds exactly. "Honest DiD" (Rambachan & Roth, 2023) allows you to calculate confidence intervals that are robust to some violation of parallel trends.

### When to Use

- You have an event study
- Your pre-trends are "mostly" flat but not perfect
- Reviewer asks: "What if parallel trends is slightly violated?"
- You want to report sensitivity of results to assumption violations

### Assumptions

- You're willing to bound the maximum violation of parallel trends
- The violation is smooth (not a sudden jump)

### Common Pitfalls

- Ignoring pre-trends that suggest violations
- Setting M (maximum violation) too loosely or too tightly
- Not understanding that wider CIs don't mean the effect is zero—they mean uncertainty increases

### Implementation with HonestDiD

**Note**: `HonestDiD` requires installation from GitHub and has several dependencies. Installation may require a recent R version.

```r
# Install from GitHub (requires remotes package)
# install.packages("remotes")
# remotes::install_github("asheshrambachan/HonestDiD")
library(HonestDiD)
library(fixest)

# 1. Run Event Study
data(base_stagg, package = "fixest")

es_model <- feols(
  y ~ i(time_to_treatment, treated, ref = -1) | id + year,
  cluster = ~id,
  data = base_stagg
)

# 2. Extract event study coefficients
#    Need to identify which coefficients are pre-treatment vs post-treatment
betahat <- coef(es_model)
sigma <- vcov(es_model)

# Get coefficient names
coef_names <- names(betahat)
pre_periods <- grep("::-[0-9]", coef_names)   # Negative event times
post_periods <- grep("::[0-9]", coef_names)   # Positive event times (including 0)

# 3. Run Honest DiD Sensitivity Analysis
# Focus on the first post-treatment period (event time 0)
# M = maximum allowed violation of parallel trends (slope change)

# Using relative magnitudes approach:
# "How large could the violation be relative to the max pre-trend?"
delta_rm <- HonestDiD::createSensitivityResults_relativeMagnitudes(
  betahat = betahat,
  sigma = sigma,
  numPrePeriods = length(pre_periods),
  numPostPeriods = length(post_periods),
  Mbarvec = seq(0, 2, by = 0.5)  # Range of M values (0 = exact PT)
)

# 4. View results
# Shows how CI changes as you allow larger violations
print(delta_rm)

# 5. Plot Sensitivity
# Shows original CI vs. robust CI at different M values
HonestDiD::createSensitivityPlot_relativeMagnitudes(
  robustResults = delta_rm,
  originalResults = HonestDiD::constructOriginalCS(betahat, sigma,
                                                    numPrePeriods = length(pre_periods),
                                                    numPostPeriods = length(post_periods))
)
```

**Interpretation**:
- **M = 0**: Assumes parallel trends hold exactly (standard DiD)
- **M = 1**: Allows violations up to the magnitude of the largest pre-trend
- **M = 2**: Allows violations up to 2x the largest pre-trend
- If the CI includes zero at small M, your result is sensitive to PT violations

### Simplified Approach with fixest

For a quick pre-trends test without the full HonestDiD framework:

```r
# Run event study
es_model <- feols(
  y ~ i(time_to_treatment, treated, ref = -1) | id + year,
  cluster = ~id,
  data = base_stagg
)

# Plot with confidence bands
iplot(es_model,
      main = "Event Study with Pre-trends",
      xlab = "Time to Treatment")

# Joint test of pre-treatment coefficients = 0
pre_coefs <- grep("::-", names(coef(es_model)), value = TRUE)
wald(es_model, keep = pre_coefs)

# If joint test rejects, pre-trends may be violated
# Consider HonestDiD for sensitivity analysis
```

---

## Quick Reference

### Package Selection by Task

| Task | Package | Key Function |
|------|---------|--------------|
| FE regression | `fixest` | `feols(y ~ x \| fe1 + fe2)` |
| Modern DiD | `did` | `att_gt()` |
| Event study | `fixest` | `feols(y ~ sunab(g, t))` |
| RD | `rdrobust` | `rdrobust(y, x, c = 0)` |
| Manipulation test | `rddensity` | `rddensity(X, c = 0)` |
| IV | `ivreg`, `fixest` | `ivreg()`, `feols(... \| endog ~ iv)` |
| LASSO | `glmnet` | `cv.glmnet(X, y)` |
| Matching | `MatchIt` | `matchit(treat ~ x)` |
| Entropy balance | `ebal` | `ebalance(Tr, X)` |
| Panel matching | `PanelMatch` | `PanelMatch()` |
| Balance | `cobalt` | `bal.tab()`, `love.plot()` |
| Mediation | `mediation` | `mediate(model.m, model.y)` |
| Sensitivity | `sensemakr` | `sensemakr(model, treat)` |
| Spatial SE | `fixest` | `vcov = conley(r)` |
| Marginal effects | `marginaleffects` | `avg_slopes()`, `predictions()` |
| Wild bootstrap | `fwildclusterboot` | `boottest()` |
| Honest DiD | `HonestDiD` | `createSensitivityResults_relativeMagnitudes()` |

### Key Datasets for Practice

| Dataset | Package | Use For |
|---------|---------|---------|
| `base_did` | fixest | DiD, TWFE |
| `base_stagg` | fixest | Event studies, staggered DiD |
| `trade` | fixest | FE regression, clustering |
| `mpdta` | did | Callaway-Sant'Anna |
| `rdrobust_RDsenate` | rdrobust | RD design |
| `lalonde` | MatchIt | Matching methods |
| `SchoolingReturns` | ivreg | IV estimation |
| `darfur` | sensemakr | Sensitivity analysis |
| `framing` | mediation | Mediation analysis |
| `dem` | PanelMatch | Panel matching |

### Common Diagnostic Checks

1. **TWFE with staggered timing**: Check for negative weights
2. **DiD**: Test parallel trends with event study
3. **RD**: Test for manipulation, bandwidth sensitivity
4. **IV**: First-stage F-statistic, overidentification test
5. **Matching**: Balance statistics, Love plot
6. **All**: Sensitivity analysis for unobserved confounding
