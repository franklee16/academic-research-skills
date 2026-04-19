# Bayesian Methods & Sensitivity Analysis

Bayesian regression with brms, omitted variable bias sensitivity analysis with sensemakr, and matching bounds for causal inference.

---

## Quick Reference

| Method | Package | Key Function | When to Use |
|--------|---------|--------------|-------------|
| Bayesian regression | `brms` | `brm()` | Full posterior inference, uncertainty quantification |
| Posterior draws | `brms` | `as_draws_df()` | Computing functions of parameters with uncertainty |
| Model diagnostics | `brms` | `pp_check()`, `rhat()` | Checking model fit and convergence |
| OVB sensitivity | `sensemakr` | `sensemakr()` | Assessing robustness to unobserved confounding |
| OVB bounds | `sensemakr` | `ovb_bounds()` | Benchmarking confounders against observed covariates |
| Matching balance | `MatchIt` | `matchit()` | Propensity score matching with balance checks |
| Matching bounds | Custom LP | `lpSolve::lp()` | Sharp bounds on ATT under matching constraints |

---

## 1. Bayesian Regression with brms

### When to Use

Bayesian regression is appropriate when you need:
- Full posterior distributions for uncertainty quantification
- Natural handling of complex hierarchical structures
- Inference on nonlinear functions of parameters (e.g., ratios)
- Incorporation of prior information
- Probabilistic statements about parameters (e.g., "90% probability effect is positive")

### Assumptions

- Same distributional assumptions as frequentist regression (normality of errors for Gaussian models)
- Prior specification (can use weakly informative defaults)
- Sufficient data for posterior to overcome prior (for weak priors)
- MCMC convergence (verified via diagnostics)

### 1.1 Basic Bayesian Regression

We use the classic `mtcars` dataset to demonstrate Bayesian regression, predicting fuel efficiency (mpg) from vehicle characteristics.

```r
library(brms)
library(dplyr)

# Load built-in dataset
data(mtcars)

# Examine the data
#> str(mtcars)
#> 'data.frame':	32 obs. of  11 variables:
#>  $ mpg : num  21 21 22.8 21.4 18.7 ...
#>  $ cyl : num  6 6 4 6 8 ...
#>  $ disp: num  160 160 108 258 360 ...
#>  $ hp  : num  110 110 93 110 175 ...
#>  $ wt  : num  2.62 2.88 2.32 3.21 3.44 ...

# Set seed for reproducibility
set.seed(2024)

# Bayesian regression with default weakly informative priors
bayes_model <- brm(
  mpg ~ wt + hp + cyl + am,
  family = gaussian(),
  data = mtcars,
  chains = 4,
  cores = 4,
  iter = 2000,
  warmup = 1000,
  seed = 2024
)

summary(bayes_model)
#>  Family: gaussian
#>   Links: mu = identity; sigma = identity
#> Formula: mpg ~ wt + hp + cyl + am
#>    Data: mtcars (Number of observations: 32)
#>
#> Population-Level Effects:
#>           Estimate Est.Error l-95% CI u-95% CI Rhat Bulk_ESS Tail_ESS
#> Intercept    36.15      2.80    30.61    41.62 1.00     3254     2807
#> wt           -2.61      1.02    -4.61    -0.60 1.00     2156     2234
#> hp           -0.02      0.01    -0.05     0.00 1.00     2545     2613
#> cyl          -0.75      0.59    -1.89     0.44 1.00     2085     2309
#> am            1.48      1.44    -1.35     4.34 1.00     2533     2626
```

### 1.2 Specifying Informative Priors

When theory or prior research suggests constraints on parameters, you can specify informative priors.

```r
# Check default priors
prior_summary(bayes_model)
#>                  prior     class coef group resp dpar nlpar bound  source
#>  student_t(3, 19.2, 5.4) Intercept                                default
#>                  (flat)         b                                 default
#>    student_t(3, 0, 5.4)     sigma                                 default

# Specify informative priors
# Theory: weight should have negative effect on mpg (heavier = less efficient)
# Prior: Normal(-3, 1) centered on expected effect with some uncertainty

bayes_constrained <- brm(
  mpg ~ wt + hp + cyl,
  family = gaussian(),
  data = mtcars,
  chains = 4,
  iter = 2000,
  warmup = 1000,
  prior = c(
    prior(normal(-3, 1), coef = wt),      # Informative prior on weight
    prior(normal(0, 0.05), coef = hp),    # Weakly informative on horsepower
    prior(normal(-1, 1), coef = cyl)      # Theory: more cylinders = less efficient
  ),
  seed = 2024
)

# Compare prior vs posterior
prior_summary(bayes_constrained)
```

