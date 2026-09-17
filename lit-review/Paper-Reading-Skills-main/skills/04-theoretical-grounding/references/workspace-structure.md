# Theoretical Grounding Workspace Structure

A Theoretical Grounding Workspace is derived from exactly one Research Question Workspace and reads from completed Problem Reality Check Reports. It lives at:

```text
{workspace-root}/theoretical-groundings/{field-slug}/
```

## Required Structure

```text
{workspace-root}/theoretical-groundings/{field-slug}/
|-- source_research_question_checks.md
|-- groundings/
|   `-- {question-slug}/
|       |-- source_problem.md
|       |-- problem_theory_decomposition.md
|       |-- theory_hooks.md
|       |-- candidate_theoretical_traditions.md
|       |-- selected_theoretical_traditions.md
|       `-- theoretical_grounding.md
`-- theoretical_groundings.md
```

## Artifact Roles

- `source_research_question_checks.md`: Records the source Research Question Workspace, available checked cards, and completed Problem Reality Check Reports that can be grounded.
- `groundings/{question-slug}/source_problem.md`: Records the Theoretical Grounding Source Gate for exactly one checked Research Question Card.
- `groundings/{question-slug}/problem_theory_decomposition.md`: Decomposes the checked problem into phenomenon, mechanism, failure, Theory-Support Claims, and boundary.
- `groundings/{question-slug}/theory_hooks.md`: Records concept relationships extracted from the decomposition.
- `groundings/{question-slug}/candidate_theoretical_traditions.md`: Records 5-8 candidate traditions, Targeted Theory Search evidence, fit, limits, and selection decisions.
- `groundings/{question-slug}/selected_theoretical_traditions.md`: Records the 2-4 selected traditions, user confirmation, support boundaries, and rationale.
- `groundings/{question-slug}/theoretical_grounding.md`: Stores the final claim-centered Theoretical Grounding Report.
- `theoretical_groundings.md`: Summarizes completed single-card groundings and open Theory Evidence Needs.

## Relationship To Research Question Workspace

The Theoretical Grounding Workspace reads from the source Research Question Workspace but does not move, rewrite, or merge Research Question Cards.

Do not modify a Research Question Card unless the user explicitly asks. If theoretical grounding changes the core motivation or framing, record a recommended card revision in `theoretical_grounding.md`.

## Relationship To Problem Reality Check Workspace

The Theoretical Grounding Workspace must read from exactly one completed Problem Reality Check Report for the selected card.

Theoretical grounding preserves Problem Reality Check fragilities. It may reframe them, narrow claims, or identify theory support, but it must not claim that theory alone resolved missing empirical evidence or saturation risk.

## Relationship To Field Map Workspace

The workflow may cite paper records from the source Field Map Workspace through links already present in the Research Question Card or Problem Reality Check.

Targeted Theory Search may add representative theoretical sources to the grounding artifacts, but it should not expand the Field Map Workspace inside this workflow.
