# Robustness Framework for FT50 Empirical Research

This reference defines the five-level Robustness Pyramid that forms the backbone of credibility in FT50 empirical research. Each level addresses a specific threat to causal inference, and the pyramid is ordered from least to most demanding of the data. A paper that survives all five levels provides compelling evidence that the estimated effect is not an artefact of measurement, sample selection, specification, or unobserved confounding.

---

## 1. The Robustness Pyramid

```
                          ▲
                         /|\
                        / | \
                       /  5  \
                      / Selection\
                     /on Unobservables\
                    /───────────────────\
                   /       4             \
                  /    Placebo &          \
                 /   Falsification Tests   \
                /─────────────────────────────\
               /            3                 \
              /    Alternative Specifications   \
             /─────────────────────────────────────\
            /               2                      \
           /        Alternative Samples             \
          /───────────────────────────────────────────\
         /                    1                        \
        /           Alternative Measures                \
       /───────────────────────────────────────────────────\
```

### Level 1: Alternative Measures

The most basic robustness check: does the result hold when the dependent variable or key independent variable is measured differently?

**Checklist:**
- [ ] Alternative DV construction (log vs. level, ratio vs. difference, different winsorisation thresholds, industry-adjusted vs. raw)
- [ ] Alternative IV construction (continuous vs. indicator, different aggregation levels)
- [ ] Different data sources for the same construct (Compustat vs. CRSP, survey vs. administrative, analyst vs. realised)
- [ ] Alternative industry classifications (SIC 2-digit vs. 3-digit vs. Fama-French vs. GICS)

**Reporting:** Create a single table with the baseline specification in column (1) and alternative measures in subsequent columns. Report the coefficient, standard error, and whether the p-value crosses 0.05.

### Level 2: Alternative Samples

Does the result generalise across different subpopulations, or is it driven by a particular subgroup, time period, or outlier?

**Checklist:**
- [ ] Exclude financial firms (SIC 6000–6999) and utilities (SIC 4900–4999)
- [ ] Exclude the top and bottom 1% of observations by key variables
- [ ] Drop observations from the Global Financial Crisis (2008–2009) or COVID-19 (2020–2021)
- [ ] Exclude the largest state/country/industry in the sample
- [ ] Split by firm size, age, profitability, or governance quality
- [ ] Balanced panel only (drop firms with missing years)
- [ ] Restrict to firms with at least T consecutive years of data
- [ ] Leave-one-industry-out: re-estimate dropping one industry at a time; plot coefficients

**Reporting:** A single table with columns for each sample restriction. The most important tests are (a) excluding the largest group, (b) excluding crisis periods, and (c) balanced panel.

### Level 3: Alternative Specifications

Does the result survive changes to the regression model — fixed effects, control variables, standard error clustering, and functional form?

**Checklist:**
- [ ] Incremental fixed effects: none → industry → industry × year → firm → firm × year
- [ ] Alternative control sets: sparse (core controls only) → full (all controls) → saturated (interactions)
- [ ] Alternative functional forms: linear → log-linear → Poisson → fractional logit → quantile regression
- [ ] Standard error clustering: robust → state → industry → firm → double-clustered (firm × year)
- [ ] Alternative DID estimators for staggered designs (see Identification Strategies reference)
- [ ] Different lag structures for dynamic models
- [ ] Alternative estimation methods: OLS → WLS → median regression → GMM

**Reporting:** The "horse race" table — each column represents a different specification. The coefficient of interest should remain stable in sign, magnitude, and significance. A coefficient that flips sign or loses significance under reasonable alternatives is a red flag.

### Level 4: Placebo & Falsification Tests

Could the result be driven by something other than the hypothesised mechanism? Falsification tests attempt to "break" the result under conditions where the theory predicts no effect.

