# Field Experiments in Marketing Research

Field experiments are the gold standard for causal inference in marketing. Unlike quasi-experimental methods that rely on untestable assumptions, randomized field experiments provide the most credible identification by design. Marketing researchers run field experiments across a wide range of platforms and contexts, each with unique design and analysis considerations.

---

## 1. Experimental Design

### 1.1 Choosing the Randomization Unit

The randomization unit is the level at which treatment is randomly assigned. The choice has profound implications for statistical power, SUTVA compliance, and the generalizability of results.

| Unit | Pros | Cons | Marketing Application |
|------|------|------|----------------------|
| **Individual customer** | Maximum power; easy analysis | SUTVA violations common (social networks, shared households); difficult to isolate | Email campaigns, personalized offers |
| **Household** | Reduces within-unit SUTVA | Harder to define; may miss individual-level heterogeneity | Direct mail, household panel |
| **Store/Outlet** | Reduces interference; natural implementation | Requires many stores; lower power (effective N = stores) | In-store displays, pricing experiments |
| **DMA (media market)** | Eliminates ad spillover; natural for TV/radio | Very few units (210 DMAs); extreme power constraints | TV, radio, outdoor advertising |
| **Zip code / Census tract** | Good for digital + offline integration | Moderate SUTVA concerns at boundaries | Geotargeted digital ads |
| **Session / Cookie** | Easy to implement digitally | Cookie churn; cross-device contamination | Online A/B tests |
| **Time period** | Simple for operational experiments | Seasonality, trends; serial correlation | Store hours, staffing experiments |

**Decision Rule**:
> Randomize at the highest level where SUTVA is likely to be violated, subject to power constraints. If customers within the same store influence each other, randomize at the store level. If stores within the same DMA share customers, randomize at the DMA level.

**Reporting the Choice**:
> "We randomize at the store level because: (1) customers frequently visit multiple stores within the same chain, creating SUTVA violations at the customer level; (2) the treatment (in-store display) is naturally implemented at the store level; and (3) we have 200 stores, providing adequate power for detecting the expected effect size."

### 1.2 Stratification and Blocking

Stratification improves precision by ensuring balance on key prognostic covariates within each stratum.

**Stratification Variables** (sorted by importance):
1. Pre-treatment outcome measure (lagged sales, past click-through rate)
2. Geographic variables (region, urban/rural)
3. Size variables (store revenue, customer lifetime value)
4. Demographic composition of catchment area

**Implementation**:

1. **Pair matching**: Sort units by a prognostic score, create adjacent pairs, randomize within pair
2. **Stratified randomization**: Divide into S strata, randomize independently within each
3. **Brewer-Hayes re-randomization**: Randomize repeatedly until all strata satisfy balance criteria

**Analysis After Stratification**:
Always include stratum fixed effects in the regression specification:

$Y_{is} = \alpha_s + \tau D_i + \varepsilon_{is}$

where $\alpha_s$ are stratum fixed effects. Omitting stratum fixed effects yields conservative (upward-biased) standard errors.

**Reporting**:
> "We stratify stores into 8 blocks defined by quartiles of pre-experiment revenue and a metro/non-metro indicator. Within each block, stores are randomly assigned to treatment or control with equal probability. All analyses include block fixed effects."

### 1.3 Power Analysis

A power analysis determines the minimum sample size needed to detect a treatment effect of a given magnitude with specified probability.

**The Basic Formula** (two-sided test, equal allocation):

$N = \frac{2(Z_{1-\alpha/2} + Z_{1-\beta})^2 \sigma^2}{\tau^2}$

where:
- $\tau$ = minimum detectable effect (MDE)
- $\sigma^2$ = variance of the outcome
- $\alpha$ = significance level (typically 0.05)
- $1-\beta$ = power (typically 0.80)

**Adjusting for Clustering** (when randomization unit ≠ analysis unit):

