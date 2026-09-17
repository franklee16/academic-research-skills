---
name: paper-reading-problem-reality-check
description: Use when the user wants to stress-test whether one selected Research Question Card's problem is real, evidence-backed, externally grounded, safely motivated, and worth keeping as a research motivation.
---

# Problem Reality Check

Use this skill to run a Problem Reality Check: route to exactly one Research Question Card, interrogate whether that card's problem is real and defensible, identify unsafe motivation claims, and write a Problem Reality Check Report with a fixed Problem Reality Verdict.

This skill checks the problem motivation. It does not critique the full method, design the experiment, or collect new papers by default.

## Output Root

Set `{workspace-root}` before creating, scanning, or updating artifacts:

- Default `{workspace-root}` to `workspace` (the repo-local `workspace/` directory).
- If the user specifies a workspace root, use that path exactly and do not add another `workspace/` layer.
- If the user provides an existing artifact or workflow path, infer `{workspace-root}` from that path and keep related artifacts under the same root.
- Do not create new generated workflow directories directly at the repository root. If the user points to an existing root-level legacy workspace, inspect or update only that existing path.

## Core Workflow

1. Locate the source Research Question Workspace.
2. Pass the Source Card Gate by identifying exactly one Research Question Card.
3. Create or resume a Problem Reality Check Workspace at `{workspace-root}/research-question-checks/{field-slug}/`.
4. Write or update `source_research_questions.md`.
5. Create a per-card check folder at `{workspace-root}/research-question-checks/{field-slug}/checks/{question-slug}/`.
6. Write `checks/{question-slug}/source_card.md`.
7. Read the source card and its cited evidence paths.
8. Review only local evidence from the source Research Question Workspace and source Field Map Workspace.
9. Draft the required Challenge Questions across all Reality Check Dimensions.
10. Write or update `checks/{question-slug}/interrogation_transcript.md`.
11. Ask exactly one Challenge Question at a time and wait for the user's response before moving on.
12. After each user response, update the Interrogation Transcript with the user's answer, corrections, provisional recommended answer, and dimension verdict.
13. Continue until every required Reality Check Dimension has been interrogated.
14. Only after the Interrogation Transcript is complete, write `checks/{question-slug}/problem_reality_check.md`.
15. Write or update `problem_reality_checks.md`.
16. Stop after one card has a completed Interrogation Transcript and Problem Reality Check Report.

If the user asks to check multiple cards, ask them to choose one card for the current run. Do not run multiple card interrogations in one workflow pass.

## Source Card Gate

The workflow must be routed to exactly one Research Question Card before interrogation begins.

If the user provides a card path, inspect it directly. If the user provides a field slug or workspace path, inspect `{workspace-root}/research-questions/{field-slug}/cards/` and `research_question_cards.md`. If the user does not provide a card, scan `{workspace-root}/research-questions/` for available Research Question Workspaces and list candidate cards.

The Source Card Gate is passed only when all of the following are recorded:

- source Research Question Workspace
- source card path
- source card short name
- research question
- contribution type
- current card decision
- evidence sufficiency status
- linked evidence paths
- reason this card is being checked now

Record the gate in `checks/{question-slug}/source_card.md` using `references/source-card-template.md`.

Hard routing rules:

- Do not begin the Problem Reality Check until exactly one source card is selected.
- If several cards are plausible, present the choices and ask the user to pick one.
- If the selected card is missing core metadata, record the missing fields and continue only if the Research Question Card is still identifiable.
- If the selected card has no evidence links, the check may proceed, but the likely verdict is `needs-evidence` or `motivation-fragile`.

## Problem Reality Check Workspace

Create durable artifacts at:

```text
{workspace-root}/research-question-checks/{field-slug}/
```

Use this structure:

- `source_research_questions.md`
- `checks/{question-slug}/source_card.md`
- `checks/{question-slug}/interrogation_transcript.md`
- `checks/{question-slug}/problem_reality_check.md`
- `problem_reality_checks.md`

Use `references/workspace-structure.md` as the structure guide.

The workspace may contain many per-card check folders over time, but each workflow run checks exactly one card.

## Local Evidence Review Rules

Before writing the report, inspect the source card's evidence base:

- linked Field Map paper records
- linked Supporting Evidence files
- `candidate_angles.md`
- `research_question_cards.md`
- source `writing_intent.md` when motivation fit affects the problem boundary
- source Field Map `research_opportunities.md` or `research_clusters.md` when the card's cited gap needs context

Do not claim that new external evidence was searched unless the user explicitly ran another workflow. This skill may identify Targeted Evidence Needs, but it should not launch a new literature search, field map expansion, or research-framing run by itself.

If local files are missing or links are broken, record that as evidence fragility rather than silently filling the gap.

## Reality Check Dimensions

Every Problem Reality Check Report must cover these six Reality Check Dimensions:

1. Problem Existence
2. Real-World Grounding
3. Evidence Support
4. Saturation / Prior-Solution Risk
5. Motivation Claim Safety
6. Scope and Stakeholder Fit

Each dimension must include at least one Challenge Question. Add more Challenge Questions only when the source card has multiple distinct weak assumptions.

## Challenge Question Rules

A Challenge Question is attack-style but answerable. It should force the card's motivation to survive a concrete skeptical claim.

Do not ask generic questions such as "Is there evidence?" or "Is this important?" Instead, phrase the challenge as something a skeptical reviewer, advisor, or domain expert might say.

