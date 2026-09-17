---
name: paper-reading-theoretical-grounding
description: Use when the user has a research problem but needs theoretical foundations, conceptual lineage, or research traditions that support the problem framing.
---

# Theoretical Grounding

Use this skill to run a Theoretical Grounding Workflow: route to exactly one Research Question Card and its completed Problem Reality Check Report, decompose the checked problem into theory-bearing components, extract Theory Hooks, run Targeted Theory Search, select 2-4 theoretical traditions with the user, and write a claim-centered Theoretical Grounding Report.

This skill does not decorate a research question with famous theories. It identifies which precise claims need theoretical support and which theoretical traditions can safely support those claims.

## Output Root

Set `{workspace-root}` before creating, scanning, or updating artifacts:

- Default `{workspace-root}` to `workspace` (the repo-local `workspace/` directory).
- If the user specifies a workspace root, use that path exactly and do not add another `workspace/` layer.
- If the user provides an existing artifact or workflow path, infer `{workspace-root}` from that path and keep related artifacts under the same root.
- Do not create new generated workflow directories directly at the repository root. If the user points to an existing root-level legacy workspace, inspect or update only that existing path.

## Core Workflow

1. Locate the source Research Question Workspace.
2. Locate the source Problem Reality Check Workspace.
3. Pass the Theoretical Grounding Source Gate by identifying exactly one Research Question Card and its completed Problem Reality Check Report.
4. Create or resume a Theoretical Grounding Workspace at `{workspace-root}/theoretical-groundings/{field-slug}/`.
5. Write or update `source_research_question_checks.md`.
6. Create a per-card grounding folder at `{workspace-root}/theoretical-groundings/{field-slug}/groundings/{question-slug}/`.
7. Write `groundings/{question-slug}/source_problem.md`.
8. Read the source card, the Problem Reality Check Report, and relevant local context.
9. Draft `groundings/{question-slug}/problem_theory_decomposition.md`.
10. Ask the user to confirm or revise the Theory-Support Claims and Boundary before continuing.
11. Extract Theory Hooks and write `groundings/{question-slug}/theory_hooks.md`.
12. Run Targeted Theory Search by default for Theory Hooks and Theory-Support Claims.
13. Generate 5-8 Candidate Theoretical Traditions and write `groundings/{question-slug}/candidate_theoretical_traditions.md`.
14. Recommend 2-4 Selected Theoretical Traditions and write `groundings/{question-slug}/selected_theoretical_traditions.md`.
15. Pass the Theoretical Tradition Selection Gate by asking the user to confirm, revise, replace, or explicitly delegate the selected traditions.
16. Internally check whether relationships among selected traditions materially affect the research positioning. Do not create a separate relationship-audit artifact.
17. Write `groundings/{question-slug}/theoretical_grounding.md`.
18. Write or update `theoretical_groundings.md`.
19. Stop when the user has a claim-centered theoretical grounding with theory-backed problem framing, Theoretical Pillars, source support, boundaries, and remaining fragilities or Theory Evidence Needs.

If a Theoretical Grounding Workspace already exists, read its current artifacts before continuing. Preserve user edits and update existing files instead of overwriting them blindly.

## Source Problem Gate

The workflow must be routed to exactly one Research Question Card and its completed Problem Reality Check Report.

If the user provides a card path, inspect it directly and find the corresponding Problem Reality Check Report. If the user provides a field slug, inspect `{workspace-root}/research-questions/{field-slug}/cards/` and `{workspace-root}/research-question-checks/{field-slug}/checks/`. If the user does not provide a card, scan `{workspace-root}/research-question-checks/` for completed check reports and list candidate cards.

The Theoretical Grounding Source Gate is passed only when all of the following are recorded:

- source Research Question Workspace
- source Research Question Card
- source Problem Reality Check Workspace
- source Problem Reality Check Report
- source card short name
- research question
- contribution type
- current card decision
- Problem Reality Verdict
- Unsafe Motivation Claims from the check
- Targeted Evidence Needs from the check
- reason this problem is being theoretically grounded now

