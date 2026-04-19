### 00_index.md

# Stata Statistical Techniques - Index

Quick lookup for statistical methods in Stata. All code tested on Stata 15.1.

---

## File Guide

| File | Topics |
|------|--------|
| `01_core_econometrics.md` | TWFE, DiD, Event Studies, IV, Matching, Mediation, Standard Errors |
| `02_survey_resampling.md` | Survey Weights, Bootstrap, Randomization Inference, Oaxaca |
| `03_synthetic_control.md` | synth package for comparative case studies |
| `04_visualization.md` | esttab tables, coefplot, graphs, summary statistics |
| `05_best_practices.md` | Master do-files, path management, code organization |

---

## Quick Lookup by Method

### Panel & Fixed Effects
- **TWFE (reghdfe)** → `01_core_econometrics.md` Section 1

### Difference-in-Differences
- **Traditional DiD** → `01_core_econometrics.md` Section 2.1
- **Callaway-Sant'Anna (csdid)** → `01_core_econometrics.md` Section 2.2
- **Event Studies** → `01_core_econometrics.md` Section 3

### Instrumental Variables
- **Basic 2SLS (ivreg2)** → `01_core_econometrics.md` Section 4
- **First-stage diagnostics** → `01_core_econometrics.md` Section 4.2
- **Overidentification tests** → `01_core_econometrics.md` Section 4.3

### Matching
- **Propensity Score (psmatch2)** → `01_core_econometrics.md` Section 5.1
- **Coarsened Exact (cem)** → `01_core_econometrics.md` Section 5.3
- **Balance testing (pstest)** → `01_core_econometrics.md` Section 5.2

### Standard Errors & Inference
- **Clustered SEs** → `01_core_econometrics.md` Section 6.1
- **Wild Cluster Bootstrap** → `01_core_econometrics.md` Section 6.2
- **Randomization Inference** → `02_survey_resampling.md` Section 4

### Survey Methods
- **Survey design (svyset)** → `02_survey_resampling.md` Section 1
- **Weighted estimation (svy:)** → `02_survey_resampling.md` Section 1
- **Subpopulation analysis** → `02_survey_resampling.md` Section 1

### Decomposition
- **Oaxaca-Blinder** → `02_survey_resampling.md` Section 5

### Synthetic Control
- **synth package** → `03_synthetic_control.md`

### Output & Visualization
- **Regression tables (esttab)** → `04_visualization.md` Section 1
- **Coefficient plots (coefplot)** → `04_visualization.md` Section 2
- **Summary statistics** → `04_visualization.md` Section 3

---

## Package Quick Reference

| Task | Package | Command |
|------|---------|---------|
| High-dim FE | `reghdfe` | `reghdfe y x, absorb(id year) cluster(id)` |
| Modern DiD | `csdid` | `csdid y, ivar(id) time(year) gvar(gvar) notyet` |
| DiD event study | `csdid_estat` | `csdid_estat event` |
| IV estimation | `ivreg2` | `ivreg2 y (endog = iv), first robust` |
| PSM | `psmatch2` | `psmatch2 treat x1 x2, outcome(y)` |
| Balance test | `pstest` | `pstest x1 x2, both` |
| CEM | `cem` | `cem x1 (bins) x2 (#5), treatment(treat)` |
| Wild bootstrap | `boottest` | `boottest x, cluster(c) reps(999) nograph` |
| Randomization | `ritest` | `ritest treat _b[treat], reps(500):` |
| Oaxaca | `oaxaca` | `oaxaca y x1 x2, by(group)` |
| Synth control | `synth` | `synth y x1 y(1985), trunit(1) trperiod(1990)` |
| Tables | `estout` | `esttab m1 m2, se star(* .10 ** .05 *** .01)` |
| Coef plots | `coefplot` | `coefplot, drop(_cons) xline(0)` |
| Survey | built-in | `svyset psu [pw=wt], strata(strat)` |

---

## Built-in Datasets for Examples

| Dataset | Command | Variables |
|---------|---------|-----------|
| auto | `sysuse auto` | price, mpg, weight, foreign |
| nlsw88 | `sysuse nlsw88` | wage, union, age, grade, tenure |
| nhanes2f | `webuse nhanes2f` | height, weight, age, sex, finalwgt |

---

## Version Notes

- **Stata 15+**: All methods except rdrobust
- **Stata 16+**: rdrobust (RD estimation)


---

### 01_core_econometrics.md

# Core Econometrics in Stata

Panel methods, causal inference, and standard errors. All code tested on Stata 15+.

---

## 1. Two-Way Fixed Effects (TWFE)

