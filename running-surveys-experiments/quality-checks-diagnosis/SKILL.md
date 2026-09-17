---
name: quality-checks-diagnosis
description: |
  Use when designing or interpreting survey checks — especially when the user can't tell which check to use.
  Triggers: "should I add attention checks?" / "how many attention checks?" / "is this a manipulation check?" /
  "what's the difference between comprehension and attention check?" / "my respondents are failing checks, what do I do?" /
  "I need to verify my experimental manipulation worked".
  Three diagnostic instruments get conflated: attention check (is respondent paying attention?),
  comprehension check (are instructions clear?), manipulation check (did the experimental treatment land?).
  Different checks have different implications. Excess attention checks bias the sample.
  Not for: design-time question-wording fixes (use clarity-concreteness); operational flow (use pilot-protocol).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §2.7, §3.2
tags: [survey, attention-check, manipulation-check, comprehension-check, diagnostics]
related_skills:
  - pilot-protocol
  - selective-attrition-audit
---

# Quality-Checks Diagnosis (which check, when, why)

## R — 原文 (Reading)

> "Including attention checks throughout your survey can help identify when people have stopped taking your survey seriously [...] attention checks are questions that are not directly relevant to your research question, but can be used to identify if participants are paying attention [...] Reading comprehension checks and manipulation checks can help you confirm whether your survey is being read and interpreted as intended. [...] Participants may be paying attention (e.g., responding correctly to attention checks), but still failing reading comprehension checks in cases where instructions are unclear or confusing. They may be paying attention, but still failing manipulation checks if a key difference across experimental conditions is ineffective at creating intended differences across conditions [...] While failure of attention checks suggests potential concern about participant quality, high failure rates on comprehension and manipulation checks suggests potential concern with the survey instrument itself."
>
> — Bergman et al., §2.7 + §3.2

## I — 方法论骨架 (Interpretation)

Three kinds of diagnostic questions get conflated. They test *different* things and point to *different* fixes:

| Check | Tests | Failure indicates | Fix |
|---|---|---|---|
| **Attention check** | Is respondent paying attention at all? (e.g., "select 'Other' and type 'read'") | Respondent-quality problem (satisficing, professional gaming, bot) | Drop the respondent's data; revisit pay / survey length / fatigue |
| **Comprehension check** | Does respondent understand the instructions? | Instrument problem (instructions unclear) | Rewrite the instructions — *not* the respondent |
| **Manipulation check** | Did the experimental treatment create the intended difference across conditions? | Treatment-design problem (treatment too subtle, control condition not neutral) | Strengthen the manipulation; reconsider treatment-vs-control difference |

A respondent can pass attention but fail comprehension — they're awake but confused; the instructions are wrong.

A respondent can pass attention but fail manipulation — they understood both arms but didn't notice the difference between them. The treatment is too subtle.

A respondent can pass all three but still produce junk data — survey length/pay mismatch (satisficing) or bot/server-farm responses. None of these checks catch that.

**Default settings**:
- 1-2 well-designed attention checks (clear, not trick). Don't pile them in.
- 1-2 comprehension checks at the *introduction of complicated instructions* — i.e., before the construct-relevant items
- 1 manipulation check per treatment arm, asking the respondent to recall or rate the manipulation
- All checks should be **counterbalanced** so position doesn't bias the failure rate

## A1 — 书中的应用 (Past Application)

### Case 1: Differential check-failure diagnosis (§3.2)
- **问题**: Authors had respondents failing checks but unclear whether the issue was respondents, instructions, or treatment
- **方法论使用**: Differentiated attention (→ drop respondent), comprehension (→ rewrite instructions), manipulation (→ strengthen treatment). Used the *kind* of failure to localize the problem
- **结论**: Failure-mode determines which fix
- **结果**: The paper's three-check framework turned one vague problem into three addressable ones

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user asks "should I add attention checks?" or "how many?"
2. The user is reporting that respondents are failing checks and asks "what do I do?"
3. The user has a treatment-vs-control survey and wants to verify the treatment landed
4. The user is choosing between checks and asks "which one do I need?"
5. The user has a survey where check-pass-rate differs across conditions

### Language signals

- "attention check" / "manipulation check" / "comprehension check"
- "instruction check" / "treatment check" / "validation"
- "is my respondent paying attention"
- "check failure rate" / "drop the respondent"
- "did my treatment work"
- "verification question"

