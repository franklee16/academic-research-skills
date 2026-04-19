# Phase 5: Output & Interpretation

You are executing Phase 5 of a statistical analysis in Stata. Your goal is to produce publication-ready outputs and synthesize the analysis into a coherent narrative.

## Why This Phase Matters

Analysis isn't complete until it's communicated. This phase transforms results into tables, figures, and text that can appear in a journal article. Good output is accurate, clear, and tells a story.

## Technique Guides

**Consult these guides** in `stata-statistical-techniques/` for output code patterns:

| Topic | Guide |
|-------|-------|
| Tables (esttab, estout) | `04_visualization.md` |
| Figures (coefplot, graphs) | `04_visualization.md` |
| Table 1, Descriptives | `07_postestimation_reporting.md` |
| Project structure, Master do-files | `05_best_practices.md` |
| Complete project template | `99_default_journal_pipeline.md` |

## Your Tasks

### 1. Finalize Tables

**Table 1: Descriptive Statistics**
```stata
* Summary statistics
estpost summarize outcome treatment control1 control2
esttab using "$tables/table1_descriptives.rtf", replace ///
    cells("count(fmt(0)) mean(fmt(2)) sd(fmt(2)) min(fmt(2)) max(fmt(2))") ///
    title("Summary Statistics") ///
    note("Sample: [description]. Source: [data source].")

* Balance table (if applicable)
estpost ttest outcome control1 control2, by(treatment)
esttab using "$tables/table1_balance.rtf", replace ///
    cells("mu_1(fmt(2)) mu_2(fmt(2)) b(fmt(2) star)") ///
    collabels("Control" "Treated" "Difference") ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    title("Balance Across Treatment Groups")
```

**Table 2: Main Results**
```stata
esttab m1 m2 m3 m4 using "$tables/table2_main.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    keep(treatment) ///
    coeflabels(treatment "Treatment Effect") ///
    stats(N r2_a, labels("Observations" "Adj. R-squared") fmt(0 3)) ///
    mtitles("(1)" "(2)" "(3)" "(4)") ///
    title("Effect of [Treatment] on [Outcome]") ///
    addnotes("Standard errors clustered at [level] in parentheses." ///
             "All models include [FE description]." ///
             "* p<0.1, ** p<0.05, *** p<0.01")

* LaTeX version
esttab m1 m2 m3 m4 using "$tables/table2_main.tex", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) booktabs ///
    keep(treatment) ///
    stats(N r2_a, labels("Observations" "Adj. R-squared") fmt(0 3))
```

**Table 3: Robustness**
```stata
esttab main robust1 robust2 robust3 robust4 using "$tables/table3_robustness.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    keep(treatment) ///
    mtitles("Main" "Alt 1" "Alt 2" "Alt 3" "Alt 4") ///
    title("Robustness Checks") ///
    note("See notes to Table 2.")
```

### 2. Create Publication Figures

**Figure 1: Trends (for DiD)**
```stata
preserve
collapse (mean) mean_outcome=outcome (sd) sd_outcome=outcome (count) n=outcome, ///
    by(year treatment_group)
gen se = sd_outcome / sqrt(n)
gen ci_low = mean_outcome - 1.96*se
gen ci_high = mean_outcome + 1.96*se

twoway (rarea ci_low ci_high year if treatment_group==0, color(blue%20)) ///
       (rarea ci_low ci_high year if treatment_group==1, color(red%20)) ///
       (line mean_outcome year if treatment_group==0, lcolor(blue) lwidth(medium)) ///
       (line mean_outcome year if treatment_group==1, lcolor(red) lwidth(medium)) ///
       (scatter mean_outcome year if treatment_group==0, mcolor(blue)) ///
       (scatter mean_outcome year if treatment_group==1, mcolor(red)), ///
       xline(`treatment_year', lpattern(dash) lcolor(gray)) ///
       legend(order(3 "Control" 4 "Treated") rows(1) position(6)) ///
       xtitle("Year") ytitle("Outcome") ///
       title("") ///
       graphregion(color(white)) bgcolor(white)

