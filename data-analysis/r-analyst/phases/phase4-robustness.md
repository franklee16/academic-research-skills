# Phase 4: Robustness & Sensitivity

You are executing Phase 4 of a statistical analysis in R. Your goal is to stress-test the main findings through robustness checks and sensitivity analysis.

## Why This Phase Matters

Main results are only as credible as their robustness. Reviewers will ask: "How do you know this isn't driven by [X]?" This phase pre-empts those questions and honestly assesses the fragility of the findings.

## Technique Guides

**Consult these guides** in `r-statistical-techniques/` for robustness code patterns:

| Topic | Guide |
|-------|-------|
| Sensitivity to unobservables | `05_bayesian_sensitivity.md` (sensemakr section) |
| DiD robustness, Event studies | `01_core_econometrics.md` |
| Bootstrap, Resampling | `02_survey_resampling.md` |
| Matching diagnostics | `01_core_econometrics.md` Section 6 |

## Your Tasks

### 1. Alternative Specifications

Run the pre-specified alternatives from Phase 2:

**Different control sets:**
```r
# Minimal controls
robust_minimal <- feols(outcome ~ treatment | fe, cluster = ~cluster_var, data = data)

# Extended controls
robust_extended <- feols(outcome ~ treatment + extra_controls | fe,
                         cluster = ~cluster_var, data = data)

# Different functional form
robust_log <- feols(log(outcome) ~ treatment | fe, cluster = ~cluster_var, data = data)
```

**Different fixed effects:**
```r
# Unit-by-year FE (more demanding)
robust_fe <- feols(outcome ~ treatment | unit^year, cluster = ~cluster_var, data = data)

# Region-by-year FE
robust_region <- feols(outcome ~ treatment | region^year + unit,
                       cluster = ~cluster_var, data = data)
```

**Different standard errors:**
```r
# Compare clustering levels
summary(main_model, cluster = ~unit)
summary(main_model, cluster = ~state)
summary(main_model, cluster = ~unit + year)
```

### 2. Placebo Tests

**Pre-treatment effects (for DiD/Event Study):**
```r
# Should see no effect before treatment
pre_data <- data %>% filter(year < treatment_year)
placebo_pre <- feols(outcome ~ fake_treatment | unit + year,
                     cluster = ~unit, data = pre_data)
```

**Fake treatment timing:**
```r
# Assign treatment X years earlier—should find no effect
data <- data %>%
  mutate(fake_treated = treated_post & year >= (treatment_year - 3))

placebo_timing <- feols(outcome ~ fake_treated | unit + year,
                        cluster = ~unit, data = data)
```

**Outcome that shouldn't be affected:**
```r
# If treatment affects X, it shouldn't affect unrelated Y
placebo_outcome <- feols(unrelated_outcome ~ treatment | unit + year,
                         cluster = ~unit, data = data)
```

### 3. Missing Data Assessment

Before running sensitivity analyses, document and address missing data:

**Document Missingness:**
```r
# Overall missingness rates
sapply(analysis_data, function(x) mean(is.na(x))) |>
  sort(decreasing = TRUE) |>
  head(10)

# Missingness by key variables
analysis_data %>%
  group_by(treatment) %>%
  summarise(across(everything(), ~mean(is.na(.))))
```

**Test for MCAR/MAR:**
```r
library(naniar)

# Visualize missingness patterns
vis_miss(analysis_data)
gg_miss_upset(analysis_data)

# Little's MCAR test (if needed)
library(mice)
mcar_test(analysis_data)
```

**Multiple Imputation (if substantial missingness):**
```r
library(mice)

# Use adequate number of imputations (m ≥ 20, preferably ≥ 50)
imp <- mice(analysis_data, m = 50, method = 'pmm', seed = 12345,
            printFlag = FALSE)

# Check imputation diagnostics
densityplot(imp)  # Compare imputed vs observed distributions
stripplot(imp)

# Run analysis on imputed datasets and pool
fit_imp <- with(imp, lm(outcome ~ treatment + control1 + control2))
pooled <- pool(fit_imp)
summary(pooled)

# Include auxiliary variables to strengthen MAR assumption
# These are variables that predict missingness or the outcome
```

