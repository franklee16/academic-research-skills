---
name: paper-reading-method-inspiration
description: Use when the user has a rough problem and reads papers to collect transferable modeling ideas, architectures, training flows, optimization objectives, agent pipelines, or data construction methods.
---

# Method Inspiration

Use this skill to run a Method Inspiration Workflow: route to exactly one Research Question Card or Source Problem Brief, decompose the problem into Method Needs, run Targeted Method Search, extract Method Patterns, map their transfer fit, assemble 3-5 Candidate Methods, and write a Method Candidate Library.

This skill helps the user collect method inspiration. It does not invent the paper's actual core method, force a quick commitment, or produce a Committed Method Design. The human researcher owns the later jump from Candidate Methods to a real method design.

## Output Root

Set `{workspace-root}` before creating, scanning, or updating artifacts:

- Default `{workspace-root}` to `workspace` (the repo-local `workspace/` directory).
- If the user specifies a workspace root, use that path exactly and do not add another `workspace/` layer.
- If the user provides an existing artifact or workflow path, infer `{workspace-root}` from that path and keep related artifacts under the same root.
- Do not create new generated workflow directories directly at the repository root. If the user points to an existing root-level legacy workspace, inspect or update only that existing path.

## Core Workflow

1. Locate the source Research Question Card or draft a Source Problem Brief from the user's rough problem.
2. Pass the Method Inspiration Source Gate.
3. Create or resume a Method Inspiration Workspace at `{workspace-root}/method-inspirations/{field-slug}/`.
4. Write or update `source_research_questions.md`.
5. Create a per-problem inspiration folder at `{workspace-root}/method-inspirations/{field-slug}/inspirations/{problem-slug}/`.
6. Write `inspirations/{problem-slug}/source_problem.md`.
7. Read the source card or Source Problem Brief and relevant local context.
8. Draft `inspirations/{problem-slug}/method_need_decomposition.md`.
9. Pass the Method Needs Confirmation Gate by asking the user to confirm, revise, or explicitly delegate the Method Needs.
10. Run Targeted Method Search for the confirmed Method Needs and write `inspirations/{problem-slug}/targeted_method_search.md`.
11. Run the Method Search Sufficiency Check.
12. Extract Method Patterns and write `inspirations/{problem-slug}/method_patterns.md`.
13. Write `inspirations/{problem-slug}/transfer_mapping.md`, including Need-Pattern Fit, Assembly Roles, and Method Pattern Dispositions.
14. Assemble 3-5 Candidate Methods and write `inspirations/{problem-slug}/candidate_methods.md`.
15. Pass the Candidate Method Selection Gate by asking the user to confirm, revise, replace, or explicitly delegate the 3-5 Candidate Methods and assembly rationales.
16. Write `inspirations/{problem-slug}/method_candidate_library.md`.
17. Write or update `method_candidate_libraries.md`.
18. Stop when the user has an auditable Method Candidate Library, not a Committed Method Design.

If a Method Inspiration Workspace already exists, read its current artifacts before continuing. Preserve user edits and update existing files instead of overwriting them blindly.

## Method Inspiration Boundary

Method Inspiration stops at auditable Candidate Methods.

Do not:

- ask the user to choose the final method as part of this workflow,
- present a Candidate Method as the paper's actual core method,
- write a Committed Method Design,
- treat novelty as established merely because an agent combined patterns,
- or overdevelop experiment-design, research-framing, or reviewer-objection sections.

It is fine to record light downstream implications, such as:

- experiment implications for `paper-reading-experiment-design`,
- likely baseline pressures for `paper-reading-experiment-design`,
- claims that may need metric signals in `paper-reading-experiment-design`,
- close-work risks for `paper-reading-research-framing`,
- and weak links for `paper-reading-experiment-design`.

These are routing hints only. The later workflows should use a human-owned Committed Method Design, not an uncommitted Candidate Method, as their main source.

## Method Inspiration Source Gate

The workflow must be routed to exactly one source:

- one Research Question Card, preferred; or
- one Source Problem Brief, allowed when the user has only a rough problem.

If the user provides a card path, inspect it directly. If the user provides a field slug or workspace path, inspect `{workspace-root}/research-questions/{field-slug}/cards/` and `research_question_cards.md`. If the user provides only a rough problem, draft a Source Problem Brief and ask the user to confirm it.

The Method Inspiration Source Gate is passed only when all of the following are recorded:

- source type: Research Question Card or Source Problem Brief
- source Research Question Workspace, if applicable
- source card path, if applicable
- source problem short name
- problem statement or research question
- contribution type, if available
- evidence status
- target failure
- intended intervention point
- constraints and non-goals
- reason method inspiration is being run now
- whether downstream Candidate Methods should be marked provisional

If the source Research Question Card has a completed Problem Reality Check Report, read it and preserve its verdict, unsafe motivation claims, and Targeted Evidence Needs. If the verdict is `reject`, stop after source routing unless the user explicitly asks for speculative inspiration despite the rejected problem.