**Checklist:**
- [ ] Placebo treatment date: shift the treatment backward by 1, 2, or 3 periods; expect null effects
- [ ] Placebo treatment group: randomly reassign treatment to a comparable untreated group; expect null
- [ ] Placebo outcome: test the "effect" on an outcome that should not be affected by treatment
- [ ] Placebo cutoff (RDD): estimate the treatment effect at arbitrary non-cutoff values
- [ ] Future treatment test: regress current outcomes on future treatment
- [ ] Pre-treatment outcome test: regress pre-treatment outcomes on eventual treatment assignment

**Reporting:** For each falsification test, report the coefficient, standard error, and whether it is statistically indistinguishable from zero. Include a visual placebo distribution for random treatment reassignment (density of placebo coefficients with vertical line at actual coefficient).

### Level 5: Selection on Unobservables

The most demanding test: how large would selection on unobservables need to be, relative to selection on observables, to explain away the result? This level acknowledges that no set of controls can fully capture all confounders.

**Checklist:**
- [ ] Oster (2019) bounds: report $\delta$ (the ratio of selection on unobservables to selection on observables) that would produce $\beta = 0$
- [ ] Altonji, Elder & Taber (2005) ratio test: compare coefficient movements with and without controls
- [ ] Rosenbaum bounds for matching estimators
- [ ] Conley, Hansen & Rossi (2012) bounds for IV exclusion restriction
- [ ] Coefficient stability plots (visual inspection of coefficient as controls are added)

---

## 2. Oster (2019) Bounds for Selection on Unobservables

### 2.1 The Oster Framework

Oster (2019) provides a method to bound the true treatment effect when there is selection on both observables and unobservables. The key insight: movements in the coefficient of interest and the $R^2$ when controls are added contain information about the likely magnitude of omitted variable bias.

**The Identification Problem:**

Consider the true model $Y = \beta X + \Psi W_1 + W_2 + \varepsilon$, where $W_1$ is observed and included in the regression, and $W_2$ is unobserved and omitted. The short regression $Y = \beta X + \varepsilon$ yields $\hat{\beta}_{short}$. The intermediate regression $Y = \beta X + \Psi W_1 + \varepsilon$ yields $\hat{\beta}_{mid}$. The goal is to bound $\beta$ given that $W_2$ cannot be observed.

**The Oster Delta ($\delta$):**

Define $\delta$ as the coefficient of proportionality relating selection on unobservables to selection on observables:

$$\LARGE \delta \cdot \frac{Cov(W_1, X)}{Var(W_1)} = \frac{Cov(W_2, X)}{Var(W_2)}$$

When $\delta = 1$, selection on unobservables is equally as important as selection on observables in determining treatment assignment. When $\delta > 1$, unobservables are more important.

**The Proportional Selection Assumption:**

$$\LARGE \delta \frac{Cov(W_1, X)}{Var(W_1)} = \frac{Cov(W_2, X)}{Var(W_2)}$$

This assumption states that the relationship between the treatment and unobservables is proportional to the relationship between the treatment and observables, scaled by $\delta$.

### 2.2 Implementation of Oster Bounds

**Step 1: Define the Controlled and Uncontrolled Models**

- Uncontrolled: $Y = \beta X + \varepsilon$ → $\hat{\beta}_{short}$, $R_{short}^2$
- Controlled: $Y = \beta X + \Psi W_1 + \varepsilon$ → $\hat{\beta}_{mid}$, $R_{mid}^2$

**Step 2: Choose $R_{max}$**

$R_{max}$ is the $R^2$ from a hypothetical regression that includes both observed ($W_1$) and unobserved ($W_2$) controls. Since $W_2$ is unobserved, $R_{max}$ must be chosen. Oster suggests:

$$\LARGE R_{max} = \min\{1.3 \times R_{mid}^2, 1\}$$

This is based on evidence from randomised studies where the $R^2$ including all controls is typically not more than 1.3 times the $R^2$ with a subset. Alternative choices:
- $R_{max} = 1$ (most conservative; all selection is on unobservables)
- $R_{max} = \min\{2.2 \times R_{mid}^2, 1\}$ (based on a comparison of RCTs with and without controls)