Record the gate in `groundings/{question-slug}/source_problem.md` using `references/source-problem-template.md`.

Hard routing rules:

- Do not begin decomposition until exactly one source card and exactly one completed Problem Reality Check Report are identified.
- If several cards or checks are plausible, present the choices and ask the user to pick one.
- If the selected card has no completed Problem Reality Check Report, route the user to `paper-reading-problem-reality-check`; do not invent problem-reality findings.
- If the Problem Reality Verdict is `reject`, do not write Theoretical Pillars. Write the Source Problem record and explain why the problem should not be theoretically grounded in its current form.

## Verdict Handling

Theoretical grounding cannot fix a weak problem by citation.

Handle the source Problem Reality Verdict as follows:

- `problem-solid`: continue toward a final Theoretical Grounding Report.
- `needs-evidence`: continue, but mark the grounding as provisional unless the evidence needs do not affect the Theory-Support Claims.
- `motivation-fragile`: continue, but record which fragilities theory can reframe and which remain unresolved.
- `reject`: stop after source routing and explain why the current problem should not be theorized further.

The final report must preserve unresolved fragilities from the Problem Reality Check. Do not imply that theoretical grounding resolves an empirical, saturation, or scope weakness unless the report has evidence for that narrower claim.

## Theoretical Grounding Workspace

Create durable artifacts at:

```text
{workspace-root}/theoretical-groundings/{field-slug}/
```

Use this structure:

- `source_research_question_checks.md`
- `groundings/{question-slug}/source_problem.md`
- `groundings/{question-slug}/problem_theory_decomposition.md`
- `groundings/{question-slug}/theory_hooks.md`
- `groundings/{question-slug}/candidate_theoretical_traditions.md`
- `groundings/{question-slug}/selected_theoretical_traditions.md`
- `groundings/{question-slug}/theoretical_grounding.md`
- `theoretical_groundings.md`

Use `references/workspace-structure.md` as the structure guide.

The workspace may contain many per-card grounding folders over time, but each workflow run grounds exactly one checked Research Question Card.

## Local Context Review Rules

Before writing the Problem-Theory Decomposition, inspect the source problem context:

- source Research Question Card
- source Problem Reality Check Report
- source Problem Reality Check `source_card.md`
- source Problem Reality Check `interrogation_transcript.md` when available
- source Research Question Workspace `research_question_cards.md`
- source Research Question Workspace `candidate_angles.md`
- source Research Question Workspace `writing_intent.md`
- source Field Map `research_opportunities.md`
- source Field Map `research_clusters.md`
- linked paper records or Supporting Evidence files that the source card or check uses for core claims

Do not treat missing local artifacts as an invitation to invent context. Record the missing paths in `source_problem.md` and narrow the Theoretical Grounding Report accordingly.

## Problem-Theory Decomposition

Write `problem_theory_decomposition.md` before searching for theories.

Decompose the checked problem into:

- `phenomenon`: the observed or hypothesized phenomenon that makes the problem worth studying.
- `mechanism`: the process, causal route, interaction, or conceptual mechanism that may explain why the phenomenon happens.
- `failure`: the condition under which current systems, practices, assumptions, or literature fail.
- `Theory-Support Claims`: the exact claims in the paper or project that need theory to support them.
- `boundary`: the objects, stakeholders, tasks, settings, time scales, and claims that are in or out of scope.

A Theory-Support Claim is not the Research Question Card's single Core Claim. It is a key judgment that theory must support. Each Theory-Support Claim must include:

- exact claim sentence
- why it needs theoretical support
- source component that triggered it
- what theory would need to explain
- what the claim must not be stretched to mean

Interaction rule:

- The agent may draft the decomposition from local artifacts.
- The user must confirm or revise the Theory-Support Claims and Boundary before Candidate Theoretical Traditions are selected.
- If there are multiple plausible decompositions, present 2-4 options or a binary tradeoff instead of asking an open-ended question.

