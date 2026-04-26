# Phase 3: Main Analysis

You are executing Phase 3 of a statistical analysis in Stata. Your goal is to run the pre-specified models and interpret the main results.

## Why This Phase Matters

This is where the analysis happens. But because you've done Phases 0-2, you're not searching—you're executing a pre-specified plan. This makes results more credible.

## Technique Guides

**Before writing code, consult the relevant technique guide** in `stata-statistical-techniques/` for method-specific patterns:

| Method | Guide |
|--------|-------|
| DiD, Event Study, IV, Matching | `01_core_econometrics.md` |
| Survey weights, Bootstrap | `02_survey_resampling.md` |
| Synthetic Control | `03_synthetic_control.md` |
| Logit, Poisson, Margins | `06_modeling_basics.md` |
| Tables, Visualization | `04_visualization.md` |
| Post-estimation, Reporting | `07_postestimation_reporting.md` |

These guides contain tested code patterns—use them rather than writing from scratch.

## Your Tasks

### 1. Run the Specification Sequence

Execute the models defined in Phase 2:

```stata
* Load analysis data
use "$clean/analysis_sample.dta", clear

* Clear stored estimates
estimates clear

* Specification sequence
* Model 1: Baseline
reghdfe outcome treatment, noabsorb cluster(cluster_var)
estimates store m1

* Model 2: Unit FE
reghdfe outcome treatment, absorb(id) cluster(cluster_var)
estimates store m2

* Model 3: Two-way FE
reghdfe outcome treatment, absorb(id year) cluster(cluster_var)
estimates store m3

* Model 4: With controls (preferred)
reghdfe outcome treatment control1 control2, absorb(id year) cluster(cluster_var)
estimates store m4
```

### 2. Create Main Results Table

```stata
* Console output for review
esttab m1 m2 m3 m4, se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2_a, labels("Observations" "Adj. R-squared"))

* Publication table (RTF for Word)
esttab m1 m2 m3 m4 using "$tables/table2_main.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2_a, labels("Observations" "Adj. R-squared") fmt(0 3)) ///
    title("Effect of Treatment on Outcome") ///
    mtitles("Baseline" "Unit FE" "Two-way FE" "Full Model") ///
    note("Standard errors clustered at [level] in parentheses. * p<0.1, ** p<0.05, *** p<0.01")

* LaTeX version
esttab m1 m2 m3 m4 using "$tables/table2_main.tex", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) booktabs ///
    stats(N r2_a, labels("Observations" "Adj. R-squared") fmt(0 3))
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
```stata
* After logit/probit/ologit/poisson/etc.
logit outcome treatment control1 control2, vce(cluster cluster_var)

* Compute AMEs for all predictors
margins, dydx(*) post
estimates store ame

* Create AME table
esttab ame using "$tables/table2_ame.rtf", replace ///
    cells(b(fmt(3)) se(fmt(3))) ///
    title("Average Marginal Effects") ///
    note("Standard errors in parentheses.")
```

**Predicted Probabilities:**
```stata
* Predictions at specific values
margins, at(treatment=(0 1)) atmeans

* Plot predicted probabilities across range of X
margins, at(treatment=(0 1) control1=(1(1)10))
marginsplot, ///
    title("Predicted Probability by Treatment and Control1") ///
    xtitle("Control1") ytitle("Predicted Probability")
graph export "$figures/predicted_probs.pdf", replace
```

**Interpreting Interactions in Nonlinear Models:**
```stata
* Estimate model with interaction
logit outcome c.treatment##c.moderator control1, vce(cluster cluster_var)

* First differences: effect of treatment at different moderator levels
margins, dydx(treatment) at(moderator=(1 2 3 4 5))
marginsplot, recast(line) recastci(rarea) ///
    title("Marginal Effect of Treatment by Moderator") ///
    yline(0, lpattern(dash))
graph export "$figures/interaction_margins.pdf", replace

* Second differences: how the effect changes
margins, dydx(treatment) at(moderator=(1 5)) contrast(atcontrast(r))
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
```stata
* After estimation, check residuals
predict resid, residuals
histogram resid, normal
graph export "$figures/residuals.pdf", replace

* VIF for multicollinearity (run without FE)
quietly reg outcome treatment control1 control2
vif
```

**For Logistic Regression:**
```stata
* Model fit
estat classification  // Classification table
lroc  // ROC curve (AUC should be > 0.7)
graph export "$figures/roc.pdf", replace

* Report pseudo-R² with context
* Note: pseudo-R² values 0.10-0.20 often indicate reasonable fit
estat ic  // AIC/BIC
```

**For Count Models (Poisson/Negative Binomial):**
```stata
* Test for overdispersion after Poisson
poisson count treatment controls
estat gof  // Deviance goodness-of-fit test

* If overdispersed, use negative binomial:
nbreg count treatment controls, vce(cluster cluster_var)

* Compare AIC
quietly poisson count treatment controls
estimates store poisson_m
quietly nbreg count treatment controls
estimates store nbreg_m
lrtest poisson_m nbreg_m  // LR test for alpha = 0
```

**For Ordered Logit:**
```stata
* Test proportional odds assumption
ologit outcome treatment controls
brant  // Brant test (if installed: ssc install brant)

* If violated, use generalized ordered logit:
gologit2 outcome treatment controls, autofit
```

**For DiD/Event Study:**
```stata
* Event study with csdid
csdid outcome, ivar(id) time(year) gvar(first_treat) notyet
csdid_estat event
csdid_plot, title("Event Study")
graph export "$figures/event_study.pdf", replace
```

**For IV:**
```stata
* First stage F-statistic
ivreg2 outcome (endogenous = instrument) controls, first robust
* Check F > 10 (or use effective F)

* Display first stage
estat firststage
```

### 5. Visualize Key Results

Create figures for the main findings:

**Coefficient plot:**
```stata
coefplot m4, drop(_cons) xline(0) ///
    title("Treatment Effect Estimate") ///
    xtitle("Coefficient") ytitle("")
graph export "$figures/coefplot.pdf", replace
```

**Event study plot:**
```stata
* After csdid
csdid_plot, ///
    title("Dynamic Treatment Effects") ///
    xtitle("Time Relative to Treatment") ///
    ytitle("Coefficient")
graph export "$figures/event_study.pdf", replace
```

**Marginal effects (for interactions):**
```stata
* If model has interactions
margins, dydx(treatment) at(moderator=(0 1))
marginsplot, ///
    title("Treatment Effect by Moderator") ///
    xtitle("Moderator") ytitle("Marginal Effect")
graph export "$figures/margins.pdf", replace
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