Every Challenge Question is a live interrogation turn. The agent may prepare a provisional recommendation from local evidence, but it must ask the question to the user and wait for feedback before marking that dimension complete.

Each Challenge Question must include:

- skeptical claim
- hidden assumption being tested
- evidence that would satisfy the challenge
- current evidence from local artifacts
- provisional recommended answer
- user response or correction
- resulting recommended answer
- dimension verdict after user response

The provisional recommended answer is required even when evidence is thin. In that case, write the most honest defensible answer and name what cannot yet be claimed. The resulting recommended answer may match the provisional answer or change after the user's response.

Dimension verdicts:

- `solid`: The dimension is defensible from current evidence.
- `needs-evidence`: The dimension may be defensible, but current evidence is insufficient or too indirect.
- `fragile`: The dimension may be true, but the current motivation wording or scope is easy to attack.
- `failing`: The dimension currently fails or contradicts available evidence.

## Interaction Rules

This is a turn-by-turn interrogation, not a one-shot report generator. The agent should read the card and local evidence before asking the first question, but it must still interrogate the user one Challenge Question at a time.

The first response after the Source Card Gate should include only:

- the selected Research Question Card,
- the planned Reality Check Dimensions,
- the first Challenge Question,
- the current evidence relevant to that question,
- the provisional recommended answer,
- and a request for the user's response.

Do not include the final Problem Reality Verdict, complete Unsafe Motivation Claims table, or final Problem Reality Check Report in the first response.

For each turn:

- ask exactly one Challenge Question,
- provide the provisional recommended answer,
- wait for the user's reply,
- update `interrogation_transcript.md`,
- then ask the next Challenge Question.

Do not skip a dimension because the local evidence seems sufficient. A strong dimension still needs a user-facing interrogation turn so the transcript records the shared judgment.

Do not treat silence, lack of time, or a previous broad instruction as a waiver. A waiver counts only when the user explicitly says to continue without live interrogation for a specific Challenge Question or for the rest of the current card.

Ask follow-up questions within the same dimension when:

- a core motivation claim has no evidence path,
- a real-world scenario requires the user's domain judgment,
- the verdict depends on the user's writing intent or target venue,
- two plausible interpretations conflict,
- or the card's scope must be narrowed to avoid an unsafe motivation claim.

When a follow-up is required, ask one focused question at a time and explain the recommended answer.

The final report must be derived from the Interrogation Transcript. If `interrogation_transcript.md` is missing or incomplete, do not write `problem_reality_check.md`; continue the interrogation instead.

## Unsafe Motivation Claims

Every Problem Reality Check Report must include an `Unsafe Motivation Claims` section.

For each unsafe claim, record:

- claim to avoid
- why it is unsafe
- safer replacement
- evidence needed if the user insists

Unsafe Motivation Claims are not generic writing polish. They are claims that could make the problem motivation collapse because they are overstated, undersupported, contradicted by evidence, too broad, or likely to be attacked during paper review.

## Targeted Evidence Needs

If the report verdict is `needs-evidence`, `motivation-fragile`, or `reject`, record Targeted Evidence Needs where useful.

Targeted Evidence Needs must be specific:

- evidence need
- why it matters for the verdict
- suggested evidence type
- suggested search question or artifact to inspect
- recommended next skill or workflow

Do not execute the next workflow automatically. The Problem Reality Check should recommend the next step and stop.

Useful next-skill routing:

- Use `paper-reading-research-framing` when existing citations must be checked against specific motivation claims.
- Use `paper-reading-field-map` when the problem area itself is under-mapped or the card may be missing a central branch of work.
- Use `paper-reading-research-framing` when the main risk is that close work already solves or reframes the problem.
- Use `paper-reading-experiment-design` when the problem is real but the executable study route or reviewer-objection coverage is unclear.

## Problem Reality Verdict

Each report must end with exactly one Problem Reality Verdict:

- `problem-solid`
- `needs-evidence`
- `motivation-fragile`
- `reject`

Verdict meanings:

- `problem-solid`: The problem is real and motivation-ready; only ordinary strengthening remains.
- `needs-evidence`: The problem may be real, but current local evidence is insufficient for a convincing motivation.
- `motivation-fragile`: The problem may be valuable, but the current motivation can be attacked because it is overstated, too broad, poorly scoped, or dependent on an unsafe assumption.
- `reject`: The problem should not continue as the current research motivation because it appears solved, unsupported, unimportant, contradicted by evidence, or badly mismatched with the user's goal.

The final verdict is not the same as the Research Question Card's `keep / needs more evidence / defer` decision. A kept card can still receive `needs-evidence` or `motivation-fragile` after a stricter problem-reality interrogation.

## Required Templates

Use the reference templates in this directory:

- `references/workspace-structure.md`
- `references/source-research-questions-template.md`
- `references/source-card-template.md`
- `references/interrogation-transcript-template.md`
- `references/problem-reality-check-report-template.md`
- `references/problem-reality-checks-summary-template.md`

## Stop Condition

Stop when exactly one selected Research Question Card has:

- a confirmed Source Card Gate record,
- a completed Interrogation Transcript,
- a completed Problem Reality Check Report,
- all six Reality Check Dimensions covered,
- at least one Challenge Question per dimension,
- user response or explicit user waiver for every Challenge Question,
- Unsafe Motivation Claims recorded,
- Targeted Evidence Needs recorded or explicitly marked as none,
- one final Problem Reality Verdict,
- and `problem_reality_checks.md` updated.