### Compared to adjacent skills

- **pilot-protocol**: covers the operational flow (when to test, who to test on). This skill is *which check to use*.
- **selective-attrition-audit**: focuses on the *asymmetric* drop-out across conditions. Different problem; this skill's manipulation check is a pre-launch instrument
- **avoid-leading-questions**: the manipulation check itself can be leading if worded wrong — apply this skill carefully to the check itself

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Classify the user's concern: which failure mode are they suspecting?**
   - (a) Respondents aren't paying attention → attention check needed
   - (b) Respondents don't understand instructions → comprehension check needed
   - (c) Treatment-vs-control arm isn't creating intended difference → manipulation check needed
   - Completion: a classification

2. **Recommend the appropriate check type.**
   - (a) **Attention check**: clear, obvious, *not trick*. Example: "If you are reading carefully, please select 'Other' and enter the word 'read' in the box."
   - (b) **Comprehension check**: ask the respondent about the instructions in their own words; or use multiple-choice covering key facts they should have read
   - (c) **Manipulation check**: ask the respondent to rate or recall the experimental manipulation (e.g., "how risky was the stock described in your scenario?")
   - Completion: each fix produces a specific check example

3. **Specify the count: 1-2 each, no more.**
   - Add: "do not pile attention checks. 1-2 well-placed is better than 5 tricky ones."
   - Add: "counterbalance position so position-in-survey doesn't bias failure rate."

4. **Specify the diagnostic interpretation.**
   - "If attention check fails: drop the respondent, but only if you have ≥2 attention checks and they pass ≥1 of them. Single-check failures can be honest confusion."
   - "If comprehension check fails broadly: rewrite instructions, not respondents."
   - "If manipulation check fails: the treatment isn't landing. Strengthen the manipulation, consider re-piloting."
   - Completion: a written interpretation rule

5. **Flag the un-addressable failure mode.**
   - "None of these three checks catch: bot responses, AI-assisted responding, professional survey-gaming, fatigue-induced satisficing in second-half of survey. For those: see `pilot-protocol`, `fair-pay-and-reputation`"

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user has *post-launch* attrition issues across conditions — that's `selective-attrition-audit`
- The user wants *operational discipline* (when to test, who to test on) — that's `pilot-protocol`
- The user wants to *fix wording* in their items — that's `clarity-concreteness` or `avoid-leading-questions`
- The user is conducting interviews / qualitative work — different check profile

### Author's warnings

- **Excess attention checks bias your sample.** Authors (§3.2): "it is important to recognize that there can be downsides to introducing an excessive number of attention checks. It is possible that going overboard in this direction can actually reduce the quality of your data by introducing bias." Seasoned survey-takers game them; naive respondents drop out.
- **Comprehension checks can be leading.** A comprehension check like "Did you understand the previous instructions?" invites yes-by-default. Use open-text or multiple-choice that tests specific facts
- **Manipulation checks can fail without respondent problems.** A subtle treatment produces low manipulation-check pass rates even among well-engaged respondents. The fix is the treatment, not the respondent

### Author era/blind-spot limits

- The paper's check examples are all from 2020. Modern best practices include more sophisticated checks (e.g., time-on-page heuristics, keystroke dynamics) that the paper doesn't cover
- AI/LLM-assisted responding can defeat straightforward attention and manipulation checks. The paper does not address this

### Adjacent confusion

- This skill is sometimes confused with **measurement validity** (does the survey measure the right construct?). Three checks test *operational* quality — they don't validate construct validity
- This skill is sometimes confused with **pilot protocol**. Different roles: pilot protocol *when* to test; quality-checks-diagnosis *what kind* of test. They compose

## 相关 skills

- **depends-on**: `pilot-protocol` (the operational vehicle for these checks)
- **composes-with**: `selective-attrition-audit` (when check failure rates differ across conditions), `avoid-leading-questions` (the checks themselves must not be leading)
- **contrasts-with**: `clarity-concreteness` (which fixes design-time wording)

## 审计信息

- **验证通过**: V1 ✓ (§2.7 main; §3.2 with full triangulation discussion) / V2 ✓ (extends to any survey check-design problem; the three-check taxonomy is general) / V3 ✓ (the three-check distinction is non-obvious — most researchers conflate them; the failure-mode → fix mapping is the actionable insight)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