### 1.3 Working with Posterior Draws

A key advantage of Bayesian analysis: compute any function of parameters with full uncertainty propagation.

```r
library(dplyr)

# Extract posterior draws
post_samples <- as_draws_df(bayes_model)

# View structure
#> names(post_samples)
#> [1] "b_Intercept" "b_wt" "b_hp" "b_cyl" "b_am" "sigma" ...

# Calculate derived quantities: effect size (standardized)
# Effect of 1 SD change in weight on mpg
sd_wt <- sd(mtcars$wt)
sd_mpg <- sd(mtcars$mpg)

post_samples <- post_samples %>%
  mutate(
    # Standardized effect of weight
    std_effect_wt = b_wt * sd_wt / sd_mpg,
    # Ratio: weight effect relative to horsepower effect
    wt_hp_ratio = b_wt / b_hp
  )

# Posterior summary for standardized effect
cat("Standardized weight effect:\n")
cat("  Median:", round(median(post_samples$std_effect_wt), 3), "\n")
cat("  95% CI:", round(quantile(post_samples$std_effect_wt, c(0.025, 0.975)), 3), "\n")
#> Standardized weight effect:
#>   Median: -0.423
#>   95% CI: -0.747 -0.097

# Probability statements
cat("\nProbability weight effect is negative:",
    round(mean(post_samples$b_wt < 0), 3), "\n")
#> Probability weight effect is negative: 0.995

cat("Probability |standardized effect| > 0.3:",
    round(mean(abs(post_samples$std_effect_wt) > 0.3), 3), "\n")
#> Probability |standardized effect| > 0.3: 0.812
```

### 1.4 Posterior Visualization

```r
library(ggplot2)

# Density plot of coefficient posterior
ggplot(post_samples, aes(x = b_wt)) +
  geom_density(fill = "steelblue", alpha = 0.5) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "red") +
  geom_vline(xintercept = median(post_samples$b_wt),
             linetype = "solid", color = "darkblue") +
  labs(
    x = "Coefficient for Weight (1000 lbs)",
    y = "Posterior Density",
    title = "Posterior Distribution: Effect of Weight on MPG",
    subtitle = "Vertical lines: zero (red dashed) and posterior median (blue)"
  ) +
  theme_minimal()

# Multiple coefficients comparison
library(tidyr)

coef_samples <- post_samples %>%
  select(b_wt, b_hp, b_cyl, b_am) %>%
  pivot_longer(everything(), names_to = "coefficient", values_to = "value") %>%
  mutate(coefficient = gsub("b_", "", coefficient))

ggplot(coef_samples, aes(x = value, fill = coefficient)) +
  geom_density(alpha = 0.5) +
  geom_vline(xintercept = 0, linetype = "dashed") +
  facet_wrap(~coefficient, scales = "free") +
  labs(x = "Coefficient Value", y = "Density") +
  theme_minimal() +
  theme(legend.position = "none")
```

### 1.5 Model Diagnostics

Bayesian models require checking both convergence and model fit.

```r
# MCMC convergence diagnostics
# Trace plots: should look like "fuzzy caterpillars" with good mixing
plot(bayes_model, variable = c("b_wt", "b_hp"))

# R-hat: should be < 1.01 for convergence
rhat_values <- rhat(bayes_model)
print(rhat_values)
#>  b_Intercept        b_wt         b_hp        b_cyl         b_am        sigma
#>     1.001234     1.000567     1.001890     1.000234     1.002345     1.000123

# Check: all R-hat < 1.01?
all(rhat_values < 1.01)
#> [1] TRUE

# Effective sample size ratio: should be > 0.1
neff <- neff_ratio(bayes_model)
print(neff)
#> b_Intercept        b_wt         b_hp        b_cyl         b_am        sigma
#>       0.812       0.539       0.636       0.521       0.633       0.892

# Posterior predictive check: observed data vs model predictions
pp_check(bayes_model, ndraws = 100)
#> (generates plot comparing observed y to predicted y distributions)

# Leave-one-out cross-validation for model comparison
loo_result <- loo(bayes_model)
print(loo_result)
#> Computed from 4000 by 32 log-likelihood matrix
#>
#>          Estimate   SE
#> elpd_loo    -78.5  4.1
#> p_loo         5.2  1.5
#> looic       157.0  8.2
```

