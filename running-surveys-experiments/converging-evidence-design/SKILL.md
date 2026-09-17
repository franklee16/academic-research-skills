---
name: converging-evidence-design
description: |
  Use when the user is designing a survey and using single items per construct, OR when the user has
  survey results that they suspect are unreliable but can't pinpoint why.
  Triggers: "I'm using one item to measure X — is that enough?" /
  "should I have multiple items per construct?" / "I want a robustness check for my survey" /
  "my survey result looks fragile" / "I want to validate this finding with another question".
  Default: For every survey hypothesis, design at least 2 items using *different elicitation methods*
  (state vs. choose, recall vs. infer, abstract vs. concrete, or different framings of the same construct).
  Not for: experimental-design robustness (treatment vs. control arms); survey-mechanics fixes
  (use pilot-protocol).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §2.3
tags: [survey, robustness, triangulation, multi-item]
related_skills:
  - relative-vs-absolute
  - clarity-concreteness
---

# Converging-Evidence Design (Multi-Item per Construct)

## R — 原文 (Reading)

> "When possible, survey experiments can be designed more effectively when there are multiple question types that can be compared against one another [...] That way, if there are concerns about a specific question type (e.g., question framing), an alternative question type (e.g., with a different question framing) testing the same hypothesis can be used to provide additional support for the overall results. Further, if there is an unusual response to one line of questioning, a researcher can cross-validate the result by comparing it to the answers of other question types."
>
> — Bergman et al., §2.3

## I — 方法论骨架 (Interpretation)

A single survey item has many failure modes (wording, framing, anchoring, social desirability, comprehension). If you measure a hypothesis with one item, *any* of those failure modes can be your entire result.

The fix is **converging evidence**: measure the same construct with at least **two items** using **different elicitation methods**, and cross-check them. The point isn't redundancy — it's *error-source diversity*. If both items measure roughly the same thing via different methods, you can attribute agreement to the construct (good) and disagreement to one of the methods (diagnostic).

Common elicitation methods to mix:

| Method | What it captures | What it doesn't |
|---|---|---|
| Stated preference ("describe your strategy") | Elicited reasoning, narrative | Susceptible to social desirability |
| Stated choice (forced-choice between options) | Revealed preference, less narrative | Susceptible to response-set effects |
| Recall ("how many times in last N days did you X") | Recent behavior | Susceptible to memory |
| Inference ("if you faced X, what would you do") | Hypothetical, can probe counterfactuals | Susceptible to demand-bias |
| Probability scale ("what's the chance you'll do X") | Forecasts | Susceptible to anchoring/calibration |
| Behavioral / revealed (admin or audit data) | Real behavior | Not feasible for many constructs |

A useful pattern is **state vs. revealed**: ask respondents to *describe* their behavior, then ask them to *make* behaviorally-equivalent decisions. Stated-revealed gaps are themselves a finding, not noise.

## A1 — 书中的应用 (Past Application)

### Case 1: Chinco et al. stated strategies vs. revealed allocation (§2.3)
- **问题**: Authors wanted to know how investors make allocation decisions
- **方法论使用**: Two question types — state your strategy (narrative), then make allocation choices in scenarios. Cross-check the same respondent's stated strategy against their revealed choices
- **结论**: Stated-revealed consistency was the metric. Inconsistent respondents (state X, choose Y) became a *finding*
- **结果**: Two question types per construct allowed triangulation. Without the second item, the inconsistency could not have been identified.

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user has one survey item per construct and is reporting a result
2. The user asks "how do I make my survey result more credible"
3. The user has run a survey but suspects one item's framing is contaminating the result
4. The user wants to test the *consistency* of respondents across survey sections
5. The user is designing a new survey and starting from scratch

### Language signals

- "I have one item for X" / "I want a robustness check"
- "triangulate" / "converging evidence" / "multiple measures"
- "is one item enough?" / "validate this"
- "stated vs. revealed" / "stated vs. choice"
- "I have a result but only one question"