$N_{eff} = \frac{N}{1 + (m-1)\rho}$

where $m$ is the average cluster size and $\rho$ is the intraclass correlation coefficient (ICC).

**Marketing-Specific Power Considerations**:
- **Ad experiments**: Effect sizes are typically small (0.5-5% lift). Power analyses must account for this.
- **Conversion rates**: When the outcome is binary (purchase/no purchase), use $\sigma^2 = p(1-p)$.
- **Skewed outcomes**: Revenue, spending, and usage are heavily skewed. Use log transformation or consider the coefficient of variation instead of standard deviation.
- **Multiple outcomes**: If testing multiple outcomes, adjust power for the multiple comparisons correction.

**Power Analysis Reporting Template**:
```
Table X: Power Analysis
─────────────────────────────────────────────
Parameter                          Value
─────────────────────────────────────────────
Minimum detectable effect (MDE)    5% lift
Significance level (alpha)         0.05
Power (1 - beta)                  0.80
Outcome SD (pre-experiment)        $42.30
ICC (intraclass correlation)       0.12
Average cluster size               250
Design effect                      30.88
Effective sample size required     428 clusters
Actual sample size                 500 clusters
Achievable MDE                    4.2% lift
─────────────────────────────────────────────
```

### 1.4 Pre-Registration

Pre-registration commits researchers to analysis plans before seeing outcomes, preventing p-hacking and specification searching.

**What to Pre-Register**:
1. Primary outcome variable(s) and exact definition
2. Secondary outcome variables (labeled as exploratory)
3. Treatment and control group definitions
4. Sample inclusion/exclusion criteria
5. Regression specification (including covariates, fixed effects)
6. Subgroup analyses (with directional hypotheses)
7. Multiple testing correction approach
8. Minimum detectable effect and power analysis

**Pre-Registration Platforms**:
- **AEA RCT Registry** (socialscienceregistry.org): Preferred for marketing; maintained by AEA
- **AsPredicted** (aspredicted.org): Lightweight, quick
- **OSF** (osf.io): Version-controlled, flexible; allows amendments
- **ClinicalTrials.gov**: Required for health-related marketing interventions

**Handling Deviations from Pre-Registration**:
- Label any analysis not in the pre-registration as "exploratory"
- Report all pre-registered analyses regardless of results
- If deviations are necessary (e.g., data quality issues), document and justify explicitly

**Reporting in Paper**:
> "This experiment was pre-registered at the AEA RCT Registry (AEARCTR-000XXXX). We report all pre-registered analyses and label post-hoc analyses as exploratory. The pre-registration specified [primary outcome] as the main dependent variable and [specification] as the primary model."

---

## 2. Analysis

### 2.1 Intent-to-Treat (ITT)

ITT estimates the effect of being **assigned** to treatment, regardless of whether the treatment was actually received. This is the most policy-relevant estimand and should always be the primary analysis.

**ITT Specification**:

$Y_i = \alpha + \tau D_i^{assign} + \beta X_i + \varepsilon_i$

where $D_i^{assign} = 1$ if unit $i$ was randomized to treatment.

**Why ITT is Primary**:
1. Preserves randomization (no selection on compliance)
2. Answers the policy question: "What happens if we try to treat everyone?"
3. Conservative: real-world implementation will never achieve 100% compliance

**Reporting**:
> "Our intent-to-treat estimate shows that assignment to the personalized email campaign increased purchase probability by 2.3 percentage points (SE = 0.4, p < 0.001). This is the causal effect of the firm's decision to send the campaign, accounting for the fact that 12% of assigned customers never opened the email."

### 2.2 Treatment-on-the-Treated (TOT) / LATE

When compliance is imperfect, TOT estimates the effect of treatment on those who actually receive it (compliers).

**IV Approach to TOT**:

First stage: $D_i^{receive} = \pi_0 + \pi_1 D_i^{assign} + \Pi X_i + \nu_i$
Second stage: $Y_i = \beta_0 + \tau_{TOT} \hat{D}_i^{receive} + \beta X_i + \varepsilon_i$

Since $D_i^{assign}$ is randomly assigned, it is a valid instrument for $D_i^{receive}$.

$\tau_{TOT} = \frac{\tau_{ITT}}{\hat{\pi}_1}$

**Complier Characteristics**:
Describe who complies with treatment assignment. This defines the population for whom the TOT applies.

**One-Sided Non-Compliance** (common in marketing):
When control units cannot receive treatment (only treatment group can be non-compliant), TOT is the same as LATE.

**Reporting**:
> "Compliance was imperfect: 78% of customers assigned to treatment opened the email within 7 days. Among compliers (those who opened the email because they were assigned to it), the treatment increased purchase probability by 3.0 percentage points (SE = 0.5, p < 0.001). We characterize compliers in Table X."

### 2.3 Heterogeneous Treatment Effects (HTE)

Marketing treatments rarely affect all customers equally. Understanding heterogeneity is central to targeting and personalization.

**Methods for HTE**:

1. **Subgroup analysis** (pre-registered):
   $Y_i = \alpha + \tau D_i + \gamma (D_i \times G_i) + \beta X_i + \varepsilon_i$
   where $G_i$ is a pre-treatment subgroup indicator.

2. **Causal forest** (Athey & Imbens, 2016; Wager & Athey, 2018):
   - Nonparametric estimation of conditional average treatment effects
   - Identifies which covariates drive treatment effect heterogeneity
   - Provides honest confidence intervals for HTEs

3. **Generic machine learning inference** (Chernozhukov et al., 2018):
   - Best linear predictor of treatment effects
   - Sorted group average treatment effects
   - Classification analysis (CLAN) of most and least affected units

4. **Bayesian Causal Forest** (Hahn, Murray & Carvalho, 2020):
   - Regularized approach with better finite-sample performance

**Reporting HTE**:
```
Table X: Heterogeneous Treatment Effects
──────────────────────────────────────────────────────
Subgroup                   ITT (SE)        p-value
──────────────────────────────────────────────────────
High past spenders        0.042 (0.008)   <0.001
Medium past spenders      0.018 (0.009)    0.045
Low past spenders         0.005 (0.010)    0.618
──────────────────────────────────────────────────────
p-value for interaction   0.003
──────────────────────────────────────────────────────
Notes: Subgroups defined by pre-experiment spending 
tertiles. p-value from F-test of interaction.
```

**Marketing Example**:
> "Using a causal forest (Athey & Imbens, 2016), we find that treatment effects vary strongly with pre-experiment engagement: the top quintile of customers by past email open rate has a treatment effect of +5.2pp (SE = 0.8), while the bottom quintile shows no significant effect (-0.3pp, SE = 0.7). This suggests that the campaign is most effective for already-engaged customers, consistent with a reinforcement rather than an acquisition mechanism."

### 2.4 Multiple Testing Correction

When evaluating treatment effects on multiple outcomes, subgroups, or over multiple time horizons, adjust for the inflated probability of false positives.

**The Problem**: If you test 20 outcomes at the 5% level, you expect 1 false positive even if there is no true effect anywhere.

**Correction Methods**:

| Method | Type | Formula / Approach | When to Use |
|--------|------|--------------------|-------------|
| **Bonferroni** | FWER | $p_{adj} = \min(m \times p, 1)$ | Primary confirmatory analysis |
| **Holm** | FWER | Step-down; $p_{(k)} \leq \alpha/(m-k+1)$ | Less conservative than Bonferroni |
| **Benjamini-Hochberg** | FDR | $p_{(k)} \leq k\alpha/m$ | Exploratory analysis with many outcomes |
| **Romano-Wolf** | FWER | Resampling-based; accounts for dependence | When outcomes are correlated |
| **List, Shaikh & Xu** | FDR | Bootstrap-based FDR control | Flexible, data-dependent thresholds |

**FWER vs. FDR**:
- **FWER** (family-wise error rate): probability of ANY false positive. Appropriate for confirmatory research.
- **FDR** (false discovery rate): expected proportion of false positives among rejections. Appropriate for discovery/exploratory research.

**Pre-Analysis Plan for Multiple Outcomes**:
1. Designate a **single primary outcome** (no correction needed)
2. Group secondary outcomes into **families** (e.g., purchase behavior, engagement, attitudes)
3. Apply correction within each family separately
4. Report both raw and adjusted p-values

**Reporting**:
> "We designate monthly purchase count as our primary outcome (pre-registered). All other outcomes are secondary and grouped into three families: engagement metrics (4 outcomes), spending metrics (3 outcomes), and attitudinal measures (5 outcomes). Within each family, we apply the Benjamini-Hochberg FDR correction. Both raw p-values and sharpened q-values are reported in Table X."

---

## 3. Reporting Standards

### 3.1 CONSORT Flow Diagram

The CONSORT (Consolidated Standards of Reporting Trials) flow diagram tracks all units through the experiment:

```
                     Assessed for eligibility
                     (n = N_total)
                              │
                     Excluded (n = N_excl)
                     • Not meeting criteria (n = n1)
                     • Declined (n = n2)
                     • Other reasons (n = n3)
                              │
                     Randomized (n = N_rand)
                              │
              ┌───────────────┴───────────────┐
              │                               │
     Allocated to treatment           Allocated to control
     (n = N_T)                        (n = N_C)
     • Received treatment (n = nT1)   • Received control (n = nC1)
     • Did not receive (n = nT2)      • Did not receive (n = nC2)
              │                               │
     Lost to follow-up (n = nT3)      Lost to follow-up (n = nC3)
              │                               │
     Analyzed (n = N_T_analyzed)      Analyzed (n = N_C_analyzed)
     • Excluded from analysis (nT4)   • Excluded from analysis (nC4)
```

**Marketing-Specific Adaptations**:
- For online experiments: include cookie/session churn, ad blocking, bot traffic
- For store experiments: include store closures, manager turnover during experiment
- For direct mail: include undeliverable addresses, opt-outs

### 3.2 Balance Table

The balance table compares pre-treatment characteristics across treatment and control groups to verify that randomization produced comparable groups.

**Template**:

```
Table X: Balance Table — Pre-Treatment Characteristics
─────────────────────────────────────────────────────────────────────
                              Treatment     Control     Std. Diff   p-value
                              (n = 500)    (n = 500)
─────────────────────────────────────────────────────────────────────
Demographics
  Age (mean)                   42.3         41.9        0.04       0.52
  Female (%)                   54.2         53.8        0.01       0.90
  Income ($000s)               68.5         67.2        0.06       0.41
  College degree (%)           38.1         39.4       -0.04       0.67

Pre-Experiment Behavior
  Past 3-month purchases       4.23         4.18        0.03       0.81
  Past 3-month spending ($)   187.42       184.91       0.02       0.85
  Tenure (months)              28.4         29.1       -0.03       0.72
  Email open rate (%)          22.3         21.8        0.05       0.59

Joint F-test p-value                                   0.74
─────────────────────────────────────────────────────────────────────
Notes: Standardized difference = (mean_T - mean_C) / pooled SD. 
Values < |0.1| indicate good balance. Joint F-test from regression 
of treatment indicator on all covariates.
```

**Balance Assessment Criteria**:
- **Standardized difference** < 0.1 (or 0.25 in small samples): acceptable balance
- **Joint F-test**: should NOT reject the null that all coefficients are zero
- If imbalance exists on a key prognostic covariate, include it in all subsequent analyses

### 3.3 Attrition Analysis

Attrition (units dropping out of the experiment after randomization) threatens internal validity if it is differential between treatment and control.

**Analysis**:
1. **Overall attrition rate**: What fraction of randomized units are missing outcome data?
2. **Differential attrition**: Is attrition rates different between treatment and control?
3. **Selective attrition**: Among attritors, do observable characteristics differ between treatment and control?

**Bounds for Attrition**:
- **Lee (2009) bounds**: Trim the distribution to bound the treatment effect under the assumption that treatment only affects sample selection in one direction
- **Manski bounds**: Worst-case bounds (no assumptions)

**Reporting**:
> "Overall attrition was 8.2% and did not differ significantly between treatment (7.8%) and control (8.6%; p = 0.41). Attriting units in both arms had slightly lower baseline spending ($162 vs. $191, p = 0.03), consistent with non-differential attrition. Lee (2009) bounds for the treatment effect under worst-case differential attrition are [0.018, 0.028], both above zero."

---

## 4. Platform-Specific Considerations

### 4.1 Online A/B Testing (Digital Platforms)

**Context**: Website optimization, email marketing, app features, recommendation algorithms, search ad copy.

**Unique Considerations**:

1. **Cookie/session churn**: Users delete cookies, switch devices, clear sessions. This creates measurement error in treatment assignment.
   - **Solution**: Use logged-in user IDs; measure compliance via server-side logging

2. **Network effects / social spillovers**: Users in treatment may influence users in control through social sharing, reviews, or word-of-mouth.
   - **Solution**: Cluster randomization (by social network cluster); estimate spillover effects explicitly

3. **Interference across experiments**: Multiple simultaneous experiments can interact.
   - **Solution**: Experiment management platforms; orthogonalization layers

4. **Peeking problem**: Stopping the experiment when results reach significance inflates Type I error.
   - **Solution**: Sequential testing with alpha-spending functions (O'Brien-Fleming, Pocock); pre-specified stopping rules

5. **Novelty effects**: Initial treatment effects may decay as the novelty wears off.
   - **Solution**: Run experiment long enough to observe steady-state effects; model time-varying treatment effects

6. **Multiple devices**: Users interact across phone, tablet, and desktop; randomization at device level misses true person-level effects.
   - **Solution**: Cross-device identity resolution; randomize at account/user level

**Specification for Online Experiments**:
$Y_{it} = \alpha + \tau D_i + \sum_{k=1}^K \beta_k \text{Week}_{kt} + \sum_{k=1}^K \gamma_k (D_i \times \text{Week}_{kt}) + \varepsilon_{it}$

This specification estimates week-specific treatment effects to capture novelty effects and learning.

**Reporting**:
> "Figure X plots the treatment effect by week since randomization. The effect peaks in week 1 (+4.5pp, p < 0.001), decays through week 3, and stabilizes at +2.1pp for weeks 4-8 (p = 0.002). The steady-state effect is our primary estimate, as it reflects the sustainable impact of the feature."

### 4.2 In-Store Experiments

**Context**: Product placement, shelf layout, price promotions, signage, sampling, store atmosphere.

**Design Considerations**:

1. **Store as the unit**: Individual customers visiting the same store see the same treatment; randomizing at the customer level would create interference.

2. **Carryover effects**: Store-level treatments may have effects that persist beyond the experiment period (inventory depletion, customer learning).
   - **Solution**: Washout periods between treatments; crossover designs

3. **Manager compliance**: Store managers may resist or modify treatments.
   - **Solution**: Blinding where possible; monitor compliance; compliance-adjusted analysis

4. **Seasonality and trends**: Store sales have strong weekly, monthly, and seasonal patterns.
   - **Solution**: Include time fixed effects; day-of-week and holiday controls

5. **Store heterogeneity**: Small number of stores with high variance.
   - **Solution**: Stratify on pre-experiment performance; use ANCOVA with pre-experiment outcome as covariate

**Specification**:
$Y_{st} = \alpha_s + \lambda_t + \tau D_{st} + \varepsilon_{st}$

where $\alpha_s$ are store fixed effects and $\lambda_t$ are time fixed effects.

**ANCOVA for Increased Precision**:
$Y_{s,post} = \alpha + \tau D_s + \beta Y_{s,pre} + \varepsilon_s$

Including the pre-experiment outcome as a covariate can dramatically increase power.

**Reporting**:
> "We randomized 200 grocery stores to treatment (endcap display) and control (no display) in matched pairs based on pre-experiment sales volume. The ANCOVA specification, controlling for pre-experiment weekly sales, yields an estimated treatment effect of $1,842 per week (SE = $412, p < 0.001). Using pre-experiment sales as a covariate reduced the standard error by 62% compared to the simple difference-in-means."

### 4.3 Direct Mail Experiments

**Context**: Catalogs, coupons, promotional offers, political advertising, fundraising.

**Design Considerations**:

1. **Address-level randomization**: Each household address is a unit; 100+ million US addresses provide massive potential sample sizes.

2. **Response rates**: Typically 0.5-5%. This means very large sample sizes are needed. A 0.1pp lift on a 1% baseline response rate requires millions of addresses for adequate power.

3. **Undeliverable addresses**: NCOA (National Change of Address) processing removes movers. Nixie (undeliverable) rate reduces effective sample size.

4. **SUTVA**: Household members share mail; neighbors may discuss mail pieces.
   - **Solution**: Randomize at the household level; test for spillovers at neighborhood level

5. **Long measurement horizons**: Effects may take weeks to materialize. Response curves should be plotted over time.

**Power Analysis for Low-Probability Events**:
$N = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2 [p_T(1-p_T) + p_C(1-p_C)]}{(p_T - p_C)^2}$