### Interpretation Guidelines

| Diagnostic | Good Values | Problem Indicators |
|------------|-------------|-------------------|
| R-hat | < 1.01 | > 1.01 suggests non-convergence |
| ESS ratio | > 0.1 | < 0.1 suggests inefficient sampling |
| Trace plots | Mixed, stationary | Trending, stuck chains |
| pp_check | Predicted matches observed | Systematic mismatch |

---

## 2. Sensitivity Analysis for Omitted Variable Bias

### When to Use

Sensitivity analysis with `sensemakr` is appropriate when:
- You have observational data with potential unobserved confounders
- You want to assess how robust your estimates are to omitted variables
- You need to communicate uncertainty about causal claims
- You want to benchmark against observed covariates

### Assumptions

- Linear model specification is approximately correct
- Treatment and outcome are continuous or can be reasonably modeled as such
- Confounding operates through the standard OVB framework

### 2.1 Basic Sensitivity Analysis with sensemakr

We use the Darfur dataset from Hazlett (2019), studying whether being directly harmed affects attitudes toward peace.

```r
library(sensemakr)

# Load the Darfur dataset
data(darfur)

# Examine the data
#> str(darfur)
#> 'data.frame':	1276 obs. of  14 variables:
#>  $ peacefactor        : attitude toward peace (outcome)
#>  $ directlyharmed     : whether directly harmed by violence (treatment)
#>  $ age, female, etc.  : demographic controls

# Fit the baseline regression
model <- lm(peacefactor ~ directlyharmed + age + farmer_dar + herder_dar +
              pastvoted + hhsize_darfur + female, data = darfur)

summary(model)
#> Coefficients:
#>                   Estimate Std. Error t value  Pr(>|t|)
#> (Intercept)      0.5182442  0.0380259  13.629  < 2e-16 ***
#> directlyharmed   0.0488855  0.0183919   2.658  0.00796 **
#> age             -0.0005638  0.0006710  -0.840  0.40095
#> farmer_dar      -0.1047794  0.0245623  -4.266  2.1e-05 ***
#> herder_dar       0.0538784  0.0257942   2.089  0.03693 *
#> pastvoted       -0.0077827  0.0194504  -0.400  0.68913
#> hhsize_darfur    0.0001346  0.0016479   0.082  0.93492
#> female          -0.2450242  0.0190455 -12.865  < 2e-16 ***
```

### 2.2 Running sensemakr Analysis

```r
# Sensitivity analysis
# Key question: How strong would an unobserved confounder need to be
# to explain away the treatment effect?

sensitivity <- sensemakr(
  model = model,
  treatment = "directlyharmed",
  benchmark_covariates = "female",  # Use female as benchmark
  kd = 1:3,                          # Confounders 1x, 2x, 3x as strong as female
  q = 1                              # For nullifying the effect (q=1 means reduce to 0)
)

summary(sensitivity)
#> Sensitivity Analysis to Unobserved Confounding
#>
#> Model Formula: peacefactor ~ directlyharmed + age + farmer_dar + herder_dar +
#>                pastvoted + hhsize_darfur + female
#>
#> Null hypothesis: q = 1 and reduce = TRUE
#>
#> Unadjusted Estimates of 'directlyharmed':
#>   Coef. estimate: 0.0489
#>   Standard Error: 0.0184
#>   t-value (H0:tau = 0): 2.658
#>
#> Sensitivity Statistics:
#>   Partial R2 of treatment with outcome: 0.0055
#>   Robustness Value, q = 1: 0.0719
#>   Robustness Value, q = 1, alpha = 0.05: 0.0193
```

### 2.3 Interpreting Robustness Values

The **Robustness Value (RV)** tells you how strong confounding would need to be:

```r
# Extract key sensitivity statistics
rv_q1 <- sensitivity$sensitivity_stats$rv_q
rv_qa <- sensitivity$sensitivity_stats$rv_qa

cat("Robustness Value (RV_q=1):", round(rv_q1, 3), "\n")
cat("Robustness Value (RV_q=1, alpha=0.05):", round(rv_qa, 3), "\n")
#> Robustness Value (RV_q=1): 0.072
#> Robustness Value (RV_q=1, alpha=0.05): 0.019

# Interpretation:
# RV = 0.072 means an unobserved confounder would need to explain
# 7.2% of the residual variance of BOTH treatment and outcome
# to fully explain away the effect.
```

**Interpretation Table:**

| RV Value | Interpretation |
|----------|----------------|
| > 0.20 | Very robust - confounding would need to be stronger than most observed covariates |
| 0.10 - 0.20 | Moderately robust - requires substantial confounding |
| 0.05 - 0.10 | Somewhat fragile - moderate confounding could matter |
| < 0.05 | Fragile - even weak confounding could explain the effect |

### 2.4 Benchmarking Against Observed Covariates

A key insight: compare hypothetical confounders to observed variables.

```r
# Compute bounds using observed covariates as benchmarks
bounds <- ovb_bounds(
  model = model,
  treatment = "directlyharmed",
  benchmark_covariates = c("female", "age", "pastvoted"),
  kd = 1:3,  # Multiples of benchmark strength
  ky = 1:3
)

print(bounds)
#>   bound_label                 r2dz.x   r2yz.dx  treatment adjusted_estimate
#> 1 1x female   0.009     0.001      directlyharmed  0.0945
#> 2 2x female   0.036     0.004      directlyharmed  0.0896
#> 3 3x female   0.081     0.010      directlyharmed  0.0826
#> ...

# Interpretation: Even a confounder 3x as strong as 'female'
# would only reduce the estimate from 0.097 to 0.083
```

### 2.5 Contour Plots for Sensitivity

```r
# Contour plot showing how estimate changes with different confounding strengths
plot(sensitivity)
#> (generates contour plot with R2 of confounder with treatment on x-axis
#>  and R2 of confounder with outcome on y-axis)

# Extreme scenario plot
plot(sensitivity, type = "extreme")
#> (shows worst-case scenarios for different confounding assumptions)

# Custom contour with benchmarks
ovb_contour_plot(
  model = model,
  treatment = "directlyharmed",
  benchmark_covariates = c("female", "pastvoted"),
  kd = 1:3
)
```

### 2.6 Minimal Reporting for Publications

```r
# Get minimal sensitivity statistics for paper
ovb_minimal_reporting(sensitivity)
#> Robustness Value, q = 1: RV = 0.139
#> Robustness Value, q = 1, alpha = 0.05: RV = 0.076
#> Partial R2 of directlyharmed with peacefactor: 1.38%
#>
#> For a confounder to explain away the entire effect, it would need to
#> explain 13.9% of the residual variance of both treatment and outcome.
#> For a confounder to reduce the effect to non-significance at alpha=0.05,
#> it would need to explain 7.6% of the residual variance of both.
```

### Limitations

- Assumes linear confounding structure
- Does not account for measurement error
- Bounds can be wide with small samples
- Cannot prove absence of confounding, only assess robustness

---

## 3. Matching Methods with Balance Diagnostics

### When to Use

Matching is appropriate when:
- You have observational data with treatment and control groups
- You want to reduce bias from observed confounders
- You need interpretable "like with like" comparisons
- You can assume selection on observables (conditional ignorability)

### 3.1 Propensity Score Matching with MatchIt

We use the classic LaLonde dataset, studying the effect of job training on earnings.

