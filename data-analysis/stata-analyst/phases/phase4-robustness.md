# Phase 4: Robustness & Sensitivity

You are executing Phase 4 of a statistical analysis in Stata. Your goal is to stress-test the main findings through robustness checks and sensitivity analysis.

## Why This Phase Matters

Main results are only as credible as their robustness. Reviewers will ask: "How do you know this isn't driven by [X]?" This phase pre-empts those questions and honestly assesses the fragility of the findings.

## Technique Guides

**Consult these guides** in `stata-statistical-techniques/` for robustness code patterns:

| Topic | Guide |
|-------|-------|
| DiD robustness, Event studies | `01_core_econometrics.md` |
| Bootstrap, Wild cluster | `02_survey_resampling.md` |
| Matching diagnostics | `01_core_econometrics.md` Section 5 |
| Post-estimation tests | `07_postestimation_reporting.md` |

## Your Tasks

### 1. Alternative Specifications

Run the pre-specified alternatives from Phase 2:

**Different control sets:**
```stata
* Minimal controls
reghdfe outcome treatment, absorb(id year) cluster(cluster_var)
estimates store robust_minimal

* Extended controls
reghdfe outcome treatment extra1 extra2 extra3, absorb(id year) cluster(cluster_var)
estimates store robust_extended

* Different functional form
gen log_outcome = log(outcome)
reghdfe log_outcome treatment control1 control2, absorb(id year) cluster(cluster_var)
estimates store robust_log
```

**Different fixed effects:**
```stata
* More demanding FE structure
reghdfe outcome treatment, absorb(id#year) cluster(cluster_var)
estimates store robust_fe1

* Region-by-year FE
reghdfe outcome treatment, absorb(region#year id) cluster(cluster_var)
estimates store robust_fe2
```

**Different standard errors:**
```stata
* Compare clustering levels
reghdfe outcome treatment control1 control2, absorb(id year) cluster(id)
estimates store se_id

reghdfe outcome treatment control1 control2, absorb(id year) cluster(state)
estimates store se_state

reghdfe outcome treatment control1 control2, absorb(id year) cluster(id year)
estimates store se_twoway
```

### 2. Placebo Tests

**Pre-treatment effects (for DiD/Event Study):**
```stata
* Should see no effect before treatment
preserve
keep if year < treatment_year
reghdfe outcome fake_treatment, absorb(id year) cluster(id)
estimates store placebo_pre
restore
```

**Fake treatment timing:**
```stata
* Assign treatment X years earlier—should find no effect
gen fake_treated = treated_post & year >= (treatment_year - 3)
reghdfe outcome fake_treated, absorb(id year) cluster(id)
estimates store placebo_timing
```

**Outcome that shouldn't be affected:**
```stata
* If treatment affects X, it shouldn't affect unrelated Y
reghdfe unrelated_outcome treatment control1 control2, absorb(id year) cluster(id)
estimates store placebo_outcome
```

### 3. Wild Cluster Bootstrap

For designs with few clusters (<50):

```stata
* After main estimation
reghdfe outcome treatment control1 control2, absorb(id year) cluster(state)

* Wild cluster bootstrap
boottest treatment, cluster(state) reps(999) nograph
* Store p-value for reporting
```

### 4. Missing Data Assessment

Before running sensitivity analyses, document and address missing data:

**Document Missingness:**
```stata
* Overall missingness rates
misstable summarize
misstable patterns

* Missingness by key variables
bysort treatment: misstable summarize outcome control1 control2
```

**Test for MCAR/MAR:**
```stata
* Little's MCAR test (if installed: ssc install mcartest)
mcartest outcome control1 control2

* Visualize missingness patterns
misstable patterns, frequency
```

**Multiple Imputation (if substantial missingness):**
```stata
* Use adequate number of imputations (m ≥ 20, preferably ≥ 50)
mi set wide
mi register imputed outcome control1 control2
mi impute chained (regress) outcome control1 control2 = treatment, add(50) rseed(12345)

* Check imputation diagnostics
mi xeq: summarize outcome control1 control2

* Run analysis on imputed datasets and pool
mi estimate: reghdfe outcome treatment control1 control2, absorb(id year) cluster(cluster_var)

* Include auxiliary variables to strengthen MAR assumption
* These are variables that predict missingness or the outcome
```

**Compare Missing Data Approaches:**
```stata
* Store estimates for comparison
* Complete case
reghdfe outcome treatment control1 control2, absorb(id year) cluster(cluster_var)
estimates store complete_case

* Multiple imputation
mi estimate: reghdfe outcome treatment control1 control2, absorb(id year) cluster(cluster_var)
estimates store mi_model

* Create comparison table
esttab complete_case mi_model using "$tables/missing_data_sensitivity.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("Complete Case" "Multiple Imputation") ///
    title("Sensitivity to Missing Data Treatment")
```