### When to Use
- Panel data with unit and time dimensions
- Unobserved unit and time confounders
- Consistent treatment timing (or verified no negative weights)

### Basic TWFE with reghdfe

```stata
* Declare panel
xtset id period

* TWFE with unit and time fixed effects, clustered SEs
reghdfe y x1 treat, absorb(id period) cluster(id)
```

### Two-Way Clustering

```stata
* Cluster by both unit and time
reghdfe y x1 treat, absorb(id period) cluster(id period)
```

### Store and Compare Models

```stata
* Run models
quietly reghdfe y x1 treat, absorb(id period) cluster(id)
estimates store m1_oneway

quietly reghdfe y x1 treat, absorb(id period) cluster(id period)
estimates store m2_twoway

* Comparison table
esttab m1_oneway m2_twoway, se mtitle("One-way" "Two-way") ///
    star(* 0.10 ** 0.05 *** 0.01)
```

---

## 2. Difference-in-Differences (DiD)

### 2.1 Traditional DiD

```stata
* Create interaction term
gen treat_post = treated_group * post_period

* DiD regression with FE
reghdfe y treat_post, absorb(id period) cluster(id)

* Or explicit interaction
reg y i.treated_group##i.post_period x1, cluster(id)
```

### 2.2 Callaway-Sant'Anna (Staggered Treatment)

For heterogeneous treatment effects with staggered timing:

```stata
* Data setup:
* - gvar: first treatment period (0 for never-treated)
* - id: panel unit identifier
* - year: time period

* Run csdid
csdid y, ivar(id) time(year) gvar(gvar) notyet

* Event study aggregation
csdid_estat event

* Simple ATT
csdid_estat simple
```

**Key options:**
- `notyet`: Use not-yet-treated as control (recommended)
- `never`: Use never-treated as control only

### 2.3 Post-Estimation for csdid

```stata
* After running csdid:

* Event study (dynamic effects)
csdid_estat event

* Group-time ATTs
csdid_estat group

* Calendar time ATTs
csdid_estat calendar

* Simple overall ATT
csdid_estat simple
```

---

## 3. Event Studies

### Manual Event Study

```stata
* Create event time relative to treatment
gen event_time = year - first_treat
replace event_time = -99 if missing(first_treat)  // Never treated

* Bin endpoints
replace event_time = -5 if event_time < -5 & event_time != -99
replace event_time = 5 if event_time > 5 & event_time != -99

* Create dummies (omit t=-1 as reference)
tab event_time, gen(et_)

* Estimate (drop reference period)
reghdfe y et_1 et_2 et_3 et_4 et_6 et_7 et_8 et_9 et_10 et_11, ///
    absorb(id year) cluster(id)
```

### Event Study from csdid

```stata
* Run csdid first
csdid y, ivar(id) time(year) gvar(gvar) notyet

* Get event study estimates
csdid_estat event
```

---

## 4. Instrumental Variables (IV)

### 4.1 Basic 2SLS

```stata
* Built-in ivregress
ivregress 2sls y (x_endog = z), robust
estat firststage

* ivreg2 with more diagnostics
ivreg2 y (x_endog = z), first robust
```

### 4.2 IV Diagnostics

ivreg2 automatically reports:
- **First-stage F-statistic**: Should be > 10 (Stock-Yogo rule)
- **Kleibergen-Paap rk F**: Robust weak instrument test
- **Anderson-Rubin CI**: Weak-instrument-robust confidence interval

```stata
* Detailed first-stage output
ivreg2 y (x_endog = z), first robust

* Key output to check:
* - F test of excluded instruments: F > 10
* - Stock-Yogo critical values for comparison
* - Kleibergen-Paap rk Wald F statistic
```

### 4.3 Multiple Instruments (Overidentification)

```stata
* Multiple instruments
ivreg2 y (x_endog = z1 z2), robust

* Hansen J statistic (overidentification test) reported automatically
* H0: All instruments are valid
* High p-value = cannot reject validity
```

### 4.4 IV with Fixed Effects

```stata
* Using ivreghdfe (install: ssc install ivreghdfe)
ivreghdfe y (x_endog = z), absorb(id year) cluster(id)
```

---

## 5. Matching Methods

### 5.1 Propensity Score Matching

```stata
* psmatch2: estimate PS and match
psmatch2 treat x1 x2 i.category, outcome(y) neighbor(1) common

* Check balance
pstest x1 x2, both

* The ATT is displayed in the output table
```

**Key options:**
- `neighbor(k)`: k nearest neighbors
- `caliper(c)`: Maximum PS distance
- `common`: Restrict to common support

### 5.2 Balance Assessment

```stata
* After psmatch2
pstest x1 x2, both

* Output shows:
* - Mean bias before/after matching
* - % reduction in bias
* - t-tests for balance
```