**Always report results for the 1.3× rule as the baseline, with 1.0× and 2.2× as robustness.**

**Step 3: Compute the Bias-Adjusted Coefficient**

$$\LARGE \beta^* = \hat{\beta}_{mid} - \delta [\hat{\beta}_{short} - \hat{\beta}_{mid}] \cdot \frac{R_{max} - R_{mid}^2}{R_{mid}^2 - R_{short}^2}$$

Setting $\beta^* = 0$ and solving for $\delta$ gives:

$$\LARGE \delta = \frac{\hat{\beta}_{mid} \cdot (R_{mid}^2 - R_{short}^2)}{(\hat{\beta}_{short} - \hat{\beta}_{mid}) \cdot (R_{max} - R_{mid}^2)}$$

This $\delta$ is interpreted as: "Selection on unobservables would need to be $\delta$ times as important as selection on observables to explain away the entire estimated effect."

**Step 4: Construct the Identified Set**

For a given $\delta$, the identified set for $\beta$ is $[\tilde{\beta}, \beta^*]$, where $\tilde{\beta} = \min(\beta^*, \hat{\beta}_{mid})$ and $\beta^*$ is obtained from the formula above. If this set excludes zero for $\delta = 1$, the result is considered robust to equal selection.

### 2.3 Interpreting Oster's $\delta$

| $\delta$ Value | Interpretation |
|----------------|----------------|
| $\delta > 1$ | Result is robust — unobservables would need to be *more* important than observables to overturn it |
| $\delta \approx 1$ | Borderline — roughly equal selection on observables and unobservables could explain the result |
| $0 < \delta < 1$ | Vulnerable — even weaker selection on unobservables could overturn the result |
| $\delta \leq 0$ | Coefficient stability implies unobservables push in the same direction; result may be conservative |

**Reporting convention:** "The estimated $\delta$ is [value], indicating that selection on unobservables would need to be [value] times as important as selection on observables to produce a treatment effect of zero. This [exceeds / is approximately equal to / falls below] the benchmark of $\delta = 1$ suggested by Oster (2019)."

### 2.4 Oster Bounds Reporting Table

```
                              Baseline      Controlled     Uncontrolled
                                 (1)            (2)             (3)
                        -------------------------------------------------
Treatment Effect (β)        0.052***        0.038***         0.085***
                            (0.012)         (0.012)          (0.018)

R²                           0.401           0.212            0.047
Controls                       Y               N                N
Fixed Effects                  Y               Y                N
Observations                18,420          18,420           18,420

Oster Bounds:
  Rmax = 1.3 × R_mid²      δ = 2.84
  Rmax = 1.0 × R_mid²      δ = 3.91
  Rmax = 2.2 × R_mid²      δ = 1.71

Identified Set (δ = 1)     [0.021, 0.038]
Identified Set (δ = 2)     [0.008, 0.038]
------------------------------------------------------------------------
Notes: Column (2) includes the full set of controls. Column (3) includes
only the treatment variable. Oster δ > 1 for all Rmax specifications,
indicating robustness to selection on unobservables.
```

### 2.5 Common Implementation Errors in Oster Bounds

| Error | Consequence | Correction |
|-------|-------------|------------|
| Using only point estimates, ignoring movement in $R^2$ | Understates or overstates delta | Always report movements in both $\beta$ and $R^2$ |
| Arbitrary choice of $R_{max}$ | Cherry-picking | Report for 1.3×, 1.0×, and 2.2× |
| Not including fixed effects in the controlled model when they are part of the baseline | $\beta$ movement is understated; delta is inflated | Include all baseline fixed effects in controlled model |
| Applying to models where $R_{mid}^2 \approx R_{short}^2$ | Delta is undefined or extremely large | Acknowledge that controls do not move $R^2$ — selection on observables is minimal |
| Claiming result is "proven robust" when $\delta > 1$ for one $R_{max}$ | Overclaiming | Use cautious language: "suggestive of robustness" |

