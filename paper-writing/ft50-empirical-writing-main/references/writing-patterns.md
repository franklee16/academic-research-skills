# Writing Patterns for FT50 Empirical Papers

This reference describes seven core writing patterns that distinguish successful FT50 empirical papers from those that are rejected or ignored. These patterns are derived from a systematic analysis of published papers across finance, accounting, management, marketing, operations, and economics. Each pattern addresses a specific rhetorical challenge that empirical researchers face when communicating complex evidence to sophisticated but sceptical readers.

---

## Pattern 1: The Motivating Puzzle

### 1.1 Purpose

The Motivating Puzzle pattern establishes *why the reader should care* about the paper before the reader has seen a single regression table. It creates intellectual tension that the rest of the paper resolves. Without this tension, even technically flawless empirical work feels flat -- the reader's response is "so what?"

### 1.2 The Structure

The Motivating Puzzle has three components that appear in the first 3-5 paragraphs of the introduction:

**Component 1: The Established View**

State what the existing literature, theory, or conventional wisdom says about the phenomenon. Be precise -- reference specific theories, stylised facts, or canonical results. The established view must be genuinely held, not a straw man.

**Component 2: The Anomaly or Tension**

Present evidence -- descriptive statistics, a figure, a natural experiment, or a simple cross-tabulation -- that contradicts or complicates the established view. This evidence should be simple enough that the reader can understand it without specialised knowledge. The best puzzles are visible in a single graph.

**Component 3: The Resolution (Preview)**

Explain in broad terms how your analysis resolves the puzzle. Do not give away all the results -- give enough that the reader wants to continue. The resolution should be surprising enough to be interesting but plausible enough to be credible.

### 1.3 Varieties of Motivating Puzzles

| Puzzle Type | Description | Example |
|-------------|-------------|---------|
| **Empirical contradiction of theory** | A well-established theoretical prediction fails in the data | "Finance theory predicts that diversification reduces firm value. Yet diversified firms trade at a premium in emerging markets." |
| **Conflicting empirical findings** | Two or more prior papers find opposite effects | "Prior work finds that CEO pay is negatively related to future performance, while other work finds a positive relation." |
| **Policy or practice paradox** | A widely adopted policy or practice seems to produce the opposite of its intended effect | "SOX was designed to improve financial reporting quality. Yet restatements and enforcement actions *increased* in the five years after passage." |
| **Cross-sectional surprise** | An effect is large in one setting but absent in a seemingly similar one | "The gender pay gap is well-documented in large firms. In small, privately held firms, we find no gap -- and in some specifications, women earn more." |
| **Temporal discontinuity** | A long-standing relationship changes abruptly | "For forty years, IPO underpricing averaged 7%. Since 2010, it has averaged 16%. What changed?" |

### 1.4 The Motivating Figure

A well-constructed figure in the first three pages of the paper is one of the most effective tools for establishing a puzzle. The ideal motivating figure has these properties:

- **Simple:** One or two data series. No more than four. The reader should understand it in 10 seconds.
- **Striking:** A clear pattern -- a trend reversal, a level shift, a divergence -- that is visually obvious.
- **Unexplained:** The figure creates a question that the existing literature cannot answer.
- **Anchored in the paper's data:** The figure should use the same data source as the main analysis. It is the reader's first exposure to the data and establishes credibility.

**Components of an effective motivating figure:**
1. Clear labelling of axes with units
2. A title that describes the pattern, not just the variables
3. A source note stating the data source and sample period
4. Visual emphasis on the anomalous pattern (shaded region, vertical line, or contrasting annotation)
5. Error bands or confidence intervals if showing means

### 1.5 Example Narrative

A paper on the effect of hedge fund activism on corporate innovation:

> *A central premise of corporate governance research is that shareholder monitoring improves managerial decision-making. Activist hedge funds, in particular, are credited with reducing agency costs by pressuring managers to cut wasteful spending, divest underperforming assets, and return capital to shareholders (Brav et al., 2008; Bebchuk et al., 2015).
>
> Yet there is a tension in this narrative. The same mechanisms that discipline managerial spending may also discourage long-term investments that require patience and tolerance for early failure. Innovation -- measured by R&D spending and patent output -- is the prototypical long-term investment. If activists shorten managerial horizons, we should observe a decline in innovation at targeted firms.
>
> Figure 1 presents the first systematic evidence on this question. It plots the patenting activity of firms targeted by activist hedge funds against a matched sample of non-targeted firms. In the three years before intervention, targeted and control firms follow parallel trends in patent output. In the three years after intervention, patent output at targeted firms falls by 18% relative to the control group -- a decline that is both statistically and economically significant.
>
> This pattern poses a puzzle: if shareholder activism reduces agency costs, why does innovation -- a value-creating activity -- decline? Our paper resolves this puzzle by showing that the decline is concentrated in exploratory innovation (new technology classes), while exploitative innovation (refinements of existing technologies) is unaffected. Activism does not harm all innovation -- it shifts the composition of innovation toward lower-risk, shorter-horizon projects. This finding reconciles the pro-monitoring and anti-innovation views of activism and has implications for how institutional investors evaluate activist campaigns.*

---

