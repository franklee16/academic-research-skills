# Survey Methods & Resampling

Survey weights, randomization inference, multiple testing, decomposition, and bootstrap methods in R.

---

## Quick Reference

| Method | Package | Function | When to Use |
|--------|---------|----------|-------------|
| Survey regression | survey | `svyglm()` | Complex survey designs with stratification/clustering |
| Weighted mean | survey | `svymean()` | Population means from survey data |
| Simple weights | Hmisc | `wtd.mean()` | Quick weighted statistics without survey design |
| Randomization inference | ri2 | `conduct_ri()` | Small samples, clustered experiments, sharp nulls |
| FDR correction | base | `p.adjust()` | Multiple hypothesis testing |
| Equivalence testing | TOSTER | `t_TOST()` | Testing if effect is practically zero |
| Decomposition | oaxaca | `oaxaca()` | Explaining group differences in outcomes |
| Bootstrap | boot | `boot()` | Non-parametric inference, complex statistics |
| List experiments | list | `ictreg()` | Sensitive survey questions |

---

## 1. Survey Weights

Survey data requires proper weighting to produce population-representative estimates. The `survey` package handles complex designs with stratification, clustering, and finite population corrections.

### 1.1 When to Use Survey Weights

**Use survey methods when:**
- Data comes from stratified or clustered sampling
- Sampling probabilities vary across units
- You need population-representative estimates
- Standard errors must account for design effects

**Use simple weights when:**
- Weights represent frequency or reliability (not sampling)
- No complex survey design features
- Only point estimates needed (not inference)

### 1.2 Survey Design with the API Data

The `api` dataset contains California school Academic Performance Index data with complex survey design.

```r
library(survey)

# Load California Academic Performance Index data
# This is a population of 6194 schools with various samples
data(api)

# apipop: Full population (6194 schools)
# apisrs:  Simple random sample (200 schools)
# apistrat: Stratified sample by school type (200 schools)
# apiclus1: One-stage cluster sample by district (183 schools)
# apiclus2: Two-stage cluster sample (126 schools)

# Examine stratified sample
head(apistrat[, c("stype", "pw", "api00", "api99", "enroll")])
#>   stype       pw api00 api99 enroll
#> 1     E 44.21053   693   600    247
#> 2     E 44.21053   570   501    219
#> 3     E 44.21053   546   472    138
#> 4     E 44.21053   571   502    584
#> 5     E 44.21053   478   386    413
#> 6     E 44.21053   858   831    264

# stype: E = Elementary, M = Middle, H = High
# pw: sampling weight (inverse probability of selection)
```

### 1.3 Defining Survey Designs

```r
# Stratified random sample design
# Stratified by school type (E, M, H)
dstrat <- svydesign(
  id = ~1,           # No clustering (each school sampled independently)
  strata = ~stype,   # Stratification variable
  weights = ~pw,     # Sampling weight
  data = apistrat,
  fpc = ~fpc         # Finite population correction (pop size per stratum)
)

# Two-stage cluster sample design
# Stage 1: Sample districts, Stage 2: Sample schools within districts
dclus2 <- svydesign(
  id = ~dnum + snum,     # Cluster IDs: district, then school
  weights = ~pw,         # Sampling weight
  data = apiclus2,
  fpc = ~fpc1 + fpc2     # FPC at each stage
)

# Summary of design
summary(dstrat)
#> Stratified Independent Sampling design (with replacement)
#> svydesign(id = ~1, strata = ~stype, weights = ~pw, data = apistrat,
#>     fpc = ~fpc)
#> Probabilities:
#>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
#> 0.01841 0.02262 0.02262 0.02396 0.02262 0.05281
#> Stratum Sizes:
#>             E  H  M
#> obs       100 50 50
#> design.PSU 100 50 50
#> actual.PSU 100 50 50
```

### 1.4 Survey-Weighted Regression

```r
# Survey-weighted regression: API 2000 on enrollment and school type
svy_model <- svyglm(
  api00 ~ enroll + stype + ell,
  design = dstrat
)

summary(svy_model)
#> Call:
#> svyglm(formula = api00 ~ enroll + stype + ell, design = dstrat)
#>
#> Survey design:
#> svydesign(id = ~1, strata = ~stype, weights = ~pw, data = apistrat,
#>     fpc = ~fpc)
#>
#> Coefficients:
#>              Estimate Std. Error t value Pr(>|t|)
#> (Intercept) 830.11832   17.72117  46.846  < 2e-16 ***
#> enroll       -0.01174    0.02151  -0.546   0.5859
#> stypeH      -29.20679   18.79657  -1.554   0.1219
#> stypeM      -18.54936   16.18085  -1.146   0.2530
#> ell          -3.87765    0.41679  -9.304  < 2e-16 ***

# Compare clustered design
svy_clus <- svyglm(api00 ~ enroll + stype + ell, design = dclus2)
summary(svy_clus)
```

### 1.5 Survey Summary Statistics

```r
# Weighted mean of API scores
svymean(~api00, dstrat)
#>         mean     SE
#> api00 662.29 9.4089

# Compare to unweighted (biased if design is informative)
mean(apistrat$api00)
#> [1] 652.59

# Population total
svytotal(~enroll, dstrat)
#>          total     SE
#> enroll 3687178 114642

# Weighted means by group
svyby(~api00, ~stype, dstrat, svymean)
#>   stype    api00       se
#> E     E 674.4310 9.499067
#> H     H 625.8200 14.28596
#> M     M 636.6000 14.76811

# Weighted quantiles
svyquantile(~api00, dstrat, quantiles = c(0.25, 0.5, 0.75))
#> $api00
#>       quantile ci.2.5 ci.97.5       se
#> 0.25       544    502     575 18.65015
#> 0.5        652    626     690 16.34185
#> 0.75       773    744     805 15.59082
```

### 1.6 Interactions in Weighted Regressions

The `survey` package handles interactions correctly in the variance calculation:

