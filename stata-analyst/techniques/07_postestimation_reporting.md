# Post-Estimation and Reporting in Stata

What you do after you estimate—so outputs match journal expectations. All code tested on Stata 15+.

---

## 1. Estimates Workflow

### Store Results

```stata
sysuse auto, clear

reg price mpg, robust
estimates store base

reg price mpg weight, robust
estimates store controls1

reg price mpg weight i.foreign, robust
estimates store controls2

reg price mpg weight i.foreign headroom trunk, robust
estimates store full
```

### List and Retrieve

```stata
* List all stored estimates
estimates dir

* Replay a specific model
estimates replay controls1

* Restore for post-estimation commands
estimates restore full
display "R-squared: " e(r2)
```

### Naming Conventions

Use consistent, descriptive names:

| Pattern | Example |
|---------|---------|
| By specification | `base`, `controls`, `full` |
| By sample | `main`, `robust_sample`, `placebo` |
| By method | `ols`, `iv`, `matching` |

---

## 2. Nested Tables with esttab

### Standard Journal Format

```stata
esttab base controls1 controls2 full, ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("(1)" "(2)" "(3)" "(4)") ///
    title("Table 2: Price Determinants") ///
    addnotes("Robust standard errors in parentheses") ///
    drop(0.foreign) ///
    stats(N r2, labels("N" "R-squared") fmt(%9.0fc %9.3f))
```

### Export to RTF (Word-Compatible)

```stata
esttab base controls1 controls2 full using "$tables/table2_models.rtf", ///
    replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("(1)" "(2)" "(3)" "(4)") ///
    title("Table 2: Price Determinants") ///
    drop(0.foreign) ///
    stats(N r2, labels("N" "R-squared") fmt(%9.0fc %9.3f))
```

### Export to CSV

```stata
esttab base controls1 controls2 full using "$tables/table2_models.csv", ///
    replace csv ///
    se star(* 0.10 ** 0.05 *** 0.01)
```

### Export to LaTeX

```stata
esttab base controls1 controls2 full using "$tables/table2_models.tex", ///
    replace booktabs ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("(1)" "(2)" "(3)" "(4)") ///
    drop(0.foreign) ///
    stats(N r2, labels("N" "R-squared") fmt(%9.0fc %9.3f))
```

---

## 3. Predicted Values and Effects

### Predicted Values for Hypothetical Cases

```stata
reg price mpg weight i.foreign, robust

* Domestic car with mpg=20, weight=3000
margins, at(mpg=20 weight=3000 foreign=0)

* Foreign car with same specs
margins, at(mpg=20 weight=3000 foreign=1)
```

### Save Predictions to Data

```stata
reg price mpg weight i.foreign, robust
predict yhat, xb          // predicted values
predict resid, residual   // residuals

summarize price yhat resid
```

### Marginal Effects for Presentation

```stata
logit union wage age grade, robust

* Average marginal effects
margins, dydx(*)

* Save to matrix for export
margins, dydx(*) post
esttab, cells("b(fmt(4)) se(fmt(4)) p(fmt(3))") ///
    title("Average Marginal Effects")
```

### Marginsplot

```stata
reg price i.foreign##c.mpg, robust
margins foreign, at(mpg=(15(5)35))
marginsplot, title("Predicted Price by MPG and Origin") ///
    ytitle("Predicted Price ($)") xtitle("Miles per Gallon")
graph export "$figures/figure1_margins.png", replace
```

---

## 4. Model Diagnostics

### Multicollinearity (VIF)

```stata
reg price mpg weight length, robust
estat vif
```

| VIF | Interpretation |
|-----|----------------|
| < 5 | Generally acceptable |
| 5-10 | Moderate concern |
| > 10 | High collinearity |

### Influential Points

```stata
reg price mpg weight
predict leverage, leverage
predict cooksd, cooksd

* Flag problematic observations
gen high_leverage = leverage > 2*(3+1)/_N  // 2*(k+1)/n rule
gen influential = cooksd > 4/_N            // 4/n rule

tab high_leverage
tab influential
list make price mpg weight if influential == 1
```

### Residual Diagnostics

```stata
reg price mpg weight, robust
predict resid, residual
predict yhat, xb

* Residual histogram
histogram resid, normal title("Residual Distribution")
graph export "$figures/residual_hist.png", replace

* Residual vs fitted plot
scatter resid yhat, yline(0, lpattern(dash)) ///
    title("Residuals vs Fitted Values")
graph export "$figures/resid_fitted.png", replace
```

