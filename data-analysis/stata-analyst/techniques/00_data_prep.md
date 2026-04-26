# Data Preparation in Stata

Making "analysis-ready data" a reproducible, auditable stage. All code tested on Stata 15+.

---

## 0. Setup and Conventions

### Minimal Header Template

```stata
* ===========================================================================
* Project: [Name]
* Purpose: [Brief description]
* Input: [raw data files]
* Output: [clean data files]
* ===========================================================================

clear all
set more off
version 15
set seed 12345

* Start log
log using "logs/01_data_prep.log", replace
```

### Naming Conventions

- Variables: `snake_case` (e.g., `first_treatment_year`)
- Files: descriptive, numbered (e.g., `01_import.do`, `02_clean.do`)
- Always label variables after creating them

---

## 1. Import Patterns

### Import CSV

```stata
* Basic import
import delimited "data/raw/mydata.csv", clear varnames(1)

* Force all columns as strings initially (for cleaning)
import delimited "data/raw/mydata.csv", clear varnames(1) stringcols(_all)

* Quick checks after import
describe
compress
codebook, compact
```

### Import Excel

```stata
* Basic import with first row as variable names
import excel "data/raw/mydata.xlsx", sheet("Sheet1") firstrow clear

* Import specific cell range
import excel "data/raw/mydata.xlsx", cellrange(A2:F100) firstrow clear
```

### Reading Multiple Files (Loop)

```stata
* Append multiple CSV files from a folder
clear
local files: dir "data/raw/" files "*.csv"
local first = 1
foreach f of local files {
    if `first' == 1 {
        import delimited "data/raw/`f'", clear varnames(1)
        local first = 0
    }
    else {
        preserve
        import delimited "data/raw/`f'", clear varnames(1)
        tempfile temp
        save `temp'
        restore
        append using `temp'
    }
}
```

### Never Edit Raw Data

```stata
* Always save a clean .dta immediately after import
import delimited "data/raw/mydata.csv", clear varnames(1)
save "data/staging/mydata_imported.dta", replace
```

---

## 2. Merge, Append, and Reshape

### Every Merge Gets an Assertion

```stata
* 1:1 merge
use "data/master.dta", clear
merge 1:1 id using "data/using.dta"

* Required checks
tab _merge
count if _merge == 1  // master only
count if _merge == 2  // using only
count if _merge == 3  // matched

* Handle unmatched - be explicit about what you're dropping
assert _merge != 2  // or: drop if _merge == 2 with comment explaining why
drop _merge
```

### Merge Patterns

```stata
* Many-to-one (e.g., individual-level to state-level)
merge m:1 state using "data/state_controls.dta"

* One-to-many (less common; be careful)
merge 1:m household_id using "data/household_members.dta"
```

### Key Verification Before Merge

```stata
* Check that merge keys are unique where expected
isid id                    // fails if id is not unique
duplicates report id       // shows duplicate structure
duplicates tag id, gen(dup)
tab dup
drop dup
```

### Append Pattern

```stata
* Append datasets
use "data/wave1.dta", clear
append using "data/wave2.dta"

* Track source
gen wave = 1
replace wave = 2 if _n > [original N]
```

### Reshape Wide to Long

```stata
* Example: income2018 income2019 income2020 -> income with year variable
clear
set obs 20
gen id = _n
gen income2018 = rnormal(50000, 10000)
gen income2019 = income2018 * 1.03 + rnormal(0, 1000)
gen income2020 = income2019 * 1.02 + rnormal(0, 1000)

reshape long income, i(id) j(year)
```

### Reshape Long to Wide

```stata
reshape wide income, i(id) j(year)
```

---

## 3. Missing Data Audit

### Missingness Summary

```stata
* Overall missing count
misstable summarize

* Missing by variable with patterns
misstable patterns
```

### Missing by Group

```stata
* Count non-missing by treatment group
tabstat x1 x2, by(treat) stat(n) nototal

* Count missing manually
count if missing(x1) & treat == 0
count if missing(x1) & treat == 1
```

### Rules of Thumb

- **Never silently drop observations** - always document exclusions
- **Don't impute without justification** - report complete-case as baseline
- **Check missingness by key subgroups** - differential attrition is a threat

### Create Analysis Sample Flag

```stata
* Complete case indicator
gen sample_main = !missing(y, x1, x2, x3)
tab sample_main