---

## 3. Altonji, Elder & Taber (2005) Ratio Test

### 3.1 The AET Ratio

The Altonji et al. (2005) approach compares the movement in the coefficient of interest to the movement in the $R^2$ when controls are added to assess how much selection on unobservables would be needed to eliminate the effect.

**The Ratio:**

$$\LARGE \text{Ratio} = \frac{\hat{\beta}_{full}}{\hat{\beta}_{restricted} - \hat{\beta}_{full}}$$

where $\hat{\beta}_{full}$ is the coefficient from the regression with controls and $\hat{\beta}_{restricted}$ is from the regression without controls (but including fixed effects).

**Interpretation:** A ratio greater than 1 indicates that selection on unobservables would need to be larger than selection on observables to explain away the entire effect. Ratios above 3–4 are typically considered strongly robust.

### 3.2 Comparing Oster and AET

| Feature | Oster (2019) | Altonji et al. (2005) |
|---------|-------------|----------------------|
| Accounts for $R^2$ movement | Yes | Implicitly |
| Requires $R_{max}$ | Yes | No |
| Produces identified set | Yes | No (point estimate only) |
| Interpretation | Delta: selection proportionality | Ratio: coefficient stability |
| Preferred venue | Post-2019 standard | Complementary check |

Report both. If they agree, the robustness case is stronger. If they disagree, investigate why (e.g., $R^2$ movement is minimal, or the coefficient is very stable).

---

## 4. Rosenbaum Bounds for Matching Estimators

### 4.1 Sensitivity to Hidden Bias

Rosenbaum (2002) bounds provide a method to assess how sensitive matching estimates are to unobserved confounding. The key parameter is $\Gamma$ (Gamma), which measures the odds ratio of treatment assignment for two matched units that differ by an unobserved confounder.

**The Sensitivity Parameter $\Gamma$:**

Two units $i$ and $j$ matched on observables $X$ have the same probability of treatment if there is no hidden bias ($\Gamma = 1$). If an unobserved confounder $U$ makes one unit $\Gamma$ times more likely to receive treatment, then:

$$\LARGE \frac{1}{\Gamma} \leq \frac{\Pr(T_i = 1 \mid X_i)(1 - \Pr(T_j = 1 \mid X_j))}{(1 - \Pr(T_i = 1 \mid X_i))\Pr(T_j = 1 \mid X_j)} \leq \Gamma$$

**Implementation:**
1. For each $\Gamma$ (starting at 1.0, increasing in steps of 0.1), compute the range of possible p-values for the treatment effect.
2. Report $\Gamma^*$, the value of $\Gamma$ at which the upper bound of the p-value crosses 0.05 (i.e., the effect becomes statistically insignificant).
3. For continuous outcomes, report the Hodges-Lehmann point estimate and confidence interval for each $\Gamma$.

**Interpretation:** $\Gamma^* = 2.5$ means that an unobserved confounder would need to more than double the odds of treatment to overturn the result. In social science applications, $\Gamma^* > 2$ is typically considered robust.

### 4.2 Rosenbaum Bounds Reporting

```
Gamma (Γ)        Lower p-value      Upper p-value      HL Estimate
------------------------------------------------------------------
1.0                  0.0001             0.0001             0.042
1.5                  0.0005             0.0032             0.034
2.0                  0.0028             0.0241             0.027
2.3                  0.0059             0.0488             0.022 *
2.5                  0.0113             0.0730             0.019 ns
3.0                  0.0342             0.1832             0.011 ns
------------------------------------------------------------------
* Γ_critical = 2.3 is the value at which the upper bound p-value
crosses 0.05. An unobserved confounder would need to increase the
odds of treatment by a factor of 2.3 to render the result
insignificant at the 5% level.
```

---

## 5. Coefficient Stability Plots

### 5.1 Construction