**Report in Methods Section:**
```markdown
[X]% of observations were missing on [variable]. We tested for patterns
of missingness and found [MCAR/MAR/evidence of MNAR]. Our primary analysis
uses [complete case / multiple imputation with m = X imputations].
Sensitivity analyses comparing complete case and multiple imputation show
[results are robust / estimates differ by X].
```

### 5. Panel/Longitudinal Data Robustness (If Applicable)

**Attrition Analysis:**
```stata
* Document attrition rates by wave
tab wave, sum(n_obs)

* Test if attrition is related to treatment or outcomes
gen dropped_out = (next_wave_outcome == .)
logit dropped_out treatment baseline_outcome covariates, vce(robust)
```

**Inverse Probability Weighting for Selection:**
```stata
* Estimate selection weights
logit observed treatment covariates
predict ps, pr
gen ipw = 1 / ps

* Apply weights in main analysis
reghdfe outcome treatment control1 control2 [pw=ipw], absorb(id year) cluster(cluster_var)
estimates store robust_ipw
```

**Fixed vs Random Effects:**
```stata
* Hausman test
xtreg outcome treatment covariates, fe
estimates store fe
xtreg outcome treatment covariates, re
estimates store re
hausman fe re  // p < 0.05 suggests FE preferred

* Within-between decomposition (correlated random effects)
* Create between-unit and within-unit deviations
bysort id: egen treatment_mean = mean(treatment)
gen treatment_within = treatment - treatment_mean

xtreg outcome treatment_within treatment_mean covariates, re
```

### 6. Sensitivity Analysis

**Sensitivity to outliers:**
```stata
* Winsorize extreme values
winsor2 outcome, cuts(1 99) suffix(_w)
reghdfe outcome_w treatment control1 control2, absorb(id year) cluster(cluster_var)
estimates store robust_winsor

* Drop extreme observations
summarize outcome, detail
drop if outcome < r(p1) | outcome > r(p99)
reghdfe outcome treatment control1 control2, absorb(id year) cluster(cluster_var)
estimates store robust_trim
```

**Sensitivity to sample restrictions:**
```stata
* Different time periods
reghdfe outcome treatment control1 control2 if year <= 2015, ///
    absorb(id year) cluster(cluster_var)
estimates store robust_early

reghdfe outcome treatment control1 control2 if year > 2015, ///
    absorb(id year) cluster(cluster_var)
estimates store robust_late

* Excluding specific units
reghdfe outcome treatment control1 control2 if !outlier_unit, ///
    absorb(id year) cluster(cluster_var)
estimates store robust_exclude
```

### 5. Subgroup Analysis

Run pre-specified heterogeneity analyses:

```stata
* By group (separate regressions)
reghdfe outcome treatment control1 control2 if subgroup == 1, ///
    absorb(id year) cluster(cluster_var)
estimates store het_group1

reghdfe outcome treatment control1 control2 if subgroup == 0, ///
    absorb(id year) cluster(cluster_var)
estimates store het_group2

* Interaction approach (preferred)
reghdfe outcome c.treatment##i.subgroup control1 control2, ///
    absorb(id year) cluster(cluster_var)
estimates store het_interact

* Test difference
test 1.subgroup#c.treatment
```

### 6. Method-Specific Diagnostics

**For DiD with staggered treatment:**
```stata
* Check for heterogeneous treatment effects
csdid outcome, ivar(id) time(year) gvar(first_treat) notyet
csdid_estat event

* Compare to traditional TWFE
reghdfe outcome treated, absorb(id year) cluster(id)
* Note any differences
```

**For IV:**
```stata
* Weak instrument test
ivreg2 outcome (endogenous = instrument) controls, first robust
* Check F > 10

* Overidentification test (if multiple instruments)
ivreg2 outcome (endogenous = inst1 inst2) controls, robust
estat overid
```

**For Matching:**
```stata
* Balance check after matching
pstest control1 control2 control3, both graph
graph export "$figures/balance.pdf", replace
```

### 7. Create Robustness Table

Compile all robustness checks:

```stata
esttab m4 robust_minimal robust_extended robust_fe1 robust_winsor robust_early robust_late ///
    using "$tables/table3_robustness.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    keep(treatment) ///
    mtitles("Main" "Minimal" "Extended" "Alt FE" "Winsor" "Pre-2015" "Post-2015") ///
    title("Robustness Checks") ///
    note("All models include unit and year fixed effects. SE clustered at [level].")
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

## Wild Cluster Bootstrap
- Conventional p-value: [X.XX]
- Bootstrap p-value: [X.XX]
- Inference [changes / doesn't change]

## Sensitivity Analysis

### Outliers
- Results [are / are not] sensitive to extreme values

### Sample restrictions
- Results [hold / change] in different subsamples

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
3. Wild bootstrap results (if applicable)
4. Any concerns about the findings
5. Questions for the user

**Do not proceed to Phase 5 until the user reviews the robustness assessment.**