* Or define incrementally with documentation
gen sample_main = 1
replace sample_main = 0 if missing(wage)
replace sample_main = 0 if missing(union)
replace sample_main = 0 if age < 25 | age > 55
```

---

## 4. Recodes, Transforms, and Outliers

### Standardize Special Missings

```stata
* Stata extended missing values: .a, .b, ... .z
replace income = .r if income == -99  // refused
replace income = .d if income == -88  // don't know
```

### Common Transforms

```stata
* Log transform
gen ln_income = ln(income)

* Handle zeros: ln(x + 1) or inverse hyperbolic sine
gen ln_income_p1 = ln(income + 1)
gen ihs_income = asinh(income)

* Standardization (z-scores)
egen z_income = std(income)
summarize z_income  // mean = 0, sd = 1
```

### Create Categorical Variables with Labels

```stata
* Create categories
gen price_cat = 1 if price < 5000
replace price_cat = 2 if price >= 5000 & price < 10000
replace price_cat = 3 if price >= 10000 & !missing(price)

* Add labels
label define price_lbl 1 "Low" 2 "Medium" 3 "High"
label values price_cat price_lbl
tab price_cat
```

### Winsorization (Optional)

```stata
* Winsorize at 1st and 99th percentiles
egen p1 = pctile(income), p(1)
egen p99 = pctile(income), p(99)
gen income_wins = income
replace income_wins = p1 if income < p1
replace income_wins = p99 if income > p99 & !missing(income)
drop p1 p99
```

---

## 5. Panel/Time Setup and Sanity Checks

### Declare Panel Structure

```stata
* xtset for panel data
xtset id time
xtdescribe

* tsset for time series (single unit)
tsset time
```

### Check for Gaps

```stata
* After xtset, check balance
xtdescribe

* Manual gap check
by id: gen gap = time - time[_n-1] if _n > 1
tab gap  // should be all 1s if no gaps
```

### Verify Panel Structure

```stata
* Check unit counts and time coverage
tab id
tab time
distinct id
distinct time
```

### Treatment Timing Construction

```stata
* Create first treatment year variable
gen treat_year = year if treatment == 1
bysort id: egen first_treat = min(treat_year)
drop treat_year

* Create relative time to treatment
gen rel_time = year - first_treat
```

---

## 6. Sample Construction Documentation

### Document Every Restriction

```stata
sysuse nlsw88, clear

* Track sample flow
display "Initial N: " _N

drop if missing(wage)
display "After dropping missing wage: " _N

drop if missing(union)
display "After dropping missing union: " _N

keep if age >= 25 & age <= 55
display "After age restriction (25-55): " _N

gen sample_main = 1
display "Final analysis sample: " _N
```

### Save Sample Flow to File

```stata
* Create sample flow log
file open flow using "$tables/sample_flow.txt", write replace
file write flow "Sample Construction" _n
file write flow "===================" _n
file write flow "Initial sample: 2,246" _n
file write flow "After dropping missing wage: 2,246" _n
file write flow "After dropping missing union: 1,878" _n
file write flow "Final analysis sample: 1,878" _n
file close flow
```

---

## 7. Output Artifacts

### Standard Save Pattern

```stata
* Save clean analysis dataset
compress
label data "Analysis sample, created [date]"
save "$clean/analysis_sample.dta", replace
```

### Export Codebook

```stata
* Save variable documentation
codebook, compact
log using "$docs/codebook.log", replace
codebook
log close
```

---

## Quick Reference

### Import Commands

| Task | Command |
|------|---------|
| CSV | `import delimited "file.csv", clear varnames(1)` |
| Excel | `import excel "file.xlsx", firstrow clear` |
| Stata | `use "file.dta", clear` |

### Merge Commands

| Type | Command |
|------|---------|
| 1:1 | `merge 1:1 id using "file.dta"` |
| m:1 | `merge m:1 group using "file.dta"` |
| 1:m | `merge 1:m id using "file.dta"` |

### Key Checks

| Task | Command |
|------|---------|
| Unique ID | `isid id` |
| Duplicates | `duplicates report id` |
| Missing | `misstable summarize` |
| Panel setup | `xtset id time` then `xtdescribe` |