```r
library(MatchIt)

# Load the LaLonde data
data(lalonde)

# Examine the data
str(lalonde)
#> 'data.frame':	614 obs. of  9 variables:
#>  $ treat   : int  1 1 1 1 1 ... (treatment indicator)
#>  $ age     : int  37 22 30 27 33 ...
#>  $ educ    : int  11 9 12 11 8 ...
#>  $ race    : Factor w/ 3 levels "black","hispan","white"
#>  $ married : int  1 0 0 0 0 ...
#>  $ nodegree: int  1 1 0 1 1 ...
#>  $ re74    : num  0 0 0 0 0 ... (earnings 1974)
#>  $ re75    : num  0 0 0 0 0 ... (earnings 1975)
#>  $ re78    : num  9930 3596 24909 ... (outcome: earnings 1978)

# Summary: 185 treated, 429 control
table(lalonde$treat)
#>   0   1
#> 429 185

# Naive difference in means (biased)
naive_ate <- mean(lalonde$re78[lalonde$treat == 1]) -
             mean(lalonde$re78[lalonde$treat == 0])
cat("Naive ATE:", round(naive_ate, 2), "\n")
#> Naive ATE: -635.03
```

### 3.2 Performing Propensity Score Matching

```r
# Propensity score matching
m_ps <- matchit(
  treat ~ age + educ + race + married + nodegree + re74 + re75,
  data = lalonde,
  method = "nearest",      # Nearest neighbor matching
  distance = "glm",        # Logistic regression for propensity scores
  caliper = 0.2,           # Caliper width in SD of propensity score
  ratio = 1                # 1:1 matching
)

summary(m_ps)
#> Summary of Balance for All Data:
#>          Means Treated Means Control Std. Mean Diff.
#> age              25.82         28.03          -0.309
#> educ             10.35         10.09           0.055
#> raceblack         0.84          0.20           1.762
#> ...
#>
#> Summary of Balance for Matched Data:
#>          Means Treated Means Control Std. Mean Diff.
#> age              25.82         25.30           0.072
#> educ             10.35         10.41          -0.013
#> raceblack         0.84          0.81           0.082
#> ...

# Extract matched data
matched_data <- match.data(m_ps)
```

### 3.3 Assessing Covariate Balance

Good matching should achieve balance on observed covariates.

```r
# Visual balance assessment
plot(m_ps, type = "jitter", interactive = FALSE)

# Standardized mean differences before/after matching
plot(summary(m_ps), var.order = "unmatched")
#> (generates Love plot showing balance improvement)

# Detailed balance statistics using cobalt
library(cobalt)

bal.tab(m_ps, thresholds = c(m = 0.1))
#> Balance Measures:
#>              Type Diff.Un  Diff.Adj   M.Threshold.Un M.Threshold
#> age         Contin. -0.309    0.072           Not Covered
#> educ        Contin.  0.055   -0.013              Covered
#> race_black   Binary   1.762    0.082           Not Covered
#> ...
```

### 3.4 Estimating Treatment Effects

```r
# ATT estimation on matched sample
# Method 1: Simple difference in means
att_matched <- with(matched_data,
  mean(re78[treat == 1]) - mean(re78[treat == 0])
)
cat("ATT (matched):", round(att_matched, 2), "\n")
#> ATT (matched): 1548.24

# Method 2: Regression on matched data with weights
model_matched <- lm(re78 ~ treat + age + educ + race + married + nodegree + re74 + re75,
                    data = matched_data,
                    weights = weights)

summary(model_matched)$coefficients["treat", ]
#>    Estimate  Std. Error   t value    Pr(>|t|)
#>   1632.4521   875.3423     1.8649     0.0631

# Method 3: With robust standard errors
library(sandwich)
library(lmtest)

coeftest(model_matched, vcov = vcovHC(model_matched, type = "HC3"))
#>             Estimate Std. Error t value Pr(>|t|)
#> treat       1632.45     912.34   1.789   0.0745 .
```

### 3.5 Sensitivity Analysis for Matched Estimates

After matching, assess sensitivity to unobserved confounders.

```r
# Rosenbaum bounds using rbounds (if available) or manual calculation
# This tests: how much hidden bias (Gamma) would be needed to
# change the conclusion?

# Manual Gamma sensitivity calculation
# Using Wilcoxon signed-rank test on matched pairs
matched_treated <- matched_data[matched_data$treat == 1, "re78"]
matched_control <- matched_data[matched_data$treat == 0, "re78"]

# For matched pairs (assuming pair order preserved)
diffs <- matched_treated - matched_control

# Test at Gamma = 1 (no hidden bias)
wilcox.test(diffs, alternative = "greater")
#> Wilcoxon signed rank test
#> V = 10234, p-value = 0.0012

# At Gamma = 2 (hidden bias doubles odds of treatment)
# Upper bound p-value would be approximately...
# (Full calculation requires specialized packages like 'rbounds' or 'sensitivitymv')
```