## Pattern 2: The Institutional Detail

### 2.1 Purpose

The Institutional Detail pattern makes the identification strategy credible by grounding it in real-world institutional knowledge. It transforms an abstract econometric argument ("treatment is as-if randomly assigned at the cutoff") into a concrete, verifiable description of how the world works ("the SEC registration threshold creates a discontinuity at $10 million in assets that firms cannot manipulate because auditors verify asset values").

### 2.2 The Structure

**Component 1: The Rule or Institution**

Describe the specific rule, regulation, law, contract, or practice that generates variation in the treatment. Include:
- The exact legal or regulatory language (with citation to the source document)
- The date of enactment or implementation
- The precise threshold, formula, or eligibility criteria
- Any exceptions, exemptions, or phase-in periods
- The enforcement mechanism

**Component 2: Why It Is Exogenous to the Outcome**

Explain why the rule is unlikely to be correlated with the outcome of interest. This is the most important paragraph in the identification section. It must address:
- Who determines the treatment variable? Do they have incentives related to the outcome?
- Can agents manipulate the assignment variable? If so, at what cost?
- Is there evidence of manipulation? (McCrary test, bunching plots, pre-trend tests)
- What are the alternative explanations for variation in the treatment?

**Component 3: The Mapping to the Empirical Design**

Translate the institutional detail into the econometric specification:
- "Because the regulation applies to firms above $X in assets, we define treatment as D_i = 1[Assets_i >= X]..."
- "Because the policy was implemented in different states at different times, we use a staggered DID design..."
- "Because the regulation only affects firms in industry A, we use firms in industry B as controls..."

### 2.3 The Institutional Detail Checklist

For every empirical design that relies on an institutional feature, the following questions must be answered:

**Thresholds and Discontinuities:**
- [ ] What is the exact value of the threshold?
- [ ] Who set the threshold? When? Why?
- [ ] Has the threshold changed over time?
- [ ] Is the threshold known to affected parties?
- [ ] Can affected parties manipulate the assignment variable near the threshold?
- [ ] Are there other policies that use the same threshold?

**Policy Changes:**
- [ ] When was the policy announced vs. implemented?
- [ ] Was there an anticipation period?
- [ ] Who is affected? Are there exemptions?
- [ ] Is compliance mandatory or voluntary?
- [ ] How is compliance monitored or enforced?
- [ ] Have there been subsequent amendments?

**Regulatory Variation:**
- [ ] Which jurisdictions adopted the policy? When?
- [ ] Why did some jurisdictions adopt earlier than others?
- [ ] Are early adopters systematically different from late/non-adopters?
- [ ] Is there cross-jurisdictional spillover?

### 2.4 Common Mistakes

| Mistake | Consequence | Correction |
|---------|-------------|------------|
| Vague description of the institution | Reviewer can imagine plausible violations of the identifying assumptions | Quote the primary source. Be precise about dates, thresholds, and eligibility. |
| Assuming institutional knowledge is common | Reviewer does not understand the design | Provide more detail than you think necessary. A reviewer unfamiliar with the institution must still be convinced. |
| Ignoring anticipation effects | Estimated treatment effects are biased downward | Document the information environment: when was the policy first proposed, discussed in the media, or signalled? |
| Overlooking concurrent policy changes | Compound treatment; cannot attribute effect to the policy of interest | Search for and document other policies that changed at the same time for the same units. |
| Failing to verify the institution | The design relies on an incorrect understanding of the policy | Interview practitioners, read regulatory filings, consult legal databases. |

---

## Pattern 3: The Coefficient of Interest

### 3.1 Purpose

The Coefficient of Interest pattern governs how regression results are presented in tables and in text. A well-presented regression table makes the reader's task effortless -- the coefficient of interest is visually prominent, the control variables are documented but not distracting, and the table notes contain all information needed for interpretation. A poorly presented table forces the reader to search for the key coefficient, guess the sample, and wonder about the unit of observation.

### 3.2 Regression Table Design

**Rule 1: The Coefficient of Interest Must Be Immediately Visible**

Place the coefficient of interest in the first row of the table (or the first row after fixed effects indicators). Never bury it in the middle of a list of control variables. The reader's eyes go to the top-left of the table first -- put the key coefficient there.

**Rule 2: One Row Per Variable**

Do not stack multiple statistics for the same variable. The standard format is:

```
Variable Name        Coefficient
                     (Standard Error)
```

Do not add t-statistics, p-values, or confidence intervals in separate rows -- they clutter the table. If needed, report them in the notes or an appendix.

**Rule 3: Standardise the Number of Specifications**

- 1 specification: Not enough to assess robustness
- 2 specifications: Acceptable if one is "no controls" and one is "full controls"
- 3-6 specifications: Ideal -- allows incremental addition of controls and fixed effects
- 7-9 specifications: Getting long -- consider moving some to the appendix
- 10+ specifications: Too many for one table -- split into main results and robustness

**Rule 4: Every Column Gets a Number**

Number every column. Refer to columns by number in the text: "Column (3) of Table 3 reports the baseline specification with firm and year fixed effects."

**Rule 5: Table Notes Are Self-Contained**