A coefficient stability plot shows how the estimated treatment effect changes as controls are added cumulatively to the regression. This provides a visual complement to Oster's formal bounds.

**Procedure:**
1. Estimate a sequence of regressions, adding controls one group at a time (e.g., demographic → firm characteristics → industry FE → year FE → firm FE).
2. For each regression, plot the point estimate and 95% confidence interval of the coefficient of interest.
3. The coefficient should stabilise — not trend toward zero — as controls are added.

**Interpretation:** If the coefficient estimates are stable across specifications with very different $R^2$ values, this is *suggestive* that selection on unobservables is unlikely to overturn the result. If the coefficient drifts toward zero systematically, unobserved confounders may be important.

### 5.2 The "Coefficient Stability vs. R²" Plot

Plot the coefficient estimate ($\hat{\beta}$) on the y-axis against the $R^2$ of the model on the x-axis, with each regression specification as a data point. The plot reveals:
- **Convergence:** $\hat{\beta}$ stabilises; unobservables unlikely to matter
- **Divergence:** $\hat{\beta}$ trends toward zero with increasing $R^2$; Oster delta likely small
- **Amplification:** $\hat{\beta}$ grows with $R^2$; observable controls actually suppress bias upward

---

## 6. Discipline-Specific Robustness Expectations

### 6.1 Finance (Journal of Finance, Journal of Financial Economics, Review of Financial Studies)

**Expectation: HIGH**

Finance reviewers demand the most exhaustive robustness. Expectations include:
- Multiple identification strategies (e.g., DID + IV + RDD as robustness)
- All five levels of the robustness pyramid, typically in this order
- Oster (2019) bounds are now standard whenever selection-on-observables is the baseline design
- Coefficient stability is plotted, not just described
- At least one falsification test specific to the finance context (e.g., testing on pre-treatment outcomes, unaffected industries, placebo policy dates)
- Subsample analyses across firm size, leverage, and market-to-book quintiles
- Alternative clustering: firm, firm×year, industry×year

### 6.2 Accounting (Journal of Accounting Research, Journal of Accounting and Economics, The Accounting Review)

**Expectation: MODERATE-HIGH**

Accounting reviewers emphasise construct validity and measurement:
- Alternative measures of earnings quality, disclosure, or audit quality receive the most scrutiny (Level 1)
- Entropy balancing or propensity score matching is common for non-randomised designs
- Cross-sectional variation is explored extensively (above/below-median splits on key characteristics)
- Falsification: testing on pre-regulation periods or unaffected industries/accounts
- Changes analysis (first-differences) as a robustness specification
- Placebo outcomes that should not be affected by the treatment

### 6.3 Management (Academy of Management Journal, Strategic Management Journal, Organization Science)

**Expectation: MODERATE-HIGH**

Management reviewers expect:
- Strong theoretical grounding for each robustness check (not a mechanical exercise)
- Multiple IV strategies with careful explanation of the exclusion restriction
- Heckman two-step selection correction when sample selection is a concern
- Sensitivity to unobserved heterogeneity via random-effects vs. fixed-effects specifications
- Endogeneity addressed through at least two approaches (e.g., IV + matching, or DID + SCM)
- Qualitative robustness checks (interviews, archival evidence) to complement quantitative ones

### 6.4 Marketing (Journal of Marketing, Journal of Marketing Research, Marketing Science)

**Expectation: MODERATE**

Marketing reviewers focus on:
- External validity and generalisability across product categories, brands, and consumer segments
- Field experiment results supplemented by lab replications
- Alternative functional forms (log-log, semi-log, Box-Cox) for demand/sales models
- Multiple testing correction for many outcome variables or segment analyses
- Heterogeneity analysis by consumer demographics and purchase history
- Holdout sample validation for predictive models

### 6.5 Operations (Manufacturing & Service Operations Management, Production and Operations Management)

**Expectation: MODERATE**