### Heteroskedasticity

Robust SEs handle this, but to test formally:

```stata
reg price mpg weight
estat hettest
```

---

## 5. Table 1: Descriptive Statistics

### Overall Summary

```stata
tabstat price mpg weight, stat(n mean sd min max) col(stat)
```

### Summary by Group

```stata
tabstat price mpg weight, by(foreign) stat(n mean sd) nototal
```

### Publication-Ready Table 1

```stata
* Using estpost + esttab
estpost summarize price mpg weight length
esttab, cells("count mean(fmt(2)) sd(fmt(2)) min max") ///
    nomtitle nonumber title("Table 1: Descriptive Statistics")
```

### Export Summary Statistics

```stata
estpost summarize price mpg weight length
esttab using "$tables/table1_descriptives.rtf", ///
    replace ///
    cells("count mean(fmt(2)) sd(fmt(2)) min max") ///
    nomtitle nonumber ///
    title("Table 1: Descriptive Statistics")
```

---

## 6. Balance Tables

For treatment/control comparisons:

### Simple Balance Check

```stata
* Means by treatment
tabstat mpg weight length, by(treat) stat(mean sd) nototal
```

### T-Tests for Differences

```stata
ttest mpg, by(treat)
ttest weight, by(treat)
ttest length, by(treat)
```

### Formal Balance Table

```stata
* Create treatment indicator
gen treat = (price > 6000)

* Compare means and run t-tests
foreach var in mpg weight length {
    display ""
    display "=== `var' ==="
    ttest `var', by(treat)
}
```

---

## 7. Output Naming Conventions

### Standard File Names

```stata
* Tables
"$tables/table1_descriptives.rtf"
"$tables/table2_main_models.rtf"
"$tables/table3_robustness.rtf"
"$tables/tableA1_balance.rtf"  // appendix

* Figures
"$figures/figure1_trends.png"
"$figures/figure2_event_study.png"
"$figures/figureA1_placebo.png"  // appendix
```

### In-Code Documentation

```stata
* ===================================
* Table 2: Main Regression Results
* ===================================
reg price mpg weight i.foreign, robust
estimates store m1
// ... more models

esttab m1 m2 m3 using "$tables/table2_main_models.rtf", replace ...
```

---

## 8. Complete Output Workflow Example

```stata
* ===========================================================================
* Output Generation Script
* ===========================================================================

clear all
set more off
use "$clean/analysis_sample.dta", clear

* -----------------------------------
* Table 1: Descriptive Statistics
* -----------------------------------
estpost summarize price mpg weight length
esttab using "$tables/table1_descriptives.rtf", replace ///
    cells("count mean(fmt(2)) sd(fmt(2)) min max") nomtitle nonumber

* -----------------------------------
* Table 2: Main Models
* -----------------------------------
reg price mpg, robust
estimates store m1

reg price mpg weight, robust
estimates store m2

reg price mpg weight i.foreign, robust
estimates store m3

esttab m1 m2 m3 using "$tables/table2_main_models.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("(1)" "(2)" "(3)") ///
    stats(N r2, labels("N" "R-squared") fmt(%9.0fc %9.3f))

* -----------------------------------
* Figure 1: Coefficient Plot
* -----------------------------------
reg price mpg weight headroom trunk length, robust
coefplot, drop(_cons) xline(0) ///
    title("Coefficient Estimates")
graph export "$figures/figure1_coef_plot.png", replace

display "Output generation complete!"
```

---

## Quick Reference

### esttab Options

| Option | Purpose |
|--------|---------|
| `se` | Show standard errors |
| `star(* .10 ** .05 *** .01)` | Significance stars |
| `mtitles()` | Column titles |
| `drop()` | Omit variables |
| `stats(N r2)` | Add statistics |
| `replace` | Overwrite file |

### Export Formats

| Format | Command |
|--------|---------|
| RTF (Word) | `using "file.rtf"` |
| CSV | `using "file.csv", csv` |
| LaTeX | `using "file.tex", booktabs` |
| Screen | no `using` clause |

### Margins Commands

| Task | Command |
|------|---------|
| Average marginal effects | `margins, dydx(*)` |
| At specific values | `margins, at(x=(1 2 3))` |
| Plot | `marginsplot` |
| Export to table | `margins, dydx(*) post` then `esttab` |
