# Identification Strategies for FT50 Empirical Research

This reference provides comprehensive guidance on the seven core identification strategies employed in top-tier empirical finance, accounting, management, marketing, and economics research. Each section contains the econometric foundation, implementation checklist, reporting template, and common pitfalls with remedies.

---

## 1. Difference-in-Differences (DID)

### 1.1 Standard 2×2 DID

The canonical DID setup compares outcomes before and after a treatment between treated and control groups.

**Econometric Specification:**

The standard two-way fixed effects (TWFE) estimator is:

$$\LARGE Y_{it} = \alpha_i + \lambda_t + \beta^{DD} \cdot (Treat_i \times Post_t) + \gamma X_{it} + \varepsilon_{it}$$

where $\alpha_i$ are unit fixed effects, $\lambda_t$ are time fixed effects, $Treat_i$ is a binary indicator for treatment group membership, $Post_t$ is a binary indicator for the post-treatment period, and $\beta^{DD}$ is the causal effect of interest under the parallel trends assumption.

**Key Assumption — Parallel Trends:**

The expected counterfactual outcome for treated units, absent treatment, would have evolved similarly to the control group:

$$\LARGE \mathbb{E}[Y_{it}(0) \mid i \in Treated, t \geq t_0] - \mathbb{E}[Y_{it}(0) \mid i \in Treated, t < t_0] = \mathbb{E}[Y_{it}(0) \mid i \in Control, t \geq t_0] - \mathbb{E}[Y_{it}(0) \mid i \in Control, t < t_0]$$

### 1.2 Staggered DID — The New Benchmark

When treatment timing varies across units, the standard TWFE estimator produces a weighted average of all possible 2×2 comparisons, some of which use already-treated units as controls. This yields biased estimates under heterogeneous treatment effects.

**Key Citations for Staggered DID:**

| Estimator | Citation | Key Feature |
|-----------|----------|-------------|
| CSDID | Callaway & Sant'Anna (2021, *Journal of Econometrics*) | Group-time ATT, never-treated or not-yet-treated controls |
| SA | Sun & Abraham (2021, *Journal of Econometrics*) | Cohort-specific ATT, IW estimator with never-treated baseline |
| BJS | Borusyak, Jaravel & Spiess (2024, *Review of Economic Studies*) | Imputation estimator, efficient under homoskedasticity |
| dCDH | de Chaisemartin & D'Haultfoeuille (2020, *AER*) | Dynamic DID with switchers, placebo estimators |
| Gardner | Gardner (2024, arXiv) | Two-stage DID, robust to heterogeneous effects |
| Wooldridge | Wooldridge (2021, *Journal of Econometrics*) | Extended TWFE with cohort-specific trends |

**Callaway & Sant'Anna (2021) Estimator Definition:**

The group-time average treatment effect on the treated for cohort $g$ at time $t$:

$$\LARGE ATT(g,t) = \mathbb{E}[Y_t(g) - Y_{g-1}(g) \mid G_g = 1] - \mathbb{E}[Y_t(C) - Y_{g-1}(C) \mid C = 1]$$

where $G_g$ indicates treatment in period $g$, and $C$ denotes the control group (never-treated or not-yet-treated). The overall ATT aggregates these group-time effects with user-chosen weights.

**Event Study Specification (preferred for all staggered designs):**

$$\LARGE Y_{it} = \alpha_i + \lambda_t + \sum_{k=-K, k \neq -1}^{-2} \beta_k \cdot D_{it}^k + \sum_{k=0}^{L} \beta_k \cdot D_{it}^k + \gamma X_{it} + \varepsilon_{it}$$

where $D_{it}^k$ are relative-time indicators (k periods before/after treatment). The period $k = -1$ is the omitted reference category. This specification directly visualises pre-trends and dynamic treatment effects.

**Binned Endpoint Convention:**

To avoid estimating noisy long-run effects from sparse data, bin the endpoints:

- Pre-treatment: bin all periods $k \leq -K$ into a single indicator
- Post-treatment: bin all periods $k \geq L$ into a single indicator

Where $K$ and $L$ are chosen so at least 5% of observations fall in each non-binned period.

### 1.3 Testing Parallel Trends

**Visual Test (primary):**

Plot coefficient estimates $\hat{\beta}_k$ from the event study specification for $k < 0$ with 95% confidence intervals. The null of parallel trends is supported if all pre-treatment coefficients are statistically indistinguishable from zero. Report both the joint F-test and individual coefficient plots.

**Granger-Style F-Test:**

Regress $Y_{it}$ on leads of the treatment indicator (periods $t+2$, $t+1$, treated at $t$, treated at $t-1$, etc.). Test the joint hypothesis that coefficients on all lead indicators equal zero:

$$\LARGE H_0: \beta_{-K} = \beta_{-K+1} = ... = \beta_{-2} = 0$$

Use cluster-robust standard errors at the unit level. Report the F-statistic, degrees of freedom, and p-value.

**Rambachan & Roth (2023) Sensitivity:**

Post a bound on the possible violation of parallel trends using Rambachan & Roth (2023, *Review of Economic Studies*) honest confidence sets. Report the breakdown point $M_{max}$ at which the confidence set includes zero.

### 1.4 Triple Differences (DDD)

When parallel trends are questionable, add a third difference to control for additional confounding.

$$\LARGE Y_{igt} = \beta_1 (Treat_g \times Post_t) + \beta_2 (Treat_g \times Group_i) + \beta_3 (Group_i \times Post_t) + \beta^{DDD} (Treat_g \times Post_t \times Group_i) + \alpha_g + \alpha_i + \alpha_t + \varepsilon_{igt}$$

