# Modeling Basics in Stata

Plain-vanilla regression and GLM patterns that sociologists use constantly. All code tested on Stata 15+.

---

## 1. OLS Foundation

### Basic OLS with Robust SEs

```stata
sysuse auto, clear

* Robust (heteroskedasticity-consistent) standard errors
reg price mpg weight, robust
```

### Clustered Standard Errors

```stata
* Cluster at the group level
reg price mpg weight, cluster(foreign)

* For panel data, typically cluster on the panel unit
reg y x1 x2, cluster(state)
```

### Nested Controls Pattern

Build models incrementally to show robustness:

```stata
* Model 1: Baseline
reg price mpg, robust
estimates store m1

* Model 2: Add controls
reg price mpg weight, robust
estimates store m2

* Model 3: Add categorical
reg price mpg weight i.foreign, robust
estimates store m3

* Model 4: Full specification
reg price mpg weight i.foreign headroom trunk, robust
estimates store m4

* Display nested table
esttab m1 m2 m3 m4, se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("(1)" "(2)" "(3)" "(4)") ///
    drop(0.foreign) ///
    stats(N r2, labels("N" "R-squared") fmt(%9.0fc %9.3f))
```

---

## 2. Interactions and Margins

### Continuous × Continuous Interaction

```stata
* c. prefix for continuous variables
reg price c.mpg##c.weight, robust

* Marginal effect of mpg at different weight levels
margins, dydx(mpg) at(weight=(2000 3000 4000))
```

**Interpretation note:** The interaction coefficient alone doesn't tell you the effect at any particular point. Always use `margins` to interpret.

### Categorical × Continuous Interaction

```stata
* i. prefix for categorical variables
reg price i.foreign##c.mpg, robust

* Effect of mpg by foreign status
margins foreign, dydx(mpg)

* Predicted values at specific mpg levels by group
margins foreign, at(mpg=(15 20 25 30))
```

### Marginsplot for Visualization

```stata
reg price i.foreign##c.mpg, robust
margins foreign, at(mpg=(15(5)35))
marginsplot, title("Price by MPG and Origin") ///
    ytitle("Predicted Price") xtitle("MPG")
graph export "$figures/interaction_plot.png", replace
```

### Reviewer-Proof Guidelines

- **Don't interpret raw interaction coefficient alone** - always compute marginal effects
- **Plot predicted values** - reviewers want to see the interaction visually
- **Report at meaningful values** - use means or policy-relevant cutpoints

---

## 3. Binary Outcomes: Logit/Probit

### Logit with Robust SEs

```stata
sysuse nlsw88, clear
keep if !missing(union, wage, age, grade, tenure)

logit union wage age grade, robust
estimates store logit1
```

### Probit Alternative

```stata
probit union wage age grade, robust
estimates store probit1

* Compare
esttab logit1 probit1, se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("Logit" "Probit")
```

### Average Marginal Effects (AME)

This is what most sociologists should report:

```stata
logit union wage age grade, robust
margins, dydx(*)
```

Interpretation: "A one-unit increase in wage is associated with a 1.25 percentage point increase in the probability of union membership."

### Predicted Probabilities at Specific Values

```stata
* Probability at specific covariate values
margins, at(wage=(5 10 15) age=35 grade=12)
```

### Odds Ratios

```stata
* Report odds ratios instead of coefficients
logit union wage age grade, or
```

Interpretation: Odds ratio of 1.07 means "each dollar increase in wage is associated with 7% higher odds of union membership."

### Choosing What to Report

| Format | When to Use |
|--------|-------------|
| Marginal effects | Most journal articles; easy to interpret |
| Odds ratios | Clinical/epidemiological conventions |
| Raw coefficients | Technical appendix; rarely main table |

### Goodness-of-Fit Notes

- **Pseudo-R² is not R²** - don't interpret as variance explained
- **Classification tables are optional** - not decisive for model quality
- Focus on coefficient interpretation, not fit statistics