A reader should understand the table without reading the main text. The table notes must include:
- Estimation method (OLS, logit, Poisson, etc.)
- Level of observation (firm-year, deal-level, etc.)
- Sample period
- Dependent variable definition
- Standard error type (robust, clustered, bootstrapped)
- Fixed effects included
- Data source(s)

**Rule 6: Statistical Significance Convention**

Follow the standard convention:
- *** p < 0.01
- ** p < 0.05
- * p < 0.10

Report exact p-values only when the coefficient is near a conventional threshold (e.g., p = 0.052). Do not report p = 0.000 -- use p < 0.001.

### 3.3 Discussing Regression Results in Text

The standard paragraph pattern for discussing a regression coefficient:

> *The coefficient on [variable name] in Column (X) of Table Y is [value] ([standard error]), which is [statistically significant at the Z% level / statistically indistinguishable from zero]. The magnitude implies that a one-standard-deviation increase in [variable] is associated with a [percentage / standard deviation] change in [outcome]. To put this in context, [benchmark comparison -- e.g., this is approximately half the effect of X found by Author (Year) in a different setting]. The inclusion of [control variables / fixed effects] [does / does not] meaningfully change the coefficient, suggesting that [interpretation].*

**Critical elements:**
1. Where to find the coefficient (table and column)
2. The point estimate
3. The standard error and/or significance level
4. Economic interpretation (standardised coefficient, comparison to mean, comparison to benchmark)
5. Relationship to the full specification (does the coefficient change when controls are added?)
6. What the coefficient means ("consistent with the hypothesis that...")

### 3.4 The "Horse Race" Table

A "horse race" table shows the coefficient of interest from multiple specifications, each in its own column, to demonstrate that the result is not sensitive to specification choices.

**Standard column progression:**
1. No controls, no fixed effects
2. Add control variables
3. Add industry fixed effects
4. Add year fixed effects
5. Add firm fixed effects (or the most demanding specification)
6. Alternative estimator (e.g., Poisson, logit, quantile regression)

The coefficient should remain stable (or at least consistent in sign and significance) across columns. Dramatic changes when adding controls or fixed effects suggest omitted variable bias.

### 3.5 Common Regression Table Errors

| Error | Consequence | Correction |
|-------|-------------|------------|
| Not reporting the number of observations | Reader cannot assess power or sample size | Always include N (and clusters if clustered SE) |
| Not reporting R-squared (or pseudo-R2) | Reader cannot assess explanatory power | Always include. If the R2 is suspiciously high or low, discuss. |
| Inconsistent decimal places | Appears sloppy | Standardise: coefficients to 3 decimal places, standard errors to 3, R2 to 3, N to integers |
| Using "Yes/No" for fixed effects without defining them | Ambiguity about what is absorbed | Name the fixed effect explicitly: "Industry FE," "Firm FE," not "Industry" |
| Omitting the constant term | Reader cannot assess baseline | Report the constant at the bottom of the table |
| Reporting coefficients for all controls in the main text | Table is cluttered; reader cannot find the key coefficient | Report only the coefficient of interest. Control variable coefficients go to an appendix. Indicate inclusion with "Controls = Yes" in the table notes. |

---

## Pattern 4: The Robustness Pyramid Narrative

### 4.1 Purpose

The Robustness Pyramid Narrative pattern transforms a mechanical list of robustness checks into a coherent argument for the credibility of the main result. It recognises that not all robustness checks are equally important and that the reader needs a structure for evaluating them.

### 4.2 The Five-Level Narrative

Organise the robustness section around the five levels of the robustness pyramid (see Robustness Framework reference), moving from least to most demanding:

**Paragraph 1: Alternative Measures (Level 1)**

> *We begin by examining whether our results are sensitive to the measurement of [key variable]. In Panel A of Table X, we replace our primary measure with [alternative 1], [alternative 2], and [alternative 3]. Across all three alternatives, the estimated coefficient remains [positive / negative] and statistically significant at conventional levels. The economic magnitude is comparable: [compare to baseline magnitude]. These results indicate that our findings are not an artefact of a particular measurement choice.*

**Paragraph 2: Alternative Samples (Level 2)**

> *We next test whether our results are driven by particular subsamples. In Panel B of Table X, we [list sample restrictions]. In each restricted sample, the coefficient of interest [remains / changes / etc.]. Of particular note, [discuss the most important restriction and why it matters]. Collectively, these sample restrictions [do / do not] alter our conclusions.*

**Paragraph 3: Alternative Specifications (Level 3)**

> *We then assess the sensitivity of our results to econometric specification. Panel C of Table X reports results from [list alternative specifications]. The coefficient is [stable / somewhat sensitive / etc.] across these alternatives, which [strengthens / qualifies] the causal interpretation of our baseline estimate.*

**Paragraph 4: Placebo and Falsification Tests (Level 4)**

> *To further address concerns about confounding factors, we conduct several falsification tests in Panel D of Table X. First, [falsification 1]. Second, [falsification 2]. In all cases, the estimated effects are statistically indistinguishable from zero, consistent with the identifying assumptions of our design. These null results are particularly informative because [explain why the falsification tests are demanding].*

**Paragraph 5: Selection on Unobservables (Level 5)**