If the source is a Source Problem Brief, mark Candidate Methods as `provisional` unless the user later provides stronger problem evidence.

## Method Inspiration Workspace

Create durable artifacts at:

```text
{workspace-root}/method-inspirations/{field-slug}/
```

Use this structure:

- `source_research_questions.md`
- `inspirations/{problem-slug}/source_problem.md`
- `inspirations/{problem-slug}/method_need_decomposition.md`
- `inspirations/{problem-slug}/targeted_method_search.md`
- `inspirations/{problem-slug}/method_patterns.md`
- `inspirations/{problem-slug}/transfer_mapping.md`
- `inspirations/{problem-slug}/candidate_methods.md`
- `inspirations/{problem-slug}/method_candidate_library.md`
- `method_candidate_libraries.md`

Use `references/workspace-structure.md` as the structure guide.

The workspace may contain many per-problem inspiration folders over time, but each workflow run handles exactly one source problem.

## Local Context Review Rules

Before writing the Method Need Decomposition, inspect the available source context:

- source Research Question Card, if present
- source Research Question Workspace `research_question_cards.md`
- source Research Question Workspace `candidate_angles.md`
- source Research Question Workspace `writing_intent.md`
- source Field Map `research_opportunities.md`
- source Field Map `research_clusters.md`
- linked Paper Position Records or Supporting Evidence files used for core method-relevant claims
- source Problem Reality Check Report and `source_card.md`, if present
- source Problem Reality Check `interrogation_transcript.md`, if present

Do not invent missing evidence. Record missing or thin context in `source_problem.md` and mark affected Method Needs or Candidate Methods as provisional.

## Method Need Decomposition

Write `method_need_decomposition.md` before searching for method papers.

Each Method Need must include:

- target failure
- intervention point
- required capability
- expected inputs
- expected outputs
- constraints
- success signal
- evidence status

Method Needs are problem-derived functional requirements, not model modules. Do not start with an architecture. First decide what the method would need to accomplish, then search for patterns that could satisfy those needs.

Method Need evidence status values:

- `supported`: directly backed by source card evidence or checked problem evidence
- `plausible`: inferred from the problem but not strongly evidenced
- `assumed`: mainly a user or agent assumption
- `needs-evidence`: important but too thin to support confident method design

## Method Needs Confirmation Gate

Do not run Targeted Method Search until the user confirms, revises, or explicitly delegates the Method Need Decomposition.

When asking for confirmation, show:

- the proposed Method Needs,
- which target failure each need addresses,
- which needs are weakly evidenced,
- and the main search consequence of accepting the decomposition.

If several decompositions are plausible, present 2-4 options or a binary tradeoff instead of asking an open-ended question.

## Targeted Method Search

Run Targeted Method Search by default for each confirmed Method Need unless the user explicitly says not to search or search is unavailable.

Targeted Method Search is narrow. It looks for method ideas that satisfy specific Method Needs; it is not a broad related-work scan, a full Field Map Workflow, or baseline selection.

Use three source-paper categories:

- **Same-Problem Papers**: directly solve the same or highly similar problem.
- **Adjacent-Problem Papers**: solve a different problem with a similar mechanism, failure mode, or required capability.
- **Far-Analogy Papers**: come from a more distant field but have a transferable method structure.

For each search result that enters the candidate set, record:

- source URL
- paper title and venue or year when available
- source-paper category
- matched Method Need
- why the paper belongs in that category
- what may transfer
- what probably will not transfer

Do not treat Same-Problem Papers as baselines by default. A paper may inspire a method pattern, become a baseline candidate later, or both, but baseline selection belongs to `paper-reading-experiment-design`.

## Method Search Sufficiency Check

Use coverage by Method Need, not fixed paper count, to decide whether search is sufficient.

For each core Method Need, aim for:

- at least 1 Same-Problem Paper, or a recorded gap if none is found
- 1-2 Adjacent-Problem Papers
- 1 Far-Analogy Paper when a real structural analogy exists, otherwise `none found`
- at least 2 extractable Method Patterns
- at least 1 Method Pattern that passes Need-Pattern Fit

If a core Method Need has no pattern eligible for assembly, mark that need as `needs-search`.

Overall search may stop when every core Method Need has at least one assembly-eligible Method Pattern, or when unresolved `needs-search` gaps are explicitly recorded in the Method Candidate Library.

## Method Pattern Extraction

Write `method_patterns.md` after Targeted Method Search.

A Method Pattern is not a paper summary. Extract only the reusable design pattern that could inspire the user's method.

Each Method Pattern must include:

- source URL
- source paper type: Same-Problem, Adjacent-Problem, or Far-Analogy
- matched Method Need
- original problem setting
- core mechanism
- Transferable Unit
- required assumptions
- inputs and outputs
- integration cost
- transfer risk
- evidence strength

Evidence strength values:

- `strong`: the source paper gives direct empirical or theoretical support for the mechanism
- `moderate`: support is relevant but indirect or limited
- `weak`: the mechanism is plausible but not well isolated
- `unknown`: evidence could not be checked

## Transfer Mapping

Write `transfer_mapping.md` before assembling Candidate Methods.

Transfer Mapping has two layers:

1. Need-Pattern Fit: whether a Method Pattern can satisfy a Method Need.
2. Assembly Role: what role the pattern could play if it enters a Candidate Method.

Need-Pattern Fit must record:

- matched capability
- mismatch
- required adaptation
- transfer boundary
- fit decision: `eligible`, `defer`, `reject`, or `needs-search`

Only Method Patterns with `eligible` fit should be used in Candidate Method Assembly unless the user explicitly asks to include a risky deferred pattern.

Assembly Roles may include input processor, retriever, planner, memory manager, critic, training objective, data generator, evaluation proxy, controller, or another precise role.

Every Method Pattern must receive a Method Pattern Disposition:

- `selected for assembly`
- `deferred`
- `rejected`
- `needs search`

Record reasons such as mismatch, too-strong assumptions, high integration cost, weak evidence, excessive similarity to a baseline, or unclear transfer boundary.

## Candidate Method Assembly

Assemble 3-5 Candidate Methods in `candidate_methods.md`.

Each Candidate Method should combine eligible Method Patterns and make the design space comparable. It is not a final method or implementation plan.

Each Candidate Method must record:

- method thesis
- covered Method Needs
- uncovered Method Needs
- Assembly Roles
- inputs, modules, and outputs
- training flow or inference flow
- source papers by role, with URLs
- novelty hypothesis
- weakest link
- feasibility
- experiment implications
- status: `promising`, `risky`, `too-expensive`, or `needs-search`

Prefer diversity among Candidate Methods. If all candidates are variations of the same idea, either merge them or explain why the design space is genuinely narrow.

## Candidate Method Selection Gate

Do not write `method_candidate_library.md` until the Candidate Method Selection Gate is passed.

This gate confirms the 3-5 Candidate Methods for the library. It does not ask the user to choose a final method or create a Committed Method Design.

When asking for confirmation, show:

- the 3-5 Candidate Methods,
- the Method Needs each covers,
- the source Method Patterns by role,
- the weakest link,
- and the recommended status.

The gate is passed when the user confirms, revises, replaces, or explicitly delegates the Candidate Methods and assembly rationales.

## Method Candidate Library

Write `method_candidate_library.md` only after the source, needs, and candidate-method gates are passed.

The Method Candidate Library must include:

- source problem and evidence status
- Method Needs and confirmation status
- Targeted Method Search coverage and unresolved search gaps
- selected, deferred, and rejected Method Patterns
- Transfer Mappings and Method Pattern Dispositions
- 3-5 Candidate Methods
- source URLs for every source paper used
- risks and weak links
- light downstream routing hints
- a clear statement that the library does not contain a Committed Method Design

Write or update `method_candidate_libraries.md` as a cross-problem summary.

Do not include a prompt that pressures the user to immediately synthesize or commit to a method. If the user wants to turn the library into a Committed Method Design, route to the reserved `paper-reading-method-commitment` workflow.

## Hard Confirmation Gates

Do not skip these gates:

1. **Source confirmed**: do not decompose method needs until exactly one Research Question Card or Source Problem Brief is identified and confirmed.
2. **Method Needs confirmed**: do not run Targeted Method Search until the user confirms, revises, or explicitly delegates the Method Needs.
3. **Candidate Methods confirmed or delegated**: do not write the final Method Candidate Library until the user confirms, revises, replaces, or explicitly delegates the 3-5 Candidate Methods and assembly rationales.

## Required Templates

Use the reference templates in this directory:

- `references/workspace-structure.md`
- `references/source-research-questions-template.md`
- `references/source-problem-template.md`
- `references/method-need-decomposition-template.md`
- `references/targeted-method-search-template.md`
- `references/method-patterns-template.md`
- `references/transfer-mapping-template.md`
- `references/candidate-methods-template.md`
- `references/method-candidate-library-template.md`
- `references/method-candidate-libraries-summary-template.md`

## Stop Condition

Stop when exactly one source problem has:

- a confirmed Method Inspiration Source Gate record,
- a confirmed or explicitly delegated Method Need Decomposition,
- Targeted Method Search attempted or marked unavailable/deferred,
- Method Search Sufficiency checked for each core Method Need,
- Method Patterns extracted with source URLs,
- Transfer Mapping completed with Need-Pattern Fit, Assembly Roles, and Method Pattern Dispositions,
- 3-5 Candidate Methods confirmed or explicitly delegated,
- selected, deferred, and rejected patterns preserved,
- unresolved `needs-search` gaps recorded,
- a Method Candidate Library written,
- `method_candidate_libraries.md` updated,
- and no Committed Method Design forced inside this workflow.