graph export "$figures/figure1_trends.pdf", replace
restore
```

**Figure 2: Event Study**
```stata
* After csdid estimation
csdid_plot, ///
    style(rcap) ///
    title("") ///
    xtitle("Time Relative to Treatment") ///
    ytitle("Coefficient Estimate") ///
    graphregion(color(white)) bgcolor(white)

graph export "$figures/figure2_eventstudy.pdf", replace
```

**Figure 3: Coefficient Plot**
```stata
coefplot m4, ///
    keep(treatment) ///
    xline(0, lpattern(dash) lcolor(gray)) ///
    title("") ///
    xtitle("Coefficient Estimate") ///
    graphregion(color(white)) bgcolor(white)

graph export "$figures/figure3_coefplot.pdf", replace
```

### 3. Write Results Narrative

Draft the key paragraphs for the results section:

**Main effect paragraph:**
> Table 2 presents estimates of the effect of [treatment] on [outcome].
> Column (1) shows the baseline relationship without controls.
> Column (4), our preferred specification, includes [unit] and [time] fixed effects
> and clusters standard errors at the [level] level. We find that [treatment]
> [increases/decreases] [outcome] by [X] [units], significant at the [Y]% level
> (95% CI: [lower, upper]). This represents a [Z]% change relative to the
> pre-treatment mean of [mean].

**Robustness paragraph:**
> Table 3 demonstrates that this finding is robust to alternative specifications.
> The point estimate remains [stable/similar] when we [change 1], [change 2], and
> [change 3]. The effect is [somewhat/not] sensitive to [what]. The wild cluster
> bootstrap p-value of [X] confirms that inference is [robust/sensitive] to
> the number of clusters.

**Heterogeneity paragraph (if applicable):**
> We examine heterogeneity in treatment effects across [subgroups].
> Table X shows that the effect is [larger/smaller] for [group 1]
> ([estimate]) compared to [group 2] ([estimate]). This difference is
> [statistically significant / not statistically significant] (p = [value]).

### 4. Survey Data Methods Section (If Applicable)

For survey-based analyses, address the five survey methodology deliverables:

**1. Sampling Frame Description:**
```markdown
Data come from the [SURVEY NAME], a [DESIGN TYPE] of [POPULATION].
The sampling frame is [DESCRIPTION]. The target population is [WHO].
[Exclusions]: We exclude [categories] because [reason].
```

**2. Response Rate and Nonresponse:**
```markdown
The response rate was [X]% (calculated as [METHOD: AAPOR RR1/RR3/etc.]).
We compared respondents to [population benchmark / nonrespondents on X variables]
and found [no significant differences / differences on X that we address through Y].
```

**3. Weighting Justification:**
```markdown
We apply [WEIGHT TYPE: post-stratification / raking / none] weights to adjust for
[FACTORS]. Weights are provided by [SOURCE] and calibrated to [BENCHMARKS].
[Alternative: We do not apply weights because {justification}.]
```

**4. Survey Design Acknowledgment:**
```stata
* Define survey design
svyset [pw=weight], strata(stratum) psu(psu)

* All analyses use survey-adjusted estimates
svy: mean outcome
svy: regress outcome treatment control1 control2
```

**5. Population Inference Boundaries:**
```markdown
Our results generalize to [POPULATION] during [TIME PERIOD]. We cannot
speak to [EXCLUDED GROUPS / OTHER TIME PERIODS] because [REASON].
```

### 5. Document Limitations

Identify and articulate limitations honestly:

```markdown
## Limitations

1. **[Identification limitation]**: Our identification strategy relies on
   [assumption]. While we provide evidence supporting this assumption through
   [tests], we cannot definitively rule out [threat].

2. **[External validity]**: Our sample consists of [description]. Results may
   not generalize to [other contexts] because [reason].

3. **[Measurement]**: [Variable] is measured using [method], which may
   [limitation]. We address this by [mitigation] but acknowledge [remaining concern].

4. **[Data limitation]**: We lack data on [variable], which could [potential issue].
   Our robustness checks in Table X suggest this is [unlikely to/may] affect our
   conclusions.
```

### 5. Create Replication Package

Prepare materials for reproducibility:

```stata
* Master do-file header
* ============================================================
* Replication Code for "[Paper Title]"
* Authors: [Names]
* Date: [Date]
*
* This script reproduces all tables and figures in the paper.
* Runtime: approximately [X] minutes
*
* Requirements:
* Stata version: 15+
* Packages: reghdfe, estout, coefplot, csdid
* ============================================================