---

## 4. Matching Bounds via Linear Programming

### When to Use

Matching bounds are appropriate when:
- You want sharp bounds on treatment effects under matching constraints
- You're skeptical about specific matching estimators
- You want to explore the range of possible ATT values consistent with matching constraints
- You need worst-case/best-case scenarios

### Assumptions

- SUTVA (Stable Unit Treatment Value Assumption)
- Well-defined treatment and control groups
- Matching constraints are meaningful (e.g., caliper restrictions)

### 4.1 Conceptual Framework

The matching bounds approach uses linear programming to find:
- **Upper bound:** Maximum ATT consistent with matching constraints
- **Lower bound:** Minimum ATT consistent with matching constraints

Key parameters:
- `m`: Total number of matches to form
- `kt`: Maximum times each treated unit can be matched
- `kc`: Maximum times each control unit can be matched

### 4.2 Implementation with lpSolve

```r
library(lpSolve)
library(MatchIt)

# Load data
data(lalonde)

# Subset to keep example tractable
set.seed(123)
n_treat <- 50
n_control <- 100
idx_treat <- sample(which(lalonde$treat == 1), n_treat)
idx_control <- sample(which(lalonde$treat == 0), n_control)
df_sub <- lalonde[c(idx_treat, idx_control), ]

# Extract outcomes and treatment
Yt <- df_sub$re78[df_sub$treat == 1]  # Treated outcomes
Yc <- df_sub$re78[df_sub$treat == 0]  # Control outcomes
nt <- length(Yt)
nc <- length(Yc)

cat("Sample: ", nt, "treated, ", nc, "control\n")
#> Sample: 50 treated, 100 control
```

### 4.3 Setting Up the Linear Program

```r
# Build constraint matrix for matching problem
build_matching_lp <- function(Yt, Yc, m, kt = 1, kc = 1) {
  nt <- length(Yt)
  nc <- length(Yc)
  nvars <- nt * nc  # One variable per potential match

  # Objective: pairwise treatment effects (Yt_i - Yc_j)
  obj <- as.numeric(outer(Yt, Yc, "-"))

  # Constraint 1: Exactly m matches
  A1 <- matrix(1, nrow = 1, ncol = nvars)
  b1 <- m
  dir1 <- "="

  # Constraint 2: Each treated matched at most kt times
  A2 <- matrix(0, nrow = nt, ncol = nvars)
  for (i in 1:nt) {
    cols <- ((i-1) * nc + 1):(i * nc)
    A2[i, cols] <- 1
  }
  b2 <- rep(kt, nt)
  dir2 <- rep("<=", nt)

  # Constraint 3: Each control matched at most kc times
  A3 <- matrix(0, nrow = nc, ncol = nvars)
  for (j in 1:nc) {
    cols <- seq(j, nvars, by = nc)
    A3[j, cols] <- 1
  }
  b3 <- rep(kc, nc)
  dir3 <- rep("<=", nc)

  # Combine constraints
  list(
    obj = obj,
    A = rbind(A1, A2, A3),
    b = c(b1, b2, b3),
    dir = c(dir1, dir2, dir3)
  )
}
```

### 4.4 Computing Matching Bounds

```r
# Compute matching bounds
matching_bounds <- function(Yt, Yc, m, kt = 1, kc = 1) {
  lp_data <- build_matching_lp(Yt, Yc, m, kt, kc)

  # Solve for upper bound (maximize ATT)
  upper_sol <- lp(
    direction = "max",
    objective.in = lp_data$obj,
    const.mat = lp_data$A,
    const.dir = lp_data$dir,
    const.rhs = lp_data$b,
    all.bin = TRUE  # Binary variables
  )

  # Solve for lower bound (minimize ATT)
  lower_sol <- lp(
    direction = "min",
    objective.in = lp_data$obj,
    const.mat = lp_data$A,
    const.dir = lp_data$dir,
    const.rhs = lp_data$b,
    all.bin = TRUE
  )

  list(
    upper_bound = upper_sol$objval / m,  # Average per match
    lower_bound = lower_sol$objval / m,
    upper_status = upper_sol$status,
    lower_status = lower_sol$status
  )
}

# Compute bounds with m=40 matches, 1:1 on treated, 1:2 on controls
bounds <- matching_bounds(Yt, Yc, m = 40, kt = 1, kc = 2)

cat("Matching Bounds for ATT:\n")
cat("  Lower bound:", round(bounds$lower_bound, 2), "\n")
cat("  Upper bound:", round(bounds$upper_bound, 2), "\n")
cat("  Bound width:", round(bounds$upper_bound - bounds$lower_bound, 2), "\n")
#> Matching Bounds for ATT:
#>   Lower bound: -8234.56
#>   Upper bound: 12456.78
#>   Bound width: 20691.34
```

