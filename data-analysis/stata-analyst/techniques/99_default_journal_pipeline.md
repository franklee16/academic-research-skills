# Default Journal Analysis Pipeline

A step-by-step workflow for sociological research. Copy this structure for new projects.

---

## Project Structure

```
project/
├── master.do              # Run everything
├── code/
│   ├── 01_import.do       # Data import
│   ├── 02_clean.do        # Cleaning and construction
│   ├── 03_analysis.do     # Main models
│   └── 04_output.do       # Tables and figures
├── data/
│   ├── raw/               # Original data (never modify)
│   ├── clean/             # Analysis-ready datasets
│   └── temp/              # Intermediate files
├── output/
│   ├── tables/            # RTF/CSV/TeX tables
│   └── figures/           # PNG/PDF figures
└── logs/                  # Log files
```

---

## Master Do-File Template

```stata
* ===========================================================================
* Master Do-File: [Project Name]
* Author: [Name]
* Date: [Date]
* ===========================================================================

clear all
set more off
version 15
set seed 12345

* -----------------------------------
* Set Paths
* -----------------------------------
global root "/path/to/project"
global code "$root/code"
global raw "$root/data/raw"
global clean "$root/data/clean"
global tables "$root/output/tables"
global figures "$root/output/figures"
global logs "$root/logs"

* -----------------------------------
* Run Analysis
* -----------------------------------
do "$code/01_import.do"
do "$code/02_clean.do"
do "$code/03_analysis.do"
do "$code/04_output.do"

display "Analysis complete: $S_DATE $S_TIME"
```

---

## The Canonical Sequence

### 1. Data Preparation (`01_import.do`, `02_clean.do`)

```stata
* ===========================================================================
* 01_import.do
* ===========================================================================

log using "$logs/01_import.log", replace

* Import raw data
import delimited "$raw/survey_data.csv", clear varnames(1)

* Quick checks
describe
codebook, compact

* Save imported version
compress
save "$clean/data_imported.dta", replace

log close
```

```stata
* ===========================================================================
* 02_clean.do
* ===========================================================================

log using "$logs/02_clean.log", replace

use "$clean/data_imported.dta", clear

* -----------------------------------
* Merge additional data
* -----------------------------------
merge m:1 state using "$raw/state_controls.dta"
tab _merge
assert _merge != 2
drop _merge

* -----------------------------------
* Construct variables
* -----------------------------------
* Treatment
gen treat = (policy_year <= year) & !missing(policy_year)

* Log income
gen ln_income = ln(income + 1)

* Standardized test score
egen z_score = std(test_score)

* -----------------------------------
* Sample restrictions
* -----------------------------------
display "Initial N: " _N

drop if missing(outcome)
display "After dropping missing outcome: " _N

drop if missing(treat)
display "After dropping missing treatment: " _N

gen sample_main = 1

* -----------------------------------
* Save analysis sample
* -----------------------------------
compress
label data "Analysis sample, created $S_DATE"
save "$clean/analysis_sample.dta", replace

log close
```

### 2. Descriptive Statistics

```stata
* -----------------------------------
* Table 1: Descriptive Statistics
* -----------------------------------
use "$clean/analysis_sample.dta", clear

* Overall descriptives
estpost summarize outcome treat income age education
esttab using "$tables/table1_descriptives.rtf", replace ///
    cells("count mean(fmt(2)) sd(fmt(2)) min max") ///
    nomtitle nonumber ///
    title("Table 1: Descriptive Statistics")

* Descriptives by treatment
tabstat outcome income age, by(treat) stat(mean sd n) nototal
```

### 3. Main Models (`03_analysis.do`)

```stata
* ===========================================================================
* 03_analysis.do
* ===========================================================================

log using "$logs/03_analysis.log", replace

use "$clean/analysis_sample.dta", clear

* -----------------------------------
* Table 2: Main Results
* -----------------------------------

* Model 1: Bivariate
reg outcome treat, robust
estimates store m1

* Model 2: Add controls
reg outcome treat income age education, robust
estimates store m2

* Model 3: Fixed effects
reghdfe outcome treat income age, absorb(state year) cluster(state)
estimates store m3

* Model 4: Full specification
reghdfe outcome treat income age education, absorb(state year) cluster(state)
estimates store m4

* Save estimates for output
estimates save "$clean/main_estimates", replace

log close
```

### 4. Robustness Checks

```stata
* -----------------------------------
* Table 3: Robustness
* -----------------------------------

* Alternative control group
* Alternative clustering
* Alternative sample
* Placebo test

* Model with alternative clustering
reghdfe outcome treat income age, absorb(state year) cluster(state year)
estimates store robust_twoway

* Placebo outcome
reghdfe placebo_outcome treat income age, absorb(state year) cluster(state)
estimates store placebo
```