**Compare Missing Data Approaches:**
```r
# Create comparison table
missing_comparison <- list(
  "Complete case" = main_model,
  "Multiple imputation" = pooled_model,
  "Single imputation" = single_imp_model  # if applicable
)

modelsummary(missing_comparison,
             output = "output/tables/missing_data_sensitivity.tex",
             title = "Sensitivity to Missing Data Treatment")
```

**Report in Methods Section:**
```markdown
[X]% of observations were missing on [variable]. We tested for patterns
of missingness and found [MCAR/MAR/evidence of MNAR]. Our primary analysis
uses [complete case / multiple imputation with m = X imputations].
Sensitivity analyses comparing complete case, single imputation, and
multiple imputation show [results are robust / estimates differ by X].
```

### 4. Sensitivity Analysis

**Sensitivity to outliers:**
```r
# Winsorize extreme values
library(DescTools)
data$outcome_w <- Winsorize(data$outcome, probs = c(0.01, 0.99))
robust_winsor <- feols(outcome_w ~ treatment | fe, cluster = ~cluster_var, data = data)

# Drop extreme observations
data_trimmed <- data %>% filter(outcome > quantile(outcome, 0.01) &
                                 outcome < quantile(outcome, 0.99))
robust_trim <- feols(outcome ~ treatment | fe, cluster = ~cluster_var, data = data_trimmed)
```

**Sensitivity to sample restrictions:**
```r
# Different time periods
robust_early <- feols(outcome ~ treatment | fe, data = filter(data, year <= 2015))
robust_late <- feols(outcome ~ treatment | fe, data = filter(data, year > 2015))

# Excluding specific units
robust_exclude <- feols(outcome ~ treatment | fe, data = filter(data, !outlier_unit))
```

**Selection on unobservables (sensemakr):**
```r
library(sensemakr)

# Fit OLS version for sensemakr
ols_model <- lm(outcome ~ treatment + controls, data = data)

# Sensitivity analysis
sens <- sensemakr(
  model = ols_model,
  treatment = "treatment",
  benchmark_covariates = c("strongest_control"),
  kd = 1:3  # How strong would confounding need to be?
)

# Summary
summary(sens)

# Plot
plot(sens)
ggsave("output/figures/sensitivity_plot.pdf", width = 8, height = 6)
```

### 4. Subgroup Analysis

Run pre-specified heterogeneity analyses:

```r
# By group
robust_subgroup1 <- feols(outcome ~ treatment | fe,
                          data = filter(data, subgroup == 1))
robust_subgroup2 <- feols(outcome ~ treatment | fe,
                          data = filter(data, subgroup == 2))

# Interaction approach (preferred)
robust_het <- feols(outcome ~ treatment * subgroup_var | fe,
                    cluster = ~cluster_var, data = data)

# Visualize heterogeneity
library(marginaleffects)
het_effects <- slopes(robust_het, variables = "treatment", by = "subgroup_var")
plot(het_effects)
```

### 5. Panel/Longitudinal Data Robustness (If Applicable)

**Attrition Analysis:**
```r
# Document attrition rates by wave
attrition_table <- data %>%
  group_by(wave) %>%
  summarise(n = n_distinct(id),
            pct_remaining = n / first(n) * 100)

# Test if attrition is related to treatment or outcomes
attrition_model <- glm(dropped_out ~ treatment + baseline_outcome + covariates,
                       family = binomial, data = baseline_data)
summary(attrition_model)
```

**Inverse Probability Weighting for Selection:**
```r
library(ipw)

# Estimate selection weights
ps_model <- glm(observed ~ treatment + covariates, family = binomial, data = data)
weights <- 1 / predict(ps_model, type = "response")

# Apply weights in main analysis
robust_ipw <- feols(outcome ~ treatment | unit + time,
                    weights = ~weights, data = data)
```