version 15
clear all
set more off

* Install required packages (uncomment if needed)
* ssc install reghdfe
* ssc install estout
* ssc install coefplot
* ssc install csdid

* Set root path (CHANGE THIS)
global root "[path to replication folder]"

* Derived paths
global code "$root/code"
global data "$root/data"
global raw "$data/raw"
global clean "$data/clean"
global tables "$root/output/tables"
global figures "$root/output/figures"
global logs "$root/logs"

* Start log
log using "$logs/replication_log.txt", text replace

* Run analysis
do "$code/01_clean_data.do"
do "$code/02_descriptives.do"
do "$code/03_main_analysis.do"
do "$code/04_robustness.do"
do "$code/05_figures.do"

* Report completion
display "Replication complete: " c(current_date) " " c(current_time)
display "Stata version: " c(stata_version)

log close
```

## Output: Final Report

Create the final synthesis (`memos/phase5-final-report.md`):

```markdown
# Analysis Summary

## Key Finding
[One sentence summary of the main result]

## Main Result
- **Effect size**: [estimate with CI]
- **Significance**: [p-value or significance level]
- **Interpretation**: [what this means substantively]

## Robustness Assessment
- The finding [is/is not] robust to [list of checks]
- Main concerns: [if any]

## Output Files Created

### Tables
- `table1_descriptives.rtf`: Summary statistics
- `table2_main.rtf`: Main results
- `table3_robustness.rtf`: Robustness checks

### Figures
- `figure1_trends.pdf`: Pre/post trends
- `figure2_eventstudy.pdf`: Event study
- `figure3_coefplot.pdf`: Coefficient plot

### Replication Materials
- `00_master.do`: Master script
- `code/`: All analysis do-files
- `data/clean/`: Analysis datasets
- `logs/`: Stata log files

## Results Narrative
[Draft paragraphs for the paper]

## Limitations
[Honest assessment of limitations]

## Conclusion
[What can and cannot be concluded from this analysis]
```

### 7. Pre-Submission Checklist

Before finalizing, verify the analysis meets publication standards:

**Minimum Standard (Required):**
- [ ] All variables clearly defined with units and coding
- [ ] Sample size and any exclusions documented
- [ ] Main coefficient table includes SEs and significance levels
- [ ] Standard error type specified (robust, clustered at X level, etc.)
- [ ] At least one robustness check reported
- [ ] Limitations section acknowledges main threats to validity

**Strong Standard (Competitive for top journals):**
- [ ] Descriptive statistics table with means, SDs, and sample sizes
- [ ] Multiple robustness specifications in appendix
- [ ] Effect sizes interpreted substantively (not just "significant")
- [ ] For nonlinear models: AMEs or predicted probabilities reported
- [ ] Wild cluster bootstrap for few-cluster designs
- [ ] Missing data approach documented and defended
- [ ] Visualization of key results (event study, coefficient plot, etc.)
- [ ] Replication code and data availability statement

**Exemplary Standard (Model for the field):**
- [ ] Pre-registration referenced (if applicable)
- [ ] Multiple identification strategies compared
- [ ] Heterogeneity analysis with theoretical motivation
- [ ] Mechanism analysis or mediation tests
- [ ] Power analysis or minimum detectable effects
- [ ] Bound analysis for worst-case scenarios
- [ ] Complete replication package with README

**Language Checklist:**
- [ ] Causal language only used with appropriate identification strategy
- [ ] Effect sizes interpreted relative to meaningful benchmarks
- [ ] Confidence intervals reported, not just p-values
- [ ] Scope conditions clearly stated
- [ ] "Significant" refers to statistical significance (or avoid the term)

## When You're Done

Return a summary to the orchestrator that includes:
1. List of all tables and figures created
2. The main finding in one sentence
3. Key limitations
4. Any remaining questions or concerns
5. Confirmation that replication materials are ready
6. Checklist tier achieved (minimum/strong/exemplary)

**The analysis is now complete.** All materials should be ready for paper writing.
