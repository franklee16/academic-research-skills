# Writing Patterns from Published Marketing Science Papers

This reference catalogues six reusable writing patterns distilled from published papers in Marketing Science, JMR, JM, and JCR. Each pattern includes: when to use it, structural template, and concrete examples from published papers. These patterns reflect the distinctive rhetorical conventions of top marketing journals.

---

## Pattern 1: The Managerial Motivating Example

**Best for**: Marketing Science, JMR, JM — all marketing papers.
**Purpose**: Ground the paper in a concrete, high-stakes marketing decision faced by a real company.

### Structure

```
Paragraph 1: The specific company and dilemma
  - Name a real company (Procter & Gamble, Amazon, Nike, Coca-Cola, etc.)
  - Cite specific numbers (marketing budget, number of products, customer base)
  - Pose a concrete marketing decision the company faces

Paragraph 2: Generalization to the industry
  - "This challenge is not unique to [company]."
  - Provide broader industry statistics (from trade press, industry reports)
  - Cite practitioners' own words: "As P&G's CMO noted..."

Paragraph 3: The academic gap
  - "Despite its practical importance, the marketing literature has largely..."
  - Cite 2-3 key references that come closest
  - State what each stream misses

Paragraph 4: Our approach and key insight
  - "In this paper, we [method] to study [phenomenon]."
  - One sentence: the main finding
  - "For marketing managers, this means..."

Paragraph 5: Numbered contributions (3-5 items)
  - Each starts with an action verb: "First, we develop... Second, we identify... Third, we demonstrate..."
  - Connect each contribution to the gap identified in P3
```

### Example Template

```latex
\section{Introduction}

In 2024, Nike allocated \$4.3 billion to what it calls "demand creation expense" 
across sponsorships, digital advertising, brand events, and retail experiences 
spanning 190 countries. Despite this massive investment, Nike's marketing 
executives face a persistent challenge: they cannot credibly measure whether 
a dollar spent on a TikTok influencer campaign generates more incremental sales 
than a dollar spent on a traditional TV spot, because each channel reaches 
overlapping audiences and creates effects on different time horizons.

This measurement challenge extends far beyond Nike. A 2024 survey by the 
Association of National Advertisers found that 82\% of senior marketers cite
cross-channel ROI measurement as their top challenge, with 67\% reporting that
they cannot distinguish between truly incremental effects and mere attribution
bias. As one CMO noted, "We know half our advertising works; we just don't
know which half."

Despite decades of research on advertising effectiveness, the academic 
literature has not provided marketers with a framework for comparing the
causal effects of advertising across fundamentally different media channels...
```

### Published Examples

| Paper | Journal | Opening Example |
|-------|---------|-----------------|
| Bronnenberg, Dubé & Gentzkow (2012) | MktSci | Brand shares across US regions; Tide vs. Wisk |
| Lewis & Rao (2015) | QJE | "The unfavorable economics of measuring returns to advertising" |
| Sahni (2015) | QME | Temporal spacing of ads on restaurant search platform |
| Datta, Ailawadi & van Heerde (2017) | JM | How advertising affects brand switching |

### When NOT to Use

- The paper is purely methodological with no clear industry connection
- The motivating company is hypothetical or anonymized (use a real company or generalize immediately)

---

## Pattern 2: The Identification Narrative

**Best for**: JMR, Marketing Science — all papers with quasi-experimental or experimental identification.
**Purpose**: Make the identification strategy feel like a detective story. The best marketing papers devote an entire section to explaining the source of exogenous variation with rich institutional detail.

### Structure

```
§3.1 Institutional Background
  - Describe the policy, rule, or marketplace institution that generates variation
  - Explain HOW it works (with timeline, flowchart, or institutional diagram)
  - Who makes the decision? What information do they have? What are their incentives?

§3.2 Why This Generates Quasi-Experimental Variation
  - "Because [institutional feature], variation in [key variable] is driven by 
    [exogenous factor], not by [endogenous factor]."
  - Use plain language: "In essence, the [institution] creates a natural experiment
    where some [units] are effectively randomized to receive [treatment]."

§3.3 Identification Assumptions
  - State each assumption explicitly in formal language
  - For each: what is testable, how we test it, and results
  - For each: what is untestable, why it is plausible given the institutional context

§3.4 Diagnostic Evidence
  - Figure: Event study plot (DID) / RD plot / first-stage scatter (IV)
  - Table: Balance table
  - Supplementary: Placebo tests, falsification, McCrary test, etc.
```