**Reporting**:
> "We mailed 2.4 million households, with 1.2M receiving the promotional catalog (treatment) and 1.2M receiving the standard catalog (control). The response rate was 2.8% in treatment vs. 2.5% in control, a 0.3pp lift (p < 0.001). With 2.4M addresses, we had 90% power to detect a 0.15pp lift."

### 4.4 Digital Advertising RCTs

**Context**: Display ads, social media ads, search ads, video ads, influencer campaigns.

**Design Considerations**:

1. **Ghost ads**: Show the control group a PSA (public service announcement) instead of the brand ad to equalize the ad-serving experience and control for ad exposure effects unrelated to the ad content.

2. **Intent-to-treat in ad experiments**: The ITT is "assigned to see the ad," not "saw the ad." Ad viewability, ad blocking, and scrolling past ads mean compliance is far below 100%.

3. **Ad stock / carryover effects**: Advertising effects persist beyond the immediate exposure period.
   - **Solution**: Measure effects over extended post-exposure windows (7, 14, 30 days)

4. **Frequency effects**: The number of exposures matters. Design experiments with multiple arms varying exposure frequency.

5. **Platform measurement vs. brand lift studies**: Platform-reported metrics (clicks, impressions) may not align with actual brand outcomes (sales, brand awareness). Run brand lift surveys or match to purchase data.

**Brand Lift Study Design**:
1. Randomly split the target audience into test (exposed to ad) and control (held back)
2. Survey both groups on brand metrics (awareness, consideration, purchase intent)
3. Lift = metric_test - metric_control
4. For statistical significance: use difference in proportions test with sample size weights

**Reporting**:
> "We ran a ghost-ad experiment on Meta with 2.5M users per arm. Users in the treatment arm were eligible to see our client's video ad; users in the control arm were eligible to see a PSA. The ITT estimate shows a 1.8pp increase in brand awareness (SE = 0.3pp, p < 0.001). Among the 62% of treatment users who actually viewed the ad (viewability > 50% for > 2 seconds), the TOT estimate suggests a 2.9pp increase."

