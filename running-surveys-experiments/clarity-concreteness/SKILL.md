---
name: clarity-concreteness
description: |
  Use on a survey question that the writer thinks is clear but could be ambiguous.
  Triggers: "make this clearer" / "this question feels vague" / "respondents may misread" /
  "fix the wording" / "rewrite this survey item to be unambiguous" / "what do you mean by 'the market'?" /
  "respondents are answering something else".
  Source mechanism: Kahneman & Frederick's attribute substitution. When respondents don't understand,
  they don't say "I don't know" — they answer the clearest *related* question they can find.
  Not for: yes/no leading questions (use avoid-leading-questions); pilot-stage fixes (use pilot-protocol).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §2.4
tags: [survey, question-wording, concreteness, attribute-substitution]
related_skills:
  - survey-design-checklist
  - avoid-leading-questions
---

# Clarity & Concreteness (anti-attribute-substitution)

## R — 原文 (Reading)

> "When selecting questions for your survey, a researcher should carefully consider wording to maximize the probability that participants will answer the question that the researchers believe they are asking [...] if you ask: 'How do you think that the market will perform in the short-term?' participants may have different interpretations of both 'market' and 'the short-term'. Instead, a better way to ask the question would be: 'The S&P index's current value is $XX. What do you think the change in the S&P 500 index's value will be between today and one month from today (DD/MM/YY)?' [...] In cases where participants do not understand the question, but try to answer accurately, they may engage in attribute substitution. This occurs when people reply to a complicated question with the answer to a simpler one."
>
> — Bergman et al., §2.4

## I — 方法论骨架 (Interpretation)

**Every abstract noun in a survey question is an invitation to attribute substitution.** The respondent doesn't say "I don't know what 'the market' means"; they answer the question as if "the market" meant whatever-it-makes-sense-to-mean-in-the-moment. They're being sincere about a different construct.

The fix is *not* "say it more clearly in general" — concreteness is a substitution game:

| Abstract word | Concrete replacement |
|---|---|
| "the market" | "the S&P 500 index" |
| "short-term" | "today to one month from today (DD/MM/YY)" |
| "important factor in investment decisions" | "your top-3 considerations when choosing a stock" |
| "your finances" | "your liquid checking + savings account balance" |
| "recently" | "in the last 7 days" |

Once you've replaced all abstract nouns with named, dated, denominated references, run a stress test: *could two reasonable respondents interpret the question differently?* If yes, the wording still has an attribute-substitution risk.

Two related fixes: (a) yes/no comprehension checks → replace with "what was confusing?" (open text); (b) bracketed ranges for personal finance questions (privacy + clarity combined).

## A1 — 书中的应用 (Past Application)

### 案例 1: "How will the market perform?" → named-index replacement (§2.4)
- **问题**: The first version of the question had ambiguous "market" and ambiguous "short-term"
- **方法论使用**: Replaced both with named and dated references: S&P 500, today → one month from today, response as percent change
- **结论**: Unambiguous question; respondents can't misread
- **结果**: Answers interpretable relative to other similar items

### 案例 2: "Did you understand the instructions?" → open-text fix (§2.5)
- **问题**: Was respondents actually understanding the survey?
- **方法论使用**: Replaced yes/no with open-text "Was anything confusing in these instructions? Please explain if so."
- **结论**: Got real signal on comprehension by sidestepping social desirability
- **结果**: Surfaced real comprehension issues that yes/no had hidden

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user shows a draft survey item and says "is this clear enough?" — run concreteness replacement
2. The user describes responses that don't make sense — "respondents all said X but I asked about Y" — likely attribute substitution; this skill should diagnose
3. The user uses abstract nouns in survey text ("recently", "the market", "your finances", "important factor")
4. The user has a survey where scores pile up at extremes (everything "agrees" / "strong yes") — sign of comprehension failure, often concreteness-driven
5. The user asks "how do I shorten this question without losing precision?"

### Language signals

