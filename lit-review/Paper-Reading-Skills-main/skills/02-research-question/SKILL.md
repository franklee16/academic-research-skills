---
name: paper-reading-research-question
description: Use when the user knows the broad field and reads papers to find concrete, researchable, experimentally testable gaps or research questions.
---

# Research Question

Use this skill to run a Research Question Workflow: select a source Field Map Workspace, confirm the user's Writing Intent, turn Research Opportunity Candidates into Candidate Angles, check whether the evidence is sufficient, collect Supporting Evidence when needed, and produce Research Question Cards.

This skill does not start from generic brainstorming. It starts from one Field Map Workspace and carries its Research Opportunity Candidates forward into decision-ready research questions.

## Output Root

Set `{workspace-root}` before creating, scanning, or updating artifacts:

- Default `{workspace-root}` to `workspace` (the repo-local `workspace/` directory).
- If the user specifies a workspace root, use that path exactly and do not add another `workspace/` layer.
- If the user provides an existing artifact or workflow path, infer `{workspace-root}` from that path and keep related artifacts under the same root.
- Do not create new generated workflow directories directly at the repository root. If the user points to an existing root-level legacy workspace, inspect or update only that existing path.

## Core Workflow

1. Locate the source Field Map Workspace.
2. Pass the Source Field Map Gate.
3. Create or resume a Research Question Workspace at `{workspace-root}/research-questions/{field-slug}/`.
4. Write `source_field_map.md`.
5. Use Guided Choice to pass the Writing Intent Gate and write `writing_intent.md`.
6. Read `research_opportunities.md`, `research_clusters.md`, and relevant Paper Position Records.
7. Derive Candidate Angles from Research Opportunity Candidates and write `candidate_angles.md`.
8. Use Guided Choice to help the user select 1-3 preferred Candidate Angles.
9. Run an Evidence Sufficiency Check for each selected Candidate Angle.
10. If evidence is insufficient but the angle is promising, collect Supporting Evidence in `evidence/`.
11. Create one Research Question Card per supported selected angle in `cards/`.
12. Write or update `research_question_cards.md`.
13. Stop when the user has 2-3 `keep` Research Question Cards, or one unusually strong `keep` card with a recorded reason for not keeping more.

If a Research Question Workspace already exists, read its current artifacts before continuing. Preserve user edits and update the existing files instead of overwriting them blindly.

## Source Field Map Gate

The Research Question Workflow must be derived from exactly one Field Map Workspace.

If the user provides a slug or path, inspect that workspace. If the user does not provide one, scan `{workspace-root}/field-maps/` for complete workspaces.

A Field Map Workspace is complete enough for this workflow only when it contains:

- `field_boundary.md`
- `research_clusters.md`
- `research_opportunities.md`
- at least one Paper Position Record in `seed_papers/` or `all_papers/`

Routing rules:

- If exactly one complete workspace exists, use it and tell the user which workspace will be used.
- If multiple complete workspaces exist, ask the user to choose one.
- If no complete workspace exists, route the user to `paper-reading-field-map`; do not invent Research Opportunity Candidates.
- If `research_opportunities.md` is missing, the user needs the Field Map Workflow's opportunity step before Research Question Cards can be produced.

Record the source workspace and completeness check in `source_field_map.md` using `references/source-field-map-template.md`.

## Research Question Workspace

Create durable artifacts at:

```text
{workspace-root}/research-questions/{field-slug}/
```

Use this structure:

- `source_field_map.md`
- `writing_intent.md`
- `candidate_angles.md`
- `evidence/`
- `cards/`
- `research_question_cards.md`

Use `references/workspace-structure.md` as the structure guide.

## Guided Choice Rules

Use Guided Choice whenever the workflow needs the user to decide between plausible directions.

Do not present one recommendation and ask the user to confirm it unless the user has already stated a clear preference. Instead, present:

- 2-4 viable options when the decision space is small enough to compare.
- A binary tradeoff when the decision space is broad or the user seems unsure.
- A recommended option or option pair, with a short reason and the main tradeoff.

Good Guided Choice prompts are comparative:

- "Do you want the question to optimize for fast empirical results, or for a more novel but riskier framing?"
- "Should we narrow toward a benchmark/evaluation contribution, or toward a system/tooling contribution?"
- "Do you prefer a question closer to your long-term research direction, or one easier to package for the next paper?"
- "Should this lean toward an AI venue framing, or a security/systems venue framing?"

When presenting multiple options, explain what each option is best for and what it sacrifices. If the user chooses one branch, continue narrowing from that branch instead of reopening every option.

## Writing Intent Gate

Do not recommend Candidate Angles until the user confirms the Writing Intent.

Start by offering a Guided Choice over plausible Writing Intent profiles from the user's stated goal. Do not ask the user to confirm a single proposed profile.

The user should choose:

- 1 primary goal
- up to 2 secondary goals
- any practical constraints

Default goal vocabulary:

- Easier to produce experimental results
- More novel
- Closer to the user's long-term research direction
- Easier to write as a systems paper
- Easier to aim at a high-level venue

Useful practical constraints include available time, number of collaborators, ability to run user studies, ability to release a benchmark, target research community, target venue type, compute budget, data access, and preferred contribution type.

If the user is unsure, use binary narrowing questions before writing the final Writing Intent:

- experimental certainty vs novelty risk
- systems-building vs benchmark/evaluation
- long-term direction vs near-term paper feasibility
- high-level venue ambition vs controlled execution risk

Write the confirmed Writing Intent to `writing_intent.md` using `references/writing-intent-template.md`.

## Candidate Angle Rules

A Candidate Angle is a narrower research cut derived from a Research Opportunity Candidate. Each Candidate Angle must include a Contribution Type.

Allowed Contribution Types:

- Benchmark / Evaluation Protocol
- Method / Defense Mechanism
- System / Tooling
- Human Study / Interaction
- Theory / Conceptual Model
- Empirical Study / Measurement

For each Research Opportunity Candidate, derive 2-5 Candidate Angles when possible. Each Candidate Angle should include:

- source Research Opportunity Candidate
- Contribution Type
- the narrower research cut
- unresolved gap
- plausible study, experiment, system, benchmark, theory, or measurement route
- evidence signals from the Field Map Workspace
- risks or objections
- fit to the confirmed Writing Intent
- recommendation rationale

Write Candidate Angles to `candidate_angles.md` using `references/candidate-angles-template.md`.

After writing Candidate Angles, present a Guided Choice set rather than a single winner. The set should include several recommended angles with different strengths, such as:

- safest empirical angle
- most novel angle
- best systems-paper angle
- best long-term-direction angle
- highest-upside but riskiest angle

Ask the user to select 1-3 angles or answer a binary narrowing question. Do not create Research Question Cards before the user selects angles.

## Writing Intent Recommendation Rules

Use Writing Intent to recommend Candidate Angles:

- Easier to produce experimental results: prefer `Benchmark / Evaluation Protocol` and `Empirical Study / Measurement`.
- More novel: prefer cross-cluster angles, new threat models, new mechanisms, or `Theory / Conceptual Model` angles with strong evidence that the field lacks a stable framing.
- Closer to the user's long-term research direction: prefer angles whose Research Clusters and Contribution Types match the user's stated direction.
- Easier to write as a systems paper: prefer `System / Tooling` angles with a clear architecture, workload, evaluation environment, and integration story.
- Easier to aim at a high-level venue: prefer angles with important stakes, strong evidence of an unresolved gap, a clear empirical plan, and a non-incremental contribution.

If Writing Intent goals conflict, explain the tradeoff instead of forcing one score to hide it.

When multiple Candidate Angles fit the Writing Intent, keep the top several options visible. Recommend a short list and say which one you would choose under each plausible user priority.

## Evidence Sufficiency Check

Run an Evidence Sufficiency Check after the user selects Candidate Angles and before generating Research Question Cards.

A Candidate Angle is minimally sufficient when it has:

- at least 3 directly relevant Paper Position Records or Supporting Evidence records
- at least 2 different evidence roles
- a clear unresolved gap
- a plausible executable study, experiment, system, benchmark, theory, or measurement route

Evidence roles include:

- problem exists
- existing methods are insufficient
- evaluation setting is reusable
- target scenario is realistic
- contribution is not saturated
- feasibility signal exists
- risk or objection is documented

Decision outcomes:

- `sufficient`: create or update a Research Question Card.
- `needs more evidence`: collect Supporting Evidence before creating a `keep` card.
- `defer`: do not create a `keep` card unless the user explicitly wants a speculative record; mark unsupported claims as evidence needs.

## Supporting Evidence Rules

If evidence is insufficient but the Candidate Angle is promising, collect Supporting Evidence under:

```text
{workspace-root}/research-questions/{field-slug}/evidence/
```

Use `references/supporting-evidence-template.md`.

Supporting Evidence should record search questions, keyword queries, discovery sources, new papers, evidence roles, useful evidence points, remaining gaps, and how the evidence changes the Candidate Angle.

If network access is unavailable, do not pretend the evidence collection is complete. Tell the user what could not be searched and ask for paper links or permission to continue when network access is available.

If a newly found paper becomes central to the field map itself, recommend adding it to the Field Map Workspace later, but do not block the Research Question Workflow unless the Research Question Card would otherwise rely on uncited claims.

## Research Question Card Rules

Each Research Question Card must cite evidence. Do not make core claims without links to Field Map paper records or Supporting Evidence files.

Use `references/research-question-card-template.md` for each card in:

```text
{workspace-root}/research-questions/{field-slug}/cards/{question-slug}.md
```

Each card must include:

- Research Question
- Short Name
- Source Candidate Angle
- Source Research Opportunity Candidate
- Contribution Type
- Writing Intent Fit
- Core Claim
- Why This Matters
- Evidence Base
- Unresolved Gap
- Possible Study / Experiment
- Feasibility
- Novelty
- Risks / Objections
- What Would Make This Publishable
- Evidence Sufficiency
- Decision: `keep`, `needs more evidence`, or `defer`

Update `research_question_cards.md` using `references/research-question-cards-summary-template.md`.

## Hard Confirmation Gates

Do not skip these gates:

1. **Source Field Map confirmed**: do not create Candidate Angles until the source Field Map Workspace is identified and complete enough.
2. **Writing Intent confirmed**: do not recommend Candidate Angles until the user chooses or revises a Writing Intent through Guided Choice.
3. **Candidate Angles selected**: do not create Research Question Cards until the user selects 1-3 Candidate Angles through Guided Choice.
4. **Evidence Sufficiency checked**: do not mark a Research Question Card as `keep` unless its core claims cite evidence.

## Required Templates

Use the reference templates in this directory:

- `references/workspace-structure.md`
- `references/source-field-map-template.md`
- `references/writing-intent-template.md`
- `references/candidate-angles-template.md`
- `references/supporting-evidence-template.md`
- `references/research-question-card-template.md`
- `references/research-question-cards-summary-template.md`

## Stop Condition

Stop when the user has:

- confirmed the source Field Map Workspace,
- confirmed the Writing Intent,
- selected 1-3 Candidate Angles,
- reviewed evidence-backed Research Question Cards,
- and kept 2-3 concrete research questions with cited evidence, unresolved gap, importance, feasibility, novelty, experimentability, and risks.

If only one Research Question Card is strong enough to keep, stop only after recording why the workflow did not keep more.
