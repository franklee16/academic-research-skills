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

## Reporting Checklists

### TWFE Checklist

**Required in methods section:**
- [ ] Define panel structure (unit ID, time variable)
- [ ] Specify fixed effects included (unit FE, time FE, or both)
- [ ] Justify clustering level (theory-based: state, firm, etc.)

**Report in results:**
- [ ] N units, N time periods, N observations
- [ ] Fixed effects included (state FE, year FE, etc.)
- [ ] Key coefficient, SE, and CI
- [ ] Clustering level in table notes

**Sensitivity checks:**
- [ ] Alternative clustering (one-way vs two-way if plausible)
- [ ] Results stable across specifications

---

### DiD Checklist (Traditional & Staggered)

**Required in methods section:**
- [ ] Treatment definition and timing
- [ ] Control group definition (never-treated vs not-yet-treated)
- [ ] Parallel trends assumption justification

**Report in results:**
- [ ] Baseline DiD estimate + SE
- [ ] Event study plot with pre-trend coefficients
- [ ] Discuss pre-trends (are they flat and near zero?)

**Robustness checks:**
- [ ] Alternative control group (for `csdid`: toggle `notyet` vs `never`)
- [ ] Alternative event window bins (e.g., 2-year vs 1-year)
- [ ] Wild cluster bootstrap if < 40 clusters (use `boottest`)

---

### IV Checklist

**Required in methods section:**
- [ ] Instrument relevance story (why does Z predict X?)
- [ ] Exclusion restriction argument (why does Z only affect Y through X?)

**Report in results:**
- [ ] First-stage F-statistic (or Kleibergen-Paap rk F from `ivreg2`)
- [ ] Stock-Yogo critical values for weak instrument comparison
- [ ] Overidentification test (Hansen J) if multiple instruments
- [ ] 2SLS coefficient + SE

**Robustness checks:**
- [ ] Reduced form regression (Y on Z directly)
- [ ] Alternative instrument sets or control variables
- [ ] Anderson-Rubin weak-instrument-robust CI

---

### Matching Checklist

**Required in methods section:**
- [ ] Covariate set justification (what variables predict treatment?)
- [ ] Common support/overlap rule
- [ ] Matching method choice (PSM, CEM, etc.)

**Report in results:**
- [ ] Balance table: before vs after matching (`pstest`)
- [ ] ATT estimate + SE
- [ ] Number matched, number dropped for common support

**Robustness checks:**
- [ ] Caliper sensitivity (try narrower/wider)
- [ ] Neighbor count sensitivity (1 vs 5 neighbors)
- [ ] Alternative matching method (PSM vs CEM)

---

### Survey Checklist

**Required in methods section:**
- [ ] `svyset` statement with PSU, strata, weights

**Report in results:**
- [ ] Weighted descriptive statistics
- [ ] Key model with survey-corrected SEs
- [ ] Note: "Analyses account for complex survey design"

**Important notes:**
- [ ] Use `subpop()` not `if` for subgroup analyses
- [ ] Comparison with unweighted results (as robustness, not truth)

---

### Synthetic Control Checklist

**Required in methods section:**
- [ ] Donor pool definition (which units? why these?)
- [ ] Predictor variable rationale

**Report in results:**
- [ ] Pre-period fit (RMSPE)
- [ ] Unit weights table (which donors contribute?)
- [ ] Gap plot (treated - synthetic over time)

**Robustness checks:**
- [ ] In-space placebo tests (run synth for each control unit)
- [ ] In-time placebo tests (fake treatment at earlier time)
- [ ] Predictor set sensitivity
- [ ] Exclude potentially contaminated donors