> *Finally, we address the possibility that unobserved confounders drive our results. Using the method of Oster (2019), we assess how large selection on unobservables would need to be, relative to selection on observables, to explain away our estimated effect. The resulting delta of [value] indicates that unobservables would need to be [X] times as important as observables to produce a treatment effect of zero. This substantially exceeds the benchmark of delta = 1 recommended by Oster (2019).*

### 4.3 The Nested Structure

The robustness narrative should follow a nested structure:

1. **State the threat:** "One concern with our baseline specification is that [specific threat]."
2. **Describe the test:** "To address this, we [description of robustness check]."
3. **Report the result:** "As reported in Column (X) of Table Y, the coefficient is [value] ([SE]), which is [consistent with / different from] our baseline estimate."
4. **Interpret:** "This suggests that [threat] is [unlikely to be / may be] driving our results."
5. **Transition:** "We next turn to the question of whether [next threat]."

### 4.4 What NOT to Do

| Don't | Why | Do Instead |
|-------|-----|------------|
| "We conducted numerous robustness checks. All confirm our results." | This is lazy. Name the checks and report the results. | Structure by threat. Name each threat and how you address it. |
| Report only that checks were done without showing coefficients | Reviewer assumes the worst -- that the results did not hold | Report coefficients, standard errors, and significance for every check |
| Cherry-pick the checks that "work" | Reviewer will notice checks that are conspicuously absent | Report all reasonable checks. If some results are weaker, discuss honestly. |
| Treat robustness as an afterthought | Reviewer interprets this as the author not taking threats seriously | Robustness is central to the paper's credibility. Allocate adequate space. |
| Run specifications without explaining what threat they address | Reviewer cannot evaluate whether the check is appropriate | For every check: name the threat, explain the check, report the result, interpret. |

---

## Pattern 5: The Mechanism Cascade

### 5.1 Purpose

The Mechanism Cascade pattern addresses the inevitable question: *why* does the effect occur? It structures the evidence for the causal channel(s) in a way that moves from the most general evidence to the most specific, building a cumulative case for the proposed mechanism.

### 5.2 The Cascade Structure

**Level 1: Cross-Sectional Heterogeneity**

The most basic mechanism evidence: the treatment effect varies across subgroups in ways predicted by the theory.

> *If [mechanism] drives our results, the treatment effect should be [larger / smaller / concentrated] in [subgroup]. Table X reports results separately for [subgroup A] and [subgroup B]. Consistent with the [mechanism] channel, we find that the effect is [larger / smaller / concentrated] in [subgroup A], where [mechanism] is predicted to be more salient.*

**Level 2: Intermediate Outcome**

Show that the treatment affects an intermediate variable that the theory identifies as part of the causal chain.

> *We next test whether [treatment] affects [intermediate variable], which theory identifies as a necessary link in the causal chain from [treatment] to [outcome]. Column (X) of Table Y reports the effect of [treatment] on [intermediate variable]. We find a [positive / negative] and significant effect, consistent with the proposed mechanism.*

**Level 3: Mediation Analysis (Formal Decomposition)**

Use the Baron-Kenny or Imai-Keele-Tingley framework to formally decompose the total effect into direct and indirect components.

**Baron and Kenny (1986) Steps:**
1. Treatment -> Outcome: beta_1 significant
2. Treatment -> Mediator: beta_2 significant
3. Mediator -> Outcome (controlling for treatment): beta_3 significant
4. Treatment -> Outcome (controlling for mediator): beta_4 attenuated relative to beta_1

**Imai, Keele and Tingley (2010) Approach (preferred):**

Estimate the Average Causal Mediation Effect (ACME):

ACME = E[Y_i(1, M_i(1)) - Y_i(1, M_i(0))]

and the Average Direct Effect (ADE):

ADE = E[Y_i(1, M_i(0)) - Y_i(0, M_i(0))]

The total effect decomposes as ATE = ACME + ADE. Report the proportion mediated: ACME / ATE.

**Level 4: Ruling Out Alternative Mechanisms**

Provide evidence against plausible alternative mechanisms.

> *An alternative interpretation of our results is that [alternative mechanism] rather than [proposed mechanism] drives the effect. We test this possibility by [test description]. The results, reported in Table Z, [are inconsistent with / do not support] the alternative mechanism. Specifically, [explain why the evidence weighs against the alternative].*

**Level 5: Qualitative or Supplementary Evidence**

For the most important mechanisms, supplement the quantitative evidence with qualitative evidence: interviews with practitioners, case studies, textual analysis of regulatory filings, or survey evidence.

> *To complement the quantitative evidence, we interviewed [N] [practitioners / managers / regulators] involved in [context]. These interviews consistently indicated that [mechanism narrative]. Appendix D provides representative quotes and a summary of the interview findings.*

### 5.3 The Funnel Narrative

The mechanism section should narrow from broad to specific:

1. **Broad:** "Our results are consistent with [general channel]"
2. **Narrower:** "Within [general channel], evidence points specifically to [specific mechanism]"
3. **Narrowest:** "We find evidence against the leading alternative explanation, [alternative mechanism]"

