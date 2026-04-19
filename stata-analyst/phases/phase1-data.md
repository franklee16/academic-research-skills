# Phase 1: Data Familiarization

You are executing Phase 1 of a statistical analysis in Stata. Your goal is to develop deep familiarity with the data before any modeling.

## Why This Phase Matters

Jumping straight to regression is a common mistake. Understanding your data prevents errors, reveals data quality issues, and often suggests refinements to the research design. This phase creates the foundation for credible analysis.

## Technique Guides

**Consult these guides** in `stata-statistical-techniques/` for data handling patterns:

| Topic | Guide |
|-------|-------|
| Data prep, Import, Merge | `00_data_prep.md` |
| Visualization, Summary stats | `04_visualization.md` |
| Survey data handling | `02_survey_resampling.md` |
| Best practices, Path management | `05_best_practices.md` |

## Your Tasks

### 1. Load and Inspect Data Structure

```stata
* Load data
use "$raw/filename.dta", clear

* Basic structure
describe
codebook, compact

* Check for duplicates
duplicates report id
isid id  // Should not error if id is unique

* Check panel structure (if applicable)
xtset id year
xtdescribe
```

Document:
- Number of observations and variables
- Unit of observation
- Key variable types
- Any obvious data issues

### 2. Generate Descriptive Statistics (Table 1)

```stata
* Summary statistics
summarize outcome treatment control1 control2, detail

* Formatted table
estpost summarize outcome treatment control1 control2
esttab using "$tables/table1_descriptives.rtf", ///
    cells("count mean sd min max") ///
    title("Summary Statistics") ///
    replace

* By treatment group
bysort treatment: summarize outcome control1 control2
tabstat outcome control1 control2, by(treatment) stats(n mean sd)

* Balance table
estpost ttest outcome control1 control2, by(treatment)
esttab using "$tables/table1_balance.rtf", ///
    cells("mu_1 mu_2 b se") ///
    title("Balance Across Treatment Groups") ///
    replace
```

### 3. Check Data Quality

**Missing values:**
```stata
* Count missing by variable
misstable summarize

* Patterns of missingness
misstable patterns

* Document how missing data will be handled
count if missing(outcome)
```

**Outliers:**
```stata
* Check key continuous variables
summarize outcome, detail
tabstat outcome, stats(p1 p5 p95 p99)

* Visualize distributions
histogram outcome, bin(50) ///
    title("Distribution of Outcome")
graph export "$figures/outcome_dist.pdf", replace
```

**Coding issues:**
```stata
* Check categorical variables
tab treatment, missing

* Check for impossible values
list if age < 0 | age > 120

* Check value labels
label list
```

### 4. Visualize Key Relationships

**For DiD/Panel:**
```stata
* Trends over time by treatment group
preserve
collapse (mean) mean_outcome=outcome, by(year treatment_group)
twoway (line mean_outcome year if treatment_group==0, lcolor(blue)) ///
       (line mean_outcome year if treatment_group==1, lcolor(red)), ///
       xline(treatment_year, lpattern(dash)) ///
       legend(order(1 "Control" 2 "Treated")) ///
       title("Outcome Trends by Treatment Status")
graph export "$figures/trends.pdf", replace
restore
```

**For RD:**
```stata
* Outcome vs. running variable
twoway (scatter outcome running_var, msize(small) mcolor(gray%50)) ///
       (lfit outcome running_var if running_var < cutoff, lcolor(blue)) ///
       (lfit outcome running_var if running_var >= cutoff, lcolor(red)), ///
       xline(cutoff, lpattern(dash)) ///
       title("Regression Discontinuity")
graph export "$figures/rd_plot.pdf", replace
```

**For any design:**
```stata
* Bivariate relationship
graph box outcome, over(treatment) ///
    title("Outcome by Treatment Status")
graph export "$figures/outcome_by_treatment.pdf", replace

* Correlation matrix
correlate outcome treatment control1 control2
```

### 5. Verify Design Requirements

Check that data supports the planned identification strategy:

**For DiD:**
```stata
* Check pre and post periods exist
tab year treatment
tab post treatment

* Cell counts
bysort treatment post: count
```

**For Panel FE:**
```stata
* Within-unit variation
xtset id year
xtsum treatment  // Check "within" variation
```

**For IV:**
```stata
* First stage relationship
regress endogenous instrument, robust
```

### 6. Create Analysis Sample

Define and document the final analysis sample:

```stata
* Count original sample
count
local n_orig = r(N)

* Apply restrictions
drop if missing(outcome)
local n_after_outcome = _N

drop if missing(treatment)
local n_after_treatment = _N

keep if year >= 2000 & year <= 2020
local n_final = _N

* Document sample construction
display "Original sample: `n_orig'"
display "After dropping missing outcome: `n_after_outcome'"
display "Final analysis sample: `n_final'"

* Save analysis sample
save "$clean/analysis_sample.dta", replace
```

## Output: Data Report

Create a data report (`memos/phase1-data-report.md`) containing:

```markdown
# Data Familiarization Report

## Data Overview
- **Source**: [where data comes from]
- **Observations**: [N]
- **Variables**: [count and key variables]
- **Time Period**: [if applicable]

## Sample Construction
| Step | N | Notes |
|------|---|-------|
| Original sample | X | |
| After restriction 1 | Y | [reason] |
| Final analysis sample | Z | |

## Descriptive Statistics
[Insert or reference Table 1]

## Data Quality Issues
- **Missing data**: [summary and how handled]
- **Outliers**: [any concerns]
- **Coding issues**: [any found and fixed]

## Key Visualizations
[Reference saved figures]

## Design Verification
- [Confirm data supports the identification strategy]
- [Note any concerns]

## Preliminary Observations
- [Anything notable in the descriptives]
- [Any surprises or concerns]

## Questions for User
- [Any decisions that need user input]
```

## When You're Done

Return a summary to the orchestrator that includes:
1. Final sample size and key restrictions
2. Any data quality issues found
3. Whether data supports the planned design
4. Key observations from descriptives
5. Questions for the user

**Do not proceed to Phase 2 until the user reviews the descriptives and confirms the sample.**