Operations reviewers prioritise:
- Robustness to different operational contexts (different plants, products, time periods)
- Alternative operational measures (e.g., different ways of computing throughput, quality, or inventory)
- Sensitivity to capacity constraints and demand assumptions
- Structural vs. reduced-form comparisons
- Out-of-sample validation and forecasting accuracy

### 6.6 Economics (American Economic Review, Econometrica, Quarterly Journal of Economics, Review of Economic Studies)

**Expectation: VERY HIGH**

Economics reviewers apply the most stringent econometric standards:
- Formal identification arguments with explicit counterfactual reasoning
- Multiple robustness estimators for the same design (e.g., for DID: CSDID, SA, BJS, dCDH — all reported)
- Pre-analysis plans and pre-registration for experimental and quasi-experimental work
- Randomisation inference for all cluster-based designs
- Weak-instrument robust inference as default, not robustness
- Honest confidence sets (Rambachan & Roth 2023) for DID
- Conley standard errors for spatial data
- Bounds analysis (partial identification) rather than point estimates when assumptions are questionable
- Extensive Monte Carlo simulations to demonstrate estimator properties in finite samples

---

## 7. The Robustness Reporting Template

For each robustness check, report a consistent structure:

### 7.1 Table Structure

```
Table X: Robustness of [Main Result] to [Category of Check]

                                (1)           (2)         Effect      Inference
                             Baseline     Robustness     Changes?     Changes?
                        --------------------------------------------------------
Panel A: Alternative Measures
  Measure 1                  0.042***      0.039***        No          No
  Measure 2                  0.042***      0.045***        No          No
  Measure 3                  0.042***      0.038**        Slight       No

Panel B: Alternative Samples
  Drop financials            0.042***      0.040***        No          No
  Drop GFC (2008-09)         0.042***      0.043***        No          No
  Balanced panel only        0.042***      0.036**        Slight       No
  Exclude top 1%             0.042***      0.041***        No          No

Panel C: Alternative Specifications
  Industry FE only           0.042***      0.048***       Moderate      No
  Firm FE                    0.042***      0.035**        Slight       No
  No controls                0.042***      0.061***       Moderate      No
  Double-clustered SE        0.042***      0.042**          No         No

Panel D: Placebo & Falsification
  Placebo treatment date     0.042***      0.008              --        Yes
  Placebo treatment group    0.042***     -0.003              --        Yes
  Placebo outcome            0.042***      0.011              --        Yes

Panel E: Selection on Unobservables
  Oster δ (Rmax = 1.3×)         --         2.84              --         --
  AET Ratio                     --         4.21              --         --
------------------------------------------------------------------------
Notes: Each panel tests a distinct threat. "Effect Changes?" indicates
whether the coefficient sign flips or magnitude changes by >50%.
"Inference Changes?" indicates whether the p-value crosses 0.05.
All specifications include the full control vector and baseline
fixed effects unless otherwise noted.
```

### 7.2 Narrative Template

Each robustness section in the paper should follow this narrative arc:

1. **State the threat:** "One concern with [main specification] is that [specific threat]."
2. **Describe the test:** "To address this, we [test description]."
3. **Report the result:** "As shown in Table X, Column Y, the estimated coefficient is [value] ([SE]), [direction of change] and [does/does not] alter the inference."
4. **Interpret the magnitude:** "The resulting δ of [value] suggests that..."
5. **Acknowledge limits:** "We acknowledge that [limitation]. Nevertheless, the collective evidence from [summary of checks] supports the conclusion that..."
6. **Transition:** "Having established the robustness of the main result, we now turn to..."

---

## 8. Implementation Guide: The Robustness Do-File / Script

### 8.1 Structure of a Reproducible Robustness Script