### The "Detective Story" Narrative Arc

```
The mystery: "We want to know whether [treatment] causally affects [outcome].
But a simple comparison of treated and untreated units is confounded by..."

The clue: "Fortunately, [institutional feature] provides a source of variation
that is plausibly unrelated to [confounders]."

The investigation: "To validate this as a natural experiment, we conduct a
series of diagnostic tests..."

The resolution: "The evidence consistently supports the validity of our
identification strategy, allowing us to interpret our estimates as causal."
```

### Key Phrases for the Identification Narrative

| Phase | Key Phrases |
|-------|-------------|
| **The puzzle** | "A naive comparison of... would be biased because..." |
| **The natural experiment** | "However, [institutional feature] creates variation in [treatment] that is..." |
| **The credibility argument** | "This variation is plausibly exogenous because [decision-makers] could not have anticipated or responded to [outcome]." |
| **The test** | "If our identification strategy is valid, we should observe... [testable prediction]" |
| **The confirmation** | "Consistent with our identification assumptions, we find that..." |

### Published Examples

| Paper | Journal | Identification Device |
|-------|---------|----------------------|
| Busse et al. (2010) | MktSci | Price discontinuities in auto retail |
| Seiler & Yao (2017) | MktSci | Staggered rollout of online reviews |
| Ailawadi et al. (2014) | JM | Store entry as a quasi-experiment |
| Blake, Nosko & Tadelis (2015) | Econometrica | Randomized ad experiments on eBay |

---

## Pattern 3: The Elasticity Matrix Table

**Best for**: Marketing Science, QME — demand estimation papers.
**Purpose**: The own- and cross-price elasticity matrix is the central empirical result of any demand estimation paper. Its presentation deserves careful attention.

### Structure

**Table Layout**:
- Rows: Products/brands whose price changes
- Columns: Products/brands whose demand responds
- Diagonal: Own-price elasticities (should be negative)
- Off-diagonal: Cross-price elasticities (should be positive for substitutes)
- Standard errors in parentheses
- Summary statistics: median own-price elasticity, average diversion ratio

**Template**:

```latex
\begin{table}[htbp]
\centering
\caption{Price Elasticity Matrix}
\label{tab:elasticities}
\footnotesize
\begin{tabular}{@{}lcccccc@{}}
\toprule
& \multicolumn{6}{c}{\textbf{\% Change in Demand for:}} \\
\cmidrule(l){2-7}
\textbf{1\% Price Increase in:} & Brand A & Brand B & Brand C & Brand D & Brand E & Outside \\
\midrule
Brand A & \textbf{-2.34} & 0.42 & 0.31 & 0.28 & 0.15 & 1.18 \\
        & \textbf{(0.18)} & (0.08) & (0.07) & (0.06) & (0.04) & (0.12) \\
Brand B & 0.38 & \textbf{-2.51} & 0.45 & 0.22 & 0.18 & 1.28 \\
        & (0.07) & \textbf{(0.21)} & (0.09) & (0.05) & (0.04) & (0.13) \\
\bottomrule
\end{tabular}

\par\medskip
\noindent\textit{Notes:} Cells report percentage change in demand for the column 
brand when the row brand's price increases by 1\%. Standard errors computed via
delta method in parentheses. Own-price elasticities on the diagonal are bolded.
All estimates from the random coefficients logit model reported in Table X.
\end{table}
```

### Economic Significance Discussion Template

```
The median own-price elasticity across the 12 brands in our sample is -2.4,
indicating that a 10% price increase would reduce a brand's market share by
approximately 24%. The average diversion ratio is 0.15, meaning that when a
consumer switches away from the focal brand due to a price increase, 15% of
those switchers go to the next-closest competitor (on average).

These elasticities have direct marketing implications. For Brand A (own-price
elasticity = -2.34), the profit-maximizing markup under single-product 
Bertrand pricing is 1/2.34 = 42.7%, which compares to the observed average 
markup of 38%. This suggests Brand A may be underpricing relative to the
profit-maximizing level, consistent with managerial concerns about short-term
volume targets overriding long-term profitability.
```

### Diversion Ratio Table (Companion to Elasticities)

The diversion ratio from product j to product k measures the fraction of consumers leaving j who go to k:

$DR_{jk} = -\frac{\varepsilon_{kj} w_k}{\varepsilon_{jj} w_j}$

