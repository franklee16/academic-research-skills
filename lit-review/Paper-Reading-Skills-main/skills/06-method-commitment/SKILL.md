---
name: paper-reading-method-commitment
description: Use when the user has a selected Candidate Method, multiple Candidate Methods to merge, a user-authored rough method, or a reconstructed chat method and wants to converge on one human-owned method outcome before experiment design, research framing, or risk review.
---

# Method Commitment

Use this skill to run a Method Commitment Workflow: normalize exactly one Source Method against exactly one Method Commitment Source Problem, review inherited local context, reconstruct the method anatomy, attack high-risk design assumptions with the user, record structure-changing decisions, assign a status, and write status-aligned artifacts.

This is a convergence workflow. It does not run broad method search, invent a full method from nothing, automatically choose the best Candidate Method, or write full experiment plans.

Only `committed` output is downstream-ready. `provisionally-committed`, `needs-redesign`, and `reject-current-method` must not be routed as normal sources for downstream workflows.

## Output Root

Set `{workspace-root}` before creating, scanning, or updating artifacts:

- Default `{workspace-root}` to `workspace` (the repo-local `workspace/` directory).
- If the user specifies a workspace root, use that path exactly and do not add another `workspace/` layer.
- If the user provides an existing artifact or workflow path, infer `{workspace-root}` from that path and keep related artifacts under the same root.
- Do not create generated workflow directories directly at the repository root.

Create or resume one method commitment folder at:

```text
{workspace-root}/method-commitments/{field-slug}/{method-slug}/
```

Use `references/workspace-structure.md` for the artifact layout and status-specific output filenames.

## Core Workflow

1. Locate or draft exactly one Source Method.
2. Identify exactly one Method Commitment Source Problem.
3. Create or resume the Method Commitment folder.
4. Write or update `source_method.md`.
5. Pass the Method Commitment Source Gate by confirming or explicitly delegating the Source Method, Method Source Mode, and Method Commitment Source Problem.
6. Run the Method Commitment Context Review from local artifacts.
7. Reconstruct the method anatomy in `method_reconstruction.md`.
8. Identify high-risk Method Design Attack dimensions and low-risk dimensions cleared from artifacts.
9. Write or update `method_attack_transcript.md`.
10. Ask one high-risk Challenge Question at a time, wait for the user's response or explicit delegation, and update the transcript.
11. Update `method_decision_log.md` after each structure-changing decision.
12. Revise the method reconstruction when the user's answers change the method.
13. Pass the Method Commitment Gate.
14. Assign exactly one Method Commitment Status.
15. Write exactly one status-aligned Method Commitment Output Artifact.
16. Always write or update `method_commitment_summary.md`.
17. Stop with clear downstream routing or do-not-route warnings.

If the workflow is resumed, read existing artifacts before editing. Preserve user edits and update existing files instead of overwriting them blindly.

## Source Method

Method Commitment starts from exactly one Source Method bound to exactly one Method Commitment Source Problem.

Allowed Method Source Modes:

- `selected-candidate-method`: the user chooses exactly one Candidate Method.
- `user-authored-method`: the user describes a rough method from scratch.
- `hybrid-method`: the user merges multiple Candidate Methods, papers, patterns, or personal ideas.
- `reconstructed-from-chat`: the method is assembled from current conversation when no durable source exists yet.

When multiple Candidate Methods or inspirations are merged, the mode must be `hybrid-method`. Record borrowed pieces, discarded pieces, merge rationale, and the new weakest link.

The Method Commitment Source Gate is passed only when `source_method.md` records:

- source method name or short name
- Method Source Mode
- exactly one Method Commitment Source Problem
- source artifacts, if available
- user goal for committing now
- current method summary
- known constraints
- non-goals
- evidence status
- open decisions
- gate confirmation mode: confirmed by user or explicitly delegated

If the user does not provide enough information, ask for a Minimal Method Brief:

- What problem does the method address?
- What failure does it intervene on?
- What input does it consume?
- What output does it produce?
- What is the core mechanism?
- What is the expected improvement?
- What should the method not try to solve?

Do not reconstruct, attack, or commit the method before the Source Gate passes.

## Context Review

Run Method Commitment Context Review before reconstructing the method. Default to local artifacts; do not run a new web search unless the user explicitly asks for one.

Read relevant available artifacts, including:

- Source Method artifact or user-authored brief
- source Research Question Card or Source Problem Brief
- Problem Reality Check report and transcript, if available
- Method Inspiration `source_problem.md`
- `method_need_decomposition.md`
- `method_patterns.md`
- `transfer_mapping.md`
- `candidate_methods.md`
- `method_candidate_library.md`
- close-work, unsafe motivation, evidence, and blocker notes already recorded upstream

Preserve inherited fragilities. If close-work evidence, transformation evidence, data feasibility, or problem evidence is thin, record the issue as a blocker, Targeted Evidence Need, or downstream routing hint instead of silently filling it in.

## Method Reconstruction

Write `method_reconstruction.md` before the attack pass. Use `references/method-reconstruction-template.md`.