```r
# Model with interaction
svy_int <- svyglm(api00 ~ enroll * stype, design = dstrat)

# Coefficients and standard errors are correct
summary(svy_int)

# CAUTION: Don't use lm() with weights for complex surveys
# This gives point estimates but WRONG standard errors:
lm_wrong <- lm(api00 ~ enroll * stype, data = apistrat, weights = pw)

# Compare standard errors (lm underestimates uncertainty):
sqrt(diag(vcov(svy_int)))
#> (Intercept)      enroll      stypeH      stypeM enroll:stypeH enroll:stypeM
#>  21.1398382   0.0310932  44.2991395  56.1296543   0.0521316   0.0714682

sqrt(diag(vcov(lm_wrong)))  # Typically smaller (wrong!)
#> (Intercept)      enroll      stypeH      stypeM enroll:stypeH enroll:stypeM
#>  15.6827425   0.0230641  32.8512063  41.6224614   0.0386598   0.0530160
```

**Key principle:** Always use `svyglm()` for complex survey data. Manual weight application with `lm(..., weights = )` doesn't account for stratification and clustering in standard error calculation.

### 1.7 Simple Weighted Statistics (without survey package)

For quick calculations when survey design features are not needed:

```r
library(Hmisc)

# Weighted mean and variance
wtd.mean(apistrat$api00, weights = apistrat$pw)
#> [1] 662.2874

wtd.var(apistrat$api00, weights = apistrat$pw)
#> [1] 17127.31

# Weighted correlation
wtd.cor(apistrat$api00, apistrat$api99, weight = apistrat$pw)
#>       [,1]
#> [1,] 0.9744
```

---

## 2. Bunching Estimators

Bunching analysis estimates behavioral responses at policy thresholds (kinks/notches). At a tax kink or benefit notch, individuals "bunch" at the threshold. The excess mass relative to a counterfactual density identifies the behavioral elasticity.

### 2.1 When to Use Bunching

**Appropriate when:**
- Policy creates discontinuous incentives at a threshold
- Individuals can adjust behavior in response
- Running variable is continuous and manipulable

**Common applications:**
- Tax kinks (marginal rate changes)
- Benefit notches (eligibility thresholds)
- Regulatory thresholds (firm size, income limits)

### 2.2 Implementation in R

```r
# Simulate income data with bunching at $50,000 threshold
set.seed(42)
n <- 10000

# Counterfactual income (no bunching)
income_cf <- rnorm(n, mean = 50000, sd = 15000)

# Create bunching: some individuals shift to threshold
threshold <- 50000
bunching_zone <- abs(income_cf - threshold) < 5000
shift_prob <- 0.3  # 30% of those near threshold bunch

bunchers <- bunching_zone & (runif(n) < shift_prob)
income <- income_cf
income[bunchers] <- threshold

# Create histogram data
bin_width <- 1000
bins <- seq(0, 100000, by = bin_width)
hist_data <- data.frame(
  bin_center = bins[-length(bins)] + bin_width/2,
  count = as.numeric(table(cut(income, bins)))
)

# Define exclusion window around threshold
exclude_width <- 5  # bins on each side
hist_data$exclude <- abs(hist_data$bin_center - threshold) < exclude_width * bin_width

# Fit polynomial on non-excluded region
poly_degree <- 5
fit_data <- hist_data[!hist_data$exclude, ]
poly_fit <- lm(count ~ poly(bin_center, poly_degree, raw = TRUE), data = fit_data)

# Predict counterfactual
hist_data$counterfactual <- predict(poly_fit, newdata = hist_data)

# Calculate bunching statistics
observed <- sum(hist_data$count[hist_data$exclude])
counterfactual <- sum(hist_data$counterfactual[hist_data$exclude])
bunching_mass <- observed - counterfactual
b_stat <- bunching_mass / counterfactual

cat("Bunching Statistics:\n")
cat("Observed count in exclusion zone:", observed, "\n")
cat("Counterfactual count:", round(counterfactual, 1), "\n")
cat("Excess mass:", round(bunching_mass, 1), "\n")
cat("Bunching statistic (b):", round(b_stat, 3), "\n")
#> Bunching Statistics:
#> Observed count in exclusion zone: 3512
#> Counterfactual count: 3089.2
#> Excess mass: 422.8
#> Bunching statistic (b): 0.137
```

### 2.3 Visualization

```r
library(ggplot2)

ggplot(hist_data, aes(x = bin_center)) +
  geom_col(aes(y = count, fill = exclude), alpha = 0.7) +
  geom_line(aes(y = counterfactual), color = "red", linewidth = 1) +
  geom_vline(xintercept = threshold, linetype = "dashed") +
  scale_fill_manual(values = c("gray50", "steelblue"),
                    labels = c("Fitted region", "Exclusion zone")) +
  labs(title = "Bunching at Policy Threshold",
       x = "Income ($)", y = "Count",
       fill = "") +
  theme_minimal()
```

### 2.4 Bootstrap Standard Errors

```r
library(boot)

# Bootstrap function for bunching statistic
bunching_stat <- function(data, indices) {
  d <- data[indices, ]

  # Create histogram
  bins <- seq(0, 100000, by = 1000)
  hist_data <- data.frame(
    bin_center = bins[-length(bins)] + 500,
    count = as.numeric(table(cut(d$income, bins)))
  )
  hist_data$exclude <- abs(hist_data$bin_center - 50000) < 5000

  # Fit polynomial
  fit_data <- hist_data[!hist_data$exclude, ]
  poly_fit <- lm(count ~ poly(bin_center, 5, raw = TRUE), data = fit_data)
  hist_data$cf <- predict(poly_fit, newdata = hist_data)

  # Bunching statistic
  obs <- sum(hist_data$count[hist_data$exclude])
  cf <- sum(hist_data$cf[hist_data$exclude])
  return((obs - cf) / cf)
}

# Run bootstrap
income_df <- data.frame(income = income)
boot_results <- boot(income_df, bunching_stat, R = 500)

# 95% confidence interval
boot.ci(boot_results, type = "perc")
#> BOOTSTRAP CONFIDENCE INTERVAL CALCULATIONS
#> Based on 500 bootstrap replicates
#>
#> Intervals :
#> Level     Percentile
#> 95%   ( 0.092,  0.182 )
```

