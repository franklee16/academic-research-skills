---
name: relative-vs-absolute
description: |
  Use when the user is analyzing/interpreting survey results and unsure what conclusions to draw.
  Triggers: "can I interpret this level?" / "is this probability meaningful?" / "my result is X%, can I claim Y?" /
  "respondents answered differently when I rewrote the question" / "is order of questions affecting my results?" /
  "my survey shows a level but only cross-condition comparison is interpretable".
  Default rule: Levels are framing-fragile (anchor/order/scale shifts can move them); relative comparisons
  (A vs. B) are robust as long as framing is held constant.
  Add benchmark items to upgrade relative → absolute.
  Not for: pre-launch design fixes (use clarity-concreteness); post-launch attrition issues
  (use selective-attrition-audit).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §2.2
tags: [survey, interpretation, levels-vs-comparisons, framing]
related_skills:
  - converging-evidence-design
  - clarity-concreteness
---

# Relative vs. Absolute Interpretation

## R — 原文 (Reading)

> "As a general rule when constructing surveys, the researcher should assume that participants will be able to accurately report certain coarse facts [...] However, participants may not be accurate when reporting more detailed levels [...] One way to think about the likelihood that participants will give you valuable responses in absolute terms is to consider whether the response is likely to change if the question were framed differently or the context were different [...] Thus, surveys are often most useful in determining relative, but not absolute, levels [...] One way to shift from pure relative comparisons to conclusions about levels is to include questions that you would expect participants to respond to as a benchmark of comparison."
>
> — Bergman et al., §2.2

## I — 方法论骨架 (Interpretation)

Most surveys produce *two kinds of conclusions*:

| Conclusion type | Robustness | Required evidence |
|---|---|---|
| **Relative comparison** (A > B) | Robust to framing if ordering/framing is randomized across A and B | Order randomization or balanced framing |
| **Absolute level** ("X% of investors do Y") | Fragile; framing/scale/anchoring can move it materially | Benchmark items that should clearly register |

The default reading of survey data should be **relative**. When you want to claim an absolute level, you have to earn it: design your survey with **benchmark items you expect to register clearly**, and show those benchmarks register in expected ways. If a benchmark fails to register, the absolute-level claim becomes suspect — your instrument may be broken.

A practical rule of thumb before reporting any level:
1. **Was the question worded identically across the comparison items?** (or randomized in order?)
2. **Was the respondent pool the same across items?**
3. **Does the level change materially with rewording?** (Sensitivity test)
4. If any of these is "no" or unknown → don't trust the level; report the comparison only.

## A1 — 书中的应用 (Past Application)

### Case 1: Chinco et al. (2020) — risk-factor correlations benchmark (§2.2)
- **问题**: Authors wanted to claim whether laypeople care about risk-factor correlations
- **方法论使用**: Designed benchmark items (means, volatility) that should clearly register if the survey is functioning; included correlations as the target item
- **结论**: Means and volatility registered (people said they care about them). Correlations did not register (people said they don't consider them)
- **结果**: Because the benchmarks registered, the authors could claim a meaningful *level* result (people don't care about correlations), not just a relative comparison

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user reports a survey result with a number ("X% of respondents said Y") and asks if they can claim a population-level prevalence
2. The user compares two survey conditions and wants to know whether their treatment effect is real
3. The user asks "is this survey result affected by question order?"
4. The user wants to use a single survey item to assert an absolute level (e.g., "60% of investors are risk-averse")
5. The user has run an A/B test with rewording and got different levels

### Language signals

- "what does this number mean" / "can I claim X%?"
- "this level is fragile" / "the level changed when I reworded"
- "is this an absolute or relative comparison"
- "order effects" / "framing effects" / "anchor effects"
- "benchmark items"

### Compared to adjacent skills

- **converging-evidence-design**: addresses the *design* side of relative-vs-absolute. This skill is the *interpretation* side. If you need to upgrade relative→absolute, `converging-evidence-design` tells you what to add to the design; this skill tells you what to claim from the data
- **clarity-concreteness**: a clarity fix can shift the level, but the level was fragile anyway. `clarity-concreteness` fixes wording; this skill fixes *what conclusions you can draw*
- **selective-attrition-audit**: condition-asymmetric drop-out also threatens comparisons. Different mechanism.

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Identify the claim type the user wants to make.**
   - Is it an absolute level claim ("X% of population does Y")?
   - Is it a relative comparison (treatment vs. control, A vs. B)?
   - Is it a correlation between items?

2. **For each item that supports the claim, test the three robustness checks.**
   - (a) Question wording identical or randomized across items
   - (b) Respondent pool identical or randomized across items
   - (c) Sensitivity to rewording tested (any prior pilot or sensitivity run?)
   - Completion: a judgment per check (yes/no/unknown)

3. **If any check fails and the user is claiming a level, downgrade the claim.**
   - Claim becomes: "in this instrument, the ranking of X > Y is preserved" — not "X > Y in population"
   - Or: "we see this difference *given* the specific questions we asked, with this specific framing"
   - Completion: a revised-claim text that survives robustness failure

4. **For level claims, recommend a benchmark check.**
   - "If your study is the only instrument, you need to add a benchmark item — but if data is already collected, post-hoc you can only flag this as a limitation in write-up."
   - Pre-design: see `converging-evidence-design` for how to add benchmarks
   - Post-analysis: write the level-claim limitation into the paper, recommend replication with rewording
   - Completion: explicit framing of the limit

5. **For comparisons, recommend reporting the asymmetry audit.**
   - Cite `selective-attrition-audit`: confirm drop-out / check-pass rate is symmetric across comparison arms before claiming a treatment effect

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user's question is about *design* (they haven't run the survey yet). Use the design-layer skills.
- The user's concern is *platform / sample composition*, not interpretation. Use `platform-selection`.
- The user is interpreting a result that is actually stable across rewordings — do not over-apply this skill and force them to downgrade

### Author's warnings

- **Levels are rarely interpretable from a single instrument.** Authors: "the goal of a survey is to understand comparisons across items [...] surveys are often most useful in determining relative, but not absolute, levels." Don't accept the level-claim by default.
- **Benchmark check is the only way to upgrade relative→absolute.** Even with benchmarks, only positive benchmarks can do it. If the benchmark fails to register, *all* level claims are suspect.

### Author era/blind-spot limits

- The paper does not address how LLM/AI-assisted responding changes absolute vs. relative. Preliminary: AI-assisted responding likely shifts both but probably distorts levels more than comparisons (since each response is a one-off, not a paired comparison).

### Adjacent confusion

- This skill is sometimes confused with **measurement-validity** (does the survey measure the construct it claims to measure). Different concerns: measurement-validity is about construct; this skill is about *level vs. comparison reliability* given an assumed construct.

## 相关 skills

- **depends-on**: none (interpretation skill; fires after data is in hand)
- **composes-with**: `converging-evidence-design` (multi-item setup feeds this interpretation), `selective-attrition-audit` (condition-symmetric attrition audit)
- **contrasts-with**: `clarity-concreteness` (design-time vs. interpretation-time)

## 审计信息

- **验证通过**: V1 ✓ (§2.2 main with multiple example rewordings; §2.4 concreteness treatment cross-references) / V2 ✓ (extends to any survey comparing across items) / V3 ✓ (the levels-are-fragile default view is counter-cultural to most economists; the relative-vs-absolute distinction is load-bearing here)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