The reconstruction must include:

1. Method Name
2. Source Problem
3. Method Thesis
4. Mechanistic Claim
5. Target Failure
6. Intervention Point
7. Inputs
8. Outputs
9. Core Mechanism
10. Module Breakdown
11. Training Flow or Inference Flow
12. Data Requirements
13. Objective, Decision Rule, or Control Policy
14. Borrowed Inspirations
15. Novelty Boundary
16. Assumptions
17. Non-goals
18. Replaceable Components
19. Required Ablations
20. Implied Baseline Pressures
21. Implied Metric Signals
22. Weakest Link
23. Intentionally Unfrozen Open Decisions
24. Candidate Blockers

Use this Method Thesis pattern:

```text
By introducing [mechanism] at [intervention point], the method aims to improve [target outcome] under [scope], because [reason it should work].
```

Separate the Method Thesis from the Mechanistic Claim. The Method Thesis states what the method claims; the Mechanistic Claim states why the mechanism should work and what later ablations, baselines, metrics, or reviewer objections should pressure-test.

Required ablations, implied baseline pressures, and implied metric signals are Method Commitment Downstream Pressure Points only. Do not write a full experiment protocol, final baseline set, or metric formula here.

## Design Attack Pass

Run a Method Design Attack Pass after reconstruction. This attacks the method structure, not the source problem's motivation. Do not repeat the Problem Reality Check unless the method contradicts the inherited problem evidence.

Check these attack dimensions:

1. Problem-Method Fit
2. Mechanism Plausibility
3. Novelty Boundary
4. Component Necessity
5. Assumption Load
6. Data / Training Feasibility
7. Evaluation Consequence
8. Scope Control

For each dimension, mark it as:

- `high-risk`: ask a live Challenge Question.
- `cleared-from-artifacts`: record why existing artifacts make the risk non-blocking.
- `blocked`: record what must be clarified before commitment can continue.

Each high-risk Challenge Question must include:

- skeptical claim
- hidden assumption being tested
- why the current design may fail
- evidence or design change that would satisfy the challenge
- provisional recommendation
- user response or explicit delegation
- resulting design decision

Ask one high-risk Challenge Question at a time and wait for the user's response before continuing. If the user explicitly delegates a question, record that delegation in `method_attack_transcript.md`.

Update `method_decision_log.md` only for structure-changing decisions, such as source mode, hybrid merge rationale, method boundary, Mechanistic Claim revision, weakest link, blockers, and final status.

## Commitment Gate

Pass the Method Commitment Gate only when the user confirms or explicitly delegates:

- one Method Thesis
- one Mechanistic Claim
- one Method Commitment Source Problem
- core mechanism
- method boundary
- required inputs and outputs
- major modules
- training or inference flow
- novelty boundary
- strongest assumptions
- weakest link
- downstream pressure points
- intentionally unfrozen open decisions
- candidate blockers

`committed` requires Explicit Method Commitment Confirmation from the researcher. Agent recommendation, broad delegation, or "you decide" is not enough. Without explicit confirmation, an otherwise stable method must be `provisionally-committed` with `missing explicit human commitment` recorded as a blocker.

## Status And Output Artifacts

Assign exactly one Method Commitment Status:

- `committed`: structurally stable, explicitly confirmed by the researcher, and downstream-ready. Write `committed_method_design.md`.
- `provisionally-committed`: nearly stable, but blocked from downstream routing by named Method Commitment Blockers. Write `provisional_method_design.md`.
- `needs-redesign`: promising direction, but the current structure is not stable enough. Write `method_redesign_brief.md`.
- `reject-current-method`: the method should not continue in its current form. Write `method_rejection_note.md`.

Never write `committed_method_design.md` for `provisionally-committed`, `needs-redesign`, or `reject-current-method`.

Always write `method_commitment_summary.md`. The summary is the routing index and must include the Source Method, source problem, status, output artifact, blockers, next recommended workflow, and do-not-route warnings.

## Required Templates

Use the reference templates in this directory:

- `references/workspace-structure.md`
- `references/source-method-template.md`
- `references/method-reconstruction-template.md`
- `references/method-attack-transcript-template.md`
- `references/method-decision-log-template.md`
- `references/committed-method-design-template.md`
- `references/provisional-method-design-template.md`
- `references/method-redesign-brief-template.md`
- `references/method-rejection-note-template.md`
- `references/method-commitment-summary-template.md`

## Stop Condition

Stop when exactly one Source Method has:

- a completed Method Commitment Source Gate,
- a completed Method Commitment Context Review,
- a reconstructed Method Anatomy,
- high-risk attack dimensions answered or explicitly delegated,
- low-risk attack dimensions cleared from artifacts or marked blocked,
- a Method Attack Transcript,
- a Method Decision Log,
- a completed Method Commitment Gate,
- one Method Commitment Status,
- one status-aligned Method Commitment Output Artifact,
- a Method Commitment Summary,
- and a clear downstream routing or do-not-route decision.