Each paragraph narrows the funnel, eliminating plausible alternatives and converging on the proposed mechanism. The reader should finish the mechanism section thinking: "Given the evidence, [mechanism] is the most likely explanation."

### 5.4 Mediational Language Conventions

| Strength of Evidence | Appropriate Language | Inappropriate Language |
|----------------------|---------------------|----------------------|
| Cross-sectional heterogeneity only | "consistent with," "suggestive of" | "demonstrates," "proves," "shows that" |
| Heterogeneity + intermediate outcome | "provides evidence for," "supports the interpretation that" | "confirms," "establishes" |
| Formal mediation + ruling out alternatives | "indicates that [mechanism] is an important channel" | "proves causation" (mediation cannot prove causation) |
| All above + qualitative evidence | "We conclude that the evidence points most strongly to" | "We have proven that" |

**Critical caveat for mediation analysis:** "We acknowledge that the mediator is likely endogenous, and the estimated ACME should be interpreted with caution. The mediation analysis is intended to document patterns consistent with the proposed mechanism rather than to identify the causal effect of the mediator on the outcome."


---

## Pattern 6: The Honest Limitation

### 6.1 Purpose

The Honest Limitation pattern acknowledges threats to validity without undermining the contribution of the paper. It anticipates reviewer criticisms and defuses them by demonstrating that the author has thought carefully about what the paper can and cannot establish. Paradoxically, papers that honestly discuss their limitations are perceived as *more* credible than papers that minimise or ignore them.

### 6.2 The Structure

The Honest Limitation paragraph has five components:

**Component 1: Name the Limitation**

Be specific. "Our paper has limitations" is worse than useless. Name the exact limitation: "Our identification strategy relies on the parallel trends assumption, which is inherently untestable."

**Component 2: Explain Why It Is a Limitation**

Why does this limitation matter for interpreting the results? "If treated and control units would have followed different trajectories in the absence of treatment, our difference-in-differences estimate would be biased in an unknown direction."

**Component 3: What You Have Done to Mitigate It**

Show that you have not ignored the limitation: "We have taken several steps to mitigate this concern. We provide visual evidence of parallel pre-treatment trends over a five-year window. The joint F-test of pre-treatment coefficients fails to reject the null of parallel trends at conventional levels. We also report Rambachan and Roth (2023) honest confidence sets that account for possible violations of parallel trends. These confidence sets continue to exclude zero for all but the most extreme violations."

**Component 4: What the Limitation Means for Interpretation**

Clarify the scope of the conclusions: "Our estimates should be interpreted as the causal effect of [treatment] under the maintained assumption of parallel trends. If this assumption is violated, our estimates may overstate or understate the true causal effect. We therefore view our results as providing suggestive evidence of a causal relationship rather than definitive proof."

**Component 5: Acknowledge Remaining Threats**

Concede what cannot be addressed: "We cannot fully rule out the possibility that time-varying unobserved confounders correlated with both the treatment and the outcome bias our estimates. The Oster (2019) delta analysis suggests that such confounders would need to be [delta value] times as important as observed confounders to explain away our results, which is [reassuring / concerning]. Future work using alternative identification strategies in different institutional settings would be valuable to corroborate (or challenge) our findings."

### 6.3 The Balance Principle

The Honest Limitation must strike a balance between acknowledging weakness and maintaining the paper's contribution:

| Too Little Honesty | Right Balance | Too Much Honesty |
|-------------------|---------------|------------------|
| "Our paper has no significant limitations." | "Our results rely on the parallel trends assumption, which we test extensively. While we cannot definitively prove that this assumption holds, our event study analysis and honest confidence sets provide evidence that violations would need to be extreme to overturn our conclusions." | "Our identification strategy is fundamentally flawed and we cannot rule out any alternative explanation for our results." |
| Reviewer reaction: "The author is naive or dishonest." | Reviewer reaction: "The author is thoughtful and credible." | Reviewer reaction: "Why was this paper written?" |

### 6.4 Where to Place Limitations

There are two schools of thought, both acceptable:

**Option A: In the Conclusion (traditional)**
- Pro: Does not interrupt the narrative flow
- Con: Reviewer may form negative impressions before reaching the conclusion
- Best for: papers with strong identification where limitations are minor

**Option B: Distributed Throughout (modern, preferred for FT50)**
- Pro: Each limitation is addressed in context, alongside the evidence that mitigates it
- Con: Can make the paper feel defensive if overdone
- Best for: papers with acknowledged identification challenges

**Recommendation:** Address the most important limitation in the identification section (Pattern 2) as part of the discussion of why the institutional feature is exogenous. Address secondary limitations in a dedicated "Limitations and Future Research" subsection of the conclusion. This combines the credibility-building of Option B with the clarity of Option A.

### 6.5 The "Limitations Cascade" Template

Structure the limitations section as a cascade from most to least important:

1. **Identification limitation:** "Our identification strategy relies on [assumption]. While we provide [evidence supporting assumption], we acknowledge that [residual concern]."
2. **External validity limitation:** "Our sample consists of [specific group] over [time period]. Whether our results generalise to [other groups / time periods] is an open question."
3. **Measurement limitation:** "Our measure of [construct] captures [aspect] but may not capture [other aspect]."
4. **Mechanism limitation:** "While our heterogeneity analysis is consistent with [mechanism], we cannot definitively establish that [mechanism] is the exclusive channel."
5. **Generalizability limitation:** "The institutional context we study -- [context] -- has specific features that may limit the applicability of our findings to other settings."

