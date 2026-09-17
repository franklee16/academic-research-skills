# Narrative and Claims

## Table of Contents

1. [What Makes a Good Narrative](#what-makes-a-good-narrative)
2. [Crafting Claims](#crafting-claims)
3. [Finding Your Narrative](#finding-your-narrative)
4. [Novelty and Positioning](#novelty-and-positioning)
5. [Finance-Specific Guidance](#finance-specific-guidance)

---

## What Makes a Good Narrative

A paper should present a narrative of one to three specific concrete claims that you believe to be true, building to useful takeaways. Everything else exists to support this narrative. The second pillar is rigorous evidence for why these claims are true.

**Four jobs of a narrative:**
- Motivate why someone should care about these claims
- Contextualize them in existing literature
- Communicate them precisely with all relevant technical detail
- Provide sufficient evidence to support them

## Crafting Claims

**One strong claim with rigorous evidence can be enough for a great paper.**

If you have multiple claims, choose ones that fit together in a cohesive theme. In empirical finance, typical claim structures:

- **Predictability claim**: "DS Score predicts monthly returns up to 4 months ahead, beyond quantitative analyst outputs."
- **Economic mechanism claim**: "The predictability is stronger for stocks with high analyst dispersion, consistent with textual information resolving uncertainty."
- **Practical value claim**: "A long-short portfolio based on DS Score earns 1.33% per month (FF5 alpha = 1.25%)."

**Claim confidence spectrum (finance version):**

| Confidence Level | Example | Evidence Required |
|-----------------|---------|-------------------|
| Existence proof | "Textual information has predictive power" | One clean, robust test |
| Systematic claim | "DS Score predicts returns across all size quintiles" | Cross-sectional tests, sub-samples |
| Causal claim | "Textual tone causes price revision" | Identification strategy, IV, or natural experiment |
| Magnitude claim | "A 1 SD increase in DS Score raises next-quarter ROA by 23% of a SD" | Precise estimates with confidence intervals |

Stronger claims require stronger evidence. Adjust confidence to match what your identification strategy supports.

## Finding Your Narrative

**Key questions:**
- Which results would be most exciting to show a colleague at lunch?
- What seems particularly important? Why should anyone care?
- What was hard about what you did that perhaps no one else has done?
- If you had 60 seconds to describe the paper, what would you say?

**Finance-specific framing:**
- Does this paper tell a fund manager something actionable?
- Does it resolve a debate in the literature?
- Does it introduce a new methodology or data source that others will use?

## Novelty and Positioning

**Be extremely clear about what is and is not novel**, especially in the introduction and related work.

- Liberally cite relevant papers and explain how your work differs
- Depending on how novelty is framed, the same paper could seem arrogant or modest
- In finance, incremental contribution is fine -- but state it honestly

**Positioning mistakes to avoid:**
- Claiming "no one has studied X" when papers exist -- search thoroughly first
- Using a straw-man version of prior work to make yours look better
- Overstating how different your approach is from existing methods

**Good positioning examples:**
- "While [Author] examines analyst tone using bag-of-words, we use an LLM that captures semantic content."
- "Our work extends [Author] by testing whether the predictability survives after controlling for quantitative analyst outputs."

## Finance-Specific Guidance

**The contribution statement:** Finance papers typically state contributions explicitly in the introduction, often as numbered items. Each should name the claim and reference the supporting evidence.

**Example structure:**
> This paper makes three contributions. First, we show that [claim 1], using [evidence 1]. Second, we document that [claim 2], which is important because [motivation]. Third, we demonstrate that [claim 3], providing practical implications for [audience].

**Three tests for your narrative:**
1. **The elevator test**: Can you state the main claim in one sentence?
2. **The skeptic test**: Would a referee at [top journal] find the claim interesting and the evidence convincing?
3. **The so-what test**: Does the claim change how anyone thinks about the topic?