```stata
/*===========================================================================
 * ROBUSTNESS ANALYSIS: [Paper Title]
 * Author: [Name]
 * Date: [Date]
 *
 * This do-file implements the five-level robustness pyramid for the main
 * specification. Run after main_results.do.
 *===========================================================================*/

*---------------------------------------------------------------------------
* SETUP
*---------------------------------------------------------------------------
clear all
set more off
cap log close
log using "robustness.log", replace
use "analysis_data.dta", clear

global depvar Y              // Dependent variable
global treatvar X            // Treatment variable
global controls C1 C2 C3     // Core controls
global fe_vars firm_id year  // Fixed effects
global cluster_var firm_id   // Clustering variable

*---------------------------------------------------------------------------
* BASELINE SPECIFICATION
*---------------------------------------------------------------------------
reghdfe $depvar $treatvar $controls, absorb($fe_vars) vce(cluster $cluster_var)
estimates store baseline
estadd local obs = e(N)
estadd local r2 = e(r2)

*---------------------------------------------------------------------------
* LEVEL 1: ALTERNATIVE MEASURES
*---------------------------------------------------------------------------
* Measure 1: Winsorized at 1%/99% instead of default
local alt_depvars Y_winsor1 Y_winsor5 Y_log Y_percapita
foreach var of local alt_depvars {
    reghdfe `var' $treatvar $controls, absorb($fe_vars) vce(cluster $cluster_var)
    estimates store alt_`var'
}

* Measure 2: Alternative independent variable
local alt_treatvars X_continuous X_dummy_alt X_binned
foreach var of local alt_treatvars {
    reghdfe $depvar `var' $controls, absorb($fe_vars) vce(cluster $cluster_var)
    estimates store alt_treat_`var'
}

*---------------------------------------------------------------------------
* LEVEL 2: ALTERNATIVE SAMPLES
*---------------------------------------------------------------------------
* Drop financials and utilities
preserve
drop if inrange(sic, 6000, 6999) | inrange(sic, 4900, 4999)
reghdfe $depvar $treatvar $controls, absorb($fe_vars) vce(cluster $cluster_var)
estimates store sample_nofin
restore

* Drop top/bottom 1%
preserve
_pctile $depvar, percentiles(1 99)
drop if $depvar < r(r1) | $depvar > r(r2)
reghdfe $depvar $treatvar $controls, absorb($fe_vars) vce(cluster $cluster_var)
estimates store sample_trimmed
restore

* Balanced panel
preserve
bysort firm_id: gen panel_length = _N
keep if panel_length == [T]
reghdfe $depvar $treatvar $controls, absorb($fe_vars) vce(cluster $cluster_var)
estimates store sample_balanced
restore

*---------------------------------------------------------------------------
* LEVEL 3: ALTERNATIVE SPECIFICATIONS
*---------------------------------------------------------------------------
* Incremental fixed effects
foreach fe in "industry" "industry year" "firm year" "firm##year" {
    reghdfe $depvar $treatvar $controls, absorb(`fe') vce(cluster $cluster_var)
    estimates store spec_fe_`fe'
}

* Alternative clustering
foreach cl in "state" "industry" "firm year" {
    reghdfe $depvar $treatvar $controls, absorb($fe_vars) vce(cluster `cl')
    estimates store cluster_`cl'
}

*---------------------------------------------------------------------------
* LEVEL 4: PLACEBO & FALSIFICATION
*---------------------------------------------------------------------------
* Placebo treatment date (shift back 2 periods)
gen placebo_post = (year >= treat_year - 2)
gen placebo_did = treat_group * placebo_post
reghdfe $depvar placebo_did $controls, absorb($fe_vars) vce(cluster $cluster_var)
estimates store placebo_time

* Placebo treatment group (random assignment)
preserve
set seed 12345
tempvar random_treat
gen `random_treat' = runiform() < [treatment proportion]
gen placebo_treat = `random_treat' * post_period
reghdfe $depvar placebo_treat $controls, absorb($fe_vars) vce(cluster $cluster_var)
estimates store placebo_group
restore

* Placebo outcome
reghdfe placebo_outcome $treatvar $controls, absorb($fe_vars) vce(cluster $cluster_var)
estimates store placebo_outcome

*---------------------------------------------------------------------------
* LEVEL 5: SELECTION ON UNOBSERVABLES
*---------------------------------------------------------------------------
* Oster (2019) bounds
* Step 1: Short regression (no controls)
reghdfe $depvar $treatvar, absorb($fe_vars) vce(cluster $cluster_var)
local beta_short = _b[$treatvar]
local r2_short = e(r2)

* Step 2: Intermediate regression (with controls)
estimates restore baseline
local beta_mid = _b[$treatvar]
local r2_mid = e(r2)

* Step 3: Compute delta for various Rmax values
foreach mult in 1.0 1.3 2.2 {
    local rmax = min(`mult' * `r2_mid', 0.999)
    local delta = (`beta_mid' * (`r2_mid' - `r2_short')) / ((`beta_short' - `beta_mid') * (`rmax' - `r2_mid'))
    display "Oster delta (Rmax = `mult'×): " `delta'
}

*---------------------------------------------------------------------------
* EXPORT ALL RESULTS
*---------------------------------------------------------------------------
esttab baseline alt_* sample_* spec_* cluster_* placebo_* ///
    using "robustness_table.tex", replace ///
    keep($treatvar) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2, fmt(%9.0fc %9.3f)) ///
    indicate("Controls = $controls") ///
    title("Robustness of Main Results")

