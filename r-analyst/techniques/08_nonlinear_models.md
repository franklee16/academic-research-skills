# Non-Linear Models (GLMs) in R

Generalized Linear Models for binary, count, and other non-linear outcomes with reproducible examples.

---

## Setup

```r
# Install packages (only run once)
packages <- c("fixest", "marginaleffects", "ggplot2", "dplyr")
install.packages(setdiff(packages, rownames(installed.packages())))

# Load packages
library(fixest)
library(marginaleffects)
library(ggplot2)
library(dplyr)
```

---

## Decision Flow: Which Model?

```
Is your outcome binary (0/1)?
├── YES → Do you have many fixed effects?
│         ├── YES → Use LPM (feols) — avoids incidental parameter problem
│         └── NO  → LPM or Logit both fine — report AMEs for Logit
│
└── NO → Is your outcome a count or non-negative continuous?
          ├── YES → Does it have zeros?
          │         ├── YES → Use Poisson/PPML (feglm) — handles zeros
          │         └── NO  → Poisson or log-OLS both fine
          │
          └── NO → Standard OLS/linear models

Additional considerations:
- Rare events (<5%)? → Consider Firth's Logit
- Overdispersion? → Poisson with robust/clustered SEs (not NegBin)
- Want comparable coefficients across models? → Report AMEs
- Interaction effects? → Plot conditional marginal effects
```

---

## Agent Guardrails (Do Not Do These)

When working with non-linear models, **refuse** to:

1. ❌ **Interpret raw logit/probit coefficients as probability changes**
   - "A coefficient of 0.5 means 50% higher probability" is WRONG
   - Always compute and report marginal effects

2. ❌ **Compare raw logit coefficients across nested models**
   - Coefficients rescale when you add variables (Mood 2010)
   - Compare AMEs instead

3. ❌ **Recommend Negative Binomial solely due to overdispersion**
   - Robust/clustered SEs handle overdispersion for inference
   - NegBin rarely necessary and computationally expensive with FEs

4. ❌ **Take log(y) when y contains zeros without explicit warning**
   - log(0) is undefined; log(y+1) is ad hoc and biased
   - Recommend PPML instead

5. ❌ **Interpret interaction coefficients directly in non-linear models**
   - The "interaction effect" varies across observations
   - Plot conditional marginal effects instead

6. ❌ **Predict to new units from FE models without warning**
   - FE predictions are conditional on estimated fixed effects
   - Cannot extrapolate to units not in the estimation sample

---

## Overview: Why GLMs?

When outcomes are binary (0/1) or counts (0, 1, 2...), linear models (OLS) can produce impossible predictions (probabilities < 0 or > 1). Generalized Linear Models (GLMs) like Logit, Probit, and Poisson handle these constraints.

### When to Use GLMs

- **Binary Data**: Outcome is Yes/No, Win/Loss, Employed/Unemployed → **Logit/Probit**
- **Count Data**: Outcome is number of patents, citations, events → **Poisson/Negative Binomial**
- **Non-negative outcomes**: When you have many zeros and cannot simply take `log(y)` → **PPML (Poisson)**

### Assumptions

1. **Functional Form**: The link function (e.g., logit, log) correctly specifies the relationship
2. **Independence**: Observations are independent (conditional on FEs)
3. **Mean-Variance Relationship**:
   - Poisson assumes Mean = Variance (equidispersion)
   - Logit/Probit assume a specific latent variable distribution

### Common Pitfalls

- **Interpretation**: Raw coefficients (β) are **log-odds** (Logit) or **log-counts** (Poisson), not marginal effects. You *must* calculate marginal effects.
- **Incidental Parameter Problem**: In short panels (small T), including unit Fixed Effects in non-linear models (like Probit) can bias estimates. Poisson FE is robust to this; Logit requires Conditional Logit or sufficient T.
- **Interaction Effects**: You cannot interpret the coefficient of an interaction term directly in non-linear models. The "interaction effect" varies for every observation.

---

## 1. Binary Choice Models (Logit/Probit)

Binary outcomes require models that constrain predictions to [0, 1].

