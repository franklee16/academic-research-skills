---
name: survey-design-checklist
description: |
  Use BEFORE writing any survey question or after drafting a survey but before launch.
  Triggers: "design a survey" / "I'm building a questionnaire" / "what should I check on this survey?" /
  "review my survey design" / "is this a good survey question?" / "I'm starting a survey study".
  Not for: pure logistics (which platform to use → use platform-selection); pure launch audits
  (use pilot-protocol); meta-questions about whether to do a survey at all.
  Activates when the user is at the design-by-writing-questions stage, not the data-collection stage.
source_book: "Survey Curious? Start-Up Guide" — Bergman, Chinco, Hartzmark, Sussman (2020)
source_chapter: §2 (full chapter) + §3.1-3.2
tags: [survey, questionnaire-design, methodology, umbrella]
related_skills:
  - clarity-concreteness
  - avoid-leading-questions
  - relative-vs-absolute
  - converging-evidence-design
  - pilot-protocol
---

# Survey Design Checklist

## R — 原文 (Reading)

> "Ultimately, the goal of a survey is to provide meaningful responses from participants [...] we refer to meaningful responses as those that would be likely to convince critical readers who are knowledgeable about survey methods that your hypothesis either is or is not correct [...] The key is to ask questions that participants are able and willing to answer. Obstacles to doing so include participants' preferences for privacy, limited memory, and limited ability to access their thoughts on certain topics."
>
> — Bergman, Chinco, Hartzmark, Sussman, Survey Curious? §2 (incl. §2.1)

## I — 方法论骨架 (Interpretation)

The paper argues that a survey has three stacked layers — **questions**, **operations**, **platform** — and a quality break at any layer invalidates the next. Even before the operational and platform layers, a single question has three failure modes stacked inside it: the respondent must **be able** to answer (recall / introspect / recognize the construct), **be willing** to answer (privacy / social cost), and **interpret** the question as you intended (wording / concreteness). Each of those three constraints can independently kill the question. The designer's job is to keep all three satisfied at once.

This skill is the umbrella. It does not itself answer "is my question clear?" — that's `clarity-concreteness`. It does not answer "is this leading?" — that's `avoid-leading-questions`. It does not answer "what conclusions can I draw?" — that's `relative-vs-absolute`. Its single function: **before writing each question, run the three-constraint check (ability × willingness × interpretation) and reject any question that fails any one of them.** It is the front gate of survey design.

## A1 — 书中的应用 (Past Application)

### 案例 1: privacy prohibits exact-dollar finance questions (§2.1)
- **问题**: Authors needed to ask about personal-finance behaviors on surveys
- **方法论的使用**: Recognized that asking for exact dollar amounts collides with willingness (privacy). Replaced with bracketed ranges: $0 / $0-10k / $10k-50k / $50k-100k / >$100k
- **结论**: Asked less-detailed questions, got meaningful ranges
- **结果**: Avoided refusal-rate spikes and gave interpretable bins

### 案例 2: recall window shortening (§2.1)
- **问题**: Survey needed to know portfolio-checking frequency
- **方法论使用**: Asked "how many times did you check your investment portfolio over the last week" rather than "...over the last year"
- **结论**: Recognized that year-scale behavior cannot be reliably recalled
- **结果**: Got meaningful numbers instead of fabricated heuristics

## A2 — 触发场景 (Future Trigger) ★

### User scenarios where this skill should fire

1. The user says "I'm designing a survey for X" / "I need to write a questionnaire" — at the start, before any question is fixed in text
2. The user shows draft question text and asks "is this question OK?" — gate each question through the three-constraint check
3. The user asks "what are the best practices for survey design in finance?" — they want the layout, not yet the operational details
4. The user asks "I'm running an experiment, what should I think about?" — at the design phase, before recruitment
5. The user pastes a survey draft and asks for a review — at the text-quality layer (not the operational layer)

### Language signals

- "Designing a survey" / "writing a survey" / "I have a survey idea"
- "Question wording" / "is this a good question"
- "Survey review" / "critique my survey"
- "Help me write questions" / "what questions should I ask"
- "I'm setting up an online experiment"

### Compared to adjacent skills