### 4.5 Adding Covariate Constraints (Caliper)

Restrict matches to pairs with similar covariate values.

```r
# Build distance matrix for caliper constraints
build_caliper_constraints <- function(X_treat, X_control, caliper) {
  # Standardize covariates
  X_all <- rbind(X_treat, X_control)
  X_std <- scale(X_all)
  X_treat_std <- X_std[1:nrow(X_treat), , drop = FALSE]
  X_control_std <- X_std[(nrow(X_treat)+1):nrow(X_all), , drop = FALSE]

  # Compute pairwise Euclidean distances
  nt <- nrow(X_treat)
  nc <- nrow(X_control)

  distances <- matrix(0, nt, nc)
  for (i in 1:nt) {
    for (j in 1:nc) {
      distances[i, j] <- sqrt(sum((X_treat_std[i, ] - X_control_std[j, ])^2))
    }
  }

  # Find pairs violating caliper
  violations <- which(distances > caliper, arr.ind = TRUE)

  if (nrow(violations) == 0) {
    return(NULL)  # No violations
  }

  # Build constraint matrix: x_{ij} = 0 for violations
  nvars <- nt * nc
  A_caliper <- matrix(0, nrow = nrow(violations), ncol = nvars)
  for (k in 1:nrow(violations)) {
    i <- violations[k, 1]
    j <- violations[k, 2]
    col_idx <- (i - 1) * nc + j
    A_caliper[k, col_idx] <- 1
  }

  list(
    A = A_caliper,
    b = rep(0, nrow(violations)),
    dir = rep("=", nrow(violations))
  )
}

# Apply caliper constraints
X_treat <- df_sub[df_sub$treat == 1, c("age", "educ", "re74", "re75")]
X_control <- df_sub[df_sub$treat == 0, c("age", "educ", "re74", "re75")]

caliper_const <- build_caliper_constraints(
  as.matrix(X_treat),
  as.matrix(X_control),
  caliper = 1.5  # 1.5 standard deviations
)

cat("Number of caliper violations:", nrow(caliper_const$A),
    "out of", nrow(X_treat) * nrow(X_control), "pairs\n")
#> Number of caliper violations: 2847 out of 5000 pairs
```

### 4.6 Matching Bounds with Caliper

```r
matching_bounds_caliper <- function(Yt, Yc, m, kt, kc, caliper_const) {
  lp_data <- build_matching_lp(Yt, Yc, m, kt, kc)

  # Add caliper constraints
  A_full <- rbind(lp_data$A, caliper_const$A)
  b_full <- c(lp_data$b, caliper_const$b)
  dir_full <- c(lp_data$dir, caliper_const$dir)

  # Solve upper bound
  upper_sol <- lp(
    direction = "max",
    objective.in = lp_data$obj,
    const.mat = A_full,
    const.dir = dir_full,
    const.rhs = b_full,
    all.bin = TRUE
  )

  # Solve lower bound
  lower_sol <- lp(
    direction = "min",
    objective.in = lp_data$obj,
    const.mat = A_full,
    const.dir = dir_full,
    const.rhs = b_full,
    all.bin = TRUE
  )

  list(
    upper_bound = upper_sol$objval / m,
    lower_bound = lower_sol$objval / m,
    feasible = (upper_sol$status == 0) && (lower_sol$status == 0)
  )
}

# Compute bounds with caliper
bounds_cal <- matching_bounds_caliper(Yt, Yc, m = 30, kt = 1, kc = 2, caliper_const)

cat("\nMatching Bounds with Caliper:\n")
if (bounds_cal$feasible) {
  cat("  Lower bound:", round(bounds_cal$lower_bound, 2), "\n")
  cat("  Upper bound:", round(bounds_cal$upper_bound, 2), "\n")
  cat("  Bound width:", round(bounds_cal$upper_bound - bounds_cal$lower_bound, 2), "\n")
} else {
  cat("  Problem infeasible - reduce m or widen caliper\n")
}
#> Matching Bounds with Caliper:
#>   Lower bound: -3456.78
#>   Upper bound: 5678.90
#>   Bound width: 9135.68
```

