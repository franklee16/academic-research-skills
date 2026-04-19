# Phase 3: Main Analysis

You are executing Phase 3 of a statistical analysis in R. Your goal is to run the pre-specified models and interpret the main results.

## Why This Phase Matters

This is where the analysis happens. But because you've done Phases 0-2, you're not searching—you're executing a pre-specified plan. This makes results more credible.

## Technique Guides

**Before writing code, consult the relevant technique guide** in `r-statistical-techniques/` for method-specific patterns:

| Method | Guide |
|--------|-------|
| DiD, Event Study, IV, Matching | `01_core_econometrics.md` |
| Survey weights, Bootstrap | `02_survey_resampling.md` |
| Synthetic Control | `04_synthetic_control.md` |
| Logit, Poisson, Margins | `08_nonlinear_models.md` |
| Visualization, Tables | `06_visualization.md` |

These guides contain tested code patterns—use them rather than writing from scratch.

## Your Tasks

### 1. Run the Specification Sequence

Execute the models defined in Phase 2:

```r
library(fixest)
library(modelsummary)

# Load analysis data
analysis_data <- readRDS("data/clean/analysis_sample.rds")

# Run specification sequence
models <- list()

models[["(1)"]] <- feols(
  outcome ~ treatment,
  data = analysis_data
)

models[["(2)"]] <- feols(
  outcome ~ treatment | unit_fe,
  data = analysis_data
)

models[["(3)"]] <- feols(
  outcome ~ treatment | unit_fe + time_fe,
  data = analysis_data
)

models[["(4)"]] <- feols(
  outcome ~ treatment + control1 + control2 | unit_fe + time_fe,
  cluster = ~cluster_var,
  data = analysis_data
)
```

### 2. Create Main Results Table

```r
# Console output for review
modelsummary(models,
             stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
             gof_omit = "AIC|BIC|Log|RMSE")

# Publication table
modelsummary(models,
             output = "output/tables/table2_main_results.tex",
             stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
             coef_rename = c("treatment" = "Treatment Effect"),
             gof_omit = "AIC|BIC|Log|RMSE",
             title = "Main Results",
             notes = "Standard errors clustered at [level]. * p<0.1, ** p<0.05, *** p<0.01")
```

### 3. Interpret the Results

For the preferred specification, document:

**Point estimate:**
- What is the estimated effect?
- What are the units? (interpret in substantive terms)
- How large is this effect? (compare to mean, SD, or meaningful benchmark)

**Statistical precision:**
- What is the standard error?
- What is the confidence interval?
- Is this precisely estimated or noisy?

**Stability across specifications:**
- Does the estimate change substantially across models?
- What does adding controls/FE do to the estimate?
- Is the sign consistent?

### 4. Interpret Nonlinear Models (If Applicable)

For logistic, Poisson, ordered logit, or other nonlinear models, coefficients alone are insufficient. Follow current methodological standards (Long and Mustillo 2017; Mize 2019):

**Average Marginal Effects (AMEs):**
```r
library(marginaleffects)

# Compute AMEs for all predictors
ame <- avg_slopes(model)
print(ame)

# Create AME table
modelsummary(model,
             output = "output/tables/table2_ame.tex",
             estimate = "AME",
             statistic = "conf.int")
```

**Predicted Probabilities:**
```r
# Predictions at specific values
predictions <- predictions(model,
                           newdata = datagrid(treatment = c(0, 1),
                                             control1 = mean))

# Plot predicted probabilities across range of X
plot_predictions(model, condition = "treatment")
ggsave("output/figures/predicted_probs.pdf", width = 8, height = 6)
```

**Interpreting Interactions in Nonlinear Models:**
```r
# Show how effect of X varies across Z (first differences)
slopes(model, variables = "treatment", by = "moderator") |>
  plot() +
  geom_hline(yintercept = 0, linetype = "dashed")

# Second differences (how the gap changes)
comparisons(model, variables = "treatment", by = "moderator",
            hypothesis = "pairwise")
```

**Model Justification Paragraph Template:**
```markdown
We use [SPECIFIC MODEL] to model [OUTCOME] because [PROPERTY OF OUTCOME].
We chose [THIS MODEL] over [ALTERNATIVE] because [DIAGNOSTIC TEST RESULT].
[If relevant: We tested the [KEY ASSUMPTION] using [TEST NAME] and found
[RESULT].]
```

