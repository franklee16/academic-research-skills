---
name: pilot-protocol
description: |
  Use when the user has a finished survey draft and is approaching launch, OR when the user has launched a
  survey and is preparing for a full-wave rollout, OR when the user had a survey that failed and didn't catch it early.
  Triggers: "is my survey ready to launch?" / "should I run a pilot?" / "I just got my pilot data back" /
  "can I trust my pilot results?" / "how do I avoid bugs in my survey?" / "free-text feedback from respondents" /
  "I want to test before full launch".
  Default: Two-stage field test. Stage 1 — pretest with non-economists (1-2 friends); Stage 2 — pilot with
  50-100 real participants before full launch. Don't analyze pilot data on the target hypothesis; only check
  the instrument.
  Not for: design fixes (use clarity-concreteness / avoid-leading-questions); post-launch attrition
  (use selective-attrition-audit); platform choice (use platform-selection).
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §3.1
tags: [survey, pilot, pretest, methodology, launch]
related_skills:
  - survey-design-checklist
  - selective-attrition-audit
  - quality-checks-diagnosis
---

# Pilot Protocol (Two-Stage Field Test)

## R — 原文 (Reading)

> "It is often useful to run a pilot version of any online survey experiment [...] Before doing that, test it out yourself. Have a friend or two (ideally someone who is not an academic or at least not trained in economics) take the survey to make sure that it is easy to understand and the questions being answered are the questions you are intending to ask. [...] After your survey passes these hurdles, do not launch the entire survey experiment all at once. If you are aiming to get 500 participants, run an initial survey experiment involving only 50−100 participants. Don't analyze the data to see if responses are in-line with your hypothesis, but do check that the data is interpretable. You will be surprised at how often you will find bugs in the survey design even after initial testing phases. It is also helpful to include free response questions at the end of the survey experiment that allow participants to offer their thoughts [...] A quick skim of these responses can alert a researcher to unanticipated issues—i.e., things only a survey taker would notice."
>
> — Bergman et al., §3.1

## I — 方法论骨架 (Interpretation)

Surveys have bugs that *cannot* be detected by the designer. The designer cannot unsee their own model. The fix is **two stages of field testing**, each catching a class of bugs the other can't:

| Stage | Stage 1: Pretest | Stage 2: Pilot |
|---|---|---|
| Who | 1-2 non-economist friends | 50-100 real respondents (target ≈10% of full sample) |
| What it catches | Wording bugs, comprehension failures, impossible UI, missing response options | Bugs only visible at scale: broken randomizations, condition-asymmetric drop-out, ceiling/floor effects, mixed-platform rendering |
| What it doesn't catch | Bugs at scale | Wording clarity (won't notice it since they're power users) |
| Cost | Days | A few hundred dollars in participant pay |
| Goal | Make survey comprehensible | Make survey runnable |

Both stages need a **free-text "what was confusing?" prompt at the end**. Survey designers are blind to their own bugs; respondents see them in seconds. Read every free-text response in both stages.

**Critical discipline**: do not analyze pilot data on the *target hypothesis*. The pilot's purpose is to detect instrument bugs, not to check whether the result holds. If you run the hypothesis test on pilot data, you will be tempted to ship early or hand-pick modifications that confirm what you want to see.

The pilot doesn't have to be a separate instrument — it can be a wave-of-N within the eventual sample. The 50-100 first respondents serve as pilot; their responses are usable as data once cleaned. But their data is **pre-registered with cleaning rules**, not exploratory.

## A1 — 书中的应用 (Past Application)

### Case 1: 500-participant budget with 50-100 pilot buffer (§3.1)
- **问题**: Authors point out that surveys have bugs only visible at scale
- **方法论使用**: Recommended: if you want N=500, run a pilot of 50-100 first. Don't run hypothesis tests on pilot. Read all free-text responses. Only check "interpretable?"
- **结论**: Bugs get caught at small cost
- **结果**: Full sample finds fewer post-hoc surprises

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user has a finished draft and says "I think I'm ready to launch" — gate-check before any launch
2. The user has just collected pilot data and asks "can I now ship the rest?"
3. The user says "my survey had bugs I didn't catch before launch"
4. The user is doing all-at-once launch and asks "should I do anything before?"
5. The user wants to add an attention check or comprehension check but doesn't know what to look for