**Fixed vs Random Effects:**
```r
library(plm)

# Hausman test
fe_model <- plm(outcome ~ treatment + covariates, model = "within",
                index = c("id", "time"), data = data)
re_model <- plm(outcome ~ treatment + covariates, model = "random",
                index = c("id", "time"), data = data)
phtest(fe_model, re_model)  # p < 0.05 suggests FE preferred

# Within-between decomposition (correlated random effects)
data <- data %>%
  group_by(id) %>%
  mutate(across(c(treatment, covariates), list(between = ~mean(., na.rm = TRUE)))) %>%
  mutate(across(c(treatment, covariates),
                list(within = ~. - mean(., na.rm = TRUE)), .names = "{.col}_within"))
```

### 6. Method-Specific Diagnostics

**For DiD with staggered treatment:**
```r
# Check for heterogeneous treatment effects
library(did)
did_result <- att_gt(
  yname = "outcome",
  tname = "year",
  idname = "unit",
  gname = "treatment_year",  # Year unit first treated
  data = data
)

# Event study
es <- aggte(did_result, type = "dynamic")
ggdid(es)
```

**For IV:**
```r
# Weak instrument test
fitstat(iv_model, "ivf")  # Should be > 10, ideally > 20

# Overidentification test (if multiple instruments)
fitstat(iv_model, "sargan")
```

**For Matching:**
```r
library(MatchIt)
library(cobalt)

# Balance check
bal.tab(matched_data, un = TRUE)

# Love plot
love.plot(matched_data)
```

### 6. Create Robustness Table

Compile all robustness checks:

```r
robustness_models <- list(
  "Main" = main_model,
  "Minimal controls" = robust_minimal,
  "Extended controls" = robust_extended,
  "Alt FE" = robust_fe,
  "Winsorized" = robust_winsor,
  "Pre-2015" = robust_early,
  "Post-2015" = robust_late
)

modelsummary(robustness_models,
             output = "output/tables/table3_robustness.tex",
             stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
             title = "Robustness Checks")
```

## Output: Robustness Report

Create a robustness report (`memos/phase4-robustness-report.md`):

```markdown
# Robustness Report

## Summary Assessment

The main findings are [robust / partially robust / not robust] to alternative specifications.

## Alternative Specifications

| Specification | Estimate | SE | Conclusion |
|---------------|----------|-----|------------|
| Main | X.XX | (X.XX) | - |
| Minimal controls | X.XX | (X.XX) | [stable/different] |
| Extended controls | X.XX | (X.XX) | [stable/different] |
| Alt FE | X.XX | (X.XX) | [stable/different] |
...

## Placebo Tests

| Test | Expected | Found | Pass? |
|------|----------|-------|-------|
| Pre-treatment | 0 | X.XX (p=X.XX) | [Yes/No] |
| Fake timing | 0 | X.XX (p=X.XX) | [Yes/No] |
| Unrelated outcome | 0 | X.XX (p=X.XX) | [Yes/No] |

## Sensitivity Analysis

### Outliers
- Results [are / are not] sensitive to extreme values

### Sample restrictions
- Results [hold / change] in different subsamples

### Selection on unobservables (sensemakr)
- An unobserved confounder would need to be [X times] as strong as
  [strongest observed covariate] to explain away the result
- This is [plausible / implausible] because [reasoning]

## Subgroup Analysis

| Subgroup | Estimate | SE | Different from main? |
|----------|----------|-----|---------------------|
| Group 1 | X.XX | (X.XX) | [Yes/No] |
| Group 2 | X.XX | (X.XX) | [Yes/No] |

## Method-Specific Diagnostics
[Results of diagnostic tests]

## Overall Assessment

**Strengths:**
- [What checks the results passed]

**Concerns:**
- [Any issues found]

**Conclusion:**
The main findings [can / cannot] be considered robust because [reasoning].

## Questions for User
- [Any interpretive questions about robustness]
```

## When You're Done

Return a summary to the orchestrator that includes:
1. Overall robustness assessment
2. Which checks passed/failed
3. Sensitivity analysis conclusions
4. Any concerns about the findings
5. Questions for the user

**Do not proceed to Phase 5 until the user reviews the robustness assessment.**
