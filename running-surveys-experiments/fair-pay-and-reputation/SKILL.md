---
name: fair-pay-and-reputation
description: |
  Use when the user is setting up payment or screening for a survey, OR has reputation problems on a platform.
  Triggers: "how much should I pay survey respondents?" / "what's the right pay rate for Prolific/MTurk?" /
  "should I pay screeners who fail?" / "my Turker reviews are bad" / "is this pay rate ethical?" /
  "I want to avoid having workers avoid my study" / "I'm blocked from MTurk".
  Two failure modes: under-paying (selects for low-quality respondents, professional survey-gamers drop out,
  sample quietly degenerates); stiffing screened-out (reputation damage, future respondents avoid).
  Different platforms have different pay-rate norms. Pay-even-when-screened is the basic ethical floor.
  Not for: which platform (use platform-selection); what items to ask (use design-layer skills).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §3.3, §3.4
tags: [survey, payment, reputation, ethics, turkerview]
related_skills:
  - platform-selection
---

# Fair Pay & Reputation

## R — 原文 (Reading)

> "be sure to offer some compensation to participants who do not pass the screening step. The best practice is to launch a short screener survey first that pays everyone a small amount. Then, invite only workers who 'pass' the screener to complete a second (main) study. [...] it is important that you do not stiff the participants who only make it to part one. [...] You are not an anonymous requester. You have a reputation. And, you should aim to maintain a good one (e.g., by paying participants promptly and fairly). You might want to consider setting up a dedicated email address to use for online participants. There are many online blogs, such as https://turkerview.com/, that workers use to review requesters. Keep in mind that participants can share information about your survey experiment with others. Periodically check your reviews on these sites. Also, pay attention to any changes in the standard pay rates that participants expect. These may be different across different crowdsourcing platforms. e.g., participants on Prolific will not be happy with standard MTurker pay."
>
> — Bergman et al., §3.3 + §3.4

## I — 方法论骨架 (Interpretation)

**Two failure modes** combined here:

| Failure mode | Mechanism | Cost | Fix |
|---|---|---|---|
| Under-paying | Above-median respondents avoid your study; remaining pool is low-quality tail | Quietly degenerating sample over multiple launches | Pay platform-norm rate; check current Turker-view rates |
| Stiffing screened-out participants | Bad reviews on Turker-view → next cohort already wary | Reputation damage compounds across launches | Two-stage design: pay-everyone-then-invite-passers |