### 1.1 Creating Binary Outcome Data

```r
# Load data
data(base_did, package = "fixest")

# Create binary outcome: Did outcome exceed threshold?
base_did$y_binary <- as.numeric(base_did$y > 0)

# Check distribution
table(base_did$y_binary)
#   0   1
# 399 681

cat("Event rate:", round(mean(base_did$y_binary) * 100, 1), "%\n")
# Event rate: 63.1%
```

### 1.2 Linear Probability Model (LPM)

The LPM is simply OLS on a binary outcome. It's often preferred in applied work.

**Pros:**
- Easy to interpret (coefficients are percentage point changes)
- No incidental parameter problem with fixed effects
- Robust to misspecification of functional form

**Cons:**
- Predictions can be < 0 or > 1
- Heteroskedastic by construction (need robust SEs)

```r
# Linear Probability Model with Fixed Effects
mod_lpm <- feols(
  y_binary ~ x1 | id + period,
  cluster = ~id,
  data = base_did
)

summary(mod_lpm)

# Output:
# OLS estimation, Pair.Clust Dep. Var.: y_binary
# Observations: 1,080
# Fixed-effects: id: 108,  period: 10
# Standard-errors: Clustered by id
#    Estimate Std. Error t value Pr(>|t|)
# x1   0.0645     0.0203   3.173  0.00198 **

# Interpretation:
# A 1 unit increase in x1 increases the probability of Y=1 by 6.45 percentage points.
```

**When to defend LPM in a paper:**
> "We employ a Linear Probability Model (LPM) to avoid the incidental parameter bias associated with non-linear fixed effects models and for ease of interpretation (Angrist and Pischke 2009)."

### 1.3 Logit with Fixed Effects

```r
# Logit with Fixed Effects
# Note: Observations with no variation in outcome within FE groups are dropped
mod_logit <- feglm(
  y_binary ~ x1 | id + period,
  family = binomial("logit"),
  data = base_did
)

summary(mod_logit)

# Output:
# GLM estimation, Pair.Clust Dep. Var.: y_binary
# Observations: 1,060 (Logit drops 20 obs with no within-group variation)
# Fixed-effects: id: 106,  period: 10
#    Estimate Std. Error t value Pr(>|t|)
# x1   0.4129     0.1396   2.958  0.00387 **

# IMPORTANT: This coefficient is in LOG-ODDS, not probability!
# 0.41 does NOT mean "41 percentage points"
```

### 1.4 Probit with Fixed Effects

```r
# Probit with Fixed Effects
mod_probit <- feglm(
  y_binary ~ x1 | id + period,
  family = binomial("probit"),
  data = base_did
)

summary(mod_probit)

# Probit coefficients are in z-score units of the latent variable
# Even harder to interpret directly than Logit
```

### 1.5 Comparing LPM, Logit, Probit

```r
# Compare coefficients (note: different scales!)
etable(mod_lpm, mod_logit, mod_probit,
       headers = c("LPM", "Logit", "Probit"),
       title = "Binary Outcome Models")

# For comparison, compute marginal effects from Logit
ame_logit <- avg_slopes(mod_logit, variables = "x1")

cat("LPM coefficient:", round(coef(mod_lpm)["x1"], 4), "\n")
cat("Logit AME:      ", round(ame_logit$estimate, 4), "\n")

# These should be similar! The LPM approximates marginal effects well.
```

### 1.6 Perfect and Quasi-Separation (Convergence Failures)

**The Problem**: If a predictor perfectly predicts Y=0 or Y=1 for some subset of data, standard logit will fail or produce infinite/extreme estimates.

**Symptoms**:
- Huge coefficients (e.g., |β| > 10)
- Convergence warnings ("algorithm did not converge")
- Standard errors that are NA or extremely large
- `feglm` dropping many observations

**Common causes**:
- Rare events with many predictors
- Categorical predictors where one level has all 0s or all 1s
- Too many fixed effects relative to variation in outcome

**Solutions**:

```r
# 1. Check for separation
# Look for predictors that perfectly predict outcome
base_did %>%
  group_by(x1_category) %>%
  summarise(mean_y = mean(y_binary), n = n()) %>%
  filter(mean_y %in% c(0, 1))  # Perfect prediction = separation

# 2. If separation detected:
# Option A: Use Firth's penalized logit (see Section 6)
# Option B: Collapse categories / drop problematic predictor
# Option C: Use LPM instead (no separation issue)
# Option D: Remove observations causing separation (document this!)

# 3. feglm handles some separation by dropping observations
# Check how many were dropped:
mod <- feglm(y_binary ~ x1 | id, family = "logit", data = base_did)
# NOTE in output tells you how many FE groups were dropped
```

**For papers**: "We use a linear probability model because [X% of observations / certain fixed effect groups] exhibited perfect separation in the logit specification."

---

## 2. Count Data Models (Poisson/PPML)

For count data or non-negative continuous data (like trade flows), Poisson Pseudo-Maximum Likelihood (PPML) is the gold standard.

### Key Insight: PPML Estimates the Conditional Mean

**Important**: PPML does not assume your data are "counts" from a Poisson distribution. It estimates the **conditional mean** E[Y|X] under the assumption that E[Y|X] = exp(Xβ).

This means PPML works for:
- Actual count data (patents, citations)
- Non-negative continuous data (trade flows, expenditures)
- Any data where you want to model a multiplicative relationship with zeros

The "Poisson" name refers to the estimating equation, not an assumption about the data-generating process.

### When to Use Poisson/PPML

- Count outcomes (0, 1, 2, ...)
- Non-negative continuous outcomes with many zeros
- Trade flows (Santos Silva & Tenreyro 2006)
- Citation counts, patent counts
- Any setting where log-linear relationships make sense but zeros exist

### Why Not Log-OLS?

- `log(0)` is undefined → drops zeros or requires arbitrary `log(y+1)`
- Log-OLS is inconsistent under heteroskedasticity
- PPML handles zeros naturally and is consistent

### 2.1 Basic Poisson with Fixed Effects

Using trade data (gravity model):

```r
# Load trade data
data(trade, package = "fixest")

# Examine data
head(trade)
#   Destination Origin Product Year dist_km    Euros
# 1          AT     AT       1 2007     0.0 65003997
# 2          AT     BE       1 2007   916.1  3684684

# Check for zeros
cat("Zeros in Euros:", sum(trade$Euros == 0), "/", nrow(trade), "\n")

# 1. Log-Linear OLS (The "Old" Way)
# Problem: Drops zeros, inconsistent under heteroskedasticity
trade_pos <- trade[trade$Euros > 0, ]
mod_ols_log <- feols(
  log(Euros) ~ log(dist_km) | Origin + Destination + Year,
  data = trade_pos
)

# 2. Poisson / PPML (The "Right" Way)
# Keeps zeros, robust to heteroskedasticity
mod_pois <- feglm(
  Euros ~ log(dist_km) | Origin + Destination + Year,
  family = "poisson",
  cluster = ~Origin,
  data = trade
)

summary(mod_pois)

# Output:
# GLM estimation, family = Poisson, Pair.Clust Dep. Var.: Euros
# Observations: 38,325
# Fixed-effects: Origin: 15,  Destination: 15,  Year: 10
# Standard-errors: Clustered by Origin
#              Estimate Std. Error t value Pr(>|t|)
# log(dist_km)  -1.5176     0.2118  -7.165 4.99e-06 ***
```

### 2.2 Interpreting Poisson Coefficients

```r
# The coefficient on log(dist_km) is an ELASTICITY
# (because we logged the independent variable)

# Interpretation:
# Coef = -1.52 means:
# A 1% increase in distance reduces trade by ~1.52%

# Compare OLS and Poisson elasticities
cat("OLS elasticity: ", round(coef(mod_ols_log)["log(dist_km)"], 3), "\n")
cat("PPML elasticity:", round(coef(mod_pois)["log(dist_km)"], 3), "\n")

# If independent variable is NOT logged, use exp(coef)-1 for % change
# Example: If year coefficient = 0.05
# exp(0.05) - 1 = 0.051 => 5.1% increase per year
```