### 6.6 Common Limitations by Design

| Design | Expected Limitation | Mitigation Language |
|--------|-------------------|---------------------|
| DID | Parallel trends untestable | "We provide evidence consistent with parallel pre-trends, but acknowledge that post-treatment counterfactual trends are inherently unobservable." |
| RDD | Local effect only (LATE at cutoff) | "Our estimates identify the treatment effect at the cutoff and may not generalise to units far from the threshold." |
| IV | LATE for compliers | "Our IV estimates capture the treatment effect for compliers -- units whose treatment status is affected by the instrument. These effects may differ from the average treatment effect for the full population." |
| RCT | Hawthorne effects; limited external validity | "Participants knew they were in a study, which may have affected their behaviour. Replication in non-experimental settings would be valuable." |
| SCM | Inference with small donor pool | "With [N] donor units, our inference relies on placebo tests that may have limited power. Parametric approaches (e.g., Xu 2017) provide complementary evidence." |
| Cross-section | Selection on unobservables | "Despite our extensive controls, we cannot rule out selection on unobservables. Oster (2019) bounds suggest that such selection would need to be [delta value] times as strong as selection on observables to overturn our results." |

---

## Pattern 7: The Policy/Practice Implication

### 7.1 Purpose

The Policy/Practice Implication pattern answers the ultimate question: "So what should someone actually do differently based on this research?" It bridges the gap between academic findings and real-world decisions, making the paper relevant to readers beyond the academic community.

### 7.2 The Structure

**Component 1: Restate the Finding in Plain Language**

Strip the finding of econometric terminology. State it as a fact about the world that a practitioner would recognise.

Not: "We find that the coefficient on the triple interaction term in our DDD specification is positive and significant at the 1% level."

Instead: "When firms are required to disclose their environmental impact, they reduce their carbon emissions by approximately 12% over the following three years."

**Component 2: Identify the Decision-Maker**

Who should act differently based on this finding? Be specific: "regulators at the SEC," "compensation committees of S&P 500 boards," "marketing managers at consumer packaged goods firms," "central bank governors in emerging markets."

**Component 3: Describe the Actionable Change**

What should this decision-maker do differently? Be concrete. "Our results suggest that mandatory ESG disclosure requirements are an effective tool for reducing corporate carbon emissions. Regulators considering climate-related disclosure rules can use our estimates to calibrate the expected environmental benefits of such policies against their compliance costs."

**Component 4: Calibrate the Magnitude**

Quantify the expected effect of the recommended action using the estimated coefficients. "Based on our estimates, a firm with median pre-regulation emissions would reduce its carbon footprint by approximately 50,000 metric tons of CO2 equivalent over three years. For the average S&P 500 firm, this represents a 15% reduction relative to baseline."

**Component 5: Acknowledge Limits of the Recommendation**

Do not oversell. Clarify the conditions under which the recommendation applies and those under which it may not. "These estimates are based on the experience of European firms subject to the EU Emissions Trading System. The estimated effects may differ for firms in regulatory environments with weaker enforcement or for firms in industries with different abatement cost structures. Policy-makers in jurisdictions with different institutional characteristics should interpret our estimates as indicative rather than definitive."

### 7.3 The Practitioner Test

After writing the implications section, apply the "Practitioner Test":
1. Could a practitioner read only the implications section and know what to do? If yes, the implications are sufficiently concrete.
2. Would a practitioner find the recommendation surprising or non-obvious? If no, the paper is not contributing new practical knowledge.
3. Could a practitioner act on the recommendation using only the information in the paper? If no, add the necessary details (cost estimates, implementation timeline, benchmarks).

### 7.4 Domain-Specific Implication Patterns

**Finance Implications:**
- For investors: portfolio allocation rule changes, screening criteria
- For corporate managers: investment policy, payout policy, financing choices
- For regulators: disclosure requirements, market structure rules
- For boards: governance changes, compensation design

**Accounting Implications:**
- For standard-setters: disclosure requirements, recognition criteria
- For auditors: audit procedures, materiality thresholds
- For managers: reporting choices, voluntary disclosure decisions
- For analysts: forecasting adjustments, valuation model inputs

**Management Implications:**
- For executives: strategic decisions (diversification, vertical integration, innovation)
- For boards: CEO selection, succession planning, monitoring mechanisms
- For human resources: hiring practices, compensation design, training programmes
- For entrepreneurs: founding team composition, financing strategy, growth tactics

**Marketing Implications:**
- For CMOs: advertising budget allocation, pricing strategy, channel selection
- For brand managers: positioning, targeting, message design
- For product managers: feature prioritisation, launch timing, bundling decisions
- For customer insights: segmentation approach, loyalty programme design

**Operations Implications:**
- For supply chain managers: supplier selection, inventory policy, facility location
- For quality managers: inspection protocols, continuous improvement programmes
- For capacity planners: expansion timing, flexibility investments
- For process designers: workflow configuration, technology adoption

