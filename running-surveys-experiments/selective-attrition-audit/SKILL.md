---
name: selective-attrition-audit
description: |
  Use AFTER the survey has been fielded and the user is analyzing results, OR as a pre-launch diagnostic
  (does the design risk differential drop-out?).
  Triggers: "my treatment arm has more dropouts" / "is the completion rate different across conditions?" /
  "I have asymmetric missing data" / "different pass-rates across groups" / "internal validity audit" /
  "I want to check whether my comparison is still random".
  Default audit: Compare (a) completion rate per condition, (b) attention-check pass-rate per condition,
  (c) response-time distribution per condition, (d) demographics per condition. If any differs,
  the comparison is confounded with respondent type.
  Not for: pre-design (use survey-design-checklist); instrument-interpretation (use relative-vs-absolute).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §3.2
tags: [survey, attrition, internal-validity, audit]
related_skills:
  - pilot-protocol
  - quality-checks-diagnosis
---

# Selective-Attrition Audit (Condition-Asymmetric Drop-Out)

## R — 原文 (Reading)

> "When filtering participants for any reason (or when participants drop out of the survey on their own), beware of selective attrition. When analyzing responses, check to see whether the pass-rate on checks, as well as the completion rate for the survey, is consistent across experimental conditions."
>
> — Bergman et al., §3.2, citing Zhou & Fishbach (2016)

## I — 方法论骨架 (Interpretation)

Survey drop-out is not random. The respondents who drop out of your treatment arm vs. your control arm can differ systematically — in patience, conscientiousness, comfort with the topic, time-pressure, etc. When that happens, your treatment-vs-control comparison is no longer between *two random samples from the same population*. It's between *treatment-arm-survivors* and *control-arm-survivors*. These two groups differ in some unobserved way that's confounded with your treatment.

The standard audit is to compare four distributions across experimental conditions:

1. **Completion rate** (did they finish?)
2. **Attention-check pass-rate**
3. **Response-time distribution** (median time-on-survey)
4. **Demographics** (age, gender, education if collected)

If any of these differs across conditions by more than a small amount, the comparison's internal validity is at risk.

Even a *small* asymmetry matters. Random assignment fixes balance on the *expected value*; what survives is a sample, and samples have noise. But a *large* asymmetry (e.g., 20% completion in treatment, 50% in control) is almost always differential attrition, not noise.

**Pre-emptively**: if your treatment is hard / long / uncomfortable, you should expect differential drop-out. Strategies to mitigate: (a) keep treatment short, (b) explicitly say upfront the survey has multiple parts with different lengths, (c) offer pay-up-front to reduce selective quitting.

## A1 — 书中的应用 (Past Application)

### Case 1: Zhou & Fishbach (2016) on selection via "unattended"
- **问题**: Authors warn that dropping-out participants are different
- **方法论使用**: Recommend always-on reporting of pass-rate per condition, completion per condition
- **结论**: Asymmetry is a quietly fatal confound
- **结果**: Surveys with asymmetric drop-out produce estimates that don't replicate

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user has survey data and asks "how do I know my comparison is valid?"
2. The user reports asymmetric drop-out or check-pass-rate across conditions
3. The user is pre-launch and asks "what should I check after launch?"
4. The user's design has treatments of different lengths or difficulty and they want a pre-emptive risk assessment
5. The user gets a reviewer comment about "selective attrition" or "differential exclusion"

### Language signals

- "selective attrition" / "differential drop-out"
- "asymmetric completion rate" / "condition asymmetry"
- "internal validity" / "comparison is confounded"
- "treatment completion vs control completion"
- "missing data pattern" / "MAR vs. MNAR"
- "respondent quality differs across arms"

### Compared to adjacent skills