### 2.3 Poisson vs. Negative Binomial

**Overdispersion**: If variance >> mean, the Poisson variance assumption is violated and *default* standard errors may be too small.

However, with **robust or clustered standard errors** (standard in applied work), overdispersion does not invalidate inference, even if the Poisson variance assumption is violated. You rarely need Negative Binomial for this reason alone.

```r
# Check for overdispersion (informal)
cat("Mean Euros:", round(mean(trade$Euros), 0), "\n")
cat("Var Euros: ", round(var(trade$Euros), 0), "\n")
# If Var >> Mean, there's overdispersion
# But robust SEs handle this!

# With clustering, Poisson is robust to overdispersion
mod_pois_robust <- feglm(
  Euros ~ log(dist_km) | Origin + Destination + Year,
  family = "poisson",
  vcov = "hetero",  # Or cluster = ~Origin
  data = trade
)

# Negative Binomial (computationally intensive with many FEs)
# Use fenegbin if needed
# mod_nb <- fenegbin(Euros ~ log(dist_km) | Origin + Destination + Year, data = trade)
# Note: Can be slow with many fixed effects
```

---

## 3. Marginal Effects (Critical for Publication)

Raw GLM coefficients are difficult to interpret. You **must** calculate marginal effects for policy-relevant statements.

### 3.1 Average Marginal Effects (AME)

"On average, how does a 1 unit change in X change the probability/count?"

```r
library(marginaleffects)

# Binary model: Effect of x1 on probability of Y=1
mod_logit <- feglm(y_binary ~ x1 | id + period, family = "logit", data = base_did)

# Calculate AME
ame <- avg_slopes(mod_logit, variables = "x1")
print(ame)

# Output:
#  Term Contrast Estimate Std. Error    z Pr(>|z|)    S  2.5 % 97.5 %
#    x1   dY/dX   0.0637     0.0225 2.84  0.00456  7.8 0.0197  0.108

# Interpretation:
# On average, a 1 unit increase in x1 increases the probability of Y=1
# by 6.37 percentage points.
```

### 3.2 Marginal Effects at Specific Values (MEM)

```r
# Poisson model: Effect of distance on trade
data(trade, package = "fixest")
mod_pois <- feglm(Euros ~ log(dist_km) + Year | Origin + Destination,
                  family = "poisson", data = trade)

# Marginal effects for specific years
slopes(mod_pois, variables = "log(dist_km)",
       newdata = datagrid(Year = c(2007, 2008, 2009)))

# This shows how the marginal effect varies by year
```

### 3.3 Predicted Probabilities/Counts

```r
# Predictions at specific values
preds <- predictions(mod_logit, newdata = datagrid(x1 = c(-1, 0, 1)))
print(preds)

# Output shows predicted probability at each x1 value
# Useful for visualization
```

### 3.4 Visualizing Marginal Effects

```r
# Plot predicted probability curve
# Effect of x1 on probability of y, holding others constant
plot_predictions(mod_logit, condition = "x1") +
  labs(y = "Predicted Probability",
       x = "X1",
       title = "Effect of X1 on Binary Outcome") +
  theme_minimal()
```

### 3.5 Warning: Predictions from FE Models

**Important limitation**: Predictions from fixed effects models are conditional on estimated fixed effects. This means:

- You **cannot** predict for new units (individuals, firms, countries) not in your estimation sample
- Predictions are only meaningful for units whose fixed effects were estimated
- Extrapolation to new contexts is not valid

```r
# This works: predict for units IN the data
preds_in_sample <- predictions(mod_logit, newdata = head(base_did, 10))

# This is MISLEADING: predicting for "new" covariate values
# The prediction assumes some fixed effect value (often the average)
# but that's not meaningful for a truly new unit
preds_new <- predictions(mod_logit, newdata = datagrid(x1 = c(-2, 0, 2)))
# These predictions are for a "hypothetical average unit" - interpret with caution
```