- **clarity-concreteness**: fires AFTER you've written a question and you suspect it's ambiguous; this skill is the upstream gate. `clarity-concreteness` is one of the three constraint checks ("can they *interpret*?") at the sentence level.
- **avoid-leading-questions**: fires AFTER you've written a question and you're checking for demand bias; this skill is the upstream gate. `avoid-leading-questions` covers the "willingness/interpretation" boundary.
- **relative-vs-absolute**: fires AFTER data collection, when interpreting; this skill is at design time.
- **pilot-protocol**: fires AT launch, not design. Different layer.

## E — 可执行步骤 (Execution)

When this skill is activated:

1. **Read the user's draft (or intended question).**
   - Completion: you can describe what the question asks in your own words.

2. **Run the three-constraint check.**
   - (a) **Ability**: Can the respondent recall or recognize this information? (If it requires year-scale recall or introspection on decision context → flag.)
   - (b) **Willingness**: Will the respondent answer honestly given privacy / social-desirability cost? (If it's about sensitive behavior → flag.)
   - (c) **Interpretation**: Will the respondent interpret the words as you intended? (If you used abstract nouns — "the market", "short-term", "important factor" → flag, then defer to `clarity-concreteness`.)
   - Completion: every question is marked PASS / FAIL with a one-sentence reason for FAILs.

3. **Route FAILs to the right downstream skill.**
   - (a) ability FAIL → suggest shorter time-horizon or field/experimental replacement; cite §2.1
   - (b) willingness FAIL → defer to `avoid-leading-questions` for sensitive topics, or recommend list-experiment / behavioral data substitute
   - (c) interpretation FAIL → defer to `clarity-concreteness` for the wording fix
   - **Stop condition**: if all questions PASS, jump to step 5
   - Completion: each FAIL has a one-line fix or a downstream skill invoked

4. **Layer-2 reminder (operations)** — do not stop at design.
   - After questions clear §2, prompt user with: "have you planned a pilot? See `pilot-protocol`." (Don't run it for them — the design layer is done.)

5. **Output a structured gate decision.**
   - Either: "All questions passed the three-constraint check; move to `pilot-protocol`."
   - Or: "N questions failed, routed to [skill list]. Fix and re-run."

## B — 边界 (Boundary) ★

### Don't use this skill when

- The user has *already* deployed the survey and is asking about results — that's `relative-vs-absolute` or `selective-attrition-audit`
- The user is asking about recruitment logistics (which platform, who to pay) — that's `platform-selection` / `fair-pay-and-reputation`
- The user is asking to *write* a survey item (not review one) — first ask which construct, then run this gate before fixing wording
- The user is reviewing a survey for a *literature-review* purpose (e.g., "what's the gold standard for measuring risk preference?") — the umbrella is too generic for that

### Author's warnings embedded

- This skill is *necessary but not sufficient*. The paper's §2 is titled "Considerations for Designing your Survey" and explicitly disclaims: "this list is by no means exhaustive." Don't claim the checklist is complete.
- The skill focuses on **text** of questions. It does NOT cover operational defenses (pilots / checks / attrition). Those are §3 and `pilot-protocol` / `quality-checks-diagnosis` / `selective-attrition-audit`.

### Author era/blind-spot limits inherited

- **Self-report has limits.** The paper acknowledges (§2.1) that some constructs (e.g., decision-process introspection; recall over long horizons) cannot be elicited reliably by any survey. This skill should hand off to "use field data or a more complicated experimental design" when both stages of internal validation (clear wording + converging question types) still produce suspect data.
- **2020 era**: bot-detection and AI-assisted responding are not addressed by the paper. Modern surveys must add bot-screening and may need to specify "do not use AI tools" guidance. Not the skill's job, but flag to user.

### Easiest confusion

- This skill is NOT "make my survey sound better." It's "would this question produce a response a critical reviewer would trust?" Those are different standards.

## 相关 skills

- **depends-on**: none (this is the umbrella)
- **composes-with**: `clarity-concreteness`, `avoid-leading-questions`, `converging-evidence-design` (the three other design-layer skills)
- **contrasts-with**: `pilot-protocol` (operational layer, fires post-design), `platform-selection` (logistics layer)

## 审计信息

- **验证通过**: V1 ✓ (whole §2 chapter and §3.1-3.2 cross-references) / V2 ✓ (extends to any new survey construct) / V3 ✓ (the three-constraint view is non-obvious vs. usual single-axis survey-design advice)
- **测试通过率**: see `test-prompts.json`
- **蒸馏时间**: 2026-08-19