The coefficient $\beta^{DDD}$ captures the differential effect of treatment on subgroup $i$ within treated group $g$. This design requires parallel trends in the *difference-in-differences* across the third dimension.

### 1.5 DID Implementation Checklist

- [ ] Document treatment assignment mechanism — what determines timing? Is it plausibly exogenous?
- [ ] Plot raw means by treatment cohort over calendar time
- [ ] Report the number of units per treatment cohort and per relative time bin
- [ ] Estimate both static TWFE and event study specifications
- [ ] Use at least one staggered-robust estimator (CSDID, SA, BJS, or dCDH)
- [ ] Test parallel pre-trends visually and with joint F-test
- [ ] Report sensitivity to different control group definitions (never-treated only vs. not-yet-treated)
- [ ] Bin endpoints to avoid noise-driven inference
- [ ] Cluster standard errors at the treatment assignment level
- [ ] Report the Goodman-Bacon (2021) decomposition for TWFE weights
- [ ] For DDD: show that the second-level parallel trends assumption holds

### 1.6 DID Reporting Table Template

```
                            (1)          (2)          (3)           (4)
                         Static       Event      CSDID         BJS
                          TWFE        Study      (2021)        (2024)
                        ---------------------------------------------------
Treat × Post          0.042***                   
                       (0.012)

ATT (aggregated)                               0.038**      0.041***
                                               (0.015)      (0.013)

Dynamic effects:
  t = 0                          0.025*
                                (0.014)
  t = 1                          0.038**
                                (0.015)
  t = 2                          0.044***
                                (0.014)
  t = 3                          0.041**
                                (0.017)
  t ≥ 4 (binned)                 0.036*
                                (0.019)

Pre-trend coefficients:
  t = -4                        -0.008
                                (0.011)
  t = -3                         0.005
                                (0.010)
  t = -2                         0.003
                                (0.012)
  t = -1 (ref.)                   ---

Pre-trend joint F-test  [p = 0.32]  [p = 0.32]   [p = 0.28]    [p = 0.30]

Controls                     Y          Y            Y             Y
Unit FE                      Y          Y            Y             Y
Time FE                      Y          Y            Y             Y
Observations              24,580     24,580       24,580        24,580
R-squared                  0.423      0.428         ---           ---
Clusters                     512        512          512           512
------------------------------------------------------------------------
Notes: Standard errors clustered at unit level in parentheses.
*** p<0.01, ** p<0.05, * p<0.10.
```

### 1.7 DID Common Pitfalls & Remedies

| Pitfall | Detection | Remedy |
|---------|-----------|--------|
| TWFE with staggered timing | Goodman-Bacon decomposition shows negative weights | Use CSDID, SA, BJS, or dCDH |
| Anticipation effects | Pre-trend coefficients are non-zero just before treatment | Shift treatment date earlier; drop anticipation window |
| Endogenous timing | Treatment timing correlated with pre-existing trends | Use matching before DID; include unit-specific linear trends |
| Few clusters (N<50) | Standard errors too narrow; over-rejection | Wild cluster bootstrap (Cameron, Gelbach & Miller 2008) |
| No never-treated group | All units eventually treated; no clean control | Use not-yet-treated as controls; note limitations |
| Covariate imbalance | Pre-treatment covariates differ significantly | Propensity score reweighting; entropy balancing |

---

## 2. Regression Discontinuity Design (RDD)

### 2.1 Sharp RDD

Treatment $D_i$ is a deterministic function of the running variable $X_i$ crossing threshold $c$:

$$\LARGE D_i = \mathbf{1}[X_i \geq c]$$

**Local Linear Regression Specification (CCT 2014, preferred):**

$$\LARGE Y_i = \alpha + \tau \cdot D_i + \beta_1 \cdot (X_i - c) + \beta_2 \cdot D_i \cdot (X_i - c) + \varepsilon_i$$

for observations within bandwidth $h$ of the cutoff: $|X_i - c| \leq h$. The parameter $\tau$ is the local average treatment effect at the cutoff. Use triangular kernel weighting.

### 2.2 Fuzzy RDD

When treatment probability jumps discontinuously but not deterministically at the cutoff:

**First Stage:**

$$\LARGE D_i = \gamma_0 + \gamma_1 \cdot \mathbf{1}[X_i \geq c] + \gamma_2 \cdot (X_i - c) + \gamma_3 \cdot \mathbf{1}[X_i \geq c] \cdot (X_i - c) + v_i$$

**Reduced Form:**

$$\LARGE Y_i = \mu_0 + \mu_1 \cdot \mathbf{1}[X_i \geq c] + \mu_2 \cdot (X_i - c) + \mu_3 \cdot \mathbf{1}[X_i \geq c] \cdot (X_i - c) + \omega_i$$

**LATE at Cutoff:**

$$\LARGE \tau_{FRD} = \frac{\mu_1}{\gamma_1}$$

This is the Wald estimator, interpreted as the LATE for compliers at the cutoff. Report the first-stage F-statistic alongside the Wald estimate.

### 2.3 Bandwidth Selection

**IK (Imbens & Kalyanaraman 2012):** Minimises the asymptotic mean squared error (MSE) of the RD estimator. Default in most software packages. Preferable when the goal is point estimation.

**CCT (Calonico, Cattaneo & Titiunik 2014):** Extends IK with robust bias-correction and modified variance estimation. Always report CCT robust confidence intervals alongside conventional ones.

**Cross-Validation (CV):** The "honest" approach: split data, optimise bandwidth to minimise out-of-sample prediction error. Useful for sensitivity analysis.

**Reporting Convention:** Report results for three bandwidths: (1) MSE-optimal (CCT), (2) half the optimal, (3) double the optimal. The main specification should use the CCT bandwidth with robust inference.

### 2.4 Polynomial Order

The consensus in the post-Gelman & Imbens (2019) literature is clear: **do not use global high-order polynomials.** Limit to local linear (p=1) or at most local quadratic (p=2).

| Polynomial | When to Use | When to Avoid |
|------------|-------------|---------------|
| Local linear (p=1) | Default — robust, interpretable, avoids Runge's phenomenon | When data clearly show curvature at cutoff |
| Local quadratic (p=2) | Curvature near cutoff, large bandwidth | Always check sensitivity to p=1 |
| Global cubic+ (p≥3) | **Never** — spurious precision, sensitivity to outliers | Gelman & Imbens (2019) show they produce misleading CIs |

### 2.5 McCrary (2008) Density Test

Test whether the density of the running variable is continuous at the cutoff — evidence of manipulation or endogenous sorting:

$$\LARGE H_0: \lim_{x \uparrow c} f(x) = \lim_{x \downarrow c} f(x)$$

Implement using the local polynomial density estimator (Cattaneo, Jansson & Ma 2020). Report the test statistic and p-value. A significant discontinuity suggests sorting around the threshold and invalidates the design.

**Remedies when McCrary fails:**
- Donut-hole RDD: drop observations in a window around the cutoff; check sensitivity to donut size
- Consider fuzzy RDD if sorting is partial
- Use the density discontinuity magnitude to bound treatment effects (Gerard, Rokkanen & Rothe 2020)

### 2.6 Donut-Hole RDD

When manipulation near the cutoff is suspected (e.g., earnings management around zero-earnings threshold), exclude a symmetric window $[-d, d]$ around the cutoff:

$$\LARGE \text{Estimate } \tau \text{ for } |X_i - c| \in [d, h]$$

Report results for $d \in \{0, 0.01\sigma_X, 0.02\sigma_X, 0.05\sigma_X\}$ to establish sensitivity.

### 2.7 Spatial RDD

When the running variable is geographic distance to a boundary:

$$\LARGE X_i = \text{signed distance to the geographic border}$$

Standard RDD procedures apply, but with two additional considerations:
- **Boundary segment fixed effects:** Include border-segment FE to control for unobserved heterogeneity along the border.
- **Conley standard errors:** Account for spatial correlation with distance-based kernel weighting.

### 2.8 RDD Implementation Checklist

- [ ] Plot the data: scatter of outcomes against the running variable, with local polynomial fits on each side
- [ ] Justify the running variable and cutoff exogeneity
- [ ] McCrary density test — report discontinuity estimate and p-value
- [ ] Covariate balance at cutoff: test whether predetermined covariates jump at the cutoff
- [ ] Report three bandwidths: CCT-optimal, half, double
- [ ] Report CCT robust confidence intervals alongside conventional ones
- [ ] Polynomial order sensitivity: p=1 (main), p=2 (robustness)
- [ ] Placebo cutoffs: estimate treatment effect at arbitrary non-cutoff values; all should be null
- [ ] Donut-hole RDD if McCrary test fails
- [ ] For fuzzy RDD: first-stage F-statistic and Stock-Yogo critical values

### 2.9 RDD Reporting Table Template

```
                                (1)          (2)          (3)
                             CCT-opt     Half-CCT     Double-CCT
                             b/w = h     b/w = h/2    b/w = 2h
                        -----------------------------------------
RD Estimate (τ)          0.087***      0.094**       0.082***
                          (0.029)       (0.038)       (0.025)
Robust CI                 [0.031,       [0.018,       [0.034,
                           0.143]        0.170]        0.130]

Bandwidth (h)              12.4          6.2           24.8
Effective N                 1,842         942          3,580

Polynomial order (p)         1             1             1
Kernel                   Triangular    Triangular    Triangular

McCrary test statistic     0.384
  p-value                 [0.701]
Robust bias-corrected       Y             Y             Y

Controls                    Y             Y             Y
Cutoff FE                   Y             Y             Y
------------------------------------------------------------------------
Notes: Robust bias-corrected standard errors in parentheses (CCT 2014).
95% robust confidence intervals in brackets. Main specification is column (1).
```

### 2.10 RDD Common Pitfalls & Remedies

| Pitfall | Detection | Remedy |
|---------|-----------|--------|
| McCrary test significant | Density plot shows heap at cutoff | Donut-hole RDD; fuzzy RDD; bounds analysis |
| Wide bandwidth | Results sensitive to bandwidth choice | Prefer CCT-optimal; report half and double |
| Global polynomial | Confidence intervals wider than the data range suggests | Use local linear only |
| Discrete running variable | Few mass points near cutoff | Use local randomisation inference; cluster SE at mass points |
| Few clusters / small N | Standard errors unreliable | Randomisation inference (Cattaneo, Frandsen & Titiunik 2015) |
| Compound treatment | Cutoff bundles multiple policy changes | Disentangle if possible; acknowledge limitation if not |

---

## 3. Instrumental Variables (IV)

### 3.1 Two-Stage Least Squares (2SLS)

**Structural Equation:**

$$\LARGE Y_i = \beta X_i + \gamma W_i + \varepsilon_i$$

**First Stage:**

$$\LARGE X_i = \pi Z_i + \delta W_i + v_i$$

**Second Stage:**

$$\LARGE Y_i = \beta \hat{X}_i + \gamma W_i + u_i$$

where $Z_i$ is the instrument (excluded from the structural equation), $X_i$ is the endogenous regressor, and $W_i$ are exogenous controls. Valid IV requires $Cov(Z, X) \neq 0$ (relevance) and $Cov(Z, \varepsilon) = 0$ (exclusion).

### 3.2 First-Stage Diagnostics

**Kleibergen-Paap F-statistic** (cluster-robust): The preferred diagnostic for instrument relevance. The rule of thumb $F > 10$ (Staiger & Stock 1997) corresponds to less than 10% of the worst-case bias relative to OLS.

**Stock-Yogo (2005) Critical Values:**

| Maximal IV Size (bias as % of OLS) | 5% Significance |
|-------------------------------------|-----------------|
| 10% | F > 16.38 (1 instrument) |
| 15% | F > 8.96 |
| 20% | F > 6.66 |
| 25% | F > 5.53 |

**Reporting Convention:** Report the Kleibergen-Paap rk Wald F-statistic and compare to the Stock-Yogo 10% maximal IV size critical value. State whether the null of weak instruments is rejected.

### 3.3 Weak-Instrument Robust Inference

When the first stage is weak, standard 2SLS inference is unreliable. Use these alternatives:

| Method | Key Property | When to Use |
|--------|-------------|-------------|
| **Anderson-Rubin (AR)** | Exact under homoskedasticity; tests structural coefficient directly | First robust check when F<10 |
| **LIML** | Median-unbiased; better finite-sample properties than 2SLS | F between 5 and 10 |
| **Conditional LR** (Moreira 2003) | Power-dominates AR when identified; robust when weak | Preferred when it converges |
| **Fuller-k estimator** | Small modification to LIML with better MSE | Alternative to LIML |
| **Confidence sets via AR** | Construct valid CIs without point identification | Report alongside conventional CIs |

Show that inference is qualitatively unchanged using at least one weak-instrument-robust method.

### 3.4 Overidentification (Hansen J-Test)

With $L$ instruments and $K$ endogenous variables ($L > K$), test the joint validity of the overidentifying restrictions:

$$\LARGE H_0: \text{All instruments are valid}$$

The Hansen J-statistic is distributed $\chi^2_{L-K}$ under the null. A significant J-statistic rejects instrument validity for at least one instrument — but cannot identify which one.

**Critical issue:** The J-test has low power against many alternatives. Passing the J-test is necessary but not sufficient for instrument validity. Never claim that the J-test "proves" validity — state that it "fails to reject the null of valid overidentifying restrictions."

### 3.5 "Plausibly Exogenous" Instruments (Conley, Hansen & Rossi 2012)

When the exclusion restriction is plausible but not exactly satisfied, use Conley et al. (2012) bounds to quantify sensitivity to violations.

**Relaxing the Exclusion Restriction:**

Allow $Cov(Z, \varepsilon) = \gamma$, where $\gamma$ measures the direct effect of the instrument on the outcome. The structural parameter is:

$$\LARGE \beta = \beta_{2SLS} - \frac{\gamma}{\pi}$$

where $\pi$ is the first-stage coefficient. By specifying a range of plausible $\gamma$ values (based on the observed reduced form and economic reasoning), construct bounds for $\beta$.

**Implementation Steps:**
1. Estimate $\pi$ from the first stage
2. Specify $\gamma \sim N(0, \sigma^2_\gamma)$ with $\sigma_\gamma$ calibrated to a fraction of the reduced-form effect
3. Report $\beta$ estimates and confidence intervals for increasingly conservative $\sigma_\gamma$ choices
4. Identify the $\sigma_\gamma$ at which the confidence interval includes zero (the "breakdown point")

### 3.6 IV Implementation Checklist

- [ ] Economic motivation for the instrument: explain the institutional source of variation
- [ ] Reduced-form graph: scatter plot of instrument vs. outcome, with fit line
- [ ] First-stage table: coefficient on Z, Kleibergen-Paap F, Stock-Yogo critical value
- [ ] Visual first stage: partial regression plot (X on Z, residualised with controls)
- [ ] Report OLS for comparison (acknowledge endogeneity bias direction)
- [ ] Report at least one weak-instrument-robust inference method
- [ ] For multiple instruments: Hansen J-test and overidentification discussion
- [ ] Sensitivity to exclusion restriction: Conley et al. (2012) bounds or plausibly exogenous approach
- [ ] Characterise the LATE population: who are compliers? What is the counterfactual for always/never-takers?

### 3.7 IV Reporting Table Template

```
                               OLS          2SLS          LIML        AR Conf.
                                (1)          (2)           (3)          Sets (4)
                        ---------------------------------------------------------
Endogenous Variable      -0.023        0.087***      0.091**       [0.031,
                          (0.015)       (0.031)       (0.036)       0.152]

First Stage — Instrument                 0.524***
                                         (0.048)
Kleibergen-Paap F-stat                   [118.4]
Stock-Yogo 10% critical val.              16.38
Hansen J-statistic                       [0.842]
  (p-value)                              (0.359)

Reduced Form — Instrument               0.046***
                                         (0.016)

Anderson-Rubin p-value                                              [0.003]

Controls                     Y            Y             Y             Y
Industry FE                  Y            Y             Y             Y
Year FE                      Y            Y             Y             Y
Observations              12,450       12,450        12,450        12,450
R-squared                  0.312        0.288         0.286          ---
------------------------------------------------------------------------
Notes: Standard errors clustered at firm level in parentheses.
Stock-Yogo critical values for 10% maximal IV size.
AR confidence sets are 95% Anderson-Rubin inversion sets.
```

### 3.8 IV Common Pitfalls & Remedies

| Pitfall | Detection | Remedy |
|---------|-----------|--------|
| Weak instrument (F<10) | KP F-stat < Stock-Yogo critical value | LIML; AR confidence sets; find stronger instrument |
| Exclusion violation | J-test significant; reduced form too large relative to first stage | Conley bounds; acknowledge limitation |
| Many weak instruments | Many Z, small F each | LIML (more robust than 2SLS); aggregate instruments |
| Heterogeneous effects | LATE vs. ATE discrepancy | Characterise compliers; discuss external validity |
| Invalid inference with few clusters | Standard errors too small | Wild bootstrap; robust (Bell & McCaffrey 2002) |
| "Story" instrument | Z is cleverly constructed but lacks economic mechanism | Pre-register; provide institutional detail |

---

## 4. Randomised Controlled Trials (RCTs)

### 4.1 Design and Power Analysis

**Minimum Detectable Effect (MDE):**

$$\LARGE MDE = (t_{\alpha/2} + t_{1-\kappa}) \cdot \sqrt{\frac{\sigma^2}{N} \cdot \frac{1}{P(1-P)}}$$

where $\alpha$ is the significance level, $1-\kappa$ is the desired power (typically 0.80), $\sigma^2$ is the outcome variance, $N$ is the total sample size, and $P$ is the treatment assignment probability. Pre-register the MDE and required sample size.

**Stratification:**

Randomise within strata defined by baseline characteristics to improve balance and precision. Include stratification fixed effects in the estimating equation:

$$\LARGE Y_i = \alpha_s + \tau \cdot T_i + \varepsilon_i$$

where $\alpha_s$ are stratum fixed effects. This reduces the minimum detectable effect by reducing residual variance.

### 4.2 Analysis with ANCOVA

Including baseline covariates in the regression improves precision without introducing bias (since treatment is randomly assigned):

$$\LARGE Y_i = \alpha + \tau \cdot T_i + \beta \cdot Y_{i,pre} + \gamma X_i + \varepsilon_i$$

The ANCOVA estimator has lower variance than the simple difference-in-means. Report both with and without covariates, noting that the specification with baseline controls is the preferred estimate.

### 4.3 Randomisation Inference (Fisher Exact)

Rather than relying on asymptotic approximations, compute exact p-values by simulating the null distribution of the test statistic under all possible treatment assignments (or a large random sample thereof).

**Steps:**
1. Compute the test statistic $\hat{\tau}$ from the actual treatment assignment
2. Randomly reassign treatment labels $B$ times (e.g., $B = 10{,}000$)
3. Compute the test statistic $\hat{\tau}_b$ for each reassignment
4. The randomisation-inference p-value is: $p = \frac{1}{B} \sum_{b=1}^B \mathbf{1}[|\hat{\tau}_b| \geq |\hat{\tau}|]$

Report randomisation-inference p-values alongside asymptotic ones, especially when the number of clusters is small.

### 4.4 Compliance and LATE

When compliance is imperfect, estimate the LATE using treatment assignment $Z_i$ as an instrument for actual treatment $D_i$:

$$\LARGE LATE = \frac{\mathbb{E}[Y_i \mid Z_i = 1] - \mathbb{E}[Y_i \mid Z_i = 0]}{\mathbb{E}[D_i \mid Z_i = 1] - \mathbb{E}[D_i \mid Z_i = 0]} = \frac{ITT}{FirstStage}$$

The ITT (intention-to-treat) preserves randomisation benefits and should always be reported first. The LATE is the treatment effect on compliers.

**Characterising Compliers:**
Report the proportion of compliers, always-takers, never-takers, and defiers (excluded by monotonicity). Characterise compliers by comparing their baseline characteristics to the full sample.

### 4.5 Attrition

**Lee (2009) Bounds:**

When outcome data are missing non-randomly, Lee bounds provide worst-case bounds on the treatment effect under monotonicity (treatment does not induce attrition in the opposite direction for opposite potential outcomes).

**Procedure:**
1. Calculate the differential attrition rate: $\Delta = \Pr(missing \mid T=1) - \Pr(missing \mid T=0)$
2. Trim the treatment group's outcome distribution by fraction $\Delta / \Pr(observed \mid T=1)$ from the top and bottom
3. The Lee bounds are the range of treatment effects obtained from trimming from the top vs. bottom
4. Report 95% confidence intervals for the bounds using Imbens & Manski (2004)

Always report: (a) differential attrition rate, (b) balance on observables for attriters vs. non-attriters, (c) Lee (2009) bounds.

### 4.6 Multiple Testing Corrections

When testing multiple outcomes or subgroups, control the family-wise error rate (FWER) or false discovery rate (FDR):

| Method | Controls | When to Use |
|--------|----------|-------------|
| **Romano-Wolf (2016)** | FWER | Primary outcomes (conservative, standard in RCTs) |
| **Benjamini-Hochberg (1995)** | FDR | Exploratory analyses; secondary outcomes |
| **Bonferroni** | FWER | Few independent tests (naive; avoid when possible) |
| **Westfall-Young** | FWER | When Romano-Wolf is unavailable |
| **Anderson (2008) index** | NA | Aggregate multiple outcomes into a single index |

Construct a Romano-Wolf stepdown procedure by resampling, and report both unadjusted and adjusted p-values in a single table.

### 4.7 RCT Implementation Checklist

- [ ] Pre-registration in AEA RCT Registry (or equivalent) before data collection
- [ ] Power analysis with MDE calculation and target sample size
- [ ] Randomisation protocol described in detail (method, stratification variables, unit)
- [ ] Balance table: test joint orthogonality of treatment and baseline covariates
- [ ] ITT as primary specification; LATE (via 2SLS) if imperfect compliance
- [ ] ANCOVA specification with baseline outcome as control (primary, but report difference-in-means too)
- [ ] Attrition analysis: differential rate, balance of attriters, Lee bounds
- [ ] Multiple testing: Romano-Wolf adjusted p-values for primary outcomes
- [ ] Heterogeneous treatment effects: pre-specified subgroup analysis with interaction terms
- [ ] Spillover checks: test whether control units near treated units are affected (SUTVA)
- [ ] Randomisation inference p-values for main specification

### 4.8 RCT Reporting Table Template

```
                              Diff-in      ITT with     LATE         Lee
                               Means       Covariates   (2SLS)      Bounds
                                (1)          (2)         (3)         (4)
                        -----------------------------------------------------
Treatment Effect          0.042**       0.038***     0.058***    [0.021,
                          (0.018)        (0.013)     (0.020)     0.062]

Controls                      N            Y            Y            Y
Stratum FE                    N            Y            Y            Y
Observed N                 3,842        3,842         3,842        3,842

First Stage (compliance)                              0.652***
                                                     (0.041)
Compliance rate (%)                                    78.4

Attrition rate: Treated      8.2%
Attrition rate: Control      7.9%
Diff. attrition (p-value)    0.3% [0.74]

Randomisation inf. p       [0.031]      [0.011]       [0.008]
Romano-Wolf adj. p         [0.048]      [0.023]       [0.015]
------------------------------------------------------------------------
Notes: Column 2 is preferred specification. Robust standard errors in
parentheses. Lee bounds at 95% confidence using Imbens & Manski (2004).
```

### 4.9 RCT Common Pitfalls & Remedies

| Pitfall | Detection | Remedy |
|---------|-----------|--------|
| Low power | MDE >> expected effect | Increase sample; add baseline controls; stratification |
| Differential attrition | Significant t-test on attrition rates | Lee bounds; bounding approach |
| SUTVA violation | Control outcomes correlated with treatment proximity | Measure spatial spillovers; cluster design |
| Hawthorne effects | Behaviour changes due to observation | Unobtrusive measurement; administrative data |
| Selective reporting | Disconnect between pre-registration and paper | Check pre-registration; report all pre-specified outcomes |
| Small number of clusters | Standard errors too small | Cluster-robust with wild bootstrap; randomisation inference |
| Non-compliance | ITT ≠ treatment effect | LATE via IV; always report ITT first |

---

## 5. Synthetic Control Method (SCM)

### 5.1 Standard SCM (Abadie, Diamond & Hainmueller 2010)

The synthetic control is a weighted average of control units designed to approximate the treated unit's pre-treatment outcome trajectory:

$$\LARGE Y_{1t} - \sum_{j=2}^{J+1} w_j^* Y_{jt}$$

**Weights selection:** Choose weights $w_j^*$ that minimise:

$$\LARGE \sum_{m=1}^k v_m (X_{1m} - \sum_{j=2}^{J+1} w_j X_{jm})^2$$

subject to $w_j \geq 0$ and $\sum w_j = 1$, where $X$ are pre-treatment predictors of the outcome and $v_m$ are predictor weights reflecting predictive power.

**Inference:** Use placebo tests — iteratively apply SCM to each control unit as if it were treated, constructing a distribution of placebo effects. Report the ratio of post-treatment RMSPE to pre-treatment RMSPE and the p-value from the placebo distribution.

### 5.2 Generalised SCM (Xu 2017)

Extends SCM to multiple treated units with an interactive fixed effects model:

$$\LARGE Y_{it} = \delta_{it} D_{it} + X_{it}'\beta + \lambda_i' f_t + \varepsilon_{it}$$

where $\lambda_i$ are unit-specific factor loadings and $f_t$ are time-varying common factors estimated from control units only. This provides individual treatment effects for each treated unit with parametric inference.

### 5.3 Matrix Completion (Athey, Bayati, Doudchenko, Imbens & Khosravi 2021)

Treats the untreated potential outcomes matrix as a low-rank matrix and uses nuclear norm regularisation to impute counterfactuals:

$$\LARGE \min_{\mathbf{L}} \frac{1}{|\mathcal{O}|} \sum_{(i,t) \in \mathcal{O}} (Y_{it} - L_{it})^2 + \lambda \|\mathbf{L}\|_*$$

where $\mathcal{O}$ is the set of observations with $D_{it}=0$, $L$ is the estimated low-rank matrix of counterfactual outcomes, and $\|\mathbf{L}\|_*$ is the nuclear norm. The treatment effect for each $(i,t)$ is $\hat{\tau}_{it} = Y_{it} - \hat{L}_{it}$. Inference via cross-validation or conformal methods.

### 5.4 SCM Implementation Checklist

- [ ] Justify donor pool: units not affected by the treatment or similar interventions
- [ ] Show pre-treatment fit: plot actual vs. synthetic outcomes for full pre-treatment period
- [ ] Report predictor balance: compare pre-treatment predictors between treated and synthetic
- [ ] Report weights: which control units contribute to the synthetic control?
- [ ] Placebo in space: apply SCM to each donor as if treated; report p-value
- [ ] Placebo in time: apply SCM to a pre-treatment pseudo-treatment date
- [ ] Leave-one-out robustness: re-estimate dropping each donor with $w_j > 0$ and the largest donor
- [ ] For multiple treated units: use generalised SCM or report average effects across units
- [ ] Report RMSPE ratio and inference based on the placebo distribution

### 5.5 SCM Common Pitfalls & Remedies

| Pitfall | Detection | Remedy |
|---------|-----------|--------|
| Poor pre-treatment fit | Large pre-treatment RMSPE | Expand predictor set; check for structural breaks |
| Overfitting | Weights concentrated on one or two donors | Ridge-augmented SCM; robustness to dropping top donor |
| No comparable donors | All control units differ systematically | Bound or partial identification; acknowledge limitations |
| Interference | Donor-pool units affected by treatment | Exclude potentially affected units from donor pool |
| Inference in small donor pool | Placebo distribution too sparse | Use parametric inference (Xu 2017) or conformal inference |

---

## 6. Event Studies (Dynamic Treatment Effects)

### 6.1 Dynamic DID / Event Study Specification

The general event study specification disentangles pre-treatment trends from dynamic treatment effects:

$$\LARGE Y_{it} = \alpha_i + \lambda_t + \sum_{k=-K}^{-2} \delta_k \cdot \mathbf{1}[t - E_i = k] + \sum_{k=0}^{L} \beta_k \cdot \mathbf{1}[t - E_i = k] + \varepsilon_{it}$$

where $E_i$ is the event (treatment) period for unit $i$. The omitted reference period is $k=-1$ (immediately before treatment). This specification is the standard for both classical event studies (e.g., stock returns around M&A announcements) and modern staggered DID applications.

### 6.2 Binning Endpoints

To avoid identification of individual coefficients from sparse data at the extremes of the event window:

$$\LARGE Y_{it} = \alpha_i + \lambda_t + \delta_{pre} \cdot B_{it}^{pre} + \sum_{k=-K}^{-2} \delta_k \cdot \mathbf{1}[t - E_i = k] + \sum_{k=0}^{L} \beta_k \cdot \mathbf{1}[t - E_i = k] + \beta_{post} \cdot B_{it}^{post} + \varepsilon_{it}$$

where $B_{it}^{pre} = \mathbf{1}[t - E_i \leq -K]$ captures all pre-periods before $-K$, and $B_{it}^{post} = \mathbf{1}[t - E_i \geq L]$ captures all post-periods after $L$. Choose $K$ and $L$ to ensure at least 5% of observations in each non-binned window.

### 6.3 Normalisation for Dynamic Effects

Cumulative dynamic effects:

$$\LARGE C_k = \sum_{j=0}^k \beta_j$$

These can be interpreted as the cumulative treatment effect up to period $k$. Report both the per-period effects $\beta_k$ and the cumulative effects $C_k$.

**Standardisation of Event Time:** When treatment occurs at different calendar times, normalise event time as $e_{it} = t - E_i$ and include calendar time fixed effects to absorb macro shocks.

### 6.4 Implementation Checklist

- [ ] Define the event precisely: what constitutes treatment onset? Is it staggered?
- [ ] Report the distribution of event-time observations across units and periods
- [ ] Plot raw means by event time, overlaid with the estimated path
- [ ] Bin endpoints with clear justification for bin choice
- [ ] Report joint test for zero pre-trends ($\delta_k = 0$ for all $k < 0$)
- [ ] Report both per-period and cumulative treatment effects
- [ ] For staggered events: use at least one robust estimator beyond TWFE
- [ ] Show sensitivity to the number of included leads and lags

### 6.5 Event Study Common Pitfalls & Remedies

| Pitfall | Detection | Remedy |
|---------|-----------|--------|
| Underspecified event window | Sparse bins at extremes; coefficients imprecise | Bin endpoints; extend window with more data |
| No never-treated units | All units treated; no pure control | Use not-yet-treated; shorter event window |
| Heterogeneous timing | Goodman-Bacon negative weights | CSDID, SA, BJS, or dCDH |
| Anticipation | Pre-trend coefficients diverge before event | Include explicit anticipation effects |
| Reporting only cumulative | Cumulative effects hide reversal patterns | Always report per-period effects alongside |

---

## 7. Cross-Sectional / Panel Regressions with Selection on Observables

### 7.1 Conditional Independence Assumption (CIA)

The identifying assumption:

$$\LARGE Y_i(0), Y_i(1) \perp T_i \mid X_i$$

Under CIA, the average treatment effect on the treated (ATT) is:

$$\LARGE ATT = \mathbb{E}[Y_i(1) - Y_i(0) \mid T_i = 1] = \mathbb{E}_X[\mathbb{E}[Y_i \mid T_i = 1, X_i] - \mathbb{E}[Y_i \mid T_i = 0, X_i] \mid T_i = 1]$$

### 7.2 Estimation Approaches

**Regression Adjustment:**

$$\LARGE Y_i = \tau T_i + X_i'\beta + \varepsilon_i$$

Include controls linearly. This is the baseline but is parametric in its dependence on $X$.

**Inverse Probability Weighting (IPW):**

Estimate propensity score $\hat{p}(X_i) = \Pr(T_i=1 \mid X_i)$ via logit/probit, then weight observations by $1/\hat{p}$ for treated and $1/(1-\hat{p})$ for controls. More robust than regression if the propensity model is correctly specified.

**Doubly Robust (DR):**

Combines regression adjustment with IPW. Consistent if either the outcome model or the propensity score model is correctly specified (but not necessarily both). This is the recommended default approach.

$$\LARGE \hat{\tau}_{DR} = \frac{1}{N} \sum_{i=1}^N \left[ \frac{T_i Y_i}{\hat{p}(X_i)} - \frac{T_i - \hat{p}(X_i)}{\hat{p}(X_i)} \hat{\mu}_1(X_i) \right] - \frac{1}{N} \sum_{i=1}^N \left[ \frac{(1-T_i) Y_i}{1-\hat{p}(X_i)} + \frac{T_i - \hat{p}(X_i)}{1-\hat{p}(X_i)} \hat{\mu}_0(X_i) \right]$$

where $\hat{\mu}_t(X_i)$ are the estimated outcome models for $t \in \{0, 1\}$.

**Matching Methods:**