**For papers**: When reporting predictions from FE models, clarify that predictions are in-sample or for hypothetical units at the mean of fixed effects.

---

## 4. Comparing Coefficients Across Models (Mood's Critique)

**The Problem**: In Logit/Probit, if you add variables to a model, the variance of the error term changes, which rescales *all* coefficients.

**Result**: If a coefficient "shrinks" after adding controls, it might just be rescaling, not actual mediation/confounding. **You cannot compare raw Logit coefficients across nested models.**

**The Solution**: Compare **Average Marginal Effects (AME)**, not raw coefficients.

### 4.1 Demonstration of the Problem

```r
# Model 1: Baseline (no controls)
mod_1 <- feglm(y_binary ~ x1, family = "logit", data = base_did)

# Model 2: With additional variable (simulated)
base_did$x2 <- rnorm(nrow(base_did))
mod_2 <- feglm(y_binary ~ x1 + x2, family = "logit", data = base_did)

# WRONG: Comparing raw coefficients
cat("Model 1 x1 coef:", round(coef(mod_1)["x1"], 4), "\n")
cat("Model 2 x1 coef:", round(coef(mod_2)["x1"], 4), "\n")
# Any difference could be rescaling, not confounding!
```

### 4.2 The Correct Comparison

```r
# RIGHT: Compare Average Marginal Effects
ame_1 <- avg_slopes(mod_1, variables = "x1")
ame_2 <- avg_slopes(mod_2, variables = "x1")

cat("Model 1 AME:", round(ame_1$estimate, 4), "\n")
cat("Model 2 AME:", round(ame_2$estimate, 4), "\n")

# Compare these estimates to make claims about mediation/confounding
# AMEs are on the probability scale, which is stable across models
```

### 4.3 For Papers

> "Following Mood (2010), we compare average marginal effects rather than raw coefficients across models to avoid the scaling problem inherent in nonlinear models."

---

## 5. Interactions in Non-Linear Models (Ai & Norton)

**The Problem**: In a linear model, the interaction effect is constant (β₃). In Logit/Probit, the interaction effect *depends on the values of all other covariates*. The raw coefficient β₃ can be positive even if the actual interaction effect is negative for some observations!

**The Solution**: Never interpret the interaction coefficient directly. Plot the **Marginal Effect of X at different levels of Z**.

### 5.1 The Wrong Way

```r
# Create interaction variable
base_did$x1_high <- as.numeric(base_did$x1 > median(base_did$x1))

# Model with Interaction
mod_int <- feglm(y_binary ~ x1 * x1_high, family = "logit", data = base_did)

# WRONG: Just looking at the interaction coefficient
summary(mod_int)
# The coefficient on x1:x1_high tells you almost nothing useful!
```

### 5.2 The Right Way: Visualize Conditional Effects

```r
# RIGHT: How does the effect of x1 change at different values of x1_high?
# Using a continuous moderator for better illustration
mod_int2 <- feglm(y_binary ~ x1 * period, family = "logit", data = base_did)

# Plot conditional marginal effects
plot_slopes(mod_int2,
            variables = "x1",
            condition = "period") +
  labs(title = "How X1's Effect Varies by Period",
       y = "Marginal Effect of X1 on Pr(Y=1)",
       x = "Period") +
  theme_minimal()
```

### 5.3 For Papers

> "Given the difficulties in interpreting interaction terms in nonlinear models (Ai and Norton 2003), we plot the marginal effect of [X] conditional on [Z] rather than relying on the interaction coefficient."

---

## 6. Rare Events (Firth's Logit)

**The Problem**: If your outcome is rare (e.g., "Civil War Onset" at 2%, "CEO Turnover" at 5%), standard Logit:
- Underestimates probability (finite sample bias)
- Can crash due to "separation" (predictors perfectly predicting zeros)