where $\varepsilon_{kj}$ is the cross-price elasticity, $\varepsilon_{jj}$ is the own-price elasticity, and $w_k$ and $w_j$ are market shares.

**Why This Matters**: Diversion ratios are critical inputs for merger analysis and competitive strategy. The DOJ/FTC use diversion ratios to define relevant markets and screen mergers.

---

## Pattern 4: The Counterfactual Triplet

**Best for**: Marketing Science, QME — structural modeling papers.
**Purpose**: For each counterfactual simulation, present a triplet: Baseline → Counterfactual → Difference. Always report consumer welfare (compensating variation) alongside firm profit.

### Structure

```
For each counterfactual:

1. BASELINE: What is the current state?
   - Observed prices, market shares, profits, consumer surplus

2. COUNTERFACTUAL: What would happen under the alternative policy?
   - Simulated prices, market shares, profits, consumer surplus

3. DIFFERENCE: What changes and by how much?
   - Δ Prices, Δ Shares, Δ Profits, Δ Consumer Surplus = Compensating Variation

4. WELFARE SUMMARY: Who gains and who loses?
   - Total welfare change = Δ Consumer Surplus + Δ Producer Surplus
   - Distributional effects: which consumers gain/lose most?
```

### Counterfactual Results Table Template

```
Table X: Counterfactual #1 — Merger of Brands A and B
────────────────────────────────────────────────────────────
                        Baseline    Merger      Δ (SE)
────────────────────────────────────────────────────────────
Prices ($)
  Brand A                 3.49       3.82      +0.33 (0.08)
  Brand B                 3.29       3.58      +0.29 (0.07)
  Brand C                 3.19       3.22      +0.03 (0.02)
  Brand D                 2.99       3.01      +0.02 (0.02)

Market Shares (%)
  Brand A                 18.2       15.3      -2.9 (0.8)
  Brand B                 16.8       14.1      -2.7 (0.7)
  Brand C                 14.5       15.2      +0.7 (0.3)
  Outside good            20.1       22.8      +2.7 (0.6)

Welfare
  Producer surplus ($M)   142.3      156.8     +14.5 (3.2)
  Consumer surplus ($M)   387.5      354.2     -33.3 (7.1)
  Total welfare ($M)      529.8      511.0     -18.8 (8.4)
────────────────────────────────────────────────────────────
Notes: Merger simulation assumes post-merger coordinated pricing 
between Brands A and B. Compensating variation is $33.3M, 
representing the amount consumers would need to be compensated
to be as well off after the merger as before. Standard errors
from 500 bootstrap replications.
```

### Narrative Template for Counterfactual Discussion

```
Our first counterfactual simulates a merger between Brands A and B 
(the two market leaders). We find that the merger would increase the 
merged firm's prices by 9.5% on average (p < 0.001), with Brand A 
increasing from $3.49 to $3.82 and Brand B from $3.29 to $3.58. 
Competitor prices increase only modestly (0.6-1.0%), consistent with 
the upward pricing pressure that would result from the elimination of 
competition between the two closest substitutes.

The merger reduces consumer surplus by $33.3 million (SE = $7.1M; 
p < 0.001), while increasing the merged firm's profits by $14.5 million 
(SE = $3.2M). The net welfare loss is $18.8 million, primarily driven 
by higher prices reducing consumption. Notably, consumers in the lowest 
income quartile bear 34% of the total consumer welfare loss, suggesting 
regressive distributional effects that antitrust authorities may wish 
to consider alongside the aggregate welfare impact.
```

### Compensating Variation Formula

For a price change from $p^0$ to $p^1$, the compensating variation (CV) for consumer $i$ is:

$CV_i = \frac{1}{|\alpha_i|} \left[ \ln\left(\sum_j \exp(V_{ij}(p^1))\right) - \ln\left(\sum_j \exp(V_{ij}(p^0))\right) \right]$

where $\alpha_i$ is the marginal utility of income.

---

## Pattern 5: The Heterogeneity Cascade

**Best for**: All empirical marketing papers — understanding who is most affected, where, when, and why.
**Purpose**: Show that the average treatment effect masks meaningful heterogeneity. Build from "who" to "where" to "when" to "why," each step deepening the theoretical mechanism.

### Structure