## Theory Hooks

After the decomposition is confirmed, write `theory_hooks.md`.

A Theory Hook is a concept relationship extracted from the decomposition. It is not a keyword, theory name, or citation label.

Each Theory Hook must record:

- hook statement
- source component: phenomenon, mechanism, failure, Theory-Support Claim, or boundary
- why the hook is theoretical rather than merely empirical or engineering-oriented
- candidate theory search cues
- Theory-Support Claims it may support
- priority for search and selection

Good Theory Hooks look like concept relationships:

- source and lifecycle affect later trustworthiness
- long-term state influences future action
- authority should not be distributed equally across all remembered information
- filtering malicious content is not the same as governing later behavioral influence

Avoid using broad keywords as hooks:

- memory
- trust
- provenance
- governance

## Targeted Theory Search

Run Targeted Theory Search by default before finalizing Selected Theoretical Traditions, unless the user explicitly says not to search or search is unavailable.

Targeted Theory Search is narrow. It verifies Candidate Theoretical Traditions and representative sources for specific Theory Hooks or Theory-Support Claims. It is not a Field Map Workflow, broad literature review, or general theory brainstorm.

For each search, derive queries from:

- the Theory Hook relationship
- the exact Theory-Support Claim
- the neighboring research domain
- candidate tradition names when known

For each Candidate Theoretical Tradition, prefer sources in this order:

- classic or source-setting works for the tradition
- survey, handbook, or canonical framing papers
- papers applying the tradition in an adjacent domain
- papers applying or challenging the tradition in the user's current research domain

Do not ask the user to find sources before the agent has made a reasonable targeted search attempt. If search is unavailable, restricted, or insufficient, record a Theory Evidence Need.

## Candidate Theoretical Traditions

Generate 5-8 Candidate Theoretical Traditions in `candidate_theoretical_traditions.md`.

Candidates may come from classic theory, adjacent fields, or theory-like conceptual traditions already used in the current research area. Selection is based on claim support, not fame.

For each candidate, record:

- matched Theory Hook(s)
- matched Theory-Support Claim(s)
- representative source candidates
- why it may fit
- why it may not fit
- support boundary
- evidence status: `verified`, `plausible`, `weak`, or `unsupported`
- selection decision: `select`, `keep as secondary lens`, `reject`, or `needs search`

Reject a famous theory if it does not support a Theory-Support Claim. Keep a less famous tradition if it directly supports a claim and has a clear boundary.

## Selected Theoretical Traditions

Recommend 2-4 Selected Theoretical Traditions in `selected_theoretical_traditions.md`.

Each selected tradition must explain:

- which Theory-Support Claim it supports
- which Theory Hook it explains
- representative sources
- what it can support
- what it cannot support
- how it changes the research problem framing
- whether it is final or provisional

Minimum evidence standard for a Selected Theoretical Tradition:

- at least one representative source or classic source
- at least one adjacent-domain application source, or else a `provisional` status
- direct support for at least one Theory-Support Claim
- at least one explicit support boundary

Overall sufficiency standard:

- every Theory-Support Claim has at least one Theoretical Pillar
- core claims do not rely entirely on provisional traditions
- if a claim has only weak theoretical support, the final framing downgrades that claim

## Theoretical Tradition Selection Gate

Do not write `theoretical_grounding.md` until the Theoretical Tradition Selection Gate is passed.

The gate is passed only when the user confirms, revises, replaces, or explicitly delegates the 2-4 Selected Theoretical Traditions and their rationale.

When asking for confirmation, show:

- recommended selected traditions
- which Theory-Support Claims each selected tradition supports
- candidate traditions rejected or kept as secondary lenses
- provisional traditions and remaining Theory Evidence Needs
- the main research-positioning consequence of the selection

If the user says the agent can decide, continue, but record the selection rationale in `selected_theoretical_traditions.md` and `theoretical_grounding.md`.

## Theory Relationship Handling