**Economics/Policy Implications:**
- For regulators: policy design, enforcement intensity, compliance cost estimation
- For legislators: bill design, sunset provisions, evaluation requirements
- For central bankers: rule vs. discretion, communication policy, mandate interpretation
- For international organisations: programme design, conditionality, evaluation frameworks

### 7.5 Example: Full Implications Paragraph

A paper on the effect of board gender diversity mandates on firm performance:

> *Our findings have direct implications for regulators considering board diversity mandates. We estimate that California's 2018 mandate -- requiring publicly traded firms headquartered in the state to have at least one female director -- increased the share of female directors from 15% to 27% within three years of passage. However, we also find evidence that firms subject to the mandate experienced a 2.3% decline in Tobin's Q relative to matched firms not subject to the mandate. This decline was concentrated in firms that added directors with less board experience and fewer industry connections, suggesting that the supply of qualified female directors was insufficient to meet the mandate-induced demand in the short run.*
>
> *For policy-makers, our results suggest that board diversity mandates are effective at changing board composition but may impose short-run costs on firm value when the pipeline of qualified candidates is shallow. A phased implementation -- with compliance timelines linked to progress in expanding the director pipeline through mentorship, board-readiness programmes, and expanded search criteria -- may achieve the diversity benefits of mandates while mitigating the short-run performance costs. Policy-makers in jurisdictions considering similar mandates (e.g., the EU directive on gender balance on corporate boards) should consider the trade-off between speed of implementation and availability of qualified candidates.*

### 7.6 Common Errors in Implications Sections

| Error | Why It Hurts | Correction |
|-------|-------------|------------|
| Implications that are generic platitudes | "Firms should consider governance quality" adds nothing | Be concrete: "Firms in the bottom quartile of our governance index should prioritise adding independent directors before pursuing major acquisitions." |
| Implications that ignore statistical uncertainty | Point estimates presented as certain | "Our point estimates suggest a 12% reduction, with a 95% confidence interval of [5%, 19%]." |
| Implications that do not follow from the empirical design | LATE interpreted as ATE; reduced-form interpreted as structural | "Our IV estimates capture the effect for firms whose governance choices are affected by the regulatory change (compliers). These effects may not generalise to firms that would have adopted similar governance practices regardless." |
| Implications that ignore costs | Policy recommendation without cost-benefit analysis | Acknowledge implementation costs, transition costs, and unintended consequences. |
| Implications that are too specific to the study context | Cannot be applied by anyone outside the specific setting | Discuss the features of the study context that are necessary for the effect to generalise. |


---

## 8. Pattern Integration: The Complete Paper Arc

### 8.1 How the Seven Patterns Fit Together

The seven patterns map to the standard IMRAD structure as follows:

| Section | Pattern | Role |
|---------|---------|------|
| Introduction | Pattern 1: The Motivating Puzzle | Create tension; justify the paper's existence |
| Introduction (end) | Pattern 7: The Policy/Practice Implication (preview) | Signal relevance; motivate reading beyond methods |
| Institutional Background | Pattern 2: The Institutional Detail | Establish identification credibility |
| Empirical Design | Pattern 2: The Institutional Detail (cont.) | Map institution to econometrics |
| Results | Pattern 3: The Coefficient of Interest | Present evidence clearly |
| Robustness | Pattern 4: The Robustness Pyramid Narrative | Defend the evidence systematically |
| Mechanisms | Pattern 5: The Mechanism Cascade | Explain the evidence; deepen contribution |
| Conclusion | Pattern 6: The Honest Limitation | Acknowledge boundaries honestly |
| Conclusion (end) | Pattern 7: The Policy/Practice Implication (full) | Close the loop; answer "so what?" |

### 8.2 The Narrative Arc

The paper should tell a single coherent story:

1. **Setup (Pattern 1):** Here is something surprising about the world that existing theories cannot explain.
2. **Approach (Pattern 2):** We use a specific institutional feature that allows us to identify the causal mechanism.
3. **Evidence (Patterns 3 and 4):** Here is what we find, and here is why you should believe it.
4. **Explanation (Pattern 5):** Here is why we think this effect occurs.
5. **Boundaries (Pattern 6):** Here is what we cannot claim and what remains uncertain.
6. **Action (Pattern 7):** Here is what our findings mean for people who make decisions.

### 8.3 The Elevator Pitch Test

After writing the paper, test whether it can be summarised in a single paragraph that follows the seven-pattern arc:

> *[Pattern 1: Motivating Puzzle] Existing theory predicts X, but the data shows Y. [Pattern 2: Institutional Detail] We exploit [institutional feature] to identify the causal effect of [treatment] on [outcome]. [Patterns 3 and 4: Evidence] We find that [main result], which is robust to [key robustness checks]. [Pattern 5: Mechanism] The effect operates through [mechanism], as evidenced by [key mechanism test]. [Pattern 6: Honest Limitation] We acknowledge that [key limitation] and interpret our results accordingly. [Pattern 7: Implication] Our findings suggest that [decision-maker] should [actionable recommendation].*

If you cannot produce this paragraph, the paper is not yet ready for submission.