log close
```

---

## 9. Decision Tree: Which Robustness Checks to Report?

```
Is the design...
├── Experimental (RCT)?
│   ├── Attrition > 5%? → Lee bounds
│   ├── Multiple outcomes? → Romano-Wolf / FDR
│   ├── Non-compliance? → LATE via IV
│   └── Always: balance table, randomisation inference, ITT vs. ATT
│
├── Quasi-experimental (DID, RDD, IV)?
│   ├── DID → parallel trends (visual + Granger), staggered-robust estimators, Oster
│   ├── RDD → McCrary, bandwidth sensitivity, placebo cutoffs
│   ├── IV → weak-instrument robust inference, Conley bounds, OLS comparison
│   └── Always: Oster bounds, falsification, alternative samples
│
├── Selection-on-observables (matching, regression)?
│   ├── Always: Oster (δ), AET ratio, coefficient stability plot
│   ├── Matching: Rosenbaum bounds, balance diagnostics, common support
│   └── Always: alternative measures, alternative specifications
│
└── Structural / calibration?
    ├── Parameter sensitivity: univariate and multivariate
    ├── Alternative calibration targets
    ├── Monte Carlo for finite-sample properties
    └── Out-of-sample validation
```

---

## References

- Altonji, J. G., Elder, T. E., & Taber, C. R. (2005). Selection on observed and unobserved variables: Assessing the effectiveness of Catholic schools. *Journal of Political Economy*, 113(1), 151-184.
- Bell, R. M., & McCaffrey, D. F. (2002). Bias reduction in standard errors for linear regression with multi-stage samples. *Survey Methodology*, 28(2), 169-181.
- Conley, T. G., Hansen, C. B., & Rossi, P. E. (2012). Plausibly exogenous. *Review of Economics and Statistics*, 94(1), 260-272.
- Imbens, G. W., & Manski, C. F. (2004). Confidence intervals for partially identified parameters. *Econometrica*, 72(6), 1845-1857.
- Lee, D. S. (2009). Training, wages, and sample selection: Estimating sharp bounds on treatment effects. *Review of Economic Studies*, 76(3), 1071-1102.
- Oster, E. (2019). Unobservable selection and coefficient stability: Theory and evidence. *Journal of Business & Economic Statistics*, 37(2), 187-204.
- Rosenbaum, P. R. (2002). *Observational Studies* (2nd ed.). Springer.
- Rosenbaum, P. R., & Rubin, D. B. (1983). Assessing sensitivity to an unobserved binary covariate in an observational study with binary outcome. *Journal of the Royal Statistical Society, Series B*, 45(2), 212-218.