**The Solution**: Penalized Likelihood (Firth's method) reduces small-sample bias.

### 6.1 When to Use Firth's Logit

- Sample size N < 500
- Event rate < 5%
- Experiencing "separation" warnings
- Many predictors relative to events (rule of thumb: need 10 events per predictor)

### 6.2 Implementation

```r
# Install logistf (may require manual installation on some systems)
# install.packages("logistf")

# Create rare event data
set.seed(123)
rare_data <- data.frame(
  y_rare = rbinom(500, 1, 0.03),  # 3% event rate
  x1 = rnorm(500),
  x2 = rnorm(500),
  year = rep(2000:2009, 50)
)

cat("Event rate:", round(mean(rare_data$y_rare) * 100, 1), "%\n")
cat("Number of events:", sum(rare_data$y_rare), "\n")

# Standard Logit (may have bias)
mod_std <- glm(y_rare ~ x1 + x2, family = "binomial", data = rare_data)

# Firth's Logit (bias-corrected)
library(logistf)
mod_firth <- logistf(y_rare ~ x1 + x2, data = rare_data)

# Compare
cat("Standard Logit x1:", round(coef(mod_std)["x1"], 4), "\n")
cat("Firth Logit x1:   ", round(coef(mod_firth)["x1"], 4), "\n")
```

**Note**: `logistf` is harder to combine with high-dimensional Fixed Effects. For FE models with rare events, consider:
- Conditional logit (`survival::clogit`)
- LPM with robust SEs (if primarily interested in marginal effects)

---

## 7. Fixed Effects Considerations

### 7.1 Incidental Parameter Problem

With many fixed effects and short panels (small T), non-linear FE models are biased.

| Model | Bias with FE | Solution |
|-------|-------------|----------|
| Logit | Yes, biased | Use Conditional Logit or long T |
| Probit | Yes, biased | Avoid FE Probit, use LPM |
| Poisson | No bias | Safe to use (`feglm`) |

```r
# Poisson is robust to incidental parameter problem
mod_pois_fe <- feglm(
  Euros ~ log(dist_km) | Origin + Destination + Year,
  family = "poisson",
  data = trade
)
# This is fine even with many FEs and short panels

# For binary data, LPM is often safer
mod_lpm_fe <- feols(
  y_binary ~ x1 | id + period,
  data = base_did
)
# No incidental parameter problem
```

### 7.2 Conditional Logit (Fixed Effects Logit)

The "true" fixed effects logit that avoids incidental parameter bias:

```r
library(survival)

# Create within-group identifier for survival::clogit
base_did$strata_id <- base_did$id

# Conditional logit (only uses within-group variation)
mod_clogit <- clogit(
  y_binary ~ x1 + strata(strata_id),
  data = base_did
)

summary(mod_clogit)

# Note: This only uses units with variation in Y
# Units always 0 or always 1 are dropped
```

---

## 8. Model Selection and Diagnostics

### 8.1 Choosing Between Models

| Scenario | Recommended Model | Why |
|----------|------------------|-----|
| Binary, want interpretable coeffs | LPM (`feols`) | Direct % point interpretation |
| Binary, theoretical reasons for Logit | Logit (`feglm`) | Report AMEs |
| Counts with zeros | Poisson (`feglm`) | Handles zeros, robust |
| Counts, severe overdispersion | Poisson with cluster SEs | Or Negative Binomial |
| Binary, rare events | Firth's Logit | Bias correction |
| Binary with many FEs | LPM or Conditional Logit | Avoid incidental parameter |

### 8.2 Pseudo R-squared

```r
# GLMs don't have true R-squared
# Use pseudo R-squared measures carefully

mod_logit <- feglm(y_binary ~ x1 | id + period, family = "logit", data = base_did)

# Extract fit statistics from etable
etable(mod_logit, fitstat = ~ pr2 + ll)
# pr2 = pseudo R-squared
# ll = log-likelihood
```

### 8.3 Goodness of Fit: Predicted vs. Actual

```r
# For binary models: Are predictions calibrated?
base_did$pred_prob <- predict(mod_lpm, type = "response")

# Bin predictions and compare to actual event rate
base_did %>%
  mutate(pred_bin = cut(pred_prob, breaks = seq(0, 1, 0.1))) %>%
  group_by(pred_bin) %>%
  summarise(
    n = n(),
    actual_rate = mean(y_binary),
    pred_rate = mean(pred_prob)
  )
```

---

## 9. Publication-Quality Tables

### 9.1 Comparing Specifications

```r
# Run multiple specifications
mod1 <- feols(y_binary ~ x1 | period, cluster = ~id, data = base_did)
mod2 <- feols(y_binary ~ x1 | id + period, cluster = ~id, data = base_did)
mod3 <- feglm(y_binary ~ x1 | id + period, family = "logit", data = base_did)

# Create comparison table
etable(mod1, mod2, mod3,
       headers = c("LPM (Year FE)", "LPM (Two-way FE)", "Logit (Two-way FE)"),
       title = "Binary Outcome: Comparing Specifications",
       notes = "Clustered SEs at unit level. Logit coefficients are log-odds.",
       fitstat = ~ n + r2 + pr2)
```

### 9.2 Reporting Marginal Effects

For Logit/Probit, always report AMEs:

```r
# Get AMEs for key variable
ame_logit <- avg_slopes(mod3, variables = "x1")

# Create formatted output
data.frame(
  Model = c("LPM", "Logit (AME)"),
  Estimate = c(round(coef(mod2)["x1"], 4),
               round(ame_logit$estimate, 4)),
  SE = c(round(se(mod2)["x1"], 4),
         round(ame_logit$std.error, 4)),
  Note = c("Direct interpretation", "Probability scale")
)
```

---

## Quick Reference

### Model Selection

| Outcome Type | Preferred Model | Package/Function |
|--------------|----------------|------------------|
| Binary (0/1) | LPM or Logit | `feols()`, `feglm(family="logit")` |
| Counts | Poisson/PPML | `feglm(family="poisson")` |
| Rare binary | Firth's Logit | `logistf::logistf()` |
| Binary with FE | LPM or Cond. Logit | `feols()`, `survival::clogit()` |

### Interpretation Checklist

1. **Report marginal effects**, not raw coefficients (except for elasticities in Poisson)
2. **Use AMEs** to compare across models (Mood's critique)
3. **Plot interactions** rather than interpreting interaction coefficients (Ai & Norton)
4. **Consider LPM** when interpretability is paramount
5. **Cluster standard errors** to handle overdispersion in Poisson

### Key Functions

```r
# Binary models
feglm(y ~ x | fe, family = "logit", data)  # Logit
feglm(y ~ x | fe, family = "probit", data) # Probit
feols(y ~ x | fe, data)                     # LPM

# Count models
feglm(y ~ x | fe, family = "poisson", data) # Poisson

# Marginal effects
avg_slopes(model)                           # Average marginal effects
slopes(model, newdata = ...)               # Conditional marginal effects
predictions(model, newdata = ...)          # Predicted values
plot_slopes(model, condition = "z")        # Visualize interactions
```

### Common Mistakes to Avoid

1. ❌ Interpreting Logit coefficients as probability changes
2. ❌ Comparing raw Logit coefficients across nested models
3. ❌ Interpreting interaction terms directly in non-linear models
4. ❌ Using log(y) with zeros instead of Poisson
5. ❌ Ignoring incidental parameter problem with short panels
6. ❌ Not clustering standard errors in Poisson models

### Paper Template Language

**For LPM:**
> "We estimate a Linear Probability Model to maintain ease of interpretation and avoid the incidental parameter bias inherent in non-linear fixed effects models."

**For Logit/Probit with AME:**
> "We report average marginal effects from our logit specification, calculated using the `marginaleffects` package (Arel-Bundock 2023)."

**For Poisson:**
> "Following Santos Silva and Tenreyro (2006), we use Poisson Pseudo-Maximum Likelihood (PPML) to handle zeros in the outcome and ensure consistency under heteroskedasticity."

**For Mood's Critique:**
> "We compare average marginal effects rather than raw coefficients to avoid scaling issues across nested non-linear models (Mood 2010)."

**For Interactions:**
> "Given the complexity of interaction effects in non-linear models (Ai and Norton 2003), we present graphical evidence of how the marginal effect of [X] varies with [Z]."