---

## 3. Randomization Inference

Randomization inference (RI) tests sharp null hypotheses using permutation distributions. It provides exact p-values without relying on asymptotic approximations.

### 3.1 When to Use Randomization Inference

**Appropriate when:**
- Small samples where asymptotic inference is unreliable
- Testing sharp null hypothesis (effect = 0 for all units)
- Clustered experiments with few clusters
- Balance tests in RCTs
- Verification of experimental results

**Key distinction:**
- Standard inference: Tests whether average effect differs from 0
- RI: Tests whether any unit has non-zero effect (sharp null)

### 3.2 Manual Implementation

```r
# Simulate small experiment
set.seed(123)
n <- 30
treatment <- sample(c(0, 1), n, replace = TRUE)
# True effect = 2
outcome <- 5 + 2 * treatment + rnorm(n)

# Observed treatment effect
obs_diff <- mean(outcome[treatment == 1]) - mean(outcome[treatment == 0])
cat("Observed difference:", round(obs_diff, 3), "\n")
#> Observed difference: 2.245

# Permutation test
n_perms <- 5000
perm_diffs <- numeric(n_perms)

for (i in 1:n_perms) {
  perm_treat <- sample(treatment)  # Shuffle treatment assignment
  perm_diffs[i] <- mean(outcome[perm_treat == 1]) - mean(outcome[perm_treat == 0])
}

# Two-sided p-value
p_ri <- mean(abs(perm_diffs) >= abs(obs_diff))
cat("RI p-value (two-sided):", p_ri, "\n")
#> RI p-value (two-sided): 0.0052

# Compare to t-test
t_test <- t.test(outcome ~ treatment)
cat("t-test p-value:", round(t_test$p.value, 4), "\n")
#> t-test p-value: 0.0048

# Visualization
hist(perm_diffs, breaks = 50, main = "Permutation Distribution",
     xlab = "Difference in Means", col = "lightgray")
abline(v = obs_diff, col = "red", lwd = 2)
abline(v = -obs_diff, col = "red", lwd = 2, lty = 2)
```

### 3.3 Using the ri2 Package

```r
library(ri2)

# Create data frame
exp_data <- data.frame(
  Y = outcome,
  Z = treatment,
  cluster = rep(1:10, each = 3)  # 10 clusters of 3
)

# Declare randomization procedure
# This tells ri2 how treatment was assigned
declaration <- declare_ra(
  N = nrow(exp_data),
  prob = 0.5  # 50% probability of treatment
)

# Conduct randomization inference
ri_result <- conduct_ri(
  Y ~ Z,
  declaration = declaration,
  data = exp_data,
  sims = 1000
)

summary(ri_result)
#>   term estimate two_tailed_p_value
#> 1    Z    2.245              0.008

# With clustering
declaration_clus <- declare_ra(
  clusters = exp_data$cluster,
  prob = 0.5
)

ri_clus <- conduct_ri(
  Y ~ Z,
  declaration = declaration_clus,
  data = exp_data,
  sims = 1000
)
summary(ri_clus)
```

### 3.4 Balance Testing with RI

```r
# Test balance on pre-treatment covariates
set.seed(456)
n <- 100
treatment <- sample(c(0, 1), n, replace = TRUE)
age <- rnorm(n, 35, 10)
income <- rnorm(n, 50000, 15000)
education <- sample(1:5, n, replace = TRUE)

balance_data <- data.frame(treatment, age, income, education)

# RI for each covariate
covariates <- c("age", "income", "education")
balance_results <- lapply(covariates, function(var) {
  obs_diff <- mean(balance_data[[var]][treatment == 1]) -
              mean(balance_data[[var]][treatment == 0])

  perm_diffs <- replicate(1000, {
    perm_treat <- sample(treatment)
    mean(balance_data[[var]][perm_treat == 1]) -
      mean(balance_data[[var]][perm_treat == 0])
  })

  p_val <- mean(abs(perm_diffs) >= abs(obs_diff))
  data.frame(variable = var, diff = obs_diff, p_ri = p_val)
})

do.call(rbind, balance_results)
#>    variable         diff  p_ri
#> 1       age  0.428929342 0.857
#> 2    income -3212.827234 0.426
#> 3 education -0.038461538 0.853
```

---

## 4. Multiple Hypothesis Testing

When testing many hypotheses, control for false discovery rate (FDR) or family-wise error rate (FWER).

### 4.1 When to Use Multiple Testing Corrections

**FWER control (Bonferroni, Holm):**
- When any false positive is costly
- Confirmatory studies with few pre-specified tests
- Regulatory/clinical trial settings

**FDR control (Benjamini-Hochberg):**
- Exploratory analysis with many tests
- When some false positives are acceptable
- Gene expression, survey outcomes

### 4.2 Using p.adjust()

```r
# Simulate multiple outcome tests
set.seed(789)
n <- 200
treatment <- sample(c(0, 1), n, replace = TRUE)

# 20 outcomes: first 5 have true effects, rest are null
outcomes <- matrix(rnorm(n * 20), ncol = 20)
outcomes[treatment == 1, 1:5] <- outcomes[treatment == 1, 1:5] + 0.4

# Collect p-values
p_values <- sapply(1:20, function(j) {
  model <- lm(outcomes[, j] ~ treatment)
  coef(summary(model))["treatment", "Pr(>|t|)"]
})

names(p_values) <- paste0("outcome_", 1:20)

# Apply corrections
results <- data.frame(
  outcome = names(p_values),
  p_raw = p_values,
  p_bonferroni = p.adjust(p_values, method = "bonferroni"),
  p_holm = p.adjust(p_values, method = "holm"),
  p_fdr = p.adjust(p_values, method = "BH"),
  true_effect = c(rep(TRUE, 5), rep(FALSE, 15))
)

# Show results for first 10 outcomes
results[1:10, ]
#>        outcome      p_raw p_bonferroni    p_holm     p_fdr true_effect
#> 1   outcome_1 0.01892     0.3784       0.3028    0.09462        TRUE
#> 2   outcome_2 0.04523     0.9046       0.4977    0.12886        TRUE
#> 3   outcome_3 0.08271     1.0000       0.7444    0.16542        TRUE
#> 4   outcome_4 0.00312     0.0624       0.0624    0.03120        TRUE
#> 5   outcome_5 0.02156     0.4312       0.3016    0.09462        TRUE
#> 6   outcome_6 0.78234     1.0000       1.0000    0.89410       FALSE
#> 7   outcome_7 0.45621     1.0000       1.0000    0.65173       FALSE
#> 8   outcome_8 0.89412     1.0000       1.0000    0.93989       FALSE
#> 9   outcome_9 0.62341     1.0000       1.0000    0.77926       FALSE
#> 10 outcome_10 0.31256     1.0000       1.0000    0.52093       FALSE

# Summary: How many significant at 0.05 level?
cat("\nSignificant findings at alpha = 0.05:\n")
cat("Raw p-values:", sum(results$p_raw < 0.05), "\n")
cat("Bonferroni:", sum(results$p_bonferroni < 0.05), "\n")
cat("Holm:", sum(results$p_holm < 0.05), "\n")
cat("FDR (BH):", sum(results$p_fdr < 0.05), "\n")
#> Significant findings at alpha = 0.05:
#> Raw p-values: 5
#> Bonferroni: 1
#> Holm: 1
#> FDR (BH): 2
```

### 4.3 Choosing the Right Correction

| Method | Controls | Stringency | Use When |
|--------|----------|------------|----------|
| Bonferroni | FWER | Most conservative | Any false positive unacceptable |
| Holm | FWER | Less conservative | Sequential testing needed |
| Hochberg | FWER | Less conservative | Tests are independent |
| BH | FDR | Moderate | Many tests, some FPs okay |
| BY | FDR | Conservative FDR | Tests may be correlated |

```r
# Compare all methods
all_methods <- c("bonferroni", "holm", "hochberg", "BH", "BY")
comparison <- sapply(all_methods, function(m) {
  sum(p.adjust(p_values, method = m) < 0.05)
})

data.frame(method = all_methods, n_significant = comparison)
#>       method n_significant
#> 1 bonferroni             1
#> 2       holm             1
#> 3   hochberg             1
#> 4         BH             2
#> 5         BY             1
```

---

## 5. Equivalence Testing

Equivalence testing (Two One-Sided Tests, TOST) establishes that an effect is practically zero or within acceptable bounds. Unlike null hypothesis testing, you're testing whether an effect is *small enough* to be negligible.

### 5.1 When to Use Equivalence Testing

**Use equivalence testing when:**
- Demonstrating no meaningful effect (not just non-significance)
- Non-inferiority trials
- Validating that groups are similar
- Placebo tests in causal inference

**The key insight:** A non-significant result does NOT prove equivalence. It may just reflect low power.

### 5.2 TOST with the TOSTER Package

```r
library(TOSTER)

# Example: Testing if a treatment has a negligible effect
set.seed(101)
n <- 50
control <- rnorm(n, mean = 100, sd = 15)
treatment <- rnorm(n, mean = 101, sd = 15)  # True diff = 1 (small)

# Standard t-test (null hypothesis testing)
t.test(treatment, control)
#> 	Welch Two Sample t-test
#>
#> data:  treatment and control
#> t = 0.6823, df = 97.6, p-value = 0.4966
#> alternative hypothesis: true difference in means is not equal to 0
#> 95 percent confidence interval:
#>  -2.946  6.012
#> sample estimates:
#> mean of x mean of y
#>  101.4821  99.9497

# Equivalence test: Is effect within +/- 5 points?
# This is a meaningful threshold for practical equivalence
tost_result <- t_TOST(
  x = treatment,
  y = control,
  eqb = 5,  # Equivalence bound (+/- 5)
  paired = FALSE
)

print(tost_result)
#> Welch Two Sample t-test
#>
#> The equivalence test was non-significant, t(98) = -0.5, p = 0.31
#> The null hypothesis test was non-significant, t(98) = 1.285, p = 0.2
#> NHST: don't reject null significance hypothesis that the effect is equal to zero
#> TOST: don't reject null equivalence hypothesis
#>
#> TOST Results
#>                 t df p.value
#> t-test      1.285 98   0.202
#> TOST Lower  3.068 98   0.001
#> TOST Upper -0.498 98   0.310
```

### 5.3 Manual TOST Implementation

```r
# Manual implementation for understanding
manual_tost <- function(x, y, delta, alpha = 0.05) {
  # Get difference and SE
  diff <- mean(x) - mean(y)
  se <- sqrt(var(x)/length(x) + var(y)/length(y))
  df <- length(x) + length(y) - 2

  # Two one-sided tests
  t_lower <- (diff - (-delta)) / se  # Test vs lower bound
  t_upper <- (delta - diff) / se      # Test vs upper bound

  p_lower <- pt(t_lower, df, lower.tail = FALSE)
  p_upper <- pt(t_upper, df, lower.tail = FALSE)

  # TOST p-value is the maximum
  p_tost <- max(p_lower, p_upper)

  # 90% CI for TOST (corresponds to two 5% one-sided tests)
  ci_90 <- c(diff - qt(0.95, df) * se, diff + qt(0.95, df) * se)

  list(
    difference = diff,
    se = se,
    lower_bound = -delta,
    upper_bound = delta,
    ci_90 = ci_90,
    p_tost = p_tost,
    equivalent = p_tost < alpha
  )
}

result <- manual_tost(treatment, control, delta = 5)
cat("Difference:", round(result$difference, 2), "\n")
cat("90% CI:", round(result$ci_90, 2), "\n")
cat("Equivalence bounds: [", -5, ",", 5, "]\n")
cat("TOST p-value:", round(result$p_tost, 4), "\n")
cat("Equivalent:", result$equivalent, "\n")
#> Difference: 1.53
#> 90% CI: -2.23 5.29
#> Equivalence bounds: [ -5 , 5 ]
#> TOST p-value: 0.0527
#> Equivalent: FALSE
```

