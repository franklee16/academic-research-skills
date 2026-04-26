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