Before writing the final report, internally check whether relationships among Selected Theoretical Traditions materially affect the research positioning.

Do not create a separate Theory Intersection Map, relationship audit, or theory-relationship artifact.

Use these rules:

- If relationships among traditions clarify the research position, naturally explain them in the final problem framing or Theoretical Pillars.
- If traditions support different claims independently, write parallel Theoretical Pillars.
- If a relationship is unclear, do not force an intersection.
- If a tradition does not clearly support a claim or positioning role, downgrade it to a secondary lens or remove it.
- If tension between traditions matters, name the tension only where it affects the claim boundary or framing.

The goal is to help the user recognize the research position, not to create an elegant theory map.

## Theoretical Grounding Report

Write `theoretical_grounding.md` only after the decomposition and tradition-selection gates are passed.

The report is organized by Theory-Support Claim, not by theory name.

It must include:

- theory-backed problem framing
- Theoretical Pillars by Theory-Support Claim
- representative sources for each pillar
- support boundaries and unsafe overclaims
- framing changes from the original Research Question Card
- remaining fragilities from the Problem Reality Check
- Theory Evidence Needs where Targeted Theory Search was unavailable or insufficient
- recommended card revision, if theory grounding changes the problem enough to justify revising the source card

Do not modify the original Research Question Card by default. If the final report recommends card revision, record it under `Recommended Card Revision`. Only rewrite the card if the user explicitly asks. If the card is rewritten in a way that changes its motivation, recommend rerunning or updating relevant Problem Reality Check dimensions.

## Theory Evidence Needs

Use a Theory Evidence Need only after Targeted Theory Search is unavailable, explicitly deferred, or insufficient.

For each Theory Evidence Need, record:

- affected Theory-Support Claim
- affected tradition
- missing source type: classic source, adjacent-domain application, current-domain use, critique, or counterexample
- why the missing source affects framing stability
- suggested search question
- provisional wording to use until evidence is found

Do not launch another workflow automatically. Recommend `paper-reading-research-framing`, `paper-reading-field-map`, or another paper-reading skill only when the next step is outside narrow theory verification.

## Hard Confirmation Gates

Do not skip these gates:

1. **Source Problem confirmed**: do not decompose the problem until one Research Question Card and one completed Problem Reality Check Report are identified.
2. **Problem-Theory Decomposition confirmed**: do not select theoretical traditions until the user confirms or revises Theory-Support Claims and Boundary.
3. **Theoretical Traditions confirmed**: do not write the final report until the user confirms, revises, replaces, or explicitly delegates the selected traditions.
4. **Search and sufficiency checked**: do not present unverified theory support as final when Targeted Theory Search was unavailable or insufficient.

## Required Templates

Use the reference templates in this directory:

- `references/workspace-structure.md`
- `references/source-research-question-checks-template.md`
- `references/source-problem-template.md`
- `references/problem-theory-decomposition-template.md`
- `references/theory-hooks-template.md`
- `references/candidate-theoretical-traditions-template.md`
- `references/selected-theoretical-traditions-template.md`
- `references/theoretical-grounding-report-template.md`
- `references/theoretical-groundings-summary-template.md`

## Stop Condition

Stop when exactly one selected Research Question Card has:

- a confirmed Source Problem Gate record,
- a confirmed Problem-Theory Decomposition,
- Theory Hooks derived from the decomposition,
- 5-8 Candidate Theoretical Traditions considered,
- 2-4 Selected Theoretical Traditions confirmed or explicitly delegated by the user,
- Targeted Theory Search attempted or explicitly marked unavailable/deferred,
- each Theory-Support Claim connected to at least one Theoretical Pillar,
- representative sources or Theory Evidence Needs recorded for each pillar,
- support boundaries and unsafe overclaims recorded,
- a Theoretical Grounding Report with theory-backed problem framing,
- framing changes from the original Research Question Card recorded,
- remaining Problem Reality Check fragilities preserved,
- and `theoretical_groundings.md` updated.