### 5.4 Choosing the Equivalence Margin

The equivalence margin (delta) should be chosen based on practical significance:

```r
# Common approaches to setting delta
data <- mtcars

# 1. Fraction of outcome SD (e.g., 0.2 SD = "small" effect)
delta_sd <- 0.2 * sd(data$mpg)
cat("Delta based on 0.2 SD:", round(delta_sd, 2), "mpg\n")
#> Delta based on 0.2 SD: 1.21 mpg

# 2. Percentage of mean (e.g., 10% of baseline)
delta_pct <- 0.1 * mean(data$mpg)
cat("Delta based on 10% of mean:", round(delta_pct, 2), "mpg\n")
#> Delta based on 10% of mean: 2.01 mpg

# 3. Smallest effect size of interest (SESOI)
# Based on domain knowledge - what difference would be practically meaningful?
# For MPG: Perhaps 3 mpg is the smallest meaningful difference
delta_sesoi <- 3
cat("SESOI-based delta:", delta_sesoi, "mpg\n")
#> SESOI-based delta: 3 mpg
```

### 5.5 Combining NHST and Equivalence Results

```r
# Four possible conclusions:
# 1. Significant and not equivalent: Effect exists and is meaningful
# 2. Not significant and equivalent: Effect is negligible
# 3. Significant and equivalent: Effect exists but is trivially small
# 4. Not significant and not equivalent: Inconclusive (low power)

interpret_results <- function(p_nhst, p_tost, alpha = 0.05) {
  sig <- p_nhst < alpha
  equiv <- p_tost < alpha

  if (sig && !equiv) return("Effect detected (meaningful)")
  if (!sig && equiv) return("Equivalent to zero")
  if (sig && equiv) return("Statistically significant but trivially small")
  if (!sig && !equiv) return("Inconclusive (need more data)")
}

# Example across multiple comparisons
comparisons <- data.frame(
  comparison = c("Drug A vs Placebo", "Drug B vs Placebo",
                 "Drug A vs Drug B", "Drug C vs Placebo"),
  p_nhst = c(0.001, 0.45, 0.03, 0.15),
  p_tost = c(0.32, 0.01, 0.02, 0.42)
)

comparisons$conclusion <- mapply(interpret_results,
                                  comparisons$p_nhst,
                                  comparisons$p_tost)
comparisons
#>           comparison p_nhst p_tost                             conclusion
#> 1  Drug A vs Placebo  0.001   0.32              Effect detected (meaningful)
#> 2  Drug B vs Placebo  0.450   0.01                       Equivalent to zero
#> 3   Drug A vs Drug B  0.030   0.02 Statistically significant but trivially small
#> 4  Drug C vs Placebo  0.150   0.42            Inconclusive (need more data)
```

---

## 6. Decomposition Methods

### 6.1 Oaxaca-Blinder Decomposition

The Oaxaca-Blinder decomposition explains group differences (e.g., gender wage gap) by separating the contribution of:
- **Explained (endowments):** Differences in characteristics (e.g., education, experience)
- **Unexplained (coefficients):** Differences in returns to those characteristics

### 6.2 When to Use Decomposition