```
§5.1 Overall Effect
  - Main treatment effect (ITT, average elasticity, etc.)
  - Statistical and economic significance

§5.2 Who: Heterogeneity by Consumer Characteristics  
  - Demographics: age, income, education, family size
  - Behavioral: past purchase frequency, loyalty status, deal proneness
  - Psychographic: brand attachment, category involvement
  - "The effect is concentrated among [specific group]..."

§5.3 Where: Heterogeneity by Context
  - Geographic: urban vs. rural, region, DMA characteristics
  - Competitive: market concentration, number of competitors
  - Store/channel: online vs. offline, store format
  - "The effect is strongest in [specific context]..."

§5.4 When: Heterogeneity Over Time
  - Short-term vs. long-term effects
  - Habituation: does the effect grow or decay?
  - Seasonality: does the effect vary by time of year?
  - "The effect [grows/decays/stabilizes] over time because..."

§5.5 Why: Mechanism Evidence
  - Mediation: through what intermediate variable does the effect operate?
  - Moderation: under what conditions is the effect amplified or attenuated?
  - Process: what psychological or economic mechanism explains the heterogeneity?
  - "The heterogeneity pattern is consistent with a [mechanism] explanation..."
```

### Visualization for the Heterogeneity Cascade

**Forest Plot of Subgroup Effects**:

```
Figure X: Heterogeneous Treatment Effects by Subgroup

Subgroup                    Effect (95% CI)
─────────────────────────────────────────────
Overall                     ●──────────●
  High loyalty              ●──────────────●
  Low loyalty               ●────●
  Urban                     ●────────────●
  Rural                     ●───────●
  High competition          ●────●
  Low competition           ●──────────────●
─────────────────────────────────────────────
        -0.05    0     0.05    0.10   0.15
               Treatment Effect
```

**Quadrant Chart: Treatment Effect × Baseline Outcome**:
- X-axis: pre-treatment level of key moderator
- Y-axis: treatment effect size
- Each point = a subgroup or market
- Fitted line showing how treatment effect varies with moderator

### Narrative Template

```
Having established a positive average treatment effect of [magnitude] 
(Table X, Column 1), we now unpack this average to understand for whom, 
where, and through what mechanism the effect operates.

Who benefits most? The effect is concentrated among [group]: [specific 
estimate, CI]. [Group 2] shows a [smaller/insignificant] effect of 
[estimate, CI]. The difference between groups is statistically significant 
(p = [value]) and economically meaningful ([magnitude] percentage points).

This heterogeneity aligns with a [theoretical mechanism] account. If 
[mechanism] is driving the effect, we would expect the effect to be 
[stronger/weaker] when [moderating condition]. Indeed, we find that 
the treatment effect is [X times larger] under [condition A] than under 
[condition B] (p = [value]; see Figure X).

The temporal pattern provides additional evidence for the [mechanism] 
interpretation. The effect [grows/decays/stabilizes] over [timeframe], 
consistent with [theoretical prediction]. Under an alternative [competing 
mechanism], we would have expected [different temporal pattern], which 
we do not observe.
```

---

## Pattern 6: The CMO Letter

**Best for**: JM, JMR — papers that need to convince practitioners of their value.
**Purpose**: Write the implications section as if you were drafting a memo to a Chief Marketing Officer. Use plain language, concrete numbers, and actionable recommendations.

### Structure

```
§Implications for Marketing Practice

Dear CMO,

If you are like most marketing leaders, you face [the challenge this 
paper addresses]. Our research provides three evidence-based 
recommendations for addressing this challenge.

RECOMMENDATION 1: [One sentence, imperative mood]
  The evidence: [2-3 sentences summarizing relevant findings with 
  specific numbers: magnitudes, not just direction]
  The action: [2-3 sentences on exactly what to DO]
  The expected impact: [Quantified estimate: "We estimate this would 
  increase [outcome] by [X]% based on our analysis of [data]"]

RECOMMENDATION 2: [Same structure]

RECOMMENDATION 3: [Same structure]

Caveats and Boundary Conditions:
  [Honest discussion of when these recommendations apply and when 
  they might not]

Next Steps:
  [What should a company do to implement these recommendations? Pilot? 
  A/B test? Phased rollout?]
```

### CMO Letter Template (Written in the Paper)

