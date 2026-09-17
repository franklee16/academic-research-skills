# Rigorous Evidence in Empirical Finance

## Table of Contents

1. [What Good Evidence Looks Like](#what-good-evidence-looks-like)
2. [Econometric Rigor](#econometric-rigor)
3. [Red-Teaming Your Narrative](#red-teaming-your-narrative)
4. [Baselines and Benchmarks](#baselines-and-benchmarks)
5. [Avoiding Misleading Evidence](#avoiding-misleading-evidence)
6. [Reproducibility](#reproducibility)

---

## What Good Evidence Looks Like

**Good experiments distinguish between hypotheses.** Results should vary significantly depending on which mechanism is true.

**Quality over quantity:** One compelling, hard-to-deny test beats ten weak ones. In finance terms: one clean identification strategy with a clear exclusion restriction beats a dozen ad-hoc regressions.

**Diverse lines of evidence are robust.** Several qualitatively different tests pointing to the same conclusion are stronger than many variations of the same test.

**Example hierarchy for finance evidence:**

| Evidence Type | Strength | Example |
|--------------|----------|---------|
| Causal identification (IV, RD, DiD) | Strong | Exogenous variation in analyst coverage |
| Portfolio sorts with risk adjustment | Strong | L/S spread earns alpha after FF5 |
| Cross-sectional predictions | Moderate | Predictability stronger for high-dispersion stocks |
| Time-series patterns | Moderate | Predictability persists 4 months |
| Correlational panel regression | Weaker | OLS with controls, no identification claim |
| Case studies / examples | Illustrative | Showing specific high/low DS Score reports |

## Econometric Rigor

### Statistical Significance

**Finance conventions differ from ML:**
- Report t-statistics (not p-values as primary)
- Report economic magnitudes alongside statistical significance
- A result can be statistically significant but economically trivial
- Use standard significance levels: * p<0.10, ** p<0.05, *** p<0.01
- Cluster standard errors appropriately (by firm, by time, or double-cluster)
- Newey-West correction for time-series regressions

### Standard Errors

- **Fama-MacBeth**: Report average coefficients and t-stats from cross-sectional regressions
- **Panel regressions**: Double-cluster by firm and time as default
- **Portfolio sorts**: Report t-statistics for alpha from factor models
- **Always state** how standard errors are computed

### Economic Magnitude

Always translate coefficients into intuitive magnitudes:
- "A one standard deviation increase in DS Score is associated with 23% of a standard deviation increase in next-quarter ROA"
- "The long-short spread of 1.33% per month corresponds to approximately 16% annually"
- "This effect is economically comparable to the size premium over our sample period"

### Multiple Testing

- When running many specifications, acknowledge the multiple testing problem
- Bonferroni or Holm adjustments for large numbers of tests
- In practice: if a result is significant in only 1 of 10 specifications, it is not robust

## Red-Teaming Your Narrative

**Assume you have made a mistake. What is it?**

Common vulnerabilities in empirical finance:
- **Look-ahead bias**: Does your variable use information not available to investors at the time? (e.g., LLM training data cutoff)
- **Sample selection**: Does your sample exclude firms that delisted, merged, or had zero coverage?
- **P-hacking**: Did you try many specifications and report only the significant ones?
- **Omitted variables**: Is there an obvious confound you are not controlling for?
- **Data mining**: Would this result survive in a different time period or market?

**Get other researchers to weigh in.** Especially experienced ones who have made these mistakes before.

## Baselines and Benchmarks

**Show your measure improves on plausible alternatives, not just that it works.**

In finance, this means:
- Compare your measure to existing alternatives (e.g., bag-of-words sentiment, analyst revisions, recommendation changes)
- Put meaningful effort into making baselines good -- tune them properly
- If your measure adds predictive power beyond the best existing alternative, that is the result
- If it does not beat a simple alternative, say so honestly

**Common benchmark comparisons:**
- Your text measure vs. simple tone/sentiment scores
- Your alpha vs. standard factor model alphas
- Your portfolio strategy vs. buy-and-hold or momentum
- Your prediction vs. analyst quantitative outputs (forecasts, revisions)

## Avoiding Misleading Evidence

### Pre- vs. Post-Hoc

- Results obtained before formulating your claim are more impressive than post-hoc interpretations
- If you discovered a result by data mining, be honest about it
- Pre-registration or pre-analysis plans add credibility

### Cherry-Picking

- Present randomly selected examples alongside compelling ones
- In finance: report results for the full sample before subsamples
- Do not selectively report only the quintiles or time periods that support your story

### Specification Search

- Report a baseline specification clearly
- Show robustness as a table of alternative specifications
- If the result is sensitive to a specific choice (e.g., lambda in EWMA), show the full range
- Report negative results -- they are informative

## Reproducibility

**Finance-specific reproducibility standards:**
- Share code (Stata/R/Python) for all results
- Provide a clear data construction pipeline from raw data
- Ensure the codebase runs on a fresh machine with standard packages
- Document all data sources, filters, and variable constructions
- Provide a README with links to key resources

**AEA Data Availability Policy compliance:**
- Replication packages must reproduce all tables and figures
- Include analysis datasets if raw data is restricted
- Document all software dependencies
