---
name: platform-selection
description: |
  Use when the user is choosing a platform for an online survey / experiment, OR when they have already launched on
  one and are reconsidering.
  Triggers: "which platform for my survey?" / "MTurk vs. Prolific vs. CloudResearch vs. Lucid" /
  "I want a US-representative sample" / "how do I reach finance professionals?" /
  "I want to recruit from non-US populations" / "is MTurk okay for my study?" /
  "I want a hardened quality pipeline".
  Default rule: Platform choice is a population choice. MTurk ≈ young, US/India, educated; Prolific ≈ pre-screened
  US/UK; Lucid Theorem/Marketplace ≈ US quota / targeted subgroups; CloudResearch = MTurk with screening layer.
  Match the platform to the *research question*, not the *convenience*.
  Not for: payment questions (use fair-pay-and-reputation); survey design (use survey-design-checklist).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §4.3, §4.4
tags: [survey, platform-selection, MTurk, Prolific, CloudResearch, Lucid]
related_skills:
  - fair-pay-and-reputation
---

# Platform Selection (Recruitment Pipeline)

## R — 原文 (Reading)

> "A separate set of survey platforms allow researchers to access participants for their studies [...] MTurk provides a population of around 500k workers from at least 190 countries [...] CloudResearch provides a user-friendly interface to launch surveys via the MTurk platform [...] Prolific is a worker-focused crowdsourcing platform that provides pre-screened populations of mostly US and UK workers [...] Lucid is a survey service that has two related platforms used to run surveys; Lucid Theorem (researcher run) and Lucid Marketplace (survey firm managed). [...] MTurk samples can be considered convenience samples. They are not representative of the general population."
>
> — Bergman et al., §4.3-4.4

## I — 方法论骨架 (Interpretation)

Choosing a recruitment platform is **choosing a population**, not a logistics choice. Each platform imposes a different population filter:

| Platform | Population | When to use | When *not* to use |
|---|---|---|---|
| **MTurk** | Young, US/India, educated, web-savvy. Convenience sample. ~500k workers, 190+ countries | Applied-finance questions; behavioral experiments where US/India education-skew is acceptable | General-population inference, esp. populations older/different from MTurk demographics |
| **CloudResearch (a.k.a. TurkPrime)** | Same MTurk pool but pre-screened, with repeat-participant tracking and bonus management | When you want MTurk-style population but with stricter QA, screening against repeat-respondents, and better bonus-payment infrastructure | When population target differs from MTurk (e.g., need US-only older adults) |
| **Prolific** | Pre-screened, mostly US/UK. Prolific enforces pay minimums (~$6.50/hr, often higher in practice). Nationally-representative samples available | Behavioral experiments with ethical pay standards; UK / US populations; pre-screenable demographic targeting | Studies needing very large N (lower worker pool); non-US/UK populations |
| **Lucid Theorem** | US population, quota-sampled. Shorter surveys (≤15 min). | Standard short surveys to US adults | Long surveys (>15 min); studies needing intense engagement |
| **Lucid Marketplace** | US (and other) targeted populations. Managed by Lucid. Costly ($3-4× Theorem) | Reaching specific subgroups (bilingual individuals, professionals, etc.) | Cost-sensitive studies |
| **Positly** | Targeted via CloudResearch infrastructure | Custom panels | Large-N convenience samples |

**The selection flow**:
1. What population do you actually need? (Define this in terms of demographics *and* behavioral profile.)
2. What pay rate is ethically defensible and platform-compatible?
3. Which platform's available population matches your population target within tolerable error?
4. Run a 50-respondent pilot on each candidate platform; compare demographics and effect direction before committing to full launch.

The 2020 paper underestimates the bot/server-farm threat on MTurk. As of 2026, MTurk alone is rarely the right primary platform; CloudResearch's screening layer is closer to baseline. Document this shift when giving current advice.

## A1 — 书中的应用 (Past Application)

### Case 1: Arechar, Kraft-Todd, Rand (2017) on MTurk timing (§3.5)
- **问题**: Authors investigated whether MTurkers at different times are different respondents
- **方法论使用**: Compared behaviors and demographics across time-of-day and day-of-week
- **结论**: Same individuals give similar *behaviors* at different times; but the *person-traits* of participants differ across times
- **结果**: Implications for *sample composition* — running at different times yields different populations. Platform-timing choices have implicit population consequences.

### Case 2: Moss & CloudResearch on bots/server-farms (§4.4)
- **问题**: Authors worried about bot responses vs. human
- **方法论使用**: CloudResearch's research did not find bots but did find server-farm workers (location-masked, duplicating)
- **结论**: Bot-detection wasn't first-order but geolocation/IP screening mattered
- **结果**: CloudResearch's geolocation-blocking is now standard practice for the bot-mitigation reason