```latex
\section{Managerial Implications}

Our results have concrete implications for how marketing executives should 
allocate their budgets across advertising channels.

\textit{Recommendation 1: Shift 15--20\% of the digital display budget to 
connected TV.} We find that connected TV advertising generates a 2.3x higher 
ROI than display advertising (p < 0.001), primarily because CTV ads have 
higher completion rates (92\% vs. 34\% for display) and are less susceptible 
to ad blocking. For a typical Fortune 500 advertiser spending \$50M annually 
on digital advertising, reallocating 15\% (\$7.5M) from display to CTV 
would increase incremental sales by an estimated \$12.4M, holding total 
spend constant (see Appendix D for calculation details).

\textit{Recommendation 2: Increase frequency to 5--7 exposures per week, 
not 3--4.} Conventional wisdom in media planning suggests diminishing returns 
beyond 3--4 exposures per week. However, our field experiment (n = 2.4M 
households) finds that the optimal frequency is 6.2 exposures per week 
(95\% CI: [5.8, 6.6]), with the marginal effect of the 6th exposure 
still positive and significant (p = 0.003). Moving from 4 to 6 exposures 
per week increases sales by 8.4\%, more than offsetting the 50\% increase 
in media cost.

\textit{Recommendation 3: Use brand keyword search as a leading indicator 
for offline sales.} Managers often struggle to connect advertising to 
offline purchases because of the long and noisy purchase cycle for 
durable goods. We find that a 10\% increase in branded search volume 
predicts a 3.2\% increase in offline sales 2--3 weeks later (p < 0.001), 
providing a fast, low-cost leading indicator that managers can monitor 
in real time while waiting for POS data to arrive.
```

### Key Principles for the CMO Letter

1. **No Greek letters, no equations, no academic jargon**: If a CMO can't understand it, rewrite it.
2. **Specific numbers**: Not "increase sales" but "increase quarterly sales by 7.2%."
3. **Back-of-the-envelope ROI**: If a manager spends X, what is the expected return? Show the math.
4. **Imperative mood**: "Do X" not "X could be done" or "managers might consider X."
5. **Prioritize**: 2-3 recommendations, not 10. Tell the CMO what matters most.
6. **Implementation guidance**: How to actually do it. A pilot? In what market? With what metrics?
7. **Honest about uncertainty**: CI around estimates. Boundary conditions. "This recommendation is strongest when..."

---

## Combination Patterns

### The Complete Marketing Paper Arc

The most successful marketing papers combine multiple patterns in sequence:

1. **Opening**: Pattern 1 (Managerial Motivating Example) — hook the reader
2. **Literature gap**: Pattern 1 (continued) + differentiation table
3. **Identification narrative**: Pattern 2 — build credibility
4. **Central results**: Pattern 3 (elasticities) or main regression table
5. **Enrichment**: Pattern 5 (heterogeneity cascade) — unpack the average
6. **Policy analysis**: Pattern 4 (counterfactual triplet) — what changes?
7. **Closing**: Pattern 6 (CMO letter) — what should a marketer DO?

### When to Use Each Pattern as Primary

| Primary Pattern | Your Paper Profile |
|----------------|-------------------|
| Motivating Example | Opening any marketing paper |
| Identification Narrative | Papers relying on natural experiments or quasi-experiments |
| Elasticity Matrix | Demand estimation / structural modeling papers |
| Counterfactual Triplet | Structural papers with policy simulations |
| Heterogeneity Cascade | Papers where "who is affected" is a central contribution |
| CMO Letter | Papers targeting JM or JMR; papers with strong practical implications |

---

## Published Examples Organized by Pattern

| Pattern | Exemplar Paper | Journal | Why It's Exemplary |
|---------|---------------|---------|--------------------|
| Motivating Example | Bronnenberg et al. (2012) | MktSci | Geographic brand share variation as a puzzle |
| Identification Narrative | Busse et al. (2010) | MktSci | RD at price thresholds; institutional detail about auto retail |
| Elasticity Matrix | Berry, Levinsohn & Pakes (1995) | Econometrica | The original; still the template (though not marketing) |
| Counterfactual Triplet | Nevo (2000) | Econometrica | Merger simulation in ready-to-eat cereal |
| Heterogeneity Cascade | Lambrecht & Tucker (2013) | JMR | When retargeting works (and when it doesn't) |
| CMO Letter | Datta et al. (2017) | JM | How advertising affects brand choice; implications section |

---

## Checklist: Before You Write

- [ ] Does the first paragraph name a real company with real numbers?
- [ ] Is the identification story told before the results (not buried in a data section)?
- [ ] Are the central results presented with both statistical AND economic significance?
- [ ] Does the heterogeneity analysis explain *why* effects vary, not just *that* they vary?
- [ ] Does the implications section speak to a practitioner in their language?
- [ ] Is every pattern appropriate for the target journal's expectations?