### 5.3 Coarsened Exact Matching (CEM)

```stata
* CEM with specified bins
cem age (20 30 40 50 60) grade (#5), treatment(treat)

* Estimate with CEM weights
reg y treat x1 x2 [iweight=cem_weights], robust
```

---

## 6. Standard Errors and Inference

### 6.1 Clustered Standard Errors

```stata
* One-way clustering
reghdfe y x treat, absorb(id period) cluster(id)

* Two-way clustering
reghdfe y x treat, absorb(id period) cluster(id period)
```

### 6.2 Wild Cluster Bootstrap (Few Clusters)

When you have fewer than ~40 clusters:

```stata
* Run regression with clustering
reg y treat x, cluster(state)

* Wild cluster bootstrap
boottest treat, cluster(state) reps(999) seed(12345) nograph

* Output:
* - Bootstrap t-statistic
* - Bootstrap p-value
* - 95% confidence interval
```

### 6.3 Standard Bootstrap

```stata
* Bootstrap standard errors
bootstrap _b, reps(500) seed(12345): reg y x1 x2 treat

* Bootstrap specific statistics
bootstrap diff = (_b[treat]), reps(500) seed(12345): reg y x1 treat
```

### 6.4 Randomization Inference

```stata
* Permutation test with stratification
ritest treat _b[treat], reps(500) seed(12345) strata(block): ///
    reg y treat, robust

* Output shows:
* - Observed coefficient
* - p-value from permutation distribution
```

---

## 7. Regression Discontinuity (RD)

**Note:** The `rdrobust` package requires Stata 16+. For Stata 15, use manual polynomial approaches.

### Manual RD (Stata 15 compatible)

```stata
* Create centered running variable
gen x_centered = running_var - cutoff

* Treatment indicator
gen treat = (running_var >= cutoff)

* Local linear regression (narrow bandwidth)
reg y treat x_centered c.x_centered#i.treat if abs(x_centered) < bandwidth

* The coefficient on treat is the RD estimate
```

### rdrobust (Stata 16+)

```stata
* Basic RD estimation
rdrobust y running_var, c(0)

* With options
rdrobust y running_var, c(0) kernel(triangular) bwselect(mserd)

* Manipulation test
rddensity running_var, c(0)

* RD plot
rdplot y running_var, c(0)
```

---

## 8. Causal Mediation

```stata
* Mediation analysis requires:
* - Treatment variable (treat)
* - Mediator variable (m)
* - Outcome variable (y)

* Using medeff (install: ssc install medeff)

* Step 1: Mediator model
reg m treat x1

* Step 2: Outcome model
reg y treat m x1

* Step 3: Mediation effects
medeff (reg m treat x1) (reg y treat m x1), ///
    treat(treat) mediate(m) sims(1000)

* Output:
* - ACME: Average Causal Mediation Effect (indirect)
* - ADE: Average Direct Effect
* - Total Effect: ACME + ADE
* - Proportion Mediated: ACME / Total
```

---

## Quick Reference

### Package Installation

```stata
* Core packages
ssc install reghdfe, replace
ssc install ftools, replace
ssc install estout, replace
ssc install coefplot, replace

* DiD methods
ssc install csdid, replace
ssc install drdid, replace

* IV
ssc install ivreg2, replace
ssc install ranktest, replace

* Matching
ssc install psmatch2, replace
ssc install cem, replace

* Inference
ssc install boottest, replace
ssc install ritest, replace

* RD (Stata 16+ only)
ssc install rdrobust, replace
ssc install rddensity, replace
```

### Command Quick Reference

| Task | Command |
|------|---------|
| TWFE | `reghdfe y x, absorb(id t) cluster(id)` |
| Modern DiD | `csdid y, ivar(id) time(t) gvar(g)` |
| Event study | `csdid_estat event` |
| IV | `ivreg2 y (endog = iv), first robust` |
| PSM | `psmatch2 treat x, outcome(y)` |
| CEM | `cem x1 x2, treatment(treat)` |
| Wild bootstrap | `boottest x, cluster(c) nograph` |
| Randomization | `ritest treat _b[treat], reps(500):` |

### Diagnostic Checks

1. **TWFE**: Check for negative weights with staggered timing
2. **DiD**: Test parallel trends with event study pre-trends
3. **IV**: First-stage F > 10, check overidentification
4. **Matching**: Balance statistics with `pstest`
5. **Clustering**: Use wild bootstrap with < 40 clusters


---

### 02_survey_resampling.md

# Survey & Resampling Methods in Stata

Survey weights, bootstrap, randomization inference, and decomposition. All code tested on Stata 15+.