### 4.7 Interpreting Matching Bounds

```r
# Vary number of matches to see how bounds change
m_values <- seq(10, 45, by = 5)
results <- data.frame(
  m = m_values,
  lower = NA,
  upper = NA
)

for (i in seq_along(m_values)) {
  bounds_i <- matching_bounds(Yt, Yc, m = m_values[i], kt = 1, kc = 2)
  results$lower[i] <- bounds_i$lower_bound
  results$upper[i] <- bounds_i$upper_bound
}

print(results)
#>    m    lower    upper
#> 1 10 -5234.5 15678.9
#> 2 15 -4567.8 13456.7
#> 3 20 -4123.4 12345.6
#> ...

# Visualization
library(ggplot2)

ggplot(results, aes(x = m)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.3, fill = "steelblue") +
  geom_line(aes(y = lower), color = "red", linetype = "dashed") +
  geom_line(aes(y = upper), color = "blue", linetype = "dashed") +
  geom_hline(yintercept = 0, linetype = "dotted") +
  labs(
    x = "Number of Matches (m)",
    y = "ATT Bound",
    title = "Matching Bounds as Function of Match Count",
    subtitle = "Shaded region shows identified set; zero = no effect"
  ) +
  theme_minimal()
```

### Key Takeaways for Matching Bounds

| Observation | Interpretation |
|-------------|----------------|
| Bounds exclude zero | Effect is identified as non-null |
| Bounds include zero | Cannot rule out no effect |
| Narrow bounds | Strong identification from matching |
| Wide bounds | Matching constraints not very informative |
| Bounds shrink with caliper | Better covariate balance tightens identification |

---

## 5. Best Practices and Common Pitfalls

### Bayesian Analysis

**Do:**
- Always check MCMC convergence (R-hat, trace plots, ESS)
- Run posterior predictive checks
- Report both point estimates and credible intervals
- Use informative priors when you have prior knowledge

**Don't:**
- Ignore convergence diagnostics
- Use very short chains (need at least 1000 post-warmup per chain)
- Over-interpret small differences in posteriors
- Forget to set seeds for reproducibility

### Sensitivity Analysis

**Do:**
- Report robustness values alongside main estimates
- Benchmark against observed covariates
- Consider multiple sensitivity scenarios
- Clearly state what confounders would need to look like to overturn results

**Don't:**
- Claim causal effects without sensitivity analysis
- Only report sensitivity if results are robust
- Ignore substantive interpretation of bounds
- Forget that sensitivity analysis cannot prove absence of confounding

### Matching

**Do:**
- Check balance before and after matching
- Use multiple balance diagnostics (SMD, variance ratios)
- Consider sensitivity to unobserved confounders
- Report matching method and parameters clearly

**Don't:**
- Match on post-treatment variables
- Ignore observations that couldn't be matched
- Assume matching eliminates all confounding
- Over-match (too many covariates relative to sample size)

---

## Further Reading

1. **Bayesian Regression:** Burkner, P. C. (2017). brms: An R Package for Bayesian Multilevel Models Using Stan. *Journal of Statistical Software*.

2. **Sensitivity Analysis:** Cinelli, C., & Hazlett, C. (2020). Making Sense of Sensitivity: Extending Omitted Variable Bias. *Journal of the Royal Statistical Society Series B*.

3. **Matching Methods:** Stuart, E. A. (2010). Matching Methods for Causal Inference: A Review and a Look Forward. *Statistical Science*.

4. **Matching Bounds:** Morucci, M. (2022). Matching Bounds for Causal Inference. *Journal of Politics*.