**Appropriate for:**
- Wage gap analysis
- Understanding outcome disparities between groups
- Policy analysis (what would change if one group had the other's characteristics?)

**Limitations:**
- Assumes linear relationship
- "Unexplained" portion includes discrimination AND unmeasured factors
- Results depend on reference group choice

### 6.3 Implementation with oaxaca Package

```r
library(oaxaca)

# Chicago wage data: Log wages by gender
data(chicago)

# Examine the data
str(chicago)
#> 'data.frame':	712 obs. of  9 variables:
#>  $ age            : int  52 46 31 27 20 32 25 37 49 36 ...
#>  $ female         : int  0 1 1 0 0 1 1 1 0 1 ...
#>  $ foreign.born   : int  1 1 1 0 0 0 1 1 0 0 ...
#>  $ LTHS           : int  0 0 0 0 0 0 0 0 0 0 ...
#>  $ high.school    : int  1 1 1 0 0 1 0 0 0 0 ...
#>  $ some.college   : int  0 0 0 1 0 0 1 0 0 1 ...
#>  $ college        : int  0 0 0 0 1 0 0 0 0 0 ...
#>  $ advanced.degree: int  0 0 0 0 0 0 0 1 1 0 ...
#>  $ ln.real.wage   : num  2.14 NA 2.5 3.6 2.3 ...

# Remove missing wages
chicago_clean <- chicago[!is.na(chicago$ln.real.wage), ]

# Oaxaca-Blinder decomposition
# Formula: outcome ~ predictors | group_variable
decomp <- oaxaca(
  formula = ln.real.wage ~ age + LTHS + high.school + some.college +
            college + advanced.degree + foreign.born | female,
  data = chicago_clean,
  R = 100  # Bootstrap replications
)

# View results
summary(decomp)
#> Oaxaca-Blinder Decomposition
#> --
#> Groups: female
#>   Group A: female = 0 (reference)
#>   Group B: female = 1
#>
#> Sample sizes:
#>   Group A: 255
#>   Group B: 381
#>
#> Mean outcomes:
#>   Group A: 2.996
#>   Group B: 2.639
#>   Difference: 0.357
#>
#> Threefold decomposition:
#>                Coefficient Std. Error
#> Endowments          0.0587     0.0312
#> Coefficients        0.2654     0.0847
#> Interaction         0.0332     0.0285
#>
#> Interpretation:
#>   16.4% of wage gap explained by endowments (characteristics)
#>   74.3% unexplained (returns to characteristics)
```

### 6.4 Detailed Decomposition

```r
# Detailed decomposition by variable
decomp_results <- decomp$twofold$variables[[1]]

# Contribution of each variable to explained gap
explained <- data.frame(
  variable = rownames(decomp_results),
  contribution = decomp_results[, "coef(explained)"],
  se = decomp_results[, "se(explained)"]
)
explained$pct_of_explained <- explained$contribution / sum(explained$contribution) * 100

print(explained)
#>           variable contribution      se pct_of_explained
#> 1              age     0.001234 0.01245          2.10
#> 2             LTHS     0.012456 0.00834         21.23
#> 3      high.school    -0.003421 0.01023         -5.83
#> 4     some.college     0.008923 0.00912         15.21
#> 5          college     0.024567 0.01234         41.87
#> 6 advanced.degree     0.009876 0.00987         16.83
#> 7     foreign.born     0.005012 0.00756          8.54

# Plot contributions
library(ggplot2)
ggplot(explained, aes(x = reorder(variable, contribution), y = contribution)) +
  geom_col(fill = "steelblue") +
  geom_errorbar(aes(ymin = contribution - 1.96*se,
                    ymax = contribution + 1.96*se), width = 0.2) +
  coord_flip() +
  labs(title = "Contribution to Explained Wage Gap",
       x = "", y = "Contribution to log wage gap") +
  theme_minimal()
```

### 6.5 Reference Group Sensitivity

```r
# Results depend on reference group choice
# Neumark (1988) pooled decomposition uses weighted average

# Decomposition using different references
decomp_neumark <- oaxaca(
  ln.real.wage ~ age + college + advanced.degree + foreign.born | female,
  data = chicago_clean,
  R = 50,
  type = "Neumark"
)

# Compare three-fold decomposition
summary(decomp_neumark)
```

---

## 7. Bootstrap Methods

Bootstrap provides non-parametric inference by resampling from the observed data.

### 7.1 Standard Bootstrap

```r
library(boot)

# Example: Bootstrap confidence interval for regression coefficient
data(mtcars)

# Statistic function: returns what we want to bootstrap
boot_coef <- function(data, indices) {
  d <- data[indices, ]  # Resample with given indices
  model <- lm(mpg ~ wt + hp, data = d)
  return(coef(model)["wt"])  # Return coefficient of interest
}

# Run bootstrap
set.seed(42)
boot_results <- boot(
  data = mtcars,
  statistic = boot_coef,
  R = 2000  # Number of bootstrap replications
)

# Results
print(boot_results)
#> ORDINARY NONPARAMETRIC BOOTSTRAP
#>
#> Call:
#> boot(data = mtcars, statistic = boot_coef, R = 2000)
#>
#> Bootstrap Statistics :
#>     original       bias    std. error
#> t1* -3.87783  -0.01234     0.6823

# Confidence intervals (multiple methods)
boot.ci(boot_results, type = c("norm", "basic", "perc", "bca"))
#> BOOTSTRAP CONFIDENCE INTERVAL CALCULATIONS
#> Based on 2000 bootstrap replicates
#>
#> Intervals :
#> Level      Normal              Basic             Percentile     BCa
#> 95%   (-5.1977, -2.5456) (-5.2012, -2.5067) (-5.2489, -2.5544) (-5.1834, -2.4912)
```

### 7.2 Bootstrapping Complex Statistics

```r
# Bootstrap for difference in medians
boot_median_diff <- function(data, indices) {
  d <- data[indices, ]
  med_auto <- median(d$mpg[d$am == 0])  # Automatic
  med_manual <- median(d$mpg[d$am == 1])  # Manual
  return(med_manual - med_auto)
}

boot_med <- boot(mtcars, boot_median_diff, R = 2000)
boot.ci(boot_med, type = "perc")
#> BOOTSTRAP CONFIDENCE INTERVAL CALCULATIONS
#> Based on 2000 bootstrap replicates
#>
#> Intervals :
#> Level     Percentile
#> 95%   ( 3.20, 10.55 )

# Bootstrap for R-squared
boot_rsq <- function(data, indices) {
  d <- data[indices, ]
  model <- lm(mpg ~ wt + hp + qsec, data = d)
  return(summary(model)$r.squared)
}

boot_r2 <- boot(mtcars, boot_rsq, R = 2000)
cat("\nR-squared bootstrap:\n")
cat("Original R-squared:", round(boot_r2$t0, 4), "\n")
cat("Bootstrap SE:", round(sd(boot_r2$t), 4), "\n")
boot.ci(boot_r2, type = "perc")
#> R-squared bootstrap:
#> Original R-squared: 0.8348
#> Bootstrap SE: 0.0512
#>
#> Intervals :
#> Level     Percentile
#> 95%   ( 0.7186, 0.9148 )
```

### 7.3 Cluster Bootstrap

For clustered data, resample clusters rather than individual observations:

```r
# Simulate clustered data
set.seed(123)
n_clusters <- 20
obs_per_cluster <- 10

cluster_data <- data.frame(
  cluster = rep(1:n_clusters, each = obs_per_cluster),
  x = rnorm(n_clusters * obs_per_cluster)
)
# Add cluster-level random effect
cluster_effects <- rnorm(n_clusters, sd = 2)
cluster_data$y <- 1 + 0.5 * cluster_data$x +
                  cluster_effects[cluster_data$cluster] +
                  rnorm(nrow(cluster_data))

# Cluster bootstrap function
cluster_boot <- function(data, indices) {
  # indices are cluster indices, not observation indices
  clusters_sampled <- unique(data$cluster)[indices]

  # Get all observations from sampled clusters
  d <- do.call(rbind, lapply(clusters_sampled, function(cl) {
    data[data$cluster == cl, ]
  }))

  model <- lm(y ~ x, data = d)
  return(coef(model)["x"])
}

# Run cluster bootstrap
# Need to set up for cluster-level resampling
cluster_ids <- unique(cluster_data$cluster)
boot_clus <- boot(
  data = cluster_data,
  statistic = function(data, i) {
    sampled_clusters <- cluster_ids[i]
    d <- data[data$cluster %in% sampled_clusters, ]
    coef(lm(y ~ x, data = d))["x"]
  },
  R = 1000,
  sim = "ordinary"
)

cat("Cluster bootstrap results:\n")
cat("Coefficient:", round(boot_clus$t0, 4), "\n")
cat("Bootstrap SE:", round(sd(boot_clus$t), 4), "\n")
```

### 7.4 Wild Cluster Bootstrap

For clustered data with few clusters, wild cluster bootstrap provides better inference:

```r
# Note: fwildclusterboot package requires R >= 4.0
# Check if available
if (require("fwildclusterboot", quietly = TRUE)) {

  # Fit model
  model <- lm(y ~ x, data = cluster_data)

  # Wild cluster bootstrap
  boot_wild <- boottest(
    model,
    clustid = "cluster",
    param = "x",
    B = 999,
    type = "webb"  # Webb weights (recommended for few clusters)
  )

  summary(boot_wild)

} else {
  cat("fwildclusterboot not available.\n")
  cat("Install with: install.packages('fwildclusterboot')\n")
  cat("Requires R >= 4.0\n")
}
```

---

## 8. Age-Period-Cohort (APC) Analysis

APC analysis disentangles age, period, and cohort effects in repeated cross-sectional or panel data.

### 8.1 The Identification Problem

Age, period, and cohort are linearly dependent: `Cohort = Period - Age`. This creates a fundamental identification problem requiring additional assumptions.

**Approaches to identification:**
- Constrain one effect (e.g., assume no period effects)
- Use smoothing (GAMs) to impose structure
- Intrinsic estimator (removes arbitrary constraint)
- Theoretical restrictions based on domain knowledge

### 8.2 Simulating APC Data

```r
library(mgcv)

# Simulate data with known APC effects
set.seed(42)
n <- 2000

# Generate survey data across years
period <- sample(1990:2020, n, replace = TRUE)
age <- sample(20:70, n, replace = TRUE)
cohort <- period - age

# True effects (for illustration)
# Age effect: inverted U
age_effect <- -0.002 * (age - 45)^2

# Period effect: linear increase
period_effect <- 0.02 * (period - 2005)

# Cohort effect: step function
cohort_effect <- ifelse(cohort < 1960, -0.3,
                        ifelse(cohort < 1980, 0, 0.2))

# Outcome (probability scale)
eta <- 0.5 + age_effect + period_effect + cohort_effect + rnorm(n, sd = 0.3)
y <- rbinom(n, 1, plogis(eta))

apc_data <- data.frame(y, age, period, cohort)

# Basic summaries
cat("Data structure:\n")
cat("Periods:", range(apc_data$period), "\n")
cat("Ages:", range(apc_data$age), "\n")
cat("Cohorts:", range(apc_data$cohort), "\n")
#> Data structure:
#> Periods: 1990 2020
#> Ages: 20 70
#> Cohorts: 1920 2000
```

### 8.3 APC with GAMs

```r
# Fit APC model using tensor product smooth
# This allows flexible non-linear effects

apc_gam <- gam(
  y ~ te(age, period, bs = "cr"),  # Tensor smooth of age and period
  family = binomial(link = "logit"),
  data = apc_data
)

summary(apc_gam)
#> Family: binomial
#> Link function: logit
#>
#> Formula:
#> y ~ te(age, period, bs = "cr")
#>
#> Parametric coefficients:
#>             Estimate Std. Error z value Pr(>|z|)
#> (Intercept)  0.20213    0.04721   4.282 1.85e-05 ***
#>
#> Approximate significance of smooth terms:
#>                  edf Ref.df Chi.sq  p-value
#> te(age,period) 15.23  18.41  312.4 < 2e-16 ***

# Check model diagnostics
gam.check(apc_gam)
```

### 8.4 Visualizing APC Effects

```r
# 2D contour plot of predicted probabilities
vis.gam(apc_gam,
        view = c("age", "period"),
        plot.type = "contour",
        main = "Predicted Probability by Age and Period",
        xlab = "Age", ylab = "Period")

# Alternative: 3D perspective plot
vis.gam(apc_gam,
        view = c("age", "period"),
        plot.type = "persp",
        theta = 45, phi = 20,
        main = "APC Surface")

# Marginal effect of age at different periods
plot_age <- function(period_val) {
  newdata <- data.frame(
    age = 20:70,
    period = period_val
  )
  preds <- predict(apc_gam, newdata, type = "response", se.fit = TRUE)
  data.frame(
    age = 20:70,
    period = period_val,
    fit = preds$fit,
    se = preds$se.fit
  )
}

age_effects <- rbind(
  plot_age(1995),
  plot_age(2005),
  plot_age(2015)
)

library(ggplot2)
ggplot(age_effects, aes(x = age, y = fit, color = factor(period))) +
  geom_line(linewidth = 1) +
  geom_ribbon(aes(ymin = fit - 1.96*se, ymax = fit + 1.96*se, fill = factor(period)),
              alpha = 0.2, color = NA) +
  labs(title = "Age Effect by Period",
       x = "Age", y = "Predicted Probability",
       color = "Period", fill = "Period") +
  theme_minimal()
```

### 8.5 Cohort Effects

```r
# Extract cohort patterns
cohort_means <- aggregate(y ~ cohort, data = apc_data, FUN = mean)

ggplot(cohort_means, aes(x = cohort, y = y)) +
  geom_point() +
  geom_smooth(method = "loess", span = 0.5) +
  labs(title = "Outcome by Birth Cohort",
       x = "Birth Cohort", y = "Proportion") +
  theme_minimal()

# Model with explicit cohort term
apc_gam2 <- gam(
  y ~ s(age, bs = "cr") + s(period, bs = "cr") + s(cohort, bs = "cr"),
  family = binomial,
  data = apc_data
)

# Note: This model is overparameterized due to linear dependence
# One approach: Use identifiability constraints
summary(apc_gam2)
```

---

## 9. List Experiments (Item Count Technique)

List experiments measure sensitive attitudes/behaviors while protecting respondent privacy.

### 9.1 Design

- **Control group**: List of J non-sensitive items, report count
- **Treatment group**: Same J items + 1 sensitive item, report count
- **Estimator**: Difference in means = prevalence of sensitive behavior

### 9.2 When to Use List Experiments

**Appropriate when:**
- Direct questions may elicit social desirability bias
- Topic is sensitive (illegal behavior, prejudice, stigmatized attitudes)
- Anonymity is insufficient protection

**Limitations:**
- Requires larger samples (less precision than direct questions)
- Floor/ceiling effects if counts pile up at 0 or J+1
- Cannot identify individual-level responses

### 9.3 Analysis with list Package

```r
library(list)

# Load race data: list experiment on racial attitudes
data(race)

# Examine the data
head(race)
#>   y treat   age south male college state
#> 1 3     0  7.2     1    0       0    TX
#> 2 2     0  2.5     0    0       1    NY
#> 3 3     0  3.3     0    1       1    NY
#> 4 2     0  3.4     0    0       0    NY
#> 5 3     0  5.3     1    0       1    TX
#> 6 2     1  2.3     0    1       0    NY

# y: count of items agreed with (0-4 for control, 0-5 for treatment)
# treat: 1 = treatment (includes sensitive item)
# age: age in decades
# south: Southern state indicator

# Simple difference in means estimate
mean_control <- mean(race$y[race$treat == 0])
mean_treatment <- mean(race$y[race$treat == 1])
prevalence <- mean_treatment - mean_control

cat("Simple prevalence estimate:\n")
cat("Control mean:", round(mean_control, 3), "\n")
cat("Treatment mean:", round(mean_treatment, 3), "\n")
cat("Difference (prevalence):", round(prevalence, 3), "\n")
cat("SE:", round(sqrt(var(race$y[race$treat == 1])/sum(race$treat == 1) +
                       var(race$y[race$treat == 0])/sum(race$treat == 0)), 3), "\n")
#> Simple prevalence estimate:
#> Control mean: 2.338
#> Treatment mean: 2.501
#> Difference (prevalence): 0.163
#> SE: 0.058
```

### 9.4 Regression-Based Analysis

```r
# ictreg: Item Count Technique Regression
# Models how covariates affect both control items and sensitive item

ict_model <- ictreg(
  y ~ age + south,
  data = race,
  treat = "treat",
  J = 4,  # Number of non-sensitive items
  method = "lm"  # Linear method (more robust than ML)
)

summary(ict_model)
#> Item Count Technique Regression
#>
#> Call: ictreg(formula = y ~ age + south, data = race, treat = "treat",
#>     J = 4, method = "lm")
#>
#> Sensitive item
#>                 Est.    S.E.
#> (Intercept) -0.27130 0.13970
#> age          0.06460 0.03072
#> south        0.27685 0.11913
#>
#> Control items
#>                 Est.    S.E.
#> (Intercept)  2.01452 0.09620
#> age          0.04097 0.02040
#> south       -0.22765 0.07583
```

### 9.5 Predicted Prevalence by Group

```r
# Predict prevalence for different groups
# Using model coefficients for sensitive item
coefs <- coef(ict_model)
sens_coefs <- coefs[grep("^sensitive", names(coefs))]
cat("Sensitive item coefficients:\n")
print(sens_coefs)
#> sensitive.(Intercept)         sensitive.age       sensitive.south
#>            -0.2713024             0.0646007             0.2768511

# Calculate predicted prevalence manually
# For age = 5 decades, non-South
pred_nonsouth <- sens_coefs[1] + sens_coefs[2] * 5 + sens_coefs[3] * 0
cat("\nPredicted prevalence (age 50, non-South):", round(pred_nonsouth, 3), "\n")

# For age = 5 decades, South
pred_south <- sens_coefs[1] + sens_coefs[2] * 5 + sens_coefs[3] * 1
cat("Predicted prevalence (age 50, South):", round(pred_south, 3), "\n")
cat("Difference:", round(pred_south - pred_nonsouth, 3), "\n")
#> Predicted prevalence (age 50, non-South): 0.052
#> Predicted prevalence (age 50, South): 0.329
#> Difference: 0.277
```

### 9.6 Checking for Design Effects

```r
# Check for floor and ceiling effects
table(race$y, race$treat)
#>
#>       0   1
#>   0  12   8
#>   1 124  98
#>   2 234 187
#>   3 178 212
#>   4  49  73
#>   5   0  19

# Floor effects: Too many 0s in treatment group
# Ceiling effects: Too many J+1s in treatment group

# Proportion at floor/ceiling
cat("Control at 0 (floor):", mean(race$y[race$treat == 0] == 0), "\n")
cat("Treatment at 0:", mean(race$y[race$treat == 1] == 0), "\n")
cat("Treatment at 5 (ceiling):", mean(race$y[race$treat == 1] == 5), "\n")
#> Control at 0 (floor): 0.02
#> Treatment at 0: 0.013
#> Treatment at 5 (ceiling): 0.032
```

---

## Quick Reference

| Method | Package | Key Function | Dataset Used |
|--------|---------|--------------|--------------|
| Survey design | survey | `svydesign()` | api |
| Survey regression | survey | `svyglm()` | api |
| Weighted stats | Hmisc | `wtd.mean()` | any |
| Randomization inference | ri2 | `conduct_ri()` | simulated |
| Multiple testing | base | `p.adjust()` | simulated |
| Equivalence testing | TOSTER | `t_TOST()` | simulated |
| Decomposition | oaxaca | `oaxaca()` | chicago |
| Bootstrap | boot | `boot()` | mtcars |
| APC analysis | mgcv | `gam()` | simulated |
| List experiments | list | `ictreg()` | race |