---

## 1. Survey Methods

### Setup Survey Design

```stata
* Using nhanes2f dataset as example
webuse nhanes2f, clear

* Setup: psuid = PSU, stratid = stratum, finalwgt = weight
svyset psuid [pweight=finalwgt], strata(stratid)
```

### Check Survey Setup

```stata
svydescribe
```

### Survey-Weighted Estimation

```stata
* Survey mean
svy: mean height weight

* Survey mean by group
svy: mean height, over(sex)

* Survey regression
svy: reg height weight age i.sex

* Survey logit
svy: logit highbp age i.sex weight
```

### Subpopulation Analysis

Correct way to analyze subgroups (maintains correct SEs):

```stata
* Analyze females only
svy, subpop(female): mean height weight

* Analyze using if condition
svy, subpop(if age >= 40): mean bpsystol
```

**Note:** Always use `subpop()` rather than `if` for survey data to get correct variance estimates.

---

## 2. Bootstrap Methods

### Standard Bootstrap

```stata
sysuse auto, clear

* Bootstrap standard errors for all coefficients
bootstrap _b, reps(500) seed(12345): reg price mpg weight foreign

* Bootstrap specific statistic
bootstrap diff = (_b[foreign]), reps(500) seed(12345): ///
    reg price mpg weight foreign
```

### Bootstrap Options

| Option | Purpose |
|--------|---------|
| `reps(#)` | Number of replications |
| `seed(#)` | Random seed for reproducibility |
| `bca` | Bias-corrected accelerated CIs |
| `strata(var)` | Stratified resampling |
| `cluster(var)` | Cluster resampling |

---

## 3. Wild Cluster Bootstrap

For inference with few clusters (< 40):

```stata
* Create clustered data
clear
set seed 12345
set obs 500
gen state = ceil(_n/50)
gen treat = (state <= 5)
gen x = rnormal()
gen y = 1 + 0.5*treat + 0.3*x + rnormal(0, 1)

* Standard clustered SE
reg y treat x, cluster(state)

* Wild cluster bootstrap
boottest treat, cluster(state) reps(999) seed(12345) nograph
```

**Output includes:**
- Bootstrap t-statistic
- Bootstrap p-value
- 95% confidence interval robust to few clusters

---

## 4. Randomization Inference

```stata
* Create experimental data
clear
set seed 12345
set obs 200
gen id = _n
gen block = ceil(_n/20)
gen treat = mod(_n, 2)
gen y = 1 + 0.5*treat + rnormal(0, 1)

* Standard OLS
reg y treat, robust

* Randomization inference with stratification
ritest treat _b[treat], reps(500) seed(12345) strata(block): ///
    reg y treat, robust
```

**Output shows:**
- Observed coefficient
- Number of permutations where |T| >= |T(obs)|
- Exact p-value from permutation distribution

---

## 5. Oaxaca-Blinder Decomposition

```stata
* Use nlsw88 data
sysuse nlsw88, clear
keep if !missing(wage, union, age, grade, tenure)

* Basic decomposition by union status
oaxaca wage age grade tenure, by(union)

* Detailed decomposition
oaxaca wage age grade tenure, by(union) detail

* Pooled reference coefficients
oaxaca wage age grade tenure, by(union) pooled
```

### Interpretation

