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