### Language signals

- "pilot" / "pretest" / "small launch" / "soft launch"
- "is the survey ready" / "ready to launch"
- "what was confusing?" / "free-text response"
- "I want to test before full launch"
- "respondents are misinterpreting" / "I have weird open-text responses"

### Compared to adjacent skills

- **survey-design-checklist**: design-time gate. This skill fires after design is "done" but before launch.
- **selective-attrition-audit**: post-launch diagnosis of condition-asymmetric drop-out. Different timeline.
- **quality-checks-diagnosis**: per-item check (which check to use). This skill is the operational flow.

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Confirm the survey has a finished draft.**
   - Completion: the user can describe their survey structure (sections, items, randomization, treatments)

2. **Run Stage 1 — pretest with 1-2 non-economist friends.**
   - Watch them take the survey in real-time if possible
   - Note any misreading, hesitation, or "what does this mean?"
   - Completion: a list of comprehension/UI bugs found

3. **Run Stage 2 — pilot with 50-100 real respondents.**
   - Use the actual platform (MTurk / Prolific / etc.)
   - Include a free-text "what was confusing?" prompt at the end
   - Don't run the hypothesis test on this data; only inspect for instrument bugs
   - Completion: a list of bugs found (broken conditions, ceiling/floor effects, drop-out asymmetries, nonsensical open-text)

4. **Add the free-text "what was confusing?" to the survey.**
   - This is non-negotiable. If the user doesn't have one, add it before pilot
   - At minimum: "Do you have any questions about this survey? Did you find anything confusing?"
   - Completion: pilot data includes free-text responses that you read in full

5. **Inspect pilot data for known failure modes.**
   - (a) Drop-out asymmetry across conditions → cite `selective-attrition-audit`
   - (b) Ceiling/floor effects (50%+ at scale endpoint) → revisit `clarity-concreteness`
   - (c) Latency drops in second half → fatigue warning
   - (d) Right-most-option pileups → satisficing signal
   - Completion: a list of instrument bugs with fixes

6. **Once instrument is clean, ship the remaining 400-450 participants.**
   - Pre-register the cleaning rules if not already done
   - Stop condition: if Stage 1 or 2 reveals serious bugs, return to design layer; do not ship
   - Completion: full launch proceeded

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user wants to *redesign* the survey (use the design-layer skills)
- The user has *already* launched and is dealing with post-hoc data issues. Use `selective-attrition-audit` or `relative-vs-absolute`
- The user is doing exploratory qualitative interviews (pilot protocol for surveys ≠ interview piloting)

### Author's warnings

- **Don't analyze pilot data on the hypothesis.** Authors explicitly forbid this. The risk: pilot data tempts you to either ship early or modify toward the result you saw
- **Pretest with non-economists.** Your economist-trained friends will read your model into the question; the whole point is to test readability for the actual respondent pool
- **Don't skip the free-text.** Reading the free-text responses is where most bugs surface

### Author era/blind-spot limits

- The paper's "50-100 participants" is from 2020 norms. With online platform access, more sophisticated protocols exist (e.g., A/A testing, sequential testing with stopping rules). The skill is a simple version that doesn't go there
- The paper does not address bot-screening during pilot. Modern pilots should include a quick bot-detection check

### Adjacent confusion

- This skill is sometimes confused with **split-sample testing** (where you randomly split the full sample between two versions). Pilot is *before* full launch; split-sample is *during* full launch. Different stages.

## 相关 skills

- **depends-on**: `survey-design-checklist` (must have a clear design before pilot)
- **composes-with**: `selective-attrition-audit` (pilot catches it; this skill flags when it happens), `quality-checks-diagnosis` (decide which check type during pilot setup)
- **contrasts-with**: `platform-selection` (which uses pay-information the user might also need for pilot)

## 审计信息

- **验证通过**: V1 ✓ (§3.1 main; one core stage of the paper) / V2 ✓ (extends to any new survey; the two-stage discipline is generally applicable) / V3 ✓ (the discipline-of-not-analyzing-pilot-on-hypothesis is non-obvious; most researchers do exactly that)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