---

## 9. Quick Reference: Sentence-Level Writing Conventions

### 9.1 Hedging Language for Empirical Claims

| Strength | Appropriate Language |
|----------|---------------------|
| Very strong evidence | "The results show that...", "We find that..." |
| Strong evidence | "The evidence indicates that...", "The results document that..." |
| Moderate evidence | "The results are consistent with...", "The evidence suggests that..." |
| Weak evidence | "The results are suggestive of...", "We cannot rule out..." |
| No evidence | "We find no evidence that...", "The coefficient is statistically indistinguishable from zero." |

### 9.2 Causal Language

| Appropriate | Inappropriate |
|-------------|---------------|
| "The coefficient on X is [value], consistent with a causal effect of X on Y under the identifying assumptions." | "X causes Y." |
| "A one-unit change in X is associated with a [beta] change in Y." | "X increases Y by [beta]." |
| "The results are consistent with the hypothesis that..." | "The results prove the hypothesis that..." |
| "Our estimates suggest that the policy increased..." | "The policy increased..." |
| "Under the maintained assumption of parallel trends..." | (no qualifier when using DID) |

### 9.3 Statistical Significance Language

| P-value Range | Appropriate Language |
|---------------|---------------------|
| p < 0.01 | "statistically significant at the 1% level" |
| 0.01 <= p < 0.05 | "statistically significant at the 5% level" |
| 0.05 <= p < 0.10 | "marginally significant" or "significant at the 10% level" |
| 0.10 <= p < 0.15 | "approaching conventional significance levels" |
| p >= 0.15 | "statistically indistinguishable from zero" or "not statistically significant at conventional levels" |

**Important:** Never say "insignificant." The correct phrase is "not statistically significant" or "statistically indistinguishable from zero."

### 9.4 Transition Phrases for Building Arguments

| Purpose | Phrases |
|---------|---------|
| Adding evidence | "Moreover, ...", "In addition, ...", "Furthermore, ..." |
| Contrasting | "However, ...", "In contrast, ...", "On the other hand, ..." |
| Conceding | "That said, ...", "To be sure, ...", "We acknowledge that..." |
| Summarising | "Taken together, ...", "Collectively, these results...", "Overall, ..." |
| Transitioning to next section | "Having established [X], we next examine [Y].", "We now turn to the question of [Z]." |
| Introducing auxiliary analysis | "To further explore this pattern, ...", "We supplement this evidence with..." |
| Framing a robustness check | "One concern with the preceding analysis is that...", "A potential alternative explanation is that..." |

### 9.5 Abstract Template

A successful FT50 abstract follows a seven-sentence structure:

1. **Motivation:** "A central question in [field] is [research question]."
2. **Tension:** "Existing theory predicts [X], but prior empirical evidence is [mixed / absent / contradictory]."
3. **Approach:** "We [exploit / examine / study] [institutional feature / setting / dataset] to [identify / estimate / document] [causal effect / relationship]."
4. **Main Result:** "We find that [key coefficient] -- a one-standard-deviation increase in [treatment] is associated with a [X]% change in [outcome]."
5. **Mechanism:** "The effect operates through [mechanism], as evidenced by [key test]."
6. **Robustness:** "The results are robust to [list 2-3 key robustness checks] and survive [key falsification test]."
7. **Implication:** "Our findings suggest that [practitioner group] should [actionable recommendation]."

---

## 10. References for Writing Quality

- Bem, D. J. (2003). Writing the empirical journal article. In *The Compleat Academic*. APA.
- McCloskey, D. N. (2000). *Economical Writing* (2nd ed.). Waveland Press.
- Cochrane, J. H. (2005). Writing tips for Ph.D. students. University of Chicago.
- Strunk, W., & White, E. B. (2000). *The Elements of Style* (4th ed.). Longman.
- Thomson, W. (2001). *A Guide for the Young Economist* (2nd ed.). MIT Press.
- Varian, H. R. (2016). How to build an economic model in your spare time. *American Economist*, 61(1), 81-90.
- Zinsser, W. (2006). *On Writing Well* (30th anniv. ed.). Harper Perennial.
- Pinker, S. (2014). *The Sense of Style: The Thinking Person's Guide to Writing in the 21st Century*. Viking.
- King, G. (2006). Publication, publication. *PS: Political Science & Politics*, 39(1), 119-125.
- Angrist, J. D., & Pischke, J.-S. (2014). *Mastering 'Metrics*. Princeton University Press.
- Imai, K., Keele, L., & Tingley, D. (2010). A general approach to causal mediation analysis. *Psychological Methods*, 15(4), 309-334.
- Baron, R. M., & Kenny, D. A. (1986). The moderator-mediator variable distinction. *Journal of Personality and Social Psychology*, 51(6), 1173-1182.
- Oster, E. (2019). Unobservable selection and coefficient stability: Theory and evidence. *Journal of Business & Economic Statistics*, 37(2), 187-204.
- Rambachan, A., & Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies*, 90(5), 2555-2591.
- Altonji, J. G., Elder, T. E., & Taber, C. R. (2005). Selection on observed and unobserved variables. *Journal of Political Economy*, 113(1), 151-184.