**The reputation loop**:
- Worker coalition sites (Turker-view on MTurk; Prolific's built-in rating) publish requester reviews
- Bad reviews → experienced workers skip your HIT → your sample becomes desperate / low-effort tail → data quality falls further
- Repeat launches compound the effect; rebuilding reputation takes dozens of clean launches
- **Therefore**: pay fairly, pay on time, don't stiff, monitor reviews.

**Pay-rate floor (2026 norms — flag shift from 2020 paper)**:
- MTurk: ≥$7.50/hr is competitive; cap at ~$30/hr
- Prolific: ethical floor $6.50/hr enforced by Prolific; best-practice $15/hr
- CloudResearch / Positly: pricing similar to MTurk by default
- Lucid Theorem: flat-rate pricing, pay-rate is set by Lucid

**Screener-payment design**:
1. Short screener at small payment (e.g., 1 min, $0.15) paid to *everyone*
2. Then invite only passers to a second survey (5 min) at higher rate ($0.85 + bonus)
3. Pass-through language: "The first part will take about 1 minute and will pay everyone $0.15. Workers who qualify will be directed to the second part which takes about 5 minutes and will pay a bonus of $0.85."
4. Never stiff — even for failing participants

## A1 — 书中的应用 (Past Application)

### Case 1: Two-step paid screener with explicit wording (§3.3)
- **问题**: Authors needed to screen for qualifications without stiffing
- **方法论使用**: Two-stage design with explicit example wording: 1-min screener at $0.15 to everyone; 5-min main at $0.85 bonus for qualifiers
- **结论**: Both groups paid; passers get more; nobody stiffed
- **结果**: Authors recommend this design as standard

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user is setting pay rate for a survey at start
2. The user is designing screening logic
3. The user has declining data quality across launches and suspects reputation issues
4. The user has bad reviews on a worker site
5. The user wants to pay under-platform-norm (a temptation) and is asking whether to do it
6. The user has screened-out participants and is asking whether they must be paid

### Language signals

- "pay rate" / "fair pay" / "wage" / "compensation"
- "ethical pay" / "Prolific minimum"
- "Turker view" / "reputation" / "worker reviews"
- "stiffing" / "not paying screened"
- "MTurk / Prolific wages" / "crowd pay norms"

### Compared to adjacent skills

- **platform-selection**: which platform; this skill is how to operate well on the chosen platform
- **pilot-protocol**: pilot participants also need to be paid fairly; this skill applies during pilot too
- **quality-checks-diagnosis**: passing checks doesn't excuse non-payment; payment is independent of check-result

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Determine the user's target platform.**
   - Completion: a platform choice (or "considering platform X")

2. **Set pay rate against current platform norms (2026).**
   - MTurk: ≥$7.50/hr, cap at $30/hr
   - Prolific: ≥$15/hr best practice
   - CloudResearch: similar to MTurk
   - Lucid Theorem: flat-rate per-impression
   - Always compute your survey's expected duration and set pay accordingly
   - Completion: a per-survey pay rate

3. **Design the screening-and-payment architecture.**
   - If screening: two-stage design — paid screener, paid (or invited) main
   - If no screening: single survey at full rate
   - Pass-through language: explicit per-stage pay and duration
   - Completion: a written design with sample wording

4. **Set up reputation monitoring.**
   - Make a dedicated email for the platform (don't use your academic email)
   - If on MTurk: claim a Turkerview profile and monitor reviews
   - Pay promptly within platform norms
   - Completion: a monitoring plan

5. **Pre-launch check: compute total per-respondent pay and confirm against norm.**
   - Expected duration × $/hour rate ≥ platform floor
   - Survey length × expected completion rate × per-survey pay ≤ user budget
   - Completion: a budget and pay table

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user is doing *field-data* collection (admin/audit). Different payment concerns
- The user has unique ethical-review constraints (institutional IRB). Compliance layer, not this skill
- The user is choosing between two platforms — that's `platform-selection`; this skill applies after the choice

### Author's warnings

- **Pay even when screened out.** Authors: "be sure to offer some compensation to participants who do not pass the screening step" (§3.3). Stiffing is a failure mode of *reputation*, not cost.
- **Platform-specific pay norms.** Authors: "participants on Prolific will not be happy with standard MTurker pay" (§3.4). Wrong rate → silent sample degeneracy.
- **Reputation is upstream of data quality.** Authors (§3.4): "Keep in mind that participants can share information about your survey experiment with others. Periodically check your reviews on these sites." This is not PR — it's data-quality infrastructure.

### Author era/blind-spot limits

- **Pay norms have moved up.** The paper quotes $3.13-$3.48/hr for MTurk as baseline; current norms are double to triple. Always give current figures.
- **Turker-view is one of several reputation venues.** Prolific's built-in rating, /r/MTurk subreddit, and similar communities also matter. The paper under-emphasizes multi-platform reputation.
- **AI-assisted responses are not addressed by paper.** Some participants may use AI to *complete the survey* even at high pay. Skills-based payment may need to evolve beyond hourly equivalents.

### Adjacent confusion

- This skill is sometimes confused with **IRB ethics**. Different — IRB is institutional research-ethics review; this skill is operational ethical-payment practice within IRB-approved work
- This skill is sometimes confused with **incentive design for accuracy**. Different — incentive design affects *quality given engagement*; this skill affects *engagement given offer*

## 相关 skills

- **depends-on**: `platform-selection` (the chosen platform sets pay norms)
- **composes-with**: `pilot-protocol` (pilot must be paid-fairly too), `quality-checks-diagnosis` (failure on checks doesn't change pay obligation)
- **contrasts-with**: `survey-design-checklist` (design and payment are largely independent)

## 审计信息

- **验证通过**: V1 ✓ (§3.3 + §3.4 with full treatment; cross-references §3.5 timing) / V2 ✓ (extends to any new platform's pay norms; the under-paying-and-stiffing failure modes are general) / V3 ✓ (the reputation-loop framing is non-obvious — most academic economists don't realize they're being reviewed)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