### Case 3: Comparing MTurk to in-person undergraduate samples (§4.4)
- **问题**: Authors address whether MTurk is "good enough"
- **方法论使用**: Note that MTurk respondents are different from undergrads in finance-relevant ways (older, more financial experience)
- **结论**: For applied finance research, MTurk can be *more* representative than undergrads even if neither is fully representative
- **结果**: Practical recommendation: pick MTurk for applied finance questions where undergrads would be inappropriate

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user is choosing a platform at the start of a survey project
2. The user has launched on one platform and questions whether their choice is right
3. The user reports data quality problems and asks "would another platform fix this?"
4. The user needs US-/UK-representative or quota-sampled data
5. The user wants to reach a specific subgroup (e.g., US finance professionals, bilingual individuals)

### Language signals

- "MTurk" / "Prolific" / "CloudResearch" / "Lucid" / "Positly"
- "what platform" / "which crowdsourcing" / "where do I recruit"
- "convenience sample" / "representative sample"
- "data quality" / "professional survey-takers" / "bots"
- "I'm switching from MTurk to..." / "should I use CloudResearch"

### Compared to adjacent skills

- **fair-pay-and-reputation**: covers pay-rate and reputation mechanics for the chosen platform. This skill is the *choice*, that skill is the *operation*
- **pilot-protocol**: 50-respondent pilot is recommended across multiple candidate platforms before committing. This skill recommends running those pilots; pilot-protocol helps run them
- **survey-design-checklist**: which platform you pick is independent of question design

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Define the target population.**
   - The user should answer: "What population do I actually need?" Demographics, behavioral profile, recruitment country constraints, ethical constraints
   - Completion: a written population definition (1-3 sentences)

2. **Score each candidate platform against the population definition.**
   - For each platform, check: (a) population match, (b) pay-rate compatibility, (c) survey-length compatibility (≤15 min on Lucid Theorem, flexible on others), (d) screening needs (CloudResearch / Prolific have prescreening; MTurk doesn't)
   - Completion: a scored table

3. **Apply the current-context adjustments.**
   - In 2026: prefer CloudResearch or Prolific over raw MTurk for new studies
   - In 2026: plan for bot-detection on any platform
   - In 2026: LLM-assisted responding — open-text items may need instructions "do not use AI tools" + self-report on AI usage
   - Completion: updated table

4. **Recommend a parallel-pilot check before committing.**
   - Suggest running a 50-respondent pilot on the top-2 candidate platforms
   - Compare: completion rate, demographics, attention-check pass-rate, median response time
   - Pick the platform that matches the user's research goals better
   - Completion: pilot plan with comparison metrics

5. **Hand off to the operational skills.**
   - Platform choice → `fair-pay-and-reputation` for what to pay and screen
   - Platform choice → `pilot-protocol` for the launch flow
   - Platform choice → `quality-checks-diagnosis` for which check to use given platform norms

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user wants to *change* a question wording. Use design-layer skills
- The user has already committed to a platform and is asking about response-time or attention-check pattern — use `quality-checks-diagnosis` or `selective-attrition-audit`
- The user is doing field-data collection (admin records, audit logs) — not a crowdsourced survey question at all

### Author's warnings

- **MTurk samples are not US-representative.** Authors (§4.4): "MTurkers tend to be younger and more educated than the US general population." Don't claim representativeness without explicit comparison to benchmarks.
- **MTurk can be more relevant than undergrads.** Authors: "if your research question involves applied questions about financial management, MTurk might represent a more relevant population than an in-person survey experiment at a college campus."
- **Pricing disparities matter across platforms.** Authors (§3.4): "participants on Prolific will not be happy with standard MTurker pay." Using the wrong pay rate for the chosen platform silently degrades sample quality.

### Author era/blind-spot limits

- **2020 era**: bot-detection was not first-order; MTurk alone was acceptable. As of 2026, raw MTurk is rarely the right primary platform; CloudResearch's screening layer is closer to baseline. **Always flag this era gap when giving advice.**
- **AI-assisted responding**: Not addressed in the paper. Add as a known consideration.
- **GDPR/CCPA compliance**: Not addressed. Modern platform choice must consider data-residency requirements.
- **Prolific's UK ethical-pay floor updates over time.** Current norms ≈$15/hr are above the paper's $6.50/hr baseline.

### Adjacent confusion

- This skill is sometimes confused with **data-collection method** (admin data vs. survey vs. experiment). Different: this skill is *within* online surveys; other methods are upstream choices
- This skill is sometimes confused with **field-data collection** (audit studies, postal surveys). Different mode of recruitment

## 相关 skills

- **depends-on**: none (a starting choice)
- **composes-with**: `fair-pay-and-reputation` (the chosen platform has norms for pay), `pilot-protocol` (which uses the chosen platform to test the survey)
- **contrasts-with**: `survey-design-checklist` (design is platform-independent)

## 审计信息

- **验证通过**: V1 ✓ (§4.3 with full platform-by-platform treatment; §4.4 with population framing; cross-references §3.4 pay norms) / V2 ✓ (extends to any new platform-selection problem; the population-vs-platform framing is the actionable insight) / V3 ✓ (platform-as-population is non-obvious — most researchers treat platform choice as logistics)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