- **pilot-protocol**: the operational probe that should catch asymmetries at small scale. This skill is *post-pilot diagnosis* and *post-launch confirmation*
- **quality-checks-diagnosis**: per-item checks. This skill is at the *condition* level — comparing across arms
- **relative-vs-absolute**: this skill's audit supports the validity of the relative comparison the user might want to claim. They compose

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Identify the experimental conditions (or comparison groups) and the comparison the user wants to make.**
   - Completion: a clear contrast (e.g., "treatment vs. control", "Stock-A condition vs. Stock-B condition")

2. **Run the four-distribution audit per condition.**
   - (a) Completion rate (% who finished the survey)
   - (b) Attention-check pass-rate (% who passed all attention checks)
   - (c) Median (or distribution of) total response time
   - (d) Demographic distribution (at minimum: age, gender, education)
   - Completion: a table with condition as columns and metric as rows

3. **Test each row for significant asymmetry.**
   - For categorical (pass-rate, completion): chi-square or proportion test
   - For continuous (response time): t-test or rank-sum
   - For demographic balance: standardized mean difference (SMD) — flag SMD > 0.1 as concerning
   - Completion: each row marked SYMMETRIC / ASYMMETRIC, with effect size

4. **Decide the audit verdict.**
   - If all four are SYMMETRIC → comparison's internal validity is preserved
   - If any are ASYMMETRIC → warn:
     - The comparison is confounded with respondent type
     - User should reweight or restrict analyses (with sensitivity analyses)
     - Or treat as a finding worth investigating (e.g., your treatment repels certain respondent types — that's an actual result)
   - Completion: a verdict (CLEAN / COMPROMISED) with adjustment options if COMPROMISED

5. **Pre-launch variant: assess design risk.**
   - If the user is checking *before* launch, ask: are treatments of different lengths? Different difficulty? Different topics?
   - If yes: predict the asymmetry direction (e.g., long treatment → more drop-out) and propose a length-matching or compensation design
   - Completion: a risk assessment + mitigation plan

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user has *no condition structure* — single-arm descriptive survey. Attrition still matters, but the audit has nothing to compare against
- The user is doing *experimental randomization*, not a survey. Different audit. (Stata/RA typical: balance table on pretreatment observables)
- The user wants to model missing-data statistically (multiple imputation, FIML). That's an analytic-method concern; this skill diagnoses *whether you should trust your analysis at all*

### Author's warnings

- **Asymmetry is rarely random.** Authors: "beware of selective attrition." Even slight asymmetries can hide large biases if the dropped-respondent types are correlated with the treatment outcome
- **Sample-size calculations don't capture this.** Power calculations on the assumed-N don't protect against asymmetric-N. The audit is necessary even with high power

### Author era/blind-spot limits

- The paper doesn't cover *modern* attrition diagnostics in depth (e.g., inverse-probability weighting, sensitivity to unobserved confounders). This skill is a basic audit; deeper diagnostics exist
- AI-assisted responding is a new attrition/detection issue. Modern bot-detection introduces a new asymmetry type. Not addressed

### Adjacent confusion

- This skill is sometimes confused with **statistical-control** (regression controls for differences). Different — this skill asks whether *balance* is preserved; controls fix imbalance at analysis time but don't fix the underlying selection-bias
- This skill is sometimes confused with **satisficing** (low-effort responding). Different — satisficing is within-survey; selective attrition is across-condition

## 相关 skills

- **depends-on**: `pilot-protocol` (the audit is the post-launch version of pilot-time bugs)
- **composes-with**: `quality-checks-diagnosis` (check-pass-rate per condition is a key audit metric)
- **contrasts-with**: `relative-vs-absolute` (which addresses interpretation, not internal validity)

## 审计信息

- **验证通过**: V1 ✓ (§3.2 main; one paragraph but tightly specified; references Zhou & Fishbach 2016) / V2 ✓ (extends to any pre-registered survey experiment) / V3 ✓ (the quietly-fatal-confound framing is non-obvious; most published survey papers don't audit this rigorously)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
