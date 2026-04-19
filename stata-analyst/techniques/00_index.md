# Stata Statistical Techniques - Index

Quick lookup for statistical methods in Stata. All code tested on Stata 15.1.

---

## Core Workflow

**For most journal-style analyses, follow this sequence:**

1. **Data Prep** → `00_data_prep.md`
   Import, merge, clean, construct variables, save analysis sample

2. **Descriptives** → `07_postestimation_reporting.md`
   Table 1 (overall + by group), Figure 1 (trends or distributions)

3. **Modeling** → `06_modeling_basics.md`
   OLS, logit/probit, margins, interactions

4. **Causal Methods** (if applicable) → `01_core_econometrics.md`
   TWFE, DiD, IV, matching, RD

5. **Output** → `04_visualization.md`, `07_postestimation_reporting.md`
   Tables to RTF/TeX, figures to PNG/PDF

6. **Pipeline Template** → `99_default_journal_pipeline.md`
   Copy this structure for new projects

---

## File Guide

| File | Topics |
|------|--------|
| `00_data_prep.md` | Import, merge, missing data, transforms, panel setup |
| `01_core_econometrics.md` | TWFE, DiD, Event Studies, IV, Matching, Mediation, Standard Errors |
| `02_survey_resampling.md` | Survey Weights, Bootstrap, Randomization Inference, Oaxaca |
| `03_synthetic_control.md` | synth package for comparative case studies |
| `04_visualization.md` | esttab tables, coefplot, graphs, summary statistics |
| `05_best_practices.md` | Master do-files, path management, code organization |
| `06_modeling_basics.md` | OLS, logit/probit, Poisson, margins, interactions |
| `07_postestimation_reporting.md` | Estimates workflow, predicted values, diagnostics, Table 1 |
| `99_default_journal_pipeline.md` | Complete project template, file naming, submission checklist |

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

### Data Preparation
- **Import CSV/Excel** → `00_data_prep.md` Section 1
- **Merge patterns** → `00_data_prep.md` Section 2
- **Missing data audit** → `00_data_prep.md` Section 3
- **Reshape** → `00_data_prep.md` Section 2
- **Panel setup (xtset)** → `00_data_prep.md` Section 5

### Basic Modeling
- **OLS with robust/clustered SEs** → `06_modeling_basics.md` Section 1
- **Interactions and margins** → `06_modeling_basics.md` Section 2
- **Logit/Probit** → `06_modeling_basics.md` Section 3
- **Marginal effects (AME)** → `06_modeling_basics.md` Section 3
- **Poisson/Negative Binomial** → `06_modeling_basics.md` Section 4
- **Ordinal logit** → `06_modeling_basics.md` Section 5
- **VIF and diagnostics** → `06_modeling_basics.md` Section 7

### Post-Estimation
- **Estimates store/restore** → `07_postestimation_reporting.md` Section 1
- **Nested tables** → `07_postestimation_reporting.md` Section 2
- **Predicted values** → `07_postestimation_reporting.md` Section 3
- **Table 1 (descriptives)** → `07_postestimation_reporting.md` Section 5
- **Balance tables** → `07_postestimation_reporting.md` Section 6

### Reporting Checklists
- **TWFE checklist** → `01_core_econometrics.md` Reporting Checklists
- **DiD checklist** → `01_core_econometrics.md` Reporting Checklists
- **IV checklist** → `01_core_econometrics.md` Reporting Checklists
- **Matching checklist** → `01_core_econometrics.md` Reporting Checklists

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