---

## 4. Count Models: Poisson and Negative Binomial

### When to Use Which

- **Poisson**: Counts with variance ≈ mean (equidispersion)
- **Negative Binomial**: Counts with variance > mean (overdispersion)
- **Rule of thumb**: If variance >> mean, use negative binomial

### Poisson with Robust SEs

```stata
poisson y_count x1 x2, robust
estimates store pois1

* Predicted counts
margins, at(x1=(-1 0 1) x2=0)
```

### Negative Binomial

```stata
nbreg y_count x1 x2, robust
estimates store nb1

* Compare Poisson vs NB
esttab pois1 nb1, se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("Poisson" "Neg Binomial")
```

### Incidence Rate Ratios

```stata
poisson y_count x1 x2, irr
```

Interpretation: IRR of 1.33 means "a one-unit increase in x1 is associated with 33% more events."

---

## 5. Ordinal Outcomes

### Ordered Logit

```stata
sysuse auto, clear

* rep78 is 1-5 repair record
ologit rep78 price mpg foreign, robust
```

### Predicted Probabilities by Category

```stata
* Probability of being in category 1
margins, predict(outcome(1))

* Probability of being in category 5
margins, predict(outcome(5))

* Predicted probabilities for all categories
margins, predict(outcome(1)) predict(outcome(2)) predict(outcome(3)) ///
    predict(outcome(4)) predict(outcome(5))
```

---

## 6. Multilevel Models (Optional)

Use when you have hierarchical data (students in schools, respondents in states) and theory suggests random effects.

### Random Intercept (Linear)

```stata
* Students (i) nested in schools (j)
mixed test_score ses || school:
```

### Random Intercept (Binary)

```stata
* Binary outcome with random intercepts
melogit graduated ses || school:
```

### Key Distinction

- **Cluster-robust SEs**: Adjusts SEs for clustering; coefficients are population-averaged
- **Multilevel models**: Explicitly models variance at each level; coefficients are conditional on random effects

Choose based on your research question and theory, not convenience.

---

## 7. Diagnostics

### Multicollinearity

```stata
reg price mpg weight length, robust
estat vif
```

**Rule of thumb**: VIF > 10 suggests problematic collinearity.

### Influential Observations

```stata
reg price mpg weight

* Leverage (unusual X values)
predict leverage, leverage
gen high_leverage = leverage > 2*(3+1)/74  // 2*(k+1)/n

* Cook's Distance (influential points)
predict cooksd, cooksd
gen influential = cooksd > 4/74  // 4/n

tab high_leverage
tab influential
```

### Residual Plots

```stata
reg price mpg weight, robust
predict resid, residual
predict yhat, xb

* Histogram of residuals
histogram resid, normal title("Residual Distribution")
graph export "$figures/residual_hist.png", replace

* Residual vs fitted
scatter resid yhat, yline(0, lpattern(dash)) ///
    title("Residuals vs Fitted")
graph export "$figures/resid_fitted.png", replace
```

---

## Quick Reference

### OLS Variants

| Task | Command |
|------|---------|
| Robust SE | `reg y x, robust` |
| Clustered SE | `reg y x, cluster(id)` |
| Two-way cluster | `reghdfe y x, cluster(id time)` |

### Binary Models

| Task | Command |
|------|---------|
| Logit | `logit y x, robust` |
| Probit | `probit y x, robust` |
| Odds ratios | `logit y x, or` |
| Marginal effects | `margins, dydx(*)` |

### Count Models

| Task | Command |
|------|---------|
| Poisson | `poisson y x, robust` |
| Negative binomial | `nbreg y x, robust` |
| IRR | `poisson y x, irr` |

### Margins Commands

| Task | Command |
|------|---------|
| AME for all | `margins, dydx(*)` |
| At specific values | `margins, at(x=(1 2 3))` |
| By group | `margins group, dydx(x)` |
| Plot | `marginsplot` |