### 5. Output Generation (`04_output.do`)

```stata
* ===========================================================================
* 04_output.do
* ===========================================================================

log using "$logs/04_output.log", replace

estimates use "$clean/main_estimates"

* -----------------------------------
* Table 2: Main Results
* -----------------------------------
esttab m1 m2 m3 m4 using "$tables/table2_main_results.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("(1)" "(2)" "(3)" "(4)") ///
    title("Table 2: Main Results") ///
    drop(0.* _cons) ///
    stats(N r2, labels("N" "R-squared") fmt(%9.0fc %9.3f)) ///
    addnotes("Robust standard errors in parentheses." ///
             "Models 3-4 include state and year fixed effects." ///
             "Standard errors clustered at state level.")

* -----------------------------------
* Figure 1: Coefficient Plot
* -----------------------------------
estimates restore m4
coefplot, drop(_cons) xline(0) ///
    title("Effect of Treatment") ///
    xtitle("Coefficient Estimate")
graph export "$figures/figure1_coef_plot.png", replace

* -----------------------------------
* Figure 2: Predicted Values
* -----------------------------------
use "$clean/analysis_sample.dta", clear
reg outcome i.treat##c.income, robust
margins treat, at(income=(20000(10000)80000))
marginsplot, title("Predicted Outcome by Treatment Status") ///
    ytitle("Predicted Outcome") xtitle("Income")
graph export "$figures/figure2_margins.png", replace

log close

display "Output generation complete!"
```

---

## Output Mapping

### File Naming Conventions

| Output | Filename |
|--------|----------|
| Descriptives | `table1_descriptives.rtf` |
| Main results | `table2_main_results.rtf` |
| Robustness | `table3_robustness.rtf` |
| Mechanisms | `table4_mechanisms.rtf` |
| Appendix balance | `tableA1_balance.rtf` |
| Main figure | `figure1_[description].png` |
| Appendix figure | `figureA1_[description].png` |

### In-Code Documentation

Mark each table/figure creation clearly:

```stata
* ===================================
* Table 2: Main Regression Results
* ===================================
```

---

## Minimal Project (Smaller Papers)

For simpler analyses, combine files:

```stata
* ===========================================================================
* analysis.do - Complete Analysis
* ===========================================================================

clear all
set more off
version 15

* Paths
global root "/path/to/project"
global tables "$root/tables"
global figures "$root/figures"

log using "$root/analysis.log", replace

* -----------------------------------
* Data Prep
* -----------------------------------
use "$root/data.dta", clear
keep if !missing(outcome, treat, x1, x2)
display "Analysis N: " _N

* -----------------------------------
* Table 1: Descriptives
* -----------------------------------
estpost summarize outcome treat x1 x2
esttab using "$tables/table1.rtf", replace ///
    cells("mean sd min max") nomtitle

* -----------------------------------
* Table 2: Main Models
* -----------------------------------
reg outcome treat, robust
estimates store m1

reg outcome treat x1 x2, robust
estimates store m2

esttab m1 m2 using "$tables/table2.rtf", replace ///
    se star(* .10 ** .05 *** .01)

* -----------------------------------
* Figure 1: Coefficient Plot
* -----------------------------------
coefplot m2, drop(_cons) xline(0)
graph export "$figures/figure1.png", replace

log close
```

---

## Checklist Before Submission

### Data and Replication
- [ ] Raw data preserved (never modified)
- [ ] All code runs from master.do
- [ ] Random seed set for reproducibility
- [ ] Sample sizes documented at each step

### Tables
- [ ] Table 1: Descriptive statistics (overall and by group)
- [ ] Table 2+: Regression results with nested specifications
- [ ] SEs and significance stars clearly noted
- [ ] N and fit statistics included

### Figures
- [ ] Clear titles and axis labels
- [ ] High resolution (300+ DPI for publication)
- [ ] Consistent styling across figures

### Methods Section
- [ ] Estimator described (OLS, FE, DiD, etc.)
- [ ] Standard error approach documented
- [ ] Sample restrictions listed
- [ ] Key assumptions acknowledged

---

## Common Patterns

### Store Multiple Models

```stata
foreach spec in base controls full {
    reg outcome treat `controls_`spec'', robust
    estimates store `spec'
}
esttab base controls full, se
```

### Export with Comments

```stata
* // Table 2 in do-file marks where table is created
esttab m1 m2 using "$tables/table2.rtf", replace ...
```

### Consistent Graph Style

```stata
* Set graph scheme at start
set scheme s2color
graph set window fontface "Arial"
```