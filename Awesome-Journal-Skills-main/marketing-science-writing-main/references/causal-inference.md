# Causal Inference in Marketing Research

Causal inference is the backbone of reduced-form empirical marketing papers. Unlike structural papers that identify parameters through model restrictions, reduced-form papers rely on quasi-experimental variation to estimate treatment effects. The credibility of the identification strategy is the **single most important determinant** of whether a paper gets past reviewers at JMR, Marketing Science, and JM.

---

## 1. Difference-in-Differences (DID)

### 1.1 The Standard 2x2 DID

The canonical two-period, two-group setup compares the change in outcome for a treated group to the change in outcome for a control group.

**Specification**:

$Y_{it} = \alpha + \beta \text{Post}_t + \gamma \text{Treat}_i + \delta (\text{Treat}_i \times \text{Post}_t) + \varepsilon_{it}$

Or in panel form with unit and time fixed effects:

$Y_{it} = \alpha_i + \lambda_t + \delta D_{it} + \varepsilon_{it}$

where $D_{it} = \text{Treat}_i \times \text{Post}_t$.

**Identification Assumption**: Parallel trends—in the absence of treatment, the average outcomes for treated and control units would have followed parallel paths.

**Checklist for Standard DID**:
- [ ] Visual event study plot showing pre-treatment trends (the most important figure in any DID paper)
- [ ] Formal test for pre-trend differences: regress outcome on treatment indicator interacted with leads
- [ ] At least 3-4 pre-treatment periods shown
- [ ] Control group composition described and justified
- [ ] Discussion of why parallel trends is plausible in this context
- [ ] Robustness to alternative control groups
- [ ] Standard errors clustered at the level of treatment assignment

**Common Pitfalls**:
1. **Using only 2 periods**: With only one pre and one post period, parallel trends is an assumption, not a testable claim. Show multiple pre-periods.
2. **Insufficient pre-trend discussion**: A flat pre-trend line with no institutional justification is unconvincing. Explain WHY the trends should be parallel.
3. **Wrong clustering level**: Clustering at too fine a level (e.g., individual when treatment is at the market level) dramatically inflates significance.
4. **Ignoring compositional changes**: If the composition of treatment and control groups changes over time, DID estimates confound treatment effects with compositional effects.
5. **Staggered adoption with TWFE**: See Section 1.2.

**Marketing-Specific Applications**:
- Effect of a new advertising campaign on sales, comparing DMAs that received the campaign to those that didn't
- Impact of a store entry by Walmart on incumbent retailer prices
- Effect of a privacy regulation (GDPR, CCPA) on digital ad effectiveness
- Response to a loyalty program introduction across customer segments

**Example**:
> "To estimate the causal effect of Facebook's introduction of video ads on advertiser outcomes, we compare the change in click-through rates for advertisers who adopted video ads (treated) to those who continued with static image ads (control), before and after the platform's video ad launch in Q2 2019."

### 1.2 Staggered DID: Callaway & Sant'Anna (2021)

When treatment is adopted at different times by different units, the standard two-way fixed effects (TWFE) estimator is biased. The TWFE estimator is a weighted average of all possible 2x2 comparisons, and some weights can be negative when already-treated units serve as controls for later-treated units (Goodman-Bacon, 2021).

**The Problem with TWFE Under Staggered Adoption**:

$\hat{\delta}^{TWFE} = \sum_k w_k \hat{\delta}_k$

where some weights $w_k$ are negative, producing biased estimates when treatment effects are heterogeneous over time.

**Callaway & Sant'Anna (2021) Solution**:

Define the group-time average treatment effect on the treated:

$ATT(g, t) = E[Y_t(g) - Y_t(0) | G_g = 1]$

where $g$ is the cohort first treated at time $g$, and $t$ is the calendar time.

Key aggregations:
1. **$ATT(g, t)$**: Cohort-specific treatment effects at each post-treatment period
2. **$\theta_{es}(e)$**: Event study aggregation, averaging $ATT(g, g+e)$ across cohorts observed at event time $e$
3. **$\theta_{sel}$**: Selective treatment timing: average of $ATT(g, t)$ for all $(g,t)$ with $t \geq g$
4. **$\theta_{bal}$**: Balanced panel aggregation, restricting to cohorts with complete data

**Specification** (using the `did` package in R or `csdid` in Stata):

```r
# R: Callaway & Sant'Anna
library(did)
att_gt <- att_gt(
  yname = "sales",
  tname = "week",
  idname = "store_id",
  gname = "first_treatment_week",
  data = df,
  est_method = "dr"  # doubly robust
)
agg_es <- aggte(att_gt, type = "dynamic")
ggdid(agg_es)  # event study plot
```

**Sun & Abraham (2021) Alternative**:

Estimates cohort-specific treatment effects using interactions of cohort dummies with relative time indicators, never using already-treated units as controls:

$Y_{it} = \alpha_i + \lambda_t + \sum_{g} \sum_{e \neq -1} \beta_{g,e} \cdot 1\{G_i = g\} \cdot 1\{t - g = e\} + \varepsilon_{it}$

with the last pre-treatment period ($e = -1$) as the reference category.

**Checklist for Staggered DID**:
- [ ] Show the timing of treatment adoption (figure showing when each unit is first treated)
- [ ] Report which estimator you use (CS, SA, BJS, or Gardner) and justify
- [ ] Present event study estimates with uniform confidence bands
- [ ] Report multiple aggregations: simple weighted average, event study, group-specific
- [ ] Discuss never-treated vs. not-yet-treated as control group choice
- [ ] Test for anticipation effects (are there pre-trend breaks at $t = g-1$?)
- [ ] Robustness to alternative estimators (report at least 2)

**Marketing Example**:
> "We study the staggered rollout of Amazon's one-day delivery across 50 metro areas from 2018-2021. Using Callaway & Sant'Anna (2021), we estimate group-time average treatment effects and aggregate to event studies. The event study reveals that one-day delivery increases order frequency by 12% within three months, with effects growing to 18% after twelve months."

### 1.3 Event Study Specification

The event study is the flexible DID estimator that visualizes treatment effect dynamics:

$Y_{it} = \alpha_i + \lambda_t + \sum_{k = -K, k \neq -1}^{L} \beta_k D_{it}^k + \varepsilon_{it}$

where $D_{it}^k = 1$ if unit $i$ is $k$ periods from treatment in period $t$. The period $k = -1$ is the omitted reference category.

**Reporting Standards for Event Study Plots**:
1. X-axis: relative time (negative = before treatment, 0 = treatment period, positive = after)
2. Y-axis: coefficient estimates with 95% confidence intervals
3. Vertical line at treatment time (t = 0 or t = -1)
4. Pre-trend coefficients should be close to zero and statistically insignificant
5. Post-treatment coefficients should show the dynamic treatment effect
6. Include both pointwise and simultaneous confidence bands

**Figure Caption Template**:
```
Figure X: Event Study Estimates of [Treatment] on [Outcome]
Notes: The figure plots coefficient estimates and 95% confidence intervals 
from the event study specification in Equation (Y). The dependent variable 
is [outcome]. The x-axis represents time relative to [treatment event], with 
period -1 serving as the reference category. Standard errors are clustered 
at the [level] level. The pre-treatment coefficients (k < 0) provide 
evidence on the parallel trends assumption.
```

### 1.4 Testing Parallel Trends

**Visual Test**:
- Plot raw means for treatment and control groups over time
- Normalize to zero at the last pre-treatment period
- Pre-treatment lines should be parallel (not necessarily overlapping)

**Formal Tests**:

1. **F-test of joint significance of pre-treatment leads**:
   $H_0: \beta_{-K} = \beta_{-K+1} = \dots = \beta_{-2} = 0$

2. **Linear pre-trend test**: Regress outcome on a linear time trend interacted with treatment status in the pre-period only. The interaction should be insignificant.

3. **Rambachan & Roth (2023)**: Instead of testing whether pre-trends are exactly zero, construct confidence sets that are robust to violations of parallel trends up to a specified magnitude $M$.

**Reporting**:
> "Figure X presents the event study estimates. The pre-treatment coefficients are individually and jointly insignificant (F = 1.23, p = 0.28), supporting the parallel trends assumption. Following Rambachan & Roth (2023), we construct robust confidence intervals allowing for linear trend deviations of up to M = 0.05 standard deviations per period; our results remain significant under these sensitivity bounds."

### 1.5 Heterogeneous Treatment Effects in DID

Modern DID methods can also estimate treatment effect heterogeneity:

**By pre-treatment covariates**:
$Y_{it} = \alpha_i + \lambda_t + \delta D_{it} + \eta (D_{it} \times Z_i) + \varepsilon_{it}$

**Quantile DID** (Callaway, Li & Oka, 2018): Estimates treatment effects at different quantiles of the outcome distribution.

**Marketing Application**:
> "We examine heterogeneous effects of a price promotion ban by pre-ban market concentration. The event study by tertile of HHI reveals that the ban had the largest effect on prices in highly concentrated markets (top tertile: +4.2%) and negligible effects in competitive markets (bottom tertile: +0.3%)."

---

## 2. Regression Discontinuity (RD)

### 2.1 Sharp RD

Treatment is a deterministic function of a running variable crossing a known threshold.

**Specification**:

$Y_i = \alpha + \tau D_i + f(X_i - c) + \varepsilon_i$

where $D_i = 1\{X_i \geq c\}$, $c$ is the cutoff, and $f(\cdot)$ is a flexible function of the centered running variable (usually local linear).

**Local Linear RD** (Calonico, Cattaneo & Titiunik, 2014):

Estimate $\tau$ using weighted local linear regression within bandwidth $h$:

$\min_{\alpha, \tau, \beta} \sum_{i} K\left(\frac{X_i - c}{h}\right) [Y_i - \alpha - \tau D_i - \beta (X_i - c) - \gamma D_i(X_i - c)]^2$

where $K(\cdot)$ is a kernel function (usually triangular or uniform).

**Bandwidth Selection**:
- **CCT optimal bandwidth** (Calonico, Cattaneo & Titiunik, 2014): Minimizes MSE of the RD point estimator. Use `rdrobust` in Stata or `rdrobust` in R.
- **CCT coverage error rate (CER) optimal bandwidth**: For robust confidence intervals.
- **Donut-hole RD**: Exclude observations immediately around the cutoff to address potential manipulation.

**Checklist for Sharp RD**:
- [ ] Graph of outcome vs. running variable with fitted local polynomials on each side
- [ ] McCrary (2008) test for manipulation of the running variable (density discontinuity at cutoff)
- [ ] Placebo tests at alternative cutoff values (where no treatment should occur)
- [ ] Balance tests on pre-determined covariates at the cutoff
- [ ] Robustness to polynomial order (local linear vs. local quadratic)
- [ ] Robustness to bandwidth choice (CCT optimal ± 50%)
- [ ] Sensitivity to donut-hole exclusion radius
- [ ] Standard errors using heteroskedasticity-robust nearest-neighbor variance estimator

**Marketing-Specific Applications**:
- Price thresholds as cutoffs: "Customers who spend ≥ $100 receive free shipping"
- Geographic boundaries: school district boundaries, media market borders
- Eligibility rules: credit score cutoffs for financing offers, age cutoffs for targeted ads
- Time-based cutoffs: fiscal quarter boundaries, campaign start dates

**Example**:
> "We exploit a sharp discontinuity in Amazon's free shipping policy: orders above $25 qualify for free shipping, while orders below do not. The running variable is the pre-shipping cart value. We estimate a local linear RD using the CCT optimal bandwidth and find that free shipping increases order completion rates by 14.5 percentage points at the threshold."

### 2.2 Fuzzy RD

Treatment probability changes discontinuously at the cutoff but not deterministically.

**Specification** (Two-stage approach within the RD framework):

First stage: $D_i = \alpha_1 + \gamma T_i + f_1(X_i - c) + \nu_i$
Second stage: $Y_i = \alpha_2 + \tau_{FRD} \hat{D}_i + f_2(X_i - c) + \eta_i$

where $T_i = 1\{X_i \geq c\}$ is the intent-to-treat indicator.

$\tau_{FRD} = \frac{\lim_{x \downarrow c} E[Y|X=x] - \lim_{x \uparrow c} E[Y|X=x]}{\lim_{x \downarrow c} E[D|X=x] - \lim_{x \uparrow c} E[D|X=x]}$

This is a local average treatment effect (LATE) for compliers at the cutoff.

**First-Stage Diagnostics**:
- Visual jump in treatment probability at the cutoff
- First-stage F-statistic (rule of thumb: F > 10, but in RD the visual jump matters more)

**Marketing Example**:
> "A credit card company offers a promotional APR to customers with FICO scores above 680, but not all eligible customers receive the offer (banks have discretion). The FICO score cutoff creates a fuzzy RD where the probability of receiving the promotional APR jumps from 0.15 to 0.62 at the cutoff. We estimate the LATE of receiving the promotional APR on subsequent spending."

### 2.3 McCrary Test (Density Test)

Tests for manipulation of the running variable at the cutoff.

**Specification**: A discontinuity in the density of the running variable at the cutoff suggests sorting or manipulation.

**Implementation**:
```r
# R
library(rddensity)
density_test <- rddensity(X = df$running_var, c = cutoff)
summary(density_test)
```

**Reporting**:
> "Figure X plots the density of the running variable around the cutoff. The McCrary (2008) test statistic is 0.23 (p = 0.82), failing to reject the null hypothesis of no density discontinuity. This suggests that individuals are not systematically manipulating their position relative to the cutoff."

### 2.4 Placebo Cutoffs

Test whether the estimated discontinuity is unique to the true cutoff by estimating the RD at alternative (placebo) cutoffs where no treatment occurs.

- Choose placebos at the 25th, 50th, and 75th percentiles of the running variable (on each side)
- Or: choose placebos at $c \pm k \times h$ for several values of $k$
- Present as a forest plot or distribution plot with the true cutoff estimate highlighted

**Reporting**:
> "We estimate our RD specification at 20 placebo cutoffs (10 on each side of the true cutoff, spaced by 0.5 standard deviations of the running variable). The placebo estimates center around zero with no systematic pattern, and only 1 out of 20 exceeds the magnitude of the true estimate. The true estimate lies at the 96th percentile of the placebo distribution."

### 2.5 Geographic RD

When the running variable is distance to a boundary (state border, DMA border, school district line).

**Specification**: Two-dimensional RD using distance to the border as the running variable, often with boundary fixed effects.

**Additional Considerations**:
- Geographic boundary fixed effects absorb unobserved heterogeneity along the border
- Segment the boundary into intervals and include segment fixed effects
- Spatially correlated standard errors (Conley standard errors)

**Marketing Example**:
> "We exploit state-level changes in alcohol advertising regulations using a geographic RD: stores within 5 miles of a state border serve as treatment (different regulation) and control (same regulation). The running variable is signed distance to the state border, with border segment fixed effects."

---

## 3. Instrumental Variables (IV)

### 3.1 Two-Stage Least Squares (2SLS)

**Specification**:

First stage: $X_i = \pi_0 + \pi_1 Z_i + \Pi W_i + \nu_i$
Second stage: $Y_i = \beta_0 + \beta_1 \hat{X}_i + B W_i + \varepsilon_i$

where $Z_i$ is the instrument, $X_i$ is the endogenous variable, and $W_i$ is a vector of controls.

The IV estimator: $\hat{\beta}_{IV} = (Z'X)^{-1}(Z'Y)$

**First-Stage Diagnostics (Crucial for Marketing Papers)**:

1. **First-stage F-statistic**: Stock & Yogo (2005) critical values. For a single endogenous variable, F > 10 is the traditional rule of thumb. For multiple endogenous variables, use the Cragg-Donald Wald F-statistic and compare to Stock-Yogo critical values.

2. **First-stage coefficient and economic interpretation**: Report the first-stage coefficient and interpret it economically. "A one standard deviation increase in the instrument changes the endogenous variable by X%, suggesting a strong economic relationship."

3. **Reduced form**: $Y_i = \gamma_0 + \gamma_1 Z_i + \Gamma W_i + u_i$. A statistically significant reduced form is necessary (but not sufficient) for a meaningful IV analysis.

4. **Limited information maximum likelihood (LIML)** as robustness when instruments are weak.

**Reporting Template (First Stage)**:
```
Table X: First-Stage Results
─────────────────────────────────────
Dependent Variable: Endogenous Var
─────────────────────────────────────
Instrument                0.342***
                         (0.041)
[Controls]                   Yes
Fixed Effects                Yes
─────────────────────────────────────
F-statistic (excl. IV)      69.4
R-squared                   0.712
Observations               45,230
─────────────────────────────────────
Notes: The instrument is [description]. 
Standard errors clustered at [level] in 
parentheses. The Kleibergen-Paap F-statistic 
exceeds the Stock-Yogo critical value (16.38 
for 10% maximal IV size).
```

### 3.2 IV Validity: The Excludability Problem

An instrument must satisfy:
1. **Relevance**: $Cov(Z, X) \neq 0$ (testable)
2. **Excludability**: $Cov(Z, \varepsilon) = 0$ (untestable, must be argued)
3. **Monotonicity**: The instrument affects all units in the same direction (for LATE interpretation)

**Strategies to Defend Excludability in Marketing**:

1. **Institutional knowledge**: Describe the institutional process that generates the instrument. Why would it be unrelated to unobserved determinants of the outcome?

2. **Placebo tests on outcomes that should not be affected**: Find outcomes that the instrument should NOT affect through any channel other than the endogenous variable.

3. **Zero first-stage for subsamples**: Show that the instrument has no effect on the endogenous variable for a subsample that, by institutional logic, should not be affected.

**Marketing Instrument Categories**:

| Instrument Type | Example | Common Concern |
|----------------|---------|----------------|
| **Cost shifters** | Input prices for advertised products | May affect demand directly through input quality |
| **Hausman instruments** | Prices in other markets (same product) | May be correlated through national demand shocks |
| **Distance/geography** | Distance to store, warehouse | Correlated with unobserved neighborhood characteristics |
| **Policy/regulation** | Tax changes, advertising bans | May reflect lobbying by industry (endogenous policy) |
| **Weather/natural** | Rainfall for agricultural commodity prices | May affect demand directly (rainy day shopping) |
| **Peer/network** | Ad exposure of friends/social connections | Peer effects may have direct effects on outcomes |

**Marketing Example**:
> "We instrument for a brand's advertising expenditure using the average advertising cost per GRP (Gross Rating Point) in the DMA, which varies due to local TV station ownership changes. The instrument is relevant (F = 87.3) because ad costs affect how much advertising a brand can afford. Excludability is supported by: (1) local TV station ownership is determined by FCC regulations unrelated to local demand for the advertised product; (2) the instrument does not predict changes in outcome in placebo tests on categories that do not advertise on TV; (3) the first-stage is zero in DMAs without TV advertising."

### 3.3 Plausibly Exogenous IV (Conley, Hansen & Rossi, 2012)

When the exclusion restriction may not hold exactly, the "plausibly exogenous" approach relaxes $Cov(Z, \varepsilon) = 0$ to $Cov(Z, \varepsilon) \approx 0$.

**Approach**:
- Specify a prior on the direct effect of the instrument on the outcome, $\gamma$: $Y = X\beta + Z\gamma + \varepsilon$
- Estimate $\beta$ conditional on a range of plausible values for $\gamma$
- Report union of confidence intervals across plausible $\gamma$ values

**Reporting**:
> "We use the Conley, Hansen & Rossi (2012) plausibly exogenous approach, allowing the instrument to have a direct effect on the outcome of up to 10% of the reduced-form estimate. Under this relaxation, the 95% confidence interval for the treatment effect remains bounded away from zero [-0.45, -0.18], supporting the robustness of our findings."

### 3.4 Heterogeneous Treatment Effects in IV

**LATE Interpretation** (Imbens & Angrist, 1994):
IV estimates the local average treatment effect for compliers—units whose treatment status changes with the instrument. It does NOT estimate the ATE unless treatment effects are constant.

**Marginal Treatment Effects (MTE)** (Heckman & Vytlacil, 2005):
Identify the treatment effect at every margin of the propensity score, allowing you to answer: "What is the treatment effect for those most (and least) likely to be treated?"

**Marketing Example**:
> "Our LATE interpretation implies that the estimated price elasticity captures the response of consumers who switch brands when relative prices change due to our cost-shifter instrument. This is precisely the margin of interest for antitrust analysis, which focuses on consumers at the margin of substitution."

---

## 4. Synthetic Control

### 4.1 Synthetic Control Method (Abadie, Diamond & Hainmueller, 2010)

For settings with a single treated unit and multiple control units, synthetic control constructs a weighted combination of control units to approximate the treated unit's pre-treatment outcome trajectory.

**Specification**:

Let $W = (w_2, \dots, w_{J+1})'$ be a vector of weights with $w_j \geq 0$ and $\sum_{j=2}^{J+1} w_j = 1$.

The synthetic control for unit 1 is: $\hat{Y}_{1t}^N = \sum_{j=2}^{J+1} w_j^* Y_{jt}$

The treatment effect at time $t$ is: $\hat{\tau}_{1t} = Y_{1t} - \hat{Y}_{1t}^N$

**Weight Selection**:
Weights are chosen to minimize the pre-treatment RMSE:
$W^* = \arg\min_{W} ||X_1 - X_0 W||$

where $X_1$ is the vector of pre-treatment predictors for the treated unit, and $X_0$ is the matrix for control units.

**Inference via Permutation**:
Since there is only one treated unit, standard errors cannot be computed conventionally. Instead:
1. Apply the synthetic control method to each control unit as if it were treated
2. Compute the ratio of post-treatment RMSE to pre-treatment RMSE for each placebo
3. The p-value is the fraction of placebos with a ratio at least as large as the treated unit's ratio

**Checklist for Synthetic Control**:
- [ ] Clearly define the treated unit and the treatment timing
- [ ] Show the donor pool composition (which units contribute to the synthetic control)
- [ ] Report the weights and which units receive positive weight
- [ ] Show pre-treatment fit (visual + RMSE)
- [ ] Present treatment effect trajectory (gap plot)
- [ ] Placebo in space (each control unit as placebo treatment)
- [ ] Placebo in time (treatment at different pre-treatment periods)
- [ ] Leave-one-out robustness (exclude each donor pool unit with positive weight)
- [ ] Sensitivity to the set of predictor variables

**Marketing-Specific Applications**:
- Effect of a marketing policy change in one country/state on sales
- Effect of a brand crisis on the affected brand's market share
- Impact of a major sponsorship deal (single event)
- Effect of a new product launch by a market leader on competitors

**Example**:
> "We use the synthetic control method to estimate the causal effect of Nike's 2018 'Dream Crazy' campaign featuring Colin Kaepernick on Nike's stock price. The donor pool consists of 25 apparel and footwear companies. The synthetic Nike is constructed with weights of 0.34 (Adidas), 0.28 (Under Armour), 0.19 (Lululemon), 0.12 (Puma), and 0.07 (Skechers). The campaign increased Nike's stock price by 5.2% within 30 days, with a placebo-in-space p-value of 0.043 (3 out of 25 placebos had larger effects)."

### 4.2 Generalized Synthetic Control (Xu, 2017)

Extends synthetic control to multiple treated units by combining the synthetic control framework with interactive fixed effects.

### 4.3 Synthetic Difference-in-Differences (Arkhangelsky et al., 2021)

Combines DID and synthetic control by using unit weights (like synthetic control) and time weights (like DID) to construct the counterfactual.

---

## 5. Matching Methods

### 5.1 Propensity Score Matching (PSM)

**Specification**:

1. Estimate the propensity score: $p(X_i) = P(D_i = 1 | X_i)$ using logit or probit
2. Match each treated unit to control units with similar propensity scores
3. Estimate ATE or ATT as the average difference in outcomes between matched pairs

**Matching Algorithms**:
- Nearest-neighbor matching (1:1, 1:k with caliper)
- Kernel matching (Epanechnikov, Gaussian)
- Stratification/blocking on the propensity score
- Radius/caliper matching

**Common Support**:
- Trim observations outside the common support region
- Present the propensity score distribution for treated and control units (Figure with overlaid histograms)

**Checklist for PSM**:
- [ ] Balance table: pre- and post-matching standardized differences for all covariates
- [ ] Propensity score distribution overlap plot
- [ ] Discussion of unobservable selection: "Matching only addresses selection on observables"
- [ ] Rosenbaum bounds for sensitivity to hidden bias
- [ ] Robustness to alternative matching algorithms
- [ ] Standard errors: Abadie-Imbens (2006) or bootstrapped

**Marketing-Specific Applications**:
- Comparing outcomes for loyalty program members vs. non-members
- Evaluating the effect of viewing a targeted ad vs. not viewing it
- Comparing retailers who adopted a new technology vs. those who didn't

**Example**:
> "We match Starbucks Rewards members to non-members on pre-program purchase frequency (30 days), average ticket size, store distance, and demographics using nearest-neighbor propensity score matching with a caliper of 0.05. Post-matching, all standardized differences are below 0.1 (well within the 0.25 threshold). The ATT estimate shows that Rewards membership increases monthly visits by 2.3 (SE = 0.4)."

### 5.2 Coarsened Exact Matching (CEM)

**Approach** (Iacus, King & Porro, 2012):
1. Temporarily coarsen each variable into substantively meaningful bins
2. Apply exact matching on the coarsened data
3. Retain only the matched observations in the original (uncoarsened) values
4. Estimate treatment effect on matched data

**Advantages over PSM**:
- No need for iterative balance checking
- Automatically bounds the imbalance ex ante
- Congenial with any estimator applied post-matching

**Reporting**:
> "Table X reports the L1 multivariate imbalance measure before and after CEM, dropping from 0.87 to 0.42, indicating substantial improvement in balance."

### 5.3 Entropy Balancing (Hainmueller, 2012)

A reweighting approach that calibrates control unit weights to match treatment group moments exactly.

**Approach**:
- Choose weights for control units such that the reweighted control group exactly matches the treatment group on pre-specified moments (mean, variance, skewness) of covariates
- Weights are chosen to minimize the entropy distance from uniform weights, subject to the moment constraints

**Advantages**:
- Achieves exact balance on specified moments
- No need for iterative balance checking
- Works as a preprocessing step for any subsequent analysis

**Marketing Example**:
> "We use entropy balancing to match the treatment (mobile app users) and control (non-users) groups on the first three moments of pre-adoption purchase frequency, basket size, and tenure. After reweighting, the treatment and control groups are identical on all target moments, and the adjusted t-test of the difference in post-adoption spending is valid without further parametric assumptions."

---

## 6. Additional Topics

### 6.1 Oster (2019) Bounds for Selection on Unobservables

When you cannot fully address endogeneity, Oster bounds provide a way to assess how strong selection on unobservables would need to be to eliminate your result.

**Approach**:
- Specify $R_{max}$: the R-squared from a hypothetical regression including both observables and unobservables (typically $R_{max} = \min\{1.3\bar{R}^2, 1\}$ where $\bar{R}^2$ is from the controlled regression)
- Specify $\delta$: the relative importance of unobservables to observables in determining treatment (typically $\delta = 1$)
- Compute the bias-adjusted coefficient: if the identified set excludes zero, the result is robust to selection on unobservables of equal importance to observables.

**Reporting**:
> "We compute Oster (2019) bounds for our main specification. Using $R_{max} = 1.3 \times R^2_{controls} = 0.52$ and $\delta = 1$, the bias-adjusted coefficient is $\beta^* = -0.34$ with an identified set of $[-0.41, -0.28]$. This set excludes zero, indicating our result is robust to selection on unobservables of up to equal importance as selection on observables."

### 6.2 Multiple Testing Correction

When testing multiple outcomes, subgroups, or specifications simultaneously, adjust for multiple comparisons.

**Methods** (in order of decreasing conservativeness):
1. **Bonferroni**: $p_{adj} = \min(m \times p, 1)$ where $m$ is the number of tests
2. **Holm step-down**: Less conservative; sequentially rejects
3. **Benjamini-Hochberg**: Controls the false discovery rate (FDR), preferred for exploratory analyses
4. **Romano-Wolf**: Resampling-based; accounts for dependence across outcomes

**Reporting**:
> "We report both unadjusted p-values and sharpened q-values (Benjamini-Hochberg FDR correction) across our 12 outcome variables. All 10 significant findings survive FDR correction at the 5% level."

### 6.3 Conley Standard Errors for Spatial Data

When treatment is assigned geographically and outcomes are spatially correlated:

$Cov(\varepsilon_i, \varepsilon_j) \neq 0$ when $dist(i,j) \leq d_{max}$

Use Conley (1999) standard errors with a specified distance cutoff.

**Reporting**:
> "We compute Conley (1999) spatial HAC standard errors assuming correlation within 50km. Results are robust to distance cutoffs of 25km, 75km, and 100km."

---

## 7. Universal Checklist for Causal Inference Papers

- [ ] **Identification narrative**: Why is this a quasi-experiment? What is the source of exogenous variation?
- [ ] **Visual evidence**: Event study plot (DID), RD plot, IV first-stage plot, synthetic control gap plot
- [ ] **Balance table**: Treatment and control on pre-treatment covariates
- [ ] **First-stage / relevance**: F > 10 (IV), visual jump (RD), parallel pre-trends (DID)
- [ ] **Placebo/falsification**: Different time, different place, different outcome, different cutoff
- [ ] **Robustness**: Alternative samples, measures, specifications, estimators, bandwidths
- [ ] **Economic significance**: Effect size relative to mean, not just statistical significance
- [ ] **Threats to identification**: Explicitly discussed, not hidden
- [ ] **Oster bounds / sensitivity**: Selection on unobservables analysis
- [ ] **Standard errors**: Clustered at the correct level; justify clustering structure
- [ ] **Multiple testing**: Corrected when testing multiple outcomes/specifications
- [ ] **Replication**: Data and code availability statement

---

## 8. Published Marketing Examples by Method

| Method | Paper | Journal | Application |
|--------|-------|---------|-------------|
| **DID** | Datta, Ailawadi & van Heerde (2017) | JM | How advertising affects brand switching |
| **Staggered DID** | Seiler & Yao (2017) | MktSci | Impact of online reviews on demand |
| **RD** | Busse et al. (2010) | MktSci | Effect of car price on purchase |
| **IV** | Bronnenberg, Dubé & Gentzkow (2012) | MktSci | Evolution of brand share differences |
| **Synthetic Control** | Tirunillai & Tellis (2017) | JMR | Effect of Super Bowl ads on stock prices |
| **PSM** | Danaher et al. (2020) | JMR | Advertising effectiveness across channels |
| **Entropy Balancing** | Habel et al. (2021) | JM | Salesperson social media use effects |

---

## References

- Abadie, A., Diamond, A., & Hainmueller, J. (2010). Synthetic control methods for comparative case studies. *JASA*.
- Callaway, B., & Sant'Anna, P. H. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*.
- Calonico, S., Cattaneo, M. D., & Titiunik, R. (2014). Robust nonparametric confidence intervals for RD designs. *Econometrica*.
- Conley, T. G., Hansen, C. B., & Rossi, P. E. (2012). Plausibly exogenous. *REStat*.
- Hainmueller, J. (2012). Entropy balancing for causal effects. *Political Analysis*.
- Iacus, S. M., King, G., & Porro, G. (2012). Causal inference without balance checking: CEM. *Political Analysis*.
- McCrary, J. (2008). Manipulation of the running variable in the RD design. *Journal of Econometrics*.
- Oster, E. (2019). Unobservable selection and coefficient stability. *JBES*.
- Rambachan, A., & Roth, J. (2023). A more credible approach to parallel trends. *RES*.
- Sun, L., & Abraham, S. (2021). Estimating dynamic treatment effects in event studies. *Journal of Econometrics*.