### Compared to adjacent skills

- **relative-vs-absolute**: the *interpretation* side. `converging-evidence-design` is the *design* side. Together they cover the full pipeline: design 2 items → interpret relative claim with potential to upgrade to level.
- **clarity-concreteness**: fixing one abstract item. `converging-evidence-design` adds redundancy across items, not within an item.
- **avoid-leading-questions**: addresses bias in *one* item; this skill protects the *hypothesis* by using multiple items.

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Enumerate the user's current items per construct.**
   - For each construct in the user's design, count items and methods
   - Completion: a construct-by-method table

2. **Identify constructs with single items.**
   - These need a second item using a *different method* (state vs. choose, recall vs. infer, etc.)
   - Construct the second item using one of: stated-choice, recall, inference, probability-elicitation, behavioral data — anything that doesn't share the failure mode of the first
   - Completion: each construct has at least 2 items across 2 methods

3. **For sensitive constructs, recommend behavioral/admin data substitute.**
   - E.g., actual brokerage holdings rather than self-reported allocations; audit logs of financial decisions
   - Don't rely on multi-item survey design if the construct is so sensitive that *every* self-report is biased. The proper fix is to remove self-report from the chain
   - Completion: explicit replacement where behavioral data exists

4. **Recommend the order in which items appear.**
   - Place the *primary* item before the *converging* item — so the second item doesn't anchor on the first
   - Completion: an ordering rationale
   - Note: this can also be addressed by counterbalancing via randomization; see `pilot-protocol`

5. **In post-collection analysis, define the consistency-metric.**
   - For each respondent: agreement between Item-1 and Item-2 (correlation, agreement rate, stated-revealed delta)
   - Completion: an analytical plan for cross-item consistency

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user has experimental robustness needs (treatment vs. control arms). That's a different concern — sampling randomization, not item-redundancy. Use experimental-design literature.
- The user has *construct*-validity issues — measuring the wrong construct. Multi-item won't fix a flawed construct.
- The user is constrained by survey length and the construct is well-established. Adding a second item costs respondent time and may push fatigue

### Author's warnings

- **Two items using the same method is not converging evidence.** Two Likert-agreement scales about the same construct via the same wording except tense are redundancy, not convergence. Convergence requires *method diversity*
- **Convergence doesn't fix bias shared across items.** Authors (§2 intro): "we refer to meaningful responses as those that would be likely to convince critical readers who are knowledgeable about survey methods that your hypothesis either is or is not correct." If bias is systematic across items (e.g., all questions load on social desirability), convergence within that bias is not convergence

### Author era/blind-spot limits

- Construct-by-item tables from psychometric traditions (Cronbach's alpha, inter-item reliability) are not in the paper. Modern psychology-survey work would check internal consistency; this skill recommends the qualitative version but not the formal psychometric test
- AI-assisted responding: multiple items per construct may be more expensive to AI-generate, slightly mitigating low-effort AI responses. Not addressed in the paper

### Adjacent confusion

- This skill is **not** about test-retest reliability. Test-retest asks "would the same item produce the same answer in different samples?" Converging-evidence asks "do different methods produce the same answer in the same sample?"

## 相关 skills

- **depends-on**: `survey-design-checklist` (this is multi-construct design; the umbrella provides per-constraint gates)
- **composes-with**: `relative-vs-absolute` (interpretation-side complement), `clarity-concreteness` (each item should still be clear)
- **contrasts-with**: `pilot-protocol` (which checks the *whole instrument*, not the per-construct redundancy)

## 审计信息

- **验证通过**: V1 ✓ (§2.3 main with worked example and direct cross-reference; §2.2 benchmark-item logic overlaps) / V2 ✓ (extends to any survey construct with single-item vulnerability) / V3 ✓ (the survey-design analog of robustness checks; under-used in empirical economics; the paper specifies the *method-diversity* requirement, which is the non-obvious bit)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