The output shows:
- **Endowments**: Differences due to characteristics (what if Group 2 had Group 1's X values)
- **Coefficients**: Differences due to returns to characteristics (unexplained/discrimination)
- **Interaction**: Combined effect

---

## Quick Reference

### Survey Commands

| Command | Purpose |
|---------|---------|
| `svyset` | Define survey design |
| `svy:` | Prefix for survey estimation |
| `svydescribe` | Describe survey design |
| `subpop()` | Analyze subpopulation |

### Resampling Commands

| Command | Purpose |
|---------|---------|
| `bootstrap` | Standard bootstrap |
| `boottest` | Wild cluster bootstrap |
| `ritest` | Randomization inference |

### Package Installation

```stata
ssc install boottest, replace
ssc install ritest, replace
ssc install oaxaca, replace
```


---

### 03_synthetic_control.md

# Synthetic Control Methods in Stata

Synthetic control method for comparative case studies. All code tested on Stata 15+.

---

## 1. Overview

The synthetic control method constructs a weighted combination of control units to serve as a counterfactual for a treated unit. It is designed for:

- Single treated unit
- Aggregate-level data (states, countries, regions)
- Clear treatment timing
- Multiple potential control units

---

## 2. Data Requirements

Panel data structure with:
- Unit identifier
- Time variable
- Outcome variable
- Predictor variables

```stata
* Declare panel structure
tsset unit_id time_var
```

---

## 3. Basic Synthetic Control

```stata
* Install synth package
ssc install synth, replace

* Basic syntax
synth outcome_var predictors, ///
    trunit(#) trperiod(#)
```

### Example with Simulated Data

```stata
clear
set seed 12345
set obs 400

* Create panel: 20 states, 20 years each
gen state = ceil(_n/20)
bysort state: gen year = 1980 + _n

* Outcome variable
gen y = 100 + state*2 + year*0.5 + rnormal(0, 5)

* Treatment: state 1 treated after year 1990
replace y = y - 15 if state == 1 & year >= 1990

* Covariates
gen x1 = rnormal(50, 10)
gen x2 = rnormal(1000, 200)

* Declare panel
tsset state year

* Run synthetic control
synth y x1 x2 y(1985) y(1988), trunit(1) trperiod(1990)
```

---

## 4. Specifying Predictors

### Average of Variable Over Pre-Period

```stata
* x1 averaged over all pre-treatment periods
synth y x1 x2, trunit(1) trperiod(1990)
```

### Specific Year Values

```stata
* y at specific years as predictors
synth y y(1985) y(1988), trunit(1) trperiod(1990)
```

### Range of Years

```stata
* y averaged over 1985-1988
synth y y(1985(1)1988), trunit(1) trperiod(1990)
```

### Combined Predictors

```stata
synth y x1 x2 y(1985) y(1988), trunit(1) trperiod(1990)
```

---

## 5. Output Interpretation

The synth output shows:

### RMSPE (Root Mean Squared Prediction Error)
- Measures pre-treatment fit
- Lower is better

### Unit Weights
- Which control units comprise the synthetic control
- Weights sum to 1

### Predictor Balance
- Compares treated vs synthetic control on predictors
- Should be similar if fit is good

---

## 6. Options

| Option | Purpose |
|--------|---------|
| `trunit(#)` | Treated unit ID |
| `trperiod(#)` | First treatment period |
| `fig` | Display results figure |
| `keep(filename)` | Save results to file |
| `nested` | Use nested optimization |
| `allopt` | Try all optimization methods |

---

## 7. Inference

### Placebo Tests (In-Space)

Run synth for each control unit as if it were treated:

```stata
* Store treated unit result
synth y x1 x2 y(1985) y(1988), trunit(1) trperiod(1990) ///
    keep(synth_treated) replace

* Placebo for control unit 2
synth y x1 x2 y(1985) y(1988), trunit(2) trperiod(1990) ///
    keep(synth_placebo2) replace

* Compare RMSPEs
* Treated effect is significant if RMSPE ratio is large
```

### Placebo Tests (In-Time)

Apply treatment at different (fake) times:

```stata
* True treatment 1990
synth y x1 x2 y(1982) y(1985), trunit(1) trperiod(1990)

* Placebo: treatment at 1985 (before actual treatment)
synth y x1 x2 y(1982), trunit(1) trperiod(1985)
```

---

## 8. Limitations

- Single treated unit (not for multiple treatment)
- Requires good pre-treatment fit
- Sensitive to predictor choice
- No built-in inference (must do placebo tests)
- Cannot extrapolate beyond donor pool characteristics

---

## Quick Reference

### Basic Syntax

```stata
synth outcome predictors, trunit(#) trperiod(#)
```

### Package Installation

```stata
ssc install synth, replace
```

### Key Components

| Component | Description |
|-----------|-------------|
| `outcome` | Dependent variable |
| `predictors` | Variables to match on |
| `trunit()` | ID of treated unit |
| `trperiod()` | First treatment period |


---

### 04_visualization.md

# Visualization & Output in Stata

Publication-quality tables, coefficient plots, and figures. All code tested on Stata 15+.

---

## 1. Regression Tables with esttab

### Basic Table

```stata
* Run and store models
quietly reg price mpg
estimates store m1

quietly reg price mpg weight
estimates store m2

quietly reg price mpg weight foreign
estimates store m3

* Basic table
esttab m1 m2 m3, se star(* 0.10 ** 0.05 *** 0.01)
```

### Publication-Ready Table

```stata
esttab m1 m2 m3, ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitle("Model 1" "Model 2" "Model 3") ///
    title("Price Regressions") ///
    keep(mpg weight foreign) ///
    order(foreign mpg weight)
```

### Export to File

```stata
* Text file
esttab m1 m2 m3 using "table1.txt", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitle("Model 1" "Model 2" "Model 3")

* LaTeX
esttab m1 m2 m3 using "table1.tex", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    booktabs label

* RTF (Word-compatible)
esttab m1 m2 m3 using "table1.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01)
```

### Common esttab Options

| Option | Description |
|--------|-------------|
| `se` | Show standard errors |
| `t` | Show t-statistics |
| `p` | Show p-values |
| `ci` | Show confidence intervals |
| `star(...)` | Define significance stars |
| `mtitle(...)` | Column titles |
| `title(...)` | Table title |
| `keep(...)` | Variables to show |
| `drop(...)` | Variables to hide |
| `order(...)` | Variable order |
| `label` | Use variable labels |
| `booktabs` | LaTeX booktabs format |
| `replace` | Overwrite existing file |

---

## 2. Coefficient Plots

### Basic Coefficient Plot

```stata
* After running regression
reg price mpg weight foreign i.rep78

* Plot coefficients
coefplot, drop(_cons) xline(0) ///
    title("Coefficient Plot")

graph export "coefplot.png", replace
```

### Multiple Model Comparison

```stata
* Store multiple models first
quietly reg price mpg
estimates store m1

quietly reg price mpg weight
estimates store m2

quietly reg price mpg weight foreign
estimates store m3

* Compare in single plot
coefplot m1 m2 m3, drop(_cons) xline(0) ///
    legend(order(2 "Model 1" 4 "Model 2" 6 "Model 3"))

graph export "coefplot_comparison.png", replace
```

### Vertical Coefficient Plot

```stata
coefplot m3, drop(_cons) vertical ///
    yline(0, lpattern(dash)) ///
    title("Vertical Coefficient Plot")
```

### Event Study Style Plot

```stata
* After event study regression with lead/lag dummies
coefplot, keep(lead_* lag_*) vertical ///
    yline(0, lpattern(dash)) ///
    xline(0.5, lpattern(dash) lcolor(red)) ///
    xlabel(, angle(45)) ///
    xtitle("Event Time") ytitle("Effect")
```

### Customizing coefplot

```stata
coefplot m1 m2, drop(_cons) xline(0) ///
    ciopts(recast(rcap)) ///              // Cap ends on CI
    msymbol(D) ///                         // Diamond markers
    mcolor(navy) ///                       // Marker color
    levels(95 90) ///                      // Multiple CI levels
    legend(order(1 "95% CI" 2 "90% CI"))
```

---

## 3. Summary Statistics

### Basic Summary

```stata
summarize price mpg weight

* Detailed with percentiles
summarize price, detail
```

### tabstat (Formatted)

```stata
* Multiple statistics
tabstat price mpg weight, stat(mean sd min max n) columns(statistics)

* By group
tabstat price mpg weight, by(foreign) stat(mean sd n)
```

### Summary Table with estpost

```stata
* Summary statistics table
estpost summarize price mpg weight
esttab, cells("mean(fmt(2)) sd(fmt(2)) min max count") nomtitle nonumber

* Export to file
esttab using "summary_stats.tex", replace ///
    cells("mean(fmt(2)) sd(fmt(2)) min max count") ///
    nomtitle nonumber booktabs
```

### Balance Table

```stata
* By treatment group
bysort treatment: summarize y x1 x2

* Or use tabstat
tabstat y x1 x2, by(treatment) stat(mean sd n) nototal
```

---

## 4. Basic Graphs

### Scatter Plot with Fit Line

```stata
twoway (scatter y x) (lfit y x), ///
    title("Scatter with Linear Fit") ///
    xtitle("X Variable") ytitle("Y Variable") ///
    legend(off)

graph export "scatter.png", replace
```

### Binned Scatter (binscatter)

```stata
* Install: ssc install binscatter
binscatter y x, controls(z1 z2) ///
    title("Binned Scatter") ///
    xtitle("X") ytitle("Y | Controls")
```

### Time Series

```stata
twoway line y year, ///
    title("Outcome Over Time") ///
    xtitle("Year") ytitle("Outcome")

* Multiple series
twoway (line y1 year) (line y2 year), ///
    legend(order(1 "Series 1" 2 "Series 2"))
```

### Histogram

```stata
histogram y, frequency ///
    title("Distribution of Y") ///
    xtitle("Y") ytitle("Frequency")
```

### Kernel Density

```stata
kdensity y, ///
    title("Density of Y") ///
    xtitle("Y") ytitle("Density")

* By group
twoway (kdensity y if treat==0) (kdensity y if treat==1), ///
    legend(order(1 "Control" 2 "Treatment"))
```

---

## 5. Graph Formatting

### Publication Scheme

```stata
* Set clean scheme
set scheme s1mono  // Black and white
set scheme s1color // Color version

* Or use custom
ssc install grstyle, replace
ssc install palettes, replace
ssc install colrspace, replace

grstyle init
grstyle set plain
grstyle set legend 6, nobox
grstyle set color navy maroon forest_green
```

### Common Graph Options

```stata
twoway ..., ///
    title("Main Title") ///
    subtitle("Subtitle") ///
    xtitle("X Axis Label") ///
    ytitle("Y Axis Label") ///
    xlabel(0(10)100) ///           // X ticks at 0,10,20,...,100
    ylabel(, angle(horizontal)) /// // Horizontal Y labels
    legend(order(1 "First" 2 "Second") pos(6)) /// // Bottom legend
    note("Note: Sample description") ///
    graphregion(color(white)) ///  // White background
    plotregion(margin(zero))       // No margins
```

### Export Formats

```stata
* PNG (web/slides)
graph export "figure.png", replace width(2400)

* PDF (publication)
graph export "figure.pdf", replace

* EPS (LaTeX)
graph export "figure.eps", replace
```

### Combine Multiple Graphs

```stata
* Create individual graphs
twoway scatter y1 x, name(g1, replace) title("Panel A")
twoway scatter y2 x, name(g2, replace) title("Panel B")

* Combine
graph combine g1 g2, rows(1) ///
    title("Combined Figure")

graph export "combined.png", replace
```

---

## 6. RD Plots (Stata 16+)

```stata
* Using rdplot (requires rdrobust package)
rdplot y running_var, c(0) ///
    graph_options(title("RD Plot") ///
                  xtitle("Running Variable") ///
                  ytitle("Outcome"))
```

---

## Quick Reference

### Table Output Commands

| Command | Purpose |
|---------|---------|
| `esttab` | Regression tables |
| `estpost` | Post results for tables |
| `tabstat` | Summary statistics |
| `tabout` | Cross-tabulations |

### Graph Commands

| Command | Purpose |
|---------|---------|
| `coefplot` | Coefficient plots |
| `binscatter` | Binned scatter plots |
| `twoway` | General 2D graphs |
| `histogram` | Histograms |
| `kdensity` | Kernel density |
| `graph combine` | Multi-panel figures |

### Export Checklist

- [ ] Use vector format (PDF/EPS) for line plots
- [ ] Use 300+ DPI for raster images
- [ ] Include informative axis labels
- [ ] Add reference lines where appropriate
- [ ] Use consistent color scheme
- [ ] Match journal font requirements


---

### 05_best_practices.md

# Best Practices for Stata Projects

Code organization, reproducibility, and style conventions based on top journal replication packages.

---

## 1. Master Do-File Structure

Every project should have a single master script that runs the entire analysis.

### Template

```stata
* ===========================================================================
* Master Do-File
*
* "[Paper Title]"
* [Authors]
* [Journal], [Year]
*
* ===========================================================================

version 15
clear all
set more off
set maxvar 10000

* ===========================================================================
* PATH SETUP - Edit this section only
* ===========================================================================

* Set root path (CHANGE THIS for your machine)
global root "/path/to/replication"

* Derived paths (do not edit)
global code "$root/code"
global data "$root/data"
    global raw "$data/raw"
    global clean "$data/clean"
global out "$root/output"
    global figures "$out/figures"
    global tables "$out/tables"
    global logs "$out/logs"

* ===========================================================================
* EXECUTION
* ===========================================================================

log using "$logs/replication_log.txt", text replace

* Data preparation
do "$code/01_import_data.do"
do "$code/02_clean_data.do"
do "$code/03_create_variables.do"

* Analysis
do "$code/10_descriptives.do"      // Table 1, Figures 1-2
do "$code/11_main_analysis.do"     // Tables 2-4
do "$code/12_robustness.do"        // Appendix Tables A1-A5

* Figures
do "$code/20_figures.do"           // Figures 3-6

log close

exit
```

---

## 2. Project Directory Structure

```
project/
├── code/
│   ├── 00_master.do
│   ├── 01_import_data.do
│   ├── 02_clean_data.do
│   ├── 03_create_variables.do
│   ├── 10_descriptives.do
│   ├── 11_main_analysis.do
│   └── 20_figures.do
├── data/
│   ├── raw/           # Original, unchanged data
│   └── clean/         # Processed data files
├── output/
│   ├── figures/
│   ├── tables/
│   └── logs/
└── README.md
```

---

## 3. Path Management

### Good: Single Root Variable

```stata
* Set root path (only line to change)
global root "/Users/name/project"

* Derived paths
global code "$root/code"
global raw "$root/data/raw"
global clean "$root/data/clean"
global figures "$root/output/figures"
global tables "$root/output/tables"
```

### Bad: Hardcoded Paths

```stata
* DON'T do this - not portable
use "/Users/name/Documents/project/data/mydata.dta"
```

---

## 4. Data Cleaning Conventions

### Recode Missing Values Consistently

```stata
* Standardize missing values
recode var1 var2 var3 (9999 = .) (-99 = .) (-1 = .)

* Document recoding with comments
* Original codes: 9999=DK, -99=Refused, -1=NA
recode satisfaction (9999 = .) (-99 = .) (-1 = .)
```

### Label Everything

```stata
* Define value labels
label define yesno 0 "No" 1 "Yes"
label values treated yesno

* Variable labels
label variable treated "Treatment indicator"
label variable outcome "Primary outcome measure"
```

### Check Merge Results

```stata
merge m:1 id using "$clean/demographics.dta"

* Document merge results
tab _merge

* Handle unmatched explicitly
assert _merge != 2  // No unmatched from using
drop if _merge == 2
drop _merge
```

---

## 5. Reproducibility Essentials

### Set Random Seed

```stata
* Set seed at the beginning of the do-file
set seed 12345  // Use meaningful seed (e.g., date: 20240115)
```

### Version Control

```stata
* Specify Stata version at top of do-file
version 15

* Record session info
display "Stata version: " c(stata_version)
display "Date: " c(current_date)
display "Time: " c(current_time)
```

### Use Log Files

```stata
* Start log
log using "$logs/analysis_log.txt", text replace

* ... analysis code ...

log close
```

---

## 6. Code Style Conventions

### Naming

```stata
* Variables: snake_case
gen treatment_effect = ...
gen log_income = log(income)

* Wave indicators: suffix with number
rename income incomeW1
rename income2 incomeW2

* Temporary variables: prefix with underscore
gen _temp_var = ...
drop _temp_var
```

### Comments

```stata
* Single-line comment for brief notes

/*
Multi-line comment for
longer explanations
*/

// Alternative single-line (less common in published code)

*--- Section break ---*
```

### Line Continuation

```stata
* Use /// for long commands
reghdfe outcome treatment control1 control2 control3 ///
    control4 control5, ///
    absorb(id year) cluster(id)
```

---

## 7. Analysis Do-File Template

```stata
* ===========================================================================
* [Descriptive title]
*
* Purpose: [What this file does]
* Input:   [Input data files]
* Output:  [Output files - tables, figures]
*
* ===========================================================================

* Load data
use "$clean/analysis_sample.dta", clear

* -------------------------------------------
* Section 1: [Description]
* -------------------------------------------

[analysis code]

* -------------------------------------------
* Section 2: [Description]
* -------------------------------------------

[analysis code]

* -------------------------------------------
* Export results
* -------------------------------------------

esttab m1 m2 m3 using "$tables/table_1.tex", replace ///
    [options]

graph export "$figures/figure_1.pdf", replace
```

---

## 8. Common Patterns

### Loop Over Variables

```stata
* Process multiple variables
foreach var in income education age {
    gen log_`var' = log(`var')
    label variable log_`var' "Log `var'"
}
```

### Loop Over Specifications

```stata
* Multiple model specifications
local controls1 "x1 x2"
local controls2 "x1 x2 x3 x4"
local controls3 "x1 x2 x3 x4 x5 x6"

