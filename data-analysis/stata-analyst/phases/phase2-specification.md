# Phase 2: Model Specification

You are executing Phase 2 of a statistical analysis in Stata. Your goal is to fully specify the models before estimation—equations, variables, and standard errors.

## Why This Phase Matters

Specification decisions are research decisions. Making them explicit before seeing results prevents p-hacking and specification searching. This phase documents the pre-analysis plan.

## Technique Guides

**Consult these guides** in `stata-statistical-techniques/` for specification patterns:

| Method | Guide |
|--------|-------|
| DiD, TWFE, Event Study, IV | `01_core_econometrics.md` |
| Matching specifications | `01_core_econometrics.md` Section 5 |
| Nonlinear models (logit, Poisson) | `06_modeling_basics.md` |
| Synthetic control | `03_synthetic_control.md` |

## Your Tasks

### 1. Write the Estimating Equation

State the model formally. Examples by design:

**Two-Way Fixed Effects:**
$$Y_{it} = \alpha_i + \gamma_t + \beta \cdot Treated_{it} + X_{it}'\delta + \varepsilon_{it}$$

**Difference-in-Differences:**
$$Y_{it} = \alpha + \beta_1 \cdot Post_t + \beta_2 \cdot Treat_i + \beta_3 \cdot (Post_t \times Treat_i) + \varepsilon_{it}$$

**Event Study:**
$$Y_{it} = \alpha_i + \gamma_t + \sum_{k \neq -1} \beta_k \cdot \mathbf{1}[t - E_i = k] + X_{it}'\delta + \varepsilon_{it}$$

**Instrumental Variables:**
- First stage: $D_i = \pi_0 + \pi_1 Z_i + X_i'\pi_2 + \nu_i$
- Second stage: $Y_i = \beta_0 + \beta_1 \hat{D}_i + X_i'\beta_2 + \varepsilon_i$

### 2. Define All Variables

Create a variable dictionary:

| Variable | Name in Data | Definition | Notes |
|----------|--------------|------------|-------|
| Outcome | `outcome` | [precise definition] | [measurement, source] |
| Treatment | `treated` | [how assigned] | [timing if applicable] |
| Control 1 | `age` | [definition] | [why included] |
| ... | | | |

**Key questions:**
- How is treatment defined? (binary, intensity, timing)
- What controls are included and why?
- Are there variables that should NOT be controlled for? (mediators, colliders)

### 3. Specify Fixed Effects Structure

For panel data, justify the FE structure:

| Specification | Absorbs | Code |
|---------------|---------|------|
| Unit FE | Time-invariant unit characteristics | `reghdfe y x, absorb(id)` |
| Time FE | Common shocks | `reghdfe y x, absorb(year)` |
| Two-way FE | Both | `reghdfe y x, absorb(id year)` |
| Unit-by-time trends | Unit-specific trends | `reghdfe y x, absorb(id year c.year#i.id)` |

Document why this structure is appropriate for the research question.

### 4. Determine Standard Error Clustering

**Default rule:** Cluster at the level of treatment assignment.

| Design | Typical Clustering | Rationale |
|--------|-------------------|-----------|
| State policy DiD | State | Treatment varies at state level |
| Individual-level RCT | Individual or strata | Assignment unit |
| Panel with firm shocks | Firm | Errors correlated within firm over time |

```stata
* reghdfe syntax
reghdfe y x, absorb(id year) cluster(id)

* Two-way clustering if needed
reghdfe y x, absorb(id year) cluster(id year)
```

**Consider wild cluster bootstrap** if few clusters (<50):
```stata
* After estimation with reghdfe
boottest x, cluster(state) reps(999) nograph
```

### 5. Plan Specification Sequence

Define the sequence of models to run:

| Model | Description | Purpose |
|-------|-------------|---------|
| (1) | Baseline: treatment only | Raw relationship |
| (2) | + Unit FE | Control time-invariant confounders |
| (3) | + Time FE | Control common shocks |
| (4) | + Controls | Address remaining confounders |
| (5) | Preferred specification | Main results |

This builds credibility by showing results are stable across specifications.

### 6. Pre-specify Robustness Checks

Before running main models, document planned robustness checks:

**Alternative specifications:**
- [ ] Different control sets
- [ ] Different FE structures
- [ ] Different treatment definitions

**Sensitivity analysis:**
- [ ] Sensitivity to outliers (winsorize, trim)
- [ ] Sensitivity to functional form

**Placebo tests:**
- [ ] Pre-treatment effects (should be zero)
- [ ] Outcomes that shouldn't be affected
- [ ] Fake treatment timing

**Heterogeneity:**
- [ ] Subgroup analyses (pre-specified)
- [ ] Interaction terms

## Output: Specification Memo

Create a specification memo (`memos/phase2-specification-memo.md`):

```markdown
# Model Specification Memo

## Estimating Equation

[LaTeX or clear written equation]

## Variable Definitions

| Variable | Name | Definition | Measurement |
|----------|------|------------|-------------|
| ... | | | |

## Fixed Effects
[Structure and justification]

## Standard Errors
Clustered at: [level]
Justification: [why]

## Specification Sequence

| Model | Specification | Purpose |
|-------|---------------|---------|
| (1) | | |
| ... | | |

## Pre-Specified Robustness Checks
1. [Check 1]
2. [Check 2]
...

## Pre-Specified Subgroup Analyses
1. [Subgroup 1]
2. [Subgroup 2]
...

## Code Skeleton

```stata
* Install packages if needed
* ssc install reghdfe
* ssc install estout

* Load data
use "$clean/analysis_sample.dta", clear

* Clear stored estimates
estimates clear

* Specification sequence
reghdfe outcome treatment, noabsorb cluster(cluster_var)
estimates store m1

reghdfe outcome treatment, absorb(id) cluster(cluster_var)
estimates store m2

reghdfe outcome treatment, absorb(id year) cluster(cluster_var)
estimates store m3

reghdfe outcome treatment control1 control2, absorb(id year) cluster(cluster_var)
estimates store m4

* Display results
esttab m1 m2 m3 m4, se star(* 0.10 ** 0.05 *** 0.01)
```

## Questions for User
[Any specification decisions that need input]
```

## When You're Done

Return a summary to the orchestrator that includes:
1. The main estimating equation
2. Fixed effects structure and clustering
3. The planned specification sequence
4. Pre-specified robustness checks
5. Any questions requiring user input

**Do not proceed to Phase 3 until the user approves the specification.**