---

## 5. Marketing-Specific Considerations

### 5.1 Ad Stock Effects

Advertising effects accumulate over time. A single exposure has a small effect; repeated exposures build "ad stock" that decays over time.

**Koyck Model** (distributed lag with geometric decay):
$Y_t = \alpha + \beta A_t + \lambda Y_{t-1} + \varepsilon_t$

where the long-run effect of advertising is $\beta / (1 - \lambda)$.

**Implications for Experiments**:
- Short experiments (1-2 weeks) may dramatically underestimate advertising effects
- Treatment effects should be reported at multiple horizons (immediate, 1-week, 1-month, 3-month)
- The decay rate $\lambda$ is itself a parameter of substantive interest

**Reporting**:
> "The estimated treatment effect grows from +1.2pp in the week of exposure to +3.5pp cumulative over the 4-week post-exposure period (p < 0.001), consistent with an ad stock model where each exposure has a small immediate effect that accumulates over time."

### 5.2 SUTVA Violations in Marketing Contexts

The Stable Unit Treatment Value Assumption (SUTVA) requires that a unit's outcome depends only on its own treatment assignment, not on the treatment assignment of other units. Marketing contexts are rich with potential SUTVA violations.

**Common SUTVA Violations in Marketing**:

| Violation | Example | Detection | Solution |
|-----------|---------|-----------|----------|
| **Social spillover** | Friend sees ad → recommends product to control user | Test for effects in control users connected to many treated users | Network cluster randomization |
| **Price spillover** | Treated store lowers price → control store loses sales | Compare control units near vs. far from treated units | Geographic buffer zones |
| **Inventory constraint** | Treatment increases demand → stockout → no effect measured | Monitor stockouts; check treatment effect timing | Additional supply during experiment |
| **Channel substitution** | Online promotion → less in-store purchasing | Measure both channels simultaneously | Unit = customer across all channels |
| **Platform learning** | Algorithm learns from treatment users and applies to all | Track algorithm changes; measure indirect effects | Platform-level randomization |
| **Competitive response** | Competitor responds to your price change | Monitor competitor actions during experiment | Larger randomization units (markets) |

**Estimating Spillover Effects**:
$Y_i = \alpha + \tau_1 D_i + \tau_2 \bar{D}_{-i} + \varepsilon_i$

where $\bar{D}_{-i}$ is the fraction of unit $i$'s neighbors assigned to treatment. $\tau_1$ is the direct effect and $\tau_2$ is the spillover effect.

**Reporting**:
> "We test for SUTVA violations by estimating the effect of neighboring stores' treatment status on control store outcomes. Control stores in DMAs with high treatment intensity (top quartile of neighboring treated stores) show no significant difference in sales relative to control stores in low-intensity DMAs (p = 0.67), supporting SUTVA at the store level."

### 5.3 Long-Term Effects Measurement

Many marketing interventions have effects that change (grow or decay) over time. Measuring only the immediate effect risks providing a misleading picture of the intervention's total impact.

**Approaches**:

1. **Extended observation period**: Continue measuring outcomes for 3-12 months post-experiment
2. **Time-varying treatment effects**: Model $\tau_t$ as a function of time since treatment
3. **Cohort analysis**: Track cohorts of users who entered the experiment at different times
4. **Surrogacy**: Identify short-term metrics that predict long-term outcomes

**The Long-Term Effects Problem**:
- Short-term lift in sales may cannibalize future sales (intertemporal substitution)
- Short-term lift may be zero, but the effect grows over time (learning, habit formation)
- Short-term lift may be positive, masking negative long-term effects (promotion addiction, reference price effects)

**Reporting**:
> "We track outcomes for 12 months post-experiment. The cumulative treatment effect on customer lifetime value (CLV) stabilizes at +$42.30 (SE = $5.10, p < 0.001) after 6 months, with no significant change between months 6-12. The month-1 effect (+$8.20) represents only 19% of the total long-term effect, underscoring the importance of extended measurement."