forvalues i = 1/3 {
    reg y treat `controls`i'', robust
    estimates store m`i'
}

esttab m1 m2 m3
```

### Store Multiple Models Efficiently

```stata
* Clear stored estimates
estimates clear

* Run and store
foreach outcome in y1 y2 y3 {
    quietly reg `outcome' treat x1 x2, robust
    estimates store m_`outcome'
}

* Combined table
esttab m_y1 m_y2 m_y3, se
```

---

## 9. Pre-Submission Checklist

### Code Quality
- [ ] Master script runs entire analysis without errors
- [ ] All paths are relative (single root variable)
- [ ] Random seeds are set and documented
- [ ] Code files have clear headers with purpose

### Documentation
- [ ] README documents execution order
- [ ] README lists software/package requirements
- [ ] Output files are named to match paper elements

### Reproducibility
- [ ] Stata version specified
- [ ] Package versions recorded
- [ ] Intermediate datasets saved
- [ ] Log files generated

### Data
- [ ] Raw data unchanged
- [ ] All data transformations documented
- [ ] Missing value handling explicit
- [ ] Merge results verified

---

## Quick Reference

### Essential Setup Commands

```stata
clear all
set more off
set maxvar 10000
version 15
```

### Global Structure

```stata
global root "/path/to/project"
global code "$root/code"
global data "$root/data"
global out "$root/output"
```

### Output Mapping Comment Style

```stata
do "$code/10_analysis.do"  // Table 1, Figure 2
```


---

