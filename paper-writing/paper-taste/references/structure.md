# Paper Structure for Empirical Finance

## Table of Contents

1. [Abstract](#abstract)
2. [Introduction](#introduction)
3. [Background / Institutional Setting](#background)
4. [Data](#data)
5. [Empirical Strategy / Methodology](#empirical-strategy)
6. [Results](#results)
7. [Robustness](#robustness)
8. [Conclusion](#conclusion)
9. [Related Work Placement](#related-work-placement)

---

## Abstract

The abstract is a self-contained TL;DR of the entire paper.

**Sentence-by-sentence template:**

1. **Context** (uncontroversial): "Analyst reports are a primary channel through which information reaches equity markets."
2. **Gap / motivation**: "However, the textual content of these reports is typically reduced to simple sentiment scores, discarding much of the qualitative information analysts provide."
3. **What you do**: "We use a large language model (DeepSeek) to score the full text of 394,328 analyst reports covering 3,799 Chinese A-share firms from 2011 to 2019."
4. **Key result** (concrete metric): "A long-short portfolio sorted on this score earns value-weighted returns of 1.33% per month (FF5 alpha = 1.25%)."
5. **Mechanism / implication**: "The predictability is stronger for stocks with high analyst forecast dispersion and high institutional ownership, consistent with textual information resolving investor uncertainty."

**Rules:**
- 150 words or fewer (most journals enforce this)
- Include at least one concrete number
- No citations in the abstract
- No undefined jargon or acronyms

## Introduction

The introduction is an extended abstract with narrative flow.

**Paragraph structure for empirical finance:**

| Paragraph | Content | Finance Example |
|-----------|---------|----------------|
| P1 | Context and motivating question | Why analyst reports matter |
| P2 | What we know / literature gap | Existing text analysis is limited to bag-of-words |
| P3 | What this paper does | We use DeepSeek to score report text |
| P3.5 | Key evidence | L/S portfolio earns 1.33%/month |
| P4 | Mechanism / why it works | Stronger for high-dispersion stocks |
| P5 | Contribution / implications | Bridging NLP and asset pricing |

**End with a contribution list:**
> Our contributions are as follows. First, we [...] Second, we document that [...] Third, [...]

**Finance introduction conventions:**
- State the research question explicitly in the first or second paragraph
- Preview the main empirical strategy
- Report the headline number early (don't save it for page 10)
- Contribution list at the end is standard and expected

## Background

Explain all concepts required for understanding the empirical design. In finance papers, this is often "Institutional Setting" or "Literature Review."

- Provide institutional context readers need (e.g., how the Chinese A-share market works, what analyst reports look like)
- Define key terms and data sources
- Review relevant literature with compare-and-contrast, not just descriptions
- Related work can come here or after main results -- both are acceptable

**Rule:** Readers have less context than you think. Err toward explaining.

## Data

Finance papers typically have a dedicated data section.

**Standard elements:**
- Sample construction: time period, exchanges, filters applied
- Summary statistics (Table 1)
- Variable definitions (in text or appendix)
- Data sources (CSMAR, WIND, Datayes, etc.)
- Sample size at each stage of filtering

**Common mistakes:**
- Describing data construction without stating the final sample size
- Not reporting summary statistics
- Defining variables inconsistently between text and tables

## Empirical Strategy

This section presents the identification approach.

**Standard elements:**
- Estimation equation(s) with all subscripts clearly defined
- Identification assumptions stated explicitly
- Fixed effects structure explained
- Expected signs and economic interpretation

**Finance conventions:**
- Present the baseline specification clearly before discussing alternatives
- State the econometric method (Fama-MacBeth, panel regression with double-clustered SE, etc.)
- Explain why this specification identifies the causal effect of interest
- Discuss threats to identification upfront

## Results

Present results in order of importance, not order of convenience.

**Standard flow:**
1. Baseline results (portfolio sorts or main regression)
2. Economic magnitude interpretation
3. Cross-sectional variation (heterogeneity tests)
4. Mechanism evidence
5. Additional tests

**For each result, provide:**
- What you estimated
- The coefficient or return spread with statistical significance
- Economic interpretation ("A one standard deviation increase in DS Score is associated with...")
- Comparison to related findings in the literature

## Robustness

Either a standalone section or integrated into Results.

**Standard robustness checks in finance:**
- Alternative variable construction (different windows, different lambda)
- Alternative model specifications (different fixed effects, controls)
- Sub-sample stability (different time periods, market conditions)
- Placebo tests (shuffled treatment, pre-period)
- Addressing specific concerns raised by the literature

**Rule:** Report robustness in a dedicated table. Don't scatter it across the text.

## Conclusion

**Standard finance conclusion structure:**
1. Restate the main finding (2-3 sentences)
2. Summarize key evidence
3. Discuss implications (theoretical or practical)
4. State limitations honestly
5. Suggest future work (optional)

**Avoid:**
- Introducing new results not discussed earlier
- Restating the abstract verbatim
- Overclaiming ("our results definitively prove...")

## Related Work Placement

Two conventions are acceptable:

1. **After Introduction** (traditional): Good when the paper builds on a specific literature
2. **After Results** (growing preference): Good when the paper's novelty is methodological and readers need results to understand the comparison

Choose based on what helps the reader most. Be consistent within the paper.