| Method | Key Feature |
|--------|-------------|
| Nearest-neighbour | Match each treated to $M$ closest controls by propensity score |
| Coarsened exact matching (CEM) | Exact match on discretised covariates; bounds imbalance ex ante |
| Entropy balancing | Choose control weights to achieve exact balance on specified moments |
| Genetic matching | Algorithmic balance optimisation using genetic search |

**Entropy Balancing** (Hainmueller 2012): Find weights $w_i$ for control units that achieve exact balance on the first, second, and potentially higher moments of the covariate distribution.

### 7.3 Diagnostics

- **Standardised bias before and after matching:** $B = \frac{\bar{X}_T - \bar{X}_C}{\sqrt{(\sigma_T^2 + \sigma_C^2)/2}}$. Target: absolute standardised bias $< 0.1$ (10%) after matching.
- **Common support:** Ensure overlap in propensity score distributions. Trim observations outside common support.
- **Pseudo-$R^2$ from propensity score re-estimation:** Should be near zero after matching.
- **Rubin's B and R statistics:** $B < 25$ and $0.5 < R < 2$ indicate adequate balance.

### 7.4 Implementation Checklist

- [ ] Argue that selection occurs on observables (acknowledge the assumption explicitly)
- [ ] Show covariate balance before vs. after matching/weighting
- [ ] Report multiple estimators: regression, IPW, doubly robust, and matching
- [ ] Common support assessment: histogram of propensity scores by treatment status
- [ ] Rosenbaum bounds for sensitivity to unobserved confounding (see Robustness Framework)
- [ ] Oster (2019) delta for selection on unobservables (see Robustness Framework)

---

## 8. Reporting Standards Summary

### 8.1 The Standard Table Sequence for an Identification Section

1. **Table 1:** Summary statistics (by treatment/control or pre/post)
2. **Table 2:** Baseline balance / parallel trends evidence
3. **Table 3:** Main results — multiple specifications increasing in controls
4. **Table 4:** Robustness — alternative samples, measures, specifications
5. **Table 5:** Falsification / placebo tests
6. **Table 6:** Mechanisms or channels
7. **Table 7:** Heterogeneity or external validity

### 8.2 The "Honest" Econometrics Checklist (per Angrist & Pischke)

For any empirical paper claiming causal effects, the reader should be able to answer:
1. What is the counterfactual? (What would have happened in the absence of treatment?)
2. What is the source of identifying variation? (Why does treatment vary in a way uncorrelated with potential outcomes?)
3. What is the regression model and what does it control for?
4. What is the interpretation of the regression coefficient? (ATE, ATT, LATE, ITT?)
5. How do standard errors account for the design? (Clustering, spatial correlation, serial correlation?)
6. How would an omitted variable have to behave to overturn the result?

---

## References

- Abadie, A., Diamond, A., & Hainmueller, J. (2010). Synthetic control methods for comparative case studies. *JASA*, 105(490), 493-505.
- Athey, S., Bayati, M., Doudchenko, N., Imbens, G., & Khosravi, K. (2021). Matrix completion methods for causal panel data models. *JASA*, 116(536), 1716-1730.
- Borusyak, K., Jaravel, X., & Spiess, J. (2024). Revisiting event study designs: Robust and efficient estimation. *Review of Economic Studies*, 91(2), 812-840.
- Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200-230.
- Calonico, S., Cattaneo, M. D., & Titiunik, R. (2014). Robust nonparametric confidence intervals for regression-discontinuity designs. *Econometrica*, 82(6), 2295-2326.
- Cattaneo, M. D., Jansson, M., & Ma, X. (2020). Simple local polynomial density estimators. *JASA*, 115(531), 1449-1455.
- Conley, T. G., Hansen, C. B., & Rossi, P. E. (2012). Plausibly exogenous. *Review of Economics and Statistics*, 94(1), 260-272.
- de Chaisemartin, C., & D'Haultfoeuille, X. (2020). Two-way fixed effects estimators with heterogeneous treatment effects. *American Economic Review*, 110(9), 2964-2996.
- Gelman, A., & Imbens, G. (2019). Why high-order polynomials should not be used in regression discontinuity designs. *Journal of Business & Economic Statistics*, 37(3), 447-456.
- Goodman-Bacon, A. (2021). Difference-in-differences with variation in treatment timing. *Journal of Econometrics*, 225(2), 254-277.
- Hainmueller, J. (2012). Entropy balancing for causal effects. *Political Analysis*, 20(1), 25-46.
- Imbens, G., & Kalyanaraman, K. (2012). Optimal bandwidth choice for the regression discontinuity estimator. *Review of Economic Studies*, 79(3), 933-959.
- Lee, D. S. (2009). Training, wages, and sample selection: Estimating sharp bounds on treatment effects. *Review of Economic Studies*, 76(3), 1071-1102.
- McCrary, J. (2008). Manipulation of the running variable in the regression discontinuity design. *Journal of Econometrics*, 142(2), 698-714.
- Rambachan, A., & Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies*, 90(5), 2555-2591.
- Romano, J. P., & Wolf, M. (2016). Efficient computation of adjusted p-values for resampling-based stepdown multiple testing. *Journal of Econometrics*, 190(1), 62-74.
- Staiger, D., & Stock, J. H. (1997). Instrumental variables regression with weak instruments. *Econometrica*, 65(3), 557-586.
- Stock, J. H., & Yogo, M. (2005). Testing for weak instruments in linear IV regression. In *Identification and Inference for Econometric Models*.
- Sun, L., & Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics*, 225(2), 175-199.
- Xu, Y. (2017). Generalized synthetic control method. *Political Analysis*, 25(1), 57-76.