### 5.4 The Incrementality Problem

In marketing experiments, not all measured conversions are "incremental"—some would have happened anyway.

**Measuring Incrementality**:
$\text{Incremental conversions} = \text{Conversions}_{\text{exposed}} - \text{Conversions}_{\text{holdout}}$

**ROI calculation**:
$\text{ROI} = \frac{\text{Incremental profit} - \text{Campaign cost}}{\text{Campaign cost}}$

**Challenges**:
- **Last-click attribution dramatically overstates incremental effects**: Exposed users who would have purchased anyway are incorrectly credited to the campaign
- **Conversion lift underestimates value if customer quality changes**: If the campaign brings in higher-LTV customers, even a small conversion lift is valuable
- **Cross-channel effects**: Activity in one channel may cannibalize or complement another

**Reporting ROI**:
> "The campaign generated $1.42M in incremental revenue at a cost of $0.48M, yielding an ROI of 196%. Importantly, only 34% of the conversions observed in the treatment group were incremental; 66% would have occurred without the campaign. This highlights the danger of attributing all observed conversions to the campaign."

---

## 6. Experiment Reporting Checklist

- [ ] CONSORT-style flow diagram
- [ ] Balance table with standardized differences and joint F-test
- [ ] Power analysis (prospective or retrospective)
- [ ] Pre-registration information and any deviations
- [ ] ITT as primary analysis; TOT as secondary
- [ ] Treatment effect in absolute AND relative terms (e.g., +3.2pp AND +18% lift)
- [ ] Time-varying treatment effects (at least short-term AND cumulative)
- [ ] Heterogeneous treatment effects analysis (pre-registered subgroups)
- [ ] Multiple testing correction where applicable
- [ ] Attrition analysis with bounds
- [ ] SUTVA / spillover discussion with evidence
- [ ] Cost-benefit / ROI calculation
- [ ] Long-term effect measurement or acknowledgment of limitation
- [ ] External validity discussion: to what populations/settings do results generalize?

---

## References

- Athey, S., & Imbens, G. W. (2016). Recursive partitioning for heterogeneous causal effects. *PNAS*.
- Athey, S., & Imbens, G. W. (2017). The econometrics of randomized experiments. *Handbook of Economic Field Experiments*.
- Berman, R., & Israeli, A. (2022). The value of descriptive analytics: Evidence from online retailers. *Marketing Science*.
- Blake, T., Nosko, C., & Tadelis, S. (2015). Consumer heterogeneity and paid search effectiveness: A large-scale field experiment. *Econometrica*.
- Chernozhukov, V., Demirer, M., Duflo, E., & Fernandez-Val, I. (2018). Generic machine learning inference on heterogeneous treatment effects in randomized experiments. *NBER Working Paper*.
- Gerber, A. S., & Green, D. P. (2012). *Field Experiments: Design, Analysis, and Interpretation*. Norton.
- Hahn, P. R., Murray, J. S., & Carvalho, C. M. (2020). Bayesian regression tree models for causal inference. *JASA*.
- Lambrecht, A., & Tucker, C. (2013). When does retargeting work? Information specificity in online advertising. *JMR*.
- Lee, D. S. (2009). Training, wages, and sample selection: Estimating sharp bounds on treatment effects. *RES*.
- Lewis, R. A., & Rao, J. M. (2015). The unfavorable economics of measuring the returns to advertising. *QJE*.
- List, J. A., Shaikh, A. M., & Xu, Y. (2019). Multiple hypothesis testing in experimental economics. *Experimental Economics*.
- Sahni, N. S. (2015). Effect of temporal spacing between advertising exposures: Evidence from online field experiments. *QME*.
- Wager, S., & Athey, S. (2018). Estimation and inference of heterogeneous treatment effects using random forests. *JASA*.
