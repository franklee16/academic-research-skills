# Conjoint Analysis in Marketing Research

Conjoint analysis is the workhorse method for measuring consumer preferences and estimating willingness-to-pay (WTP) in marketing. From new product design to pricing optimization to market segmentation, conjoint experiments decompose overall product preferences into part-worth utilities for each attribute level. Marketing Science and JMR reviewers expect sophisticated designs, rigorous estimation, and thorough validation.

---

## 1. Design Types

### 1.1 Choice-Based Conjoint (CBC)

The standard approach: respondents choose among product profiles (including a "none" option) in multiple choice tasks.

**Task Structure**:
```
If you were shopping for a smartphone, which would you choose?

                    Option A      Option B      Option C
Brand               Apple         Samsung       Google
Screen Size         6.1"          6.7"          6.4"
Battery Life        20 hours      24 hours      18 hours
Price               $899          $799          $699
Camera              12MP          48MP          50MP
Storage             128GB         256GB         128GB

○ Option A    ○ Option B    ○ Option C    ○ None: I wouldn't choose any
```

**Utility Specification** (Random Utility Model):

$U_{ijt} = V_{ijt} + \varepsilon_{ijt} = \beta_i X_{jt} + \varepsilon_{ijt}$

where $i$ indexes respondents, $j$ indexes alternatives, $t$ indexes choice tasks, $X_{jt}$ is the vector of attribute levels for alternative $j$ in task $t$, and $\varepsilon_{ijt} \sim \text{Type I Extreme Value}$.

Under the logit assumption, the choice probability is:

$P_{ijt} = \frac{\exp(V_{ijt})}{\sum_{k \in C_t} \exp(V_{ikt})}$

**Number of Tasks**: Typically 12-20 choice tasks per respondent. More tasks improve estimation but increase respondent fatigue.

**Number of Alternatives per Task**: 2-4 product profiles plus an outside option.

**Number of Attributes**: 5-8 attributes is standard. More than 10 attributes dramatically increases cognitive load and degrades response quality.

**Number of Levels per Attribute**: 2-5 levels per attribute. Continuous attributes (price, size) can have more levels; categorical attributes (brand, color) should be kept manageable.

**Marketing Example**:
> "We design a CBC experiment with 6 attributes (brand, screen size, battery life, price, camera quality, storage) at 3-4 levels each, generating 16 choice tasks per respondent. Each task presents 3 product profiles and a 'none' option. The design is a D-efficient fractional factorial minimizing the D-error of the multinomial logit model."

### 1.2 Adaptive Choice-Based Conjoint (ACBC)

Extensions that improve efficiency by adapting the design to each respondent.

**Key ACBC Features**:

1. **Build-Your-Own (BYO)**: Respondent first configures their ideal product
2. **Screening**: Eliminate attribute levels that are "completely unacceptable"
3. **Choice tasks**: Standard CBC tasks but tailored to near-ideal products (more informative)

**Advantages**:
- Higher respondent engagement
- More efficient preference measurement (each choice is more informative)
- Handles larger numbers of attributes
- Identifies must-have features and deal-breakers

**Disadvantages**:
- Longer survey duration
- More complex analysis (BYO data must be integrated with choice data)
- Design is not fully orthogonal—potential for confounding

**When to Use ACBC**:
- Many attributes (10-20)
- Heterogeneous preferences with strong non-compensatory rules
- Need to identify "must-have" features for product design

**Marketing Example**:
> "Given the large number of smartphone features (12 attributes), we use ACBC. The BYO and screening stages identify each respondent's 'consideration set,' and subsequent choice tasks focus on trade-offs within that set. The ACBC reduces the D-error by 34% compared to an orthogonal CBC design of equivalent length."

### 1.3 Menu-Based Conjoint (MBC)

For choices where consumers select a **bundle** of items rather than a single product (e.g., subscription plans, meal combos, insurance coverage).

**Structure**: Each task presents a menu of available features. Respondents can select multiple features, with a total price constraint.

**Utility**: Extends the standard CBC to allow multiple selections:

$U_{ijt}(b) = \sum_{k \in b} \beta_{ik} + \gamma_i P(b) + \varepsilon_{ijt}$

where $b$ is a bundle of features and $P(b)$ is the total price.

**Marketing Example**:
> "We use MBC to study consumer preferences for streaming service bundles. Respondents select any combination of content types (sports, movies, news, kids) and quality levels (HD, 4K, number of screens), subject to a monthly price. The MBC reveals complementarities between content types that would be missed by a standard CBC design."

### 1.4 Incentive-Aligned Conjoint

Standard conjoint suffers from hypothetical bias: respondents may not make the same choices when real money is at stake.

**Incentive Alignment Approaches**:

1. **BDM mechanism** (Becker-DeGroot-Marschak): One choice task is randomly selected as binding. Respondent states WTP; a random price is drawn. If WTP > price, they buy at the random price.

2. **Real choice with random implementation**: One choice task is randomly selected. The chosen option is provided to the respondent (if feasible).

3. **Consequentiality script**: Inform respondents that their answers will influence actual product design decisions.

**Evidence**: Incentive-aligned conjoint reduces WTP estimates by 20-40% compared to hypothetical conjoint (Ding, Grewal & Liechty, 2005; Miller et al., 2011).

**When Incentive Alignment Matters**:
- New product forecasting where WTP estimates directly inform pricing
- High-stakes managerial decisions informed by conjoint results
- Products where hypothetical bias is known to be large (luxury goods, socially desirable products)

**Reporting**:
> "To mitigate hypothetical bias, we implement an incentive-aligned conjoint using the BDM mechanism. One of the 16 choice tasks is randomly selected as binding. For that task, the respondent participates in a real BDM auction: they state their maximum WTP for their chosen product, a random price is drawn, and if their WTP exceeds the random price, they purchase the product at that price. This is communicated to respondents before they begin the conjoint."

---

## 2. Experimental Design

### 2.1 Fractional Factorial Designs

Full factorial designs (all possible combinations of attribute levels) are infeasible for all but the simplest conjoints. A 4^5 design (5 attributes × 4 levels) generates 1,024 possible profiles.

**Fractional Factorial Approach**:
- Select a fraction of the full factorial that preserves orthogonality for main effects
- Typically, use resolution III or IV designs (main effects not confounded with each other)
- Resolution V designs also avoid confounding two-way interactions with main effects

**Design Principles**:
- **Orthogonality**: Attribute levels are uncorrelated across profiles (enables clean estimation)
- **Level balance**: Each level of each attribute appears equally often
- **Minimal overlap**: Avoid profiles where all alternatives have the same level of an attribute (provides no information about that attribute)
- **Utility balance**: Avoid profiles that are clearly dominated (all respondents choose the same alternative—provides no information)

### 2.2 D-Efficient Designs

Modern conjoint designs maximize D-efficiency rather than strict orthogonality.

**D-Efficiency Criterion**:
$\text{D-error} = |\Omega(\beta, X)|^{-1/P}$

where $\Omega$ is the asymptotic variance-covariance matrix of the parameter estimates, $X$ is the design matrix, and $P$ is the number of parameters. A D-efficient design minimizes the D-error.

**Why D-Efficiency Over Orthogonality**:
- Prior knowledge about parameters can improve design (Bayesian D-efficient)
- Non-linear models (multinomial logit) have design efficiency that depends on the parameter values
- D-efficient designs can be 20-40% more efficient than orthogonal designs of the same size

**Bayesian D-Efficient (DB-efficient)**:
Incorporate prior distributions on parameters (from pilot studies or theory):
$\text{DB-error} = \int |\Omega(\beta, X)|^{-1/P} \pi(\beta) d\beta$

**Implementation**:
- Software: Ngene (ChoiceMetrics), SAS (proc optex), R (idefix, support.CEs)
- Algorithm: Modified Fedorov, coordinate exchange, or random search

**Reporting**:
> "We generated a Bayesian D-efficient design using Ngene, with priors from a pilot study (n = 80). The design has a D-error of 0.042, compared to 0.068 for an orthogonal design of equivalent size—a 38% improvement in efficiency. Priors were assumed normally distributed with means from the pilot and standard deviations of 0.5 × mean to reflect moderate uncertainty."

### 2.3 Random Designs (Full Profile)

Some recent approaches use randomly generated profiles rather than designed profiles.

**When Random Designs are Appropriate**:
- Very large number of attributes or levels (designs become unwieldy)
- Continuous attributes (price, size) where any level in a range is possible
- When analysis will use machine learning methods that benefit from random variation

**Advantages**:
- Simple to implement (no complex design algorithm)
- No design confounding
- Compatible with any analysis method

**Considerations**:
- Less efficient than D-efficient designs for the same number of tasks
- May generate implausible or dominated profiles (should filter these)
- Requires more respondents to achieve equivalent precision

**Marketing Example**:
> "Given the 15 continuous and discrete attributes in our product space, we use a random design where each attribute level is drawn independently from its range in each choice task. We filter out implausible combinations (e.g., a luxury brand with the lowest price tier) and dominated alternatives. The random design yields unbiased demand estimates under mild conditions."

### 2.4 Number of Tasks and Respondent Fatigue

**Rules of Thumb**:
- Minimum tasks: $N_{tasks} \geq \frac{P}{A - 1 - N_{none}}$ where $P$ is parameters, $A$ is alternatives per task
- Typical range: 12-20 tasks
- Maximum before fatigue degrades quality: ~30 tasks

**Detecting Fatigue**:
1. **Response time**: Fatigue leads to faster choices (less deliberation)
2. **Attribute non-attendance**: Respondents ignore attributes in later tasks
3. **Scale factor**: The error variance increases in later tasks (respondents are noisier)
4. **Consistency checks**: Include a repeated task to measure test-retest reliability

**Addressing Fatigue**:
- Randomize task order across respondents
- Include attention checks (dominant alternatives, repeated tasks)
- Model the scale factor as a function of task position:

$U_{ijt} = \lambda_t (\beta_i X_{jt}) + \varepsilon_{ijt}$

where $\lambda_t$ captures the scale (inverse error variance) in task $t$.

**Reporting**:
> "We include 16 choice tasks per respondent and randomize task order. Response time analysis shows no significant decrease across tasks (mean response time 12.3s, trend p = 0.34). A repeated task (task 16 replicates task 1) yields 87% identical choices, indicating good reliability. We estimate a model with task-specific scale factors and find no degradation in response quality (likelihood ratio test: p = 0.28)."

---

## 3. Estimation Methods

### 3.1 Multinomial Logit (MNL)

The basic model assuming homogeneous preferences and IIA (independence of irrelevant alternatives).

**Likelihood**:
$\mathcal{L}(\beta) = \prod_i \prod_t \prod_{j \in C_t} P_{ijt}^{y_{ijt}}$

where $y_{ijt} = 1$ if respondent $i$ chose alternative $j$ in task $t$.

**Limitations**:
- IIA property: the ratio of choice probabilities between any two alternatives is independent of other alternatives (red bus / blue bus problem)
- Cannot capture respondent heterogeneity
- Cannot capture correlations in unobservables across alternatives

**When MNL is Acceptable**:
- Exploratory / pilot studies
- Simple designs with clearly differentiated alternatives
- When the purpose is descriptive, not predictive

### 3.2 Mixed Logit (Random Parameters Logit)

The mixed logit relaxes the IIA property and accommodates respondent heterogeneity by allowing parameters to vary across respondents.

**Specification**:
$U_{ijt} = \beta_i X_{jt} + \varepsilon_{ijt}$
$\beta_i \sim N(\bar{\beta}, \Sigma)$ or $\beta_i \sim \text{other distribution}$

**Key Features**:
- Any substitution pattern: mixed logit can approximate any random utility model (McFadden & Train, 2000)
- Estimated via maximum simulated likelihood
- Requires specification of which parameters are random and their distributions

**Distribution Choices**:
- **Normal**: Common for most attributes; allows both positive and negative preferences
- **Log-normal**: For parameters with a known sign (e.g., price coefficient should be negative for all respondents)
- **Triangular/Uniform**: Bounded distributions when extreme values are implausible
- **Johnson's SB**: Flexible bounded distribution
- **Discrete (latent class)**: See Section 3.3

**Number of Draws**: 500-1,000 Halton draws standard; more for publication-quality results. Halton draws outperform pseudo-random draws (fewer draws needed for the same precision).

**Reporting**:
> "We estimate a mixed logit model with normally distributed coefficients for all non-price attributes (to capture taste heterogeneity) and a log-normally distributed price coefficient (to ensure negative marginal utility of price for all respondents). We use 1,000 Halton draws for simulation. The significant standard deviations of the random coefficients (Table X) confirm substantial preference heterogeneity."

### 3.3 Hierarchical Bayes (HB) Multinomial Logit

The gold standard for conjoint estimation in marketing. HB combines prior distributions (upper level) with individual-level likelihoods (lower level) to obtain individual-level part-worth estimates.

**Model Hierarchy**:

**Upper Level (Population)**:
$\beta_i \sim N(\bar{\beta}, \Sigma)$

**Lower Level (Individual)**:
$P(y_i | \beta_i) = \prod_t \frac{\exp(X_{ij(i,t),t} \beta_i)}{\sum_k \exp(X_{ikt} \beta_i)}$

**Estimation via MCMC (Gibbs Sampling)**:

Step 1: Draw $\beta_i | \bar{\beta}, \Sigma$ using Metropolis-Hastings
Step 2: Draw $\bar{\beta} | \{\beta_i\}, \Sigma$ from multivariate normal
Step 3: Draw $\Sigma | \{\beta_i\}, \bar{\beta}$ from inverse Wishart

**Burn-in and Convergence**:
- Typical: 20,000-50,000 iterations with 10,000-20,000 burn-in
- Convergence diagnostics: Gelman-Rubin $\hat{R} < 1.1$, trace plots, effective sample size
- Keep every k-th draw for inference (thinning to reduce autocorrelation)

**Advantages of HB**:
- Individual-level part-worths (enables targeting and segmentation)
- Borrows strength across respondents (stable estimates even with limited data)
- Naturally handles heterogeneity
- Bayesian framework provides full posterior distributions for WTP

**Software**: Sawtooth Software (CBC/HB), R (bayesm, ChoiceModelR), Python (PyMC)

**Reporting**:
> "We estimate a hierarchical Bayes multinomial logit model using the `bayesm` package in R. The MCMC chain runs for 50,000 iterations, with the first 20,000 discarded as burn-in and every 10th draw retained for inference. Convergence is confirmed by Gelman-Rubin statistics (all $\hat{R} < 1.05$) and visual inspection of trace plots. We report posterior means and 95% credible intervals for population-level parameters (Table X) and use individual-level posterior means for WTP calculations and segmentation."

### 3.4 Latent Class (LC) Model

A finite mixture model that assigns respondents to a small number of discrete segments, each with its own preference vector.

**Specification**:
$P(y_i | \beta_1, \dots, \beta_S, \pi) = \sum_{s=1}^S \pi_s \prod_t \frac{\exp(X_{ij(i,t),t} \beta_s)}{\sum_k \exp(X_{ikt} \beta_s)}$

where $S$ is the number of latent classes and $\pi_s$ is the class membership probability.

**Choosing the Number of Classes**:
- **BIC** (Bayesian Information Criterion): Most commonly used; penalizes model complexity
- **CAIC** (Consistent AIC): More conservative
- **AIC3**: Less conservative; useful when BIC suggests too few classes
- **Entropy**: Measures class separation ($E \geq 0.7$ is desirable)

**Class Membership Covariates**:
$\pi_{is} = \frac{\exp(Z_i \gamma_s)}{\sum_{s'} \exp(Z_i \gamma_{s'})}$

Include demographics and other covariates to predict class membership.

**When LC is Preferred Over Mixed Logit**:
- Discrete segments exist a priori (different usage contexts, roles)
- Managerially relevant segmentation is the primary goal
- Preference distributions are multimodal (mixed logit assumes unimodal)

**Marketing Example**:
> "We estimate latent class models with 2-6 segments. BIC is minimized at S = 4 classes (BIC = 12,340; entropy = 0.82). Class 1 ('Brand Loyalists,' 28%) weights brand heavily; Class 2 ('Price Sensitive,' 34%) weights price most; Class 3 ('Feature Seekers,' 22%) weights camera and battery; Class 4 ('Bargain Hunters,' 16%) shows moderate sensitivity to all attributes. Membership in Class 2 is predicted by lower income and younger age."

---

## 4. Willingness-to-Pay (WTP) Calculation

### 4.1 WTP from Part-Worths

The marginal WTP for a change in attribute $k$ from level $l$ to level $l'$ is:

$WTP_{k, l \to l'} = -\frac{\beta_{kl'} - \beta_{kl}}{\beta_{price}}$

where $\beta_{kl}$ is the part-worth for level $l$ of attribute $k$, and $\beta_{price}$ is the price coefficient (usually coded linearly).

For continuous attributes coded linearly:
$WTP_k = -\frac{\beta_k}{\beta_{price}}$

### 4.2 Confidence Intervals for WTP

WTP is a ratio of estimated parameters, which is non-linear. Several methods exist for computing confidence intervals:

#### Delta Method

Linear approximation of the variance of the ratio:

$\text{Var}(WTP_k) \approx \frac{1}{\beta_{price}^2} \text{Var}(\beta_k) + \frac{\beta_k^2}{\beta_{price}^4} \text{Var}(\beta_{price}) - 2\frac{\beta_k}{\beta_{price}^3} \text{Cov}(\beta_k, \beta_{price})$

- Simple and fast
- Assumes WTP is approximately normally distributed
- **Can perform poorly when the price coefficient is imprecisely estimated** (common in small samples)
- Produces symmetric confidence intervals that can include negative WTP for attributes that are clearly valued positively

**When to Use**: Large samples where the price coefficient is well-estimated (t > 10)

#### Krinsky-Robb (Parametric Bootstrap)

1. Draw $R$ parameter vectors from $N(\hat{\beta}, \hat{\Sigma})$
2. For each draw $r$, compute $WTP^{(r)}_k = -\beta^{(r)}_k / \beta^{(r)}_{price}$
3. CI is the $(\alpha/2, 1-\alpha/2)$ quantiles of the empirical WTP distribution

- Accounts for the non-linear nature of the ratio
- Does not assume WTP is normally distributed
- **Does not handle finite sample bias**
- Standard method in marketing conjoint papers

#### Bayesian Posterior Intervals (for HB Models)

For HB models, WTP is computed at each MCMC draw, producing a posterior distribution:
$WTP_{ik}^{(d)} = -\beta_{ik}^{(d)} / \beta_{i,price}^{(d)}$

The 95% credible interval is the (2.5, 97.5) percentiles of the posterior distribution.

**Advantages**:
- Full distributional information
- Accounts for all sources of uncertainty simultaneously
- Can compute individual-level and population-level WTP distributions

**Reporting**:
> "We compute WTP using the Krinsky-Robb method with 10,000 draws from the asymptotic distribution of the mixed logit parameters. The 95% confidence intervals reflect both estimation uncertainty in the attribute coefficients and the price coefficient. Results are reported in Table X alongside Bayesian posterior intervals from the HB model."

### 4.3 WTP Reporting Template

```
Table X: Willingness-to-Pay Estimates ($)
────────────────────────────────────────────────────────────────────
Attribute Change              WTP   95% CI (KR)   95% CI (Delta)
────────────────────────────────────────────────────────────────────
Screen: 6.1" → 6.7"         $47.30  [32.10, 62.50]  [29.40, 65.20]
Battery: 18h → 24h          $38.20  [25.80, 50.60]  [23.90, 52.50]
Brand: Samsung → Apple      $124.50  [98.30, 150.70] [95.10, 153.90]
Camera: 12MP → 48MP         $82.10  [60.40, 103.80] [57.20, 107.00]
Storage: 128GB → 256GB      $31.60  [18.20, 45.00]  [15.30, 47.90]
────────────────────────────────────────────────────────────────────
Notes: WTP estimates from mixed logit model (1,000 Halton draws). 
95% confidence intervals computed using Krinsky-Robb (KR) with 
10,000 draws and Delta method. All WTP values in USD.
```

### 4.4 WTP for Non-Monetary Attributes

When price is not in the design, WTP cannot be computed in monetary terms. Instead, use:

1. **Relative attribute importance**: The range of part-worths for an attribute divided by the sum of ranges across all attributes

$\text{Importance}_k = \frac{\max_l \beta_{kl} - \min_l \beta_{kl}}{\sum_{k'} (\max_l \beta_{k'l} - \min_l \beta_{k'l})} \times 100\%$

2. **Willingness-to-trade**: How much of one attribute are consumers willing to give up for another?
   $-\beta_{k1} / \beta_{k2}$

**Reporting**:
> "Attribute importance is computed as the range of part-worths for each attribute relative to the total range across all attributes. Screen size accounts for 28% of relative importance, followed by brand (24%), price (19%), battery life (15%), and camera (14%)."

---

## 5. Validation

### 5.1 Holdout Prediction

Holdout tasks (not used in estimation) test the predictive accuracy of the estimated model.

**Design**: Include 2-4 holdout choice tasks per respondent that are NOT used in estimation.

**Metrics**:
1. **Hit rate**: Fraction of holdout choices correctly predicted
2. **Mean absolute error (MAE)**: Average absolute difference between predicted and actual choice shares
3. **Root mean squared error (RMSE)**: RMSE of predicted vs. actual choice shares
4. **First-choice hit rate** vs. **share-of-preference hit rate**

**Benchmarks**:
- Hit rate > 33% for 3-alternative tasks (better than random)
- Hit rate > 50% is good; > 60% is excellent
- MAE < 0.05 (5 percentage points) on choice share predictions

**Reporting**:
> "We reserved 3 of the 16 choice tasks as holdouts for out-of-sample validation. The HB model achieves a first-choice hit rate of 58.3% (random = 33.3%) and an MAE of 3.2 percentage points on predicted choice shares. The mixed logit achieves 52.1% hit rate (MAE = 4.7pp), and the MNL achieves 44.8% (MAE = 7.1pp), confirming the superiority of the HB model."

### 5.2 Face Validity

Attribute importances and WTP should align with intuition, theory, and prior research.

**Checks**:
1. **Sign**: Are the signs of coefficients as expected? (e.g., negative price, positive quality)
2. **Ordering**: Are higher quality levels preferred to lower ones? Is a well-known brand preferred to a generic?
3. **Magnitude**: Are WTP estimates within a plausible range? (e.g., WTP for brand should not exceed product price)
4. **Comparison to external benchmarks**: If market data exists, do conjoint-derived elasticities align with market-observed elasticities?

**Reporting**:
> "All attribute coefficients have the expected signs: utility increases with screen size, battery life, camera quality, and brand reputation; utility decreases with price. The ordering of brand preferences (Apple > Samsung > Google > Other) aligns with market share data. The own-price elasticity from the conjoint (-2.3) is comparable to the market-observed elasticity (-2.1) from scanner panel data, supporting external validity."

### 5.3 Attribute Non-Attendance (ANA)

Some respondents ignore certain attributes when making choices. This can bias aggregate estimates.

**Detection Methods**:
1. **Stated ANA**: Ask respondents directly which attributes they ignored
2. **Inferred ANA**: Use the variance of individual-level part-worths to infer which attributes had zero weight
3. **Model-based ANA**: Estimate an equality-constrained latent class model where some classes have zero coefficients for specific attributes

**Addressing ANA**:
- Remove respondents with high rates of stated ANA (or report sensitivity)
- Estimate ANA-corrected models that allow zero coefficients
- In HB models, a tight prior around zero can capture near-zero weights without explicit zero constraints

**Reporting**:
> "Stated attribute non-attendance was low: 4% of respondents reported ignoring battery life, 3% storage, and 1% or fewer for other attributes. Inferred ANA (coefficient of variation < 0.1) identified 6% likely non-attenders. Excluding these respondents does not change the substantive conclusions (Appendix Table A3)."

### 5.4 External Validation

The most demanding test: do conjoint predictions match real market outcomes?

**Approaches**:

1. **Market share validation**: Compare predicted choice shares to actual market shares
   - Requires an outside good to account for non-purchasers
   - Calibrate the scale parameter to match market-level price elasticity

2. **Purchase prediction**: After conjoint, observe actual purchases. Do part-worths predict who buys what?
   - Requires linking conjoint respondents to subsequent purchase data

3. **A/B test validation**: Run a field experiment varying an attribute. Does the conjoint predict the A/B test result?

**Reporting**:
> "We validate the conjoint externally using the firm's actual A/B test of a price change from $899 to $849. The conjoint predicted a 12.3% increase in choice share; the A/B test (n = 50,000 customers) showed an 11.8% increase (95% CI: [10.2%, 13.4%]). The difference between conjoint prediction and field experiment is not significant (p = 0.62), supporting the external validity of our conjoint estimates."

---

## 6. Reporting Standards

### 6.1 What Marketing Science and JMR Reviewers Expect

**Design Section** must include:
- [ ] Attribute selection justification (managerial interviews, prior literature, qualitative research)
- [ ] Number of tasks, alternatives per task, and presence of outside option
- [ ] Design type (fractional factorial, D-efficient, random) with efficiency metric
- [ ] Pilot study details for Bayesian priors (if DB-efficient design)
- [ ] Sample size justification (power analysis or rules of thumb)
- [ ] Respondent screening criteria (and excluded respondents count)
- [ ] Attention checks and results

**Estimation Section** must include:
- [ ] Model specification (which parameters are fixed vs. random; distributional assumptions)
- [ ] Estimation method with technical details (number of draws, burn-in, convergence diagnostics)
- [ ] Model selection criteria (BIC, AIC, log-likelihood)
- [ ] Comparison with simpler models (MNL, then mixed logit or LC)

**Results Section** must include:
- [ ] Table of parameter estimates with standard errors (or credible intervals)
- [ ] Attribute importance chart
- [ ] WTP table with confidence intervals (at least two methods)
- [ ] Holdout validation metrics
- [ ] Heterogeneity analysis (segment-level or distribution of WTP)

**Appendix** must include:
- [ ] Full attribute and level definitions (with visuals for complex levels)
- [ ] Example choice task (screenshot or detailed description)
- [ ] Survey instrument
- [ ] Estimation details (MCMC diagnostics, convergence plots)
- [ ] Robustness checks (alternative distributions, different number of classes, etc.)

### 6.2 Sample Size Guidelines

| Method | Minimum N | Recommended N | Per Subgroup |
|--------|-----------|---------------|--------------|
| MNL (pooled) | 150 | 300+ | N/A |
| Mixed Logit | 200 | 500+ | 150+ |
| HB | 200 | 400+ | 100+ |
| Latent Class | 300 | 500+ | 100+ per class |
| ACBC | 150 | 300+ | N/A |
| MBC | 200 | 400+ | N/A |

**Rules of Thumb** (from Orme, 2010):
$N \geq \frac{500 \times c}{t \times a}$

where $c$ = largest number of levels for any attribute, $t$ = number of tasks, $a$ = number of alternatives per task (excluding none).

### 6.3 Presentation of Results

**Parameter Table Template**:
```
Table X: Mixed Logit and HB Parameter Estimates
────────────────────────────────────────────────────────────────────
                        Mixed Logit              HB
                        Mean (SE)    SD (SE)     Post. Mean (SD)
────────────────────────────────────────────────────────────────────
Price (log-normal)       -3.42***     0.89***     -3.28 (0.72)
                         (0.34)       (0.12)

Brand (base = Other)
  Apple                   1.24***     0.45***      1.31 (0.38)
                         (0.18)       (0.08)
  Samsung                 0.87***     0.38***      0.92 (0.35)
                         (0.15)       (0.09)

Screen Size (cont.)       0.42***     0.21***      0.45 (0.18)
                         (0.08)       (0.05)

Battery Life (cont.)      0.31***     0.15**       0.33 (0.14)
                         (0.07)       (0.06)
────────────────────────────────────────────────────────────────────
Model Fit
  Log-likelihood        -18,234                  -17,891
  BIC                     36,892                   36,204
  Holdout hit rate        52.1%                    58.3%
────────────────────────────────────────────────────────────────────
Notes: Mixed logit with 1,000 Halton draws. HB with 50,000 iterations
(20,000 burn-in). *** p < 0.001, ** p < 0.01.
```

### 6.4 Common Mistakes in Conjoint Submissions

| Mistake | Frequency | How to Avoid |
|---------|-----------|--------------|
| No holdout validation | High | Always include 2-4 holdout tasks |
| Only MNL estimation | High | Always estimate at least mixed logit or HB |
| No WTP confidence intervals | Medium | Report both delta method and Krinsky-Robb |
| Unjustified number of classes | Medium | Report BIC/CAIC/AIC across multiple S |
| Overly complex designs | Medium | Keep attributes to 5-8; more is noise |
| Insufficient attention checks | Medium | Include dominant alternative and repeated task |
| No external validation discussion | Medium | Acknowledge limitation; compare to market data if possible |
| Hypothetical bias not addressed | Low | Discuss; consider incentive alignment |
| HB convergence not shown | Low | Report R-hat and trace plots in appendix |
| Attribute levels not clearly defined | Low | Show visual examples in appendix |

---

## 7. Published Marketing Examples

| Paper | Journal | Conjoint Type | Key Methodological Contribution |
|-------|---------|---------------|--------------------------------|
| Allenby & Ginter (1995) | MktSci | CBC + HB | Early application of HB to conjoint |
| Toubia et al. (2003) | MktSci | ACBC | Polyhedral adaptive questioning |
| Ding, Grewal & Liechty (2005) | JMR | Incentive-aligned CBC | BDM mechanism for incentive alignment |
| Netzer et al. (2008) | MktSci | ACBC + MBC | Adaptive self-explicated approach |
| Evgeniou, Pontil & Toubia (2007) | MktSci | CBC | Convex optimization for preference measurement |
| Howell et al. (2016) | JMR | Menu-based | Menu-based for complex choice environments |
| Dzyabura & Hauser (2019) | MktSci | General | Active machine learning for efficient questioning |

---

## References

- Allenby, G. M., & Rossi, P. E. (1998). Marketing models of consumer heterogeneity. *Journal of Econometrics*.
- Carson, R. T., & Louviere, J. J. (2011). A common nomenclature for stated preference elicitation approaches. *Environmental and Resource Economics*.
- Chapman, C. N., & Feit, E. M. (2019). *R for Marketing Research and Analytics* (2nd ed.). Springer. [Chapters on conjoint]
- Ding, M., Grewal, R., & Liechty, J. (2005). Incentive-aligned conjoint analysis. *JMR*.
- Eggers, F., & Sattler, H. (2011). Preference measurement with conjoint analysis: Overview and recent developments. *German Medical Science*.
- Hauser, J. R., & Rao, V. R. (2004). Conjoint analysis, related modeling, and applications. In *Advances in Marketing Research: Progress and Prospects*.
- Hensher, D. A., Rose, J. M., & Greene, W. H. (2015). *Applied Choice Analysis* (2nd ed.). Cambridge.
- Krinsky, I., & Robb, A. L. (1986). On approximating the statistical properties of elasticities. *REStat*.
- Louviere, J. J., Hensher, D. A., & Swait, J. D. (2000). *Stated Choice Methods: Analysis and Application*. Cambridge.
- McFadden, D., & Train, K. (2000). Mixed MNL models for discrete response. *Journal of Applied Econometrics*.
- Orme, B. K. (2010). *Getting Started with Conjoint Analysis* (2nd ed.). Research Publishers.
- Rao, V. R. (2014). *Applied Conjoint Analysis*. Springer.
- Rossi, P. E., Allenby, G. M., & McCulloch, R. (2005). *Bayesian Statistics and Marketing*. Wiley.
- Train, K. E. (2009). *Discrete Choice Methods with Simulation* (2nd ed.). Cambridge.
