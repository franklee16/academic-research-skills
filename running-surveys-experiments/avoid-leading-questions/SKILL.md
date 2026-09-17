---
name: avoid-leading-questions
description: |
  Use when the user is reviewing or drafting a survey question that may induce demand bias or social desirability.
  Triggers: "is this a leading question?" / "I'm worried about social desirability" /
  "respondents answer what they think I want" / "this question is sensitive" /
  "how do I ask about insider trading / drug use / cheating without people lying?" /
  "I have an evaluative framing in my question".
  Two distinct mechanisms: experimenter demand (strip the framing sentence) and social desirability
  (use list experiments, randomized response, or skip self-report).
  Not for: clarity/abstract-noun issues (use clarity-concreteness); recall problems
  (use survey-design-checklist's "ability" check).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §2.5
tags: [survey, leading-questions, demand-bias, social-desirability]
related_skills:
  - survey-design-checklist
  - clarity-concreteness
---

# Avoiding Leading Questions (demand-bias + social-desirability)

## R — 原文 (Reading)

> "Communicating a questions' intent to participants is likely to influence their responses [...] This could occur for reasons of social desirability or experimenter demand. In the case of social desirability, people want to answer your survey in a way that is socially acceptable, even when this response is not truthful [...] In the case of experimenter demand, participants will try to understand the answer the researcher wanted them to give and be more likely to give that answer [...] asking: 'Academics consider X factor to be very important in investment decisions. To what extent do you consider X in your own investment decisions?' can suggest that the researchers believe that factor X is important [...] Eliminating the first part of that question would largely address this issue. However, researchers should still be cognizant of the fact that asking participants about a select number of factors may indicate their perceived importance from the perspective of the researcher. Therefore, in this example, it would also be useful to include certain factors that you would anticipate being relevant and others that you would anticipate being irrelevant."
>
> — Bergman et al., §2.5

## I — 方法论骨架 (Interpretation)

There are **two distinct biases** that look similar but require different fixes:

| Bias | Mechanism | Default fix |
|---|---|---|
| **Experimenter demand** | Respondent reads researcher intent from context | Strip leading evaluative framing |
| **Social desirability** | Respondent self-censors against an imagined social audience | Use indirect elicitation (list experiments, randomized response, behavioral data) |

**Default fixes for experimenter demand:**
- Cut the lead-in: "Experts say X is important — to what extent do you consider X?" → "To what extent do you consider X?"
- Include *expected-irrelevant* items to catch consistency-seekers — they will rate them similarly to relevant ones, exposing the bias
- Avoid naming the hypothesis before the question

**Default fixes for social desirability:**
- Sensitive behaviors (insider trading, illegal drug use, infidelity, undeclared income): use **list experiments**, **randomized response**, or **behavioral/admin data substitutes**
- *Direct yes/no on a sensitive behavior never produces interpretable data* — the response is at best a "moral floor" of the sample, not a prevalence estimate
- Yes/no confirmation questions ("Did you understand?") are also social-desirability-laden — replace with open-text "what was confusing?"
- **Acquiescence bias** (tendency to say "agree"): rotate the order of "agree" vs. "disagree" anchors; mix positively and negatively-keyed items

## A1 — 书中的应用 (Past Application)

### 案例 1: Insiders-and-academics lead-in (§2.5)
- **问题**: Authors' draft asked "Academics consider X important in investment decisions. To what extent do you consider X?"
- **方法论使用**: Identified it as experimenter demand (the "Academics consider..." sentence broadcasts the expected answer). Removed that sentence. Also added expected-irrelevant factors to catch consistency-bias respondents
- **结论**: Demand-bias removed; consistency-seekers flagged
- **结果**: Items not biased toward "I should care about this"

### 案例 2: "Did you understand?" → open-text (§2.5)
- **问题**: Checking whether respondents actually understood the survey instructions
- **方法论使用**: Replaced yes/no with "Was anything confusing in these instructions? Please explain if so." (open-text)
- **结论**: Got real signal on comprehension by sidestepping social desirability
- **结果**: Surfaced real comprehension issues hidden by the yessing floor

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user has a survey item that contains lead-ins like "Researchers have shown that..." / "Experts believe..." / "Most people think..."
2. The user is asking about behaviors with moral or illegal valence (insider trading, drug use, financial dishonesty, infidelity)
3. The user reports "everyone answers yes/agree" or "everyone says they understand" — acquiescence / social desirability signal
4. The user wants to test respondents' beliefs/predictions about an attitude without priming the answer
5. The user asks "is this question biased?" — common context for this skill

### Language signals

- "leading question" / "leading wording" / "framing effect"
- "social desirability" / "demand bias" / "acquiescence"
- "respondents all say yes" / "everyone agrees"
- "sensitive topic" / "insider trading" / "illegal" / "drug use" / "cheating"
- "How do I ask about a stigmatized behavior?"

### Compared to adjacent skills

- **clarity-concreteness**: addresses *interpretation* problems from abstract nouns; this skill addresses *willingness* and demand-bias problems
- **survey-design-checklist**: upstream gate; this skill is a specific fix when you suspect bias
- **converging-evidence-design**: when you suspect a single-item vulnerability, design multiple items — this skill removes the *bias in the specific item*; converging-evidence designs redundancy

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Classify the question by which bias it's most vulnerable to.**
   - (a) Demand-bias risk: contains evaluative lead-in, primes one direction
   - (b) Social-desirability risk: touches moral/illegal/private behavior
   - (c) Acquiescence risk: yes/no or strongly-agree scale, sits downstream of one-directional items
   - Completion: a classification per question

2. **Apply the default fix for each.**
   - (a) Demand-bias: cut the lead-in sentence. Suggest an alternate item or expected-irrelevant filler items
   - (b) Social-desirability: recommend **list experiments**, **randomized response**, or **substitute behaviorally-measured data** (brokerage records, audit logs, admin data). Never accept a direct yes/no on a sensitive behavior as final
   - (c) Acquiescence: rotate item direction; mix positively and negatively-keyed; balance agree/disagree anchors
   - Completion: each question has either PASS (already clean) or a rewritten version

3. **Add a catch-question for bias-detected designs.**
   - For experimenter-demand items: include 1-2 expected-irrelevant items; if respondents rate them highly, flag the respondent as a consistency-seeker
   - For acquiescence-prone instruments: rotate order across participants
   - Completion: the design includes at least one bias-detection item or randomization

4. **If the topic is so sensitive that even list experiments are unlikely to work, recommend a different method.**
   - Examples: insider trading detection → audit data; drug use prevalence → national-health surveys; financial fraud → regulatory filings
   - Don't push the survey instrument when the construct cannot be measured through self-report

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user's question is abstract-vague, not leading — that's `clarity-concreteness`
- The user has a recall problem (year-scale memory) — that's `survey-design-checklist` (ability)
- The user is asking about *post-hoc* analysis, not question design — defer to `relative-vs-absolute`
- The user is doing interviewing or qualitative work — different bias profile

### Author's warnings

- **Direct questions on insider trading produce a "no" floor.** The paper (§2.5): "if you were to ask: 'Have you ever engaged in insider trading?' most people would answer that they have not, irrespective of the truth."
- **Leading-tone removal is not enough.** Even after stripping the evaluative lead-in, merely *selecting* which factors to ask about primes the researcher-perspective. Authors: "researchers should still be cognizant of the fact that asking participants about a select number of factors may indicate their perceived importance from the perspective of the researcher." Always include expected-irrelevant filler items.
- **Acquiescence is robust.** Authors: "Most people want to be agreeable, which biases them towards responses like 'yes' and 'agree'." Single-question fixes are usually insufficient — instrument-level design (mixing positive/negative items) is the real fix.

### Author era/blind-spot limits

- **Bot-driven and AI-assisted responses** are not addressed. Sensitive items may attract *more* AI-assisted responses than neutral items. Not the skill's job to fix but should be flagged to the user.

### Adjacent confusion

- This skill is sometimes confused with **manipulation checks** (`quality-checks-diagnosis`). Different concerns: demand-bias is in the *question design* (cause: question wording; fix: rewrite). Manipulation checks are in the *experimental design* (cause: treatment that doesn't land; fix: stronger treatment).

## 相关 skills

- **depends-on**: `survey-design-checklist` (one branch of the willingness/interpretation check)
- **composes-with**: `clarity-concreteness` (often co-occurs in the same draft)
- **contrasts-with**: `quality-checks-diagnosis` (which addresses *post-design* checks)

## 审计信息

- **验证通过**: V1 ✓ (§2.5 main, with cross-references to §2.1 sensitive data and §2.7 acquiescence) / V2 ✓ (extends to any sensitive-domain elicitation problem) / V3 ✓ (the two-bias decomposition — demand vs. social desirability — with different fixes is non-obvious to most researchers)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