- "This question feels vague" / "respondents don't seem to get it"
- "Why is everyone picking the same answer?"
- "How do I rephrase this question?"
- "Some respondents misinterpret"
- "The question wording"
- Abstract nouns in the user's draft: market, recent, important, your situation, performance, etc.

### Compared to adjacent skills

- **survey-design-checklist**: fires upstream, before any question is written; this skill fires after the question has abstract language that needs replacement
- **avoid-leading-questions**: addresses *willingness* and demand-bias. They often co-occur (a leading question usually also has substitution risk), but the fixes differ. Concreteness replaces abstract nouns; avoiding-lead strips evaluative framing.
- **pilot-protocol**: catches clarity bugs at small scale; this skill catches them at design time before any respondent sees them

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Extract every abstract noun from the user's question(s).**
   - Completion: a list like `[market, short-term, important factor, your situation]`

2. **Replace each abstract noun with a named concrete reference.**
   - Pattern: "the [INDEX NAME]" / "between [DATE A] and [DATE B]" / "[N-th percentile] of [DENOMINATOR]" / "your top-3 [CATEGORY]"
   - For sensitive items (income, exact holdings), use bracketed ranges, not point values
   - Completion: every abstract noun has a concrete replacement or a bracketed option

3. **Run the dual-interpretation stress test.**
   - Ask: "Could two reasonable respondents interpret the reworded question differently? If yes, what's the source of ambiguity?"
   - If yes → another concreteness pass on the residual source
   - If no → proceed to step 4
   - Completion: a yes/no judgment on dual-interpretation, with reason if yes

4. **For sensitive or rare behaviors, also add brackets.**
   - Dollar amounts: ranges
   - Frequency: time-bounded recall (last week, not last year)
   - Completion: every sensitive item has brackets

5. **For comprehension checks**, replace yes/no with "what was confusing?" open text.
   - Same applies if the survey was checking "did you find any issues?"

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user's question is concrete but asks for a *prediction* (probabilities, forecasts) that the literature shows is unstable → defer to `relative-vs-absolute`. Concreteness won't fix that problem.
- The user is asking about a question that cannot be elicited reliably by *any* survey wording — e.g., "why did you make this decision last year?" (introspection-illusion; Nisbett & Wilson 1977). Acknowledge: no wording fix gets reliable data here. Use field data or skip the construct.
- The user has a *platform* issue (bots, professional survey-takers), not a wording issue
- The user wants to *add* questions to a survey rather than fix existing wording — this skill doesn't design, it refines

### Author's warnings

- **Concreteness does not fix interpretation-illusion.** Authors: "if you ask a question about how context affected a decision-making process [...] participants are unlikely to be able to access the relevance of the context and therefore will be unable to report it to you. [...] This type of question cannot be merely reworded, but requires field data or a more complicated experimental design." (§2.1)
- **Concreteness does not fix sensitivity.** Income can be concretely asked ("what was your household income last year?") but the answer is unreliable for willingness reasons. Use brackets regardless.

### Author era/blind-spot limits

- The 2020 paper does not address *AI-assisted responses*. Open-text responses may now be partly LLM-generated. This skill cannot fix that — defer to operational/IRB-level screening.

### Adjacent confusion

- This skill is sometimes mistaken for "make my survey more readable." Readability ≠ concreteness. Concreteness is *substitution-prevention*, not style.

## 相关 skills

- **depends-on**: `survey-design-checklist` (this skill is one branch of the umbrella)
- **composes-with**: `avoid-leading-questions` (often co-occurs)
- **contrasts-with**: `relative-vs-absolute` (which addresses the level-vs-comparison problem that concreteness cannot fix)

## 审计信息

- **验证通过**: V1 ✓ (§2.4 main; cross-references to §2.1 and §2.5 in the paper) / V2 ✓ (extends to any survey construct using abstract nouns) / V3 ✓ (Kahneman-Frederick's attribute-substitution framework is genuinely non-obvious and load-bearing here)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