**Key Rules:**
- Report AMEs, not just odds ratios or log-odds
- Show predicted probabilities for substantive scenarios
- For interactions: show first differences (group comparisons) and second differences (how gaps change)
- Never interpret main effect coefficients when interactions are present (those are conditional effects)
- Always include confidence intervals

### 5. Check Model Assumptions

Run diagnostics appropriate to the method:

**For OLS/Fixed Effects:**
```r
# Residual diagnostics
plot(models[["(4)"]])

# Check for multicollinearity
library(car)
vif(lm(outcome ~ treatment + control1 + control2, data = analysis_data))
```

**For Logistic Regression:**
```r
# Model fit
library(pROC)
roc_result <- roc(analysis_data$outcome, predict(model, type = "response"))
auc(roc_result)  # Should be > 0.7

# Classification accuracy (note: compare to base rate!)
pred_class <- ifelse(predict(model, type = "response") > 0.5, 1, 0)
mean(pred_class == analysis_data$outcome)

# Report pseudo-R² with context
# Note: pseudo-R² values 0.10-0.20 often indicate reasonable fit
```

**For Count Models (Poisson/Negative Binomial):**
```r
# Test for overdispersion
library(AER)
dispersiontest(poisson_model)

# If overdispersed (p < 0.05), use negative binomial:
library(MASS)
nb_model <- glm.nb(count ~ treatment + controls, data = analysis_data)

# Compare AIC
AIC(poisson_model, nb_model)
```

**For Ordered Logit:**
```r
library(brant)
# Test proportional odds assumption
brant_test <- brant(ordered_model)
print(brant_test)  # If violated, use generalized ordered logit
```

**For DiD:**
```r
# Pre-trends (visual)
event_study <- feols(
  outcome ~ i(time_to_treat, ref = -1) | unit_fe + time_fe,
  cluster = ~cluster_var,
  data = analysis_data
)

iplot(event_study, main = "Event Study")
```

**For IV:**
```r
# First stage F-statistic
first_stage <- feols(endogenous ~ instrument + controls | fe, data = analysis_data)
summary(first_stage)  # Check F > 10 (or use effective F)

# Report first stage
fitstat(iv_model, "ivf")
```

### 5. Visualize Key Results

Create figures for the main findings:

**Coefficient plot:**
```r
library(ggplot2)

modelplot(models[["(4)"]], coef_omit = "Intercept") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  theme_minimal() +
  labs(title = "Treatment Effect Estimate")

ggsave("output/figures/figure_coefplot.pdf", width = 8, height = 6)
```

**Event study plot:**
```r
iplot(event_study)
# or custom with ggplot
coef_data <- broom::tidy(event_study, conf.int = TRUE)
ggplot(coef_data, aes(x = term, y = estimate, ymin = conf.low, ymax = conf.high)) +
  geom_pointrange() +
  geom_hline(yintercept = 0, linetype = "dashed") +
  theme_minimal()
```

**Marginal effects (for interactions):**
```r
library(marginaleffects)

# If model has interactions
mfx <- slopes(model, variables = "treatment", by = "moderator")
plot(mfx)
```

## Output: Results Report

Create a results report (`memos/phase3-results-report.md`):

```markdown
# Main Results Report

## Summary of Findings

**Main estimate**: [interpretation in words]

The preferred specification (Model X) shows that [treatment] is associated with
a [magnitude] [direction] in [outcome]. This effect is [statistically significant
at the X% level / not statistically significant].

## Results Table

[Reference Table 2 or include formatted output]

## Interpretation

### Magnitude
- Point estimate: [value]
- Units: [what this means]
- Context: [comparison to mean/SD/other benchmark]

### Precision
- Standard error: [value]
- 95% CI: [lower, upper]
- This is [precise/noisy] because [reason]

### Stability
- The estimate [is stable / changes] across specifications
- Adding controls [increases/decreases/doesn't change] the estimate
- This suggests [interpretation of stability pattern]

## Diagnostic Checks
- [Results of assumption tests]
- [Any concerns raised]

## Visualizations
- Figure X: [description]
- Figure Y: [description]

## Preliminary Assessment
- These results [support / do not support / partially support] the hypothesis
- Key caveat: [main limitation]
- Next step: robustness checks in Phase 4

## Questions for User
- [Any interpretive questions]
- [Should we proceed to robustness?]
```

## When You're Done

Return a summary to the orchestrator that includes:
1. The main estimate and its interpretation
2. Whether the effect is statistically significant
3. Whether results are stable across specifications
4. Any diagnostic concerns
5. Questions for the user

**Do not proceed to Phase 4 until the user reviews the main results.**
