# Problem Reality Check Workspace Structure

A Problem Reality Check Workspace is derived from exactly one Research Question Workspace and lives at:

```text
{workspace-root}/research-question-checks/{field-slug}/
```

## Required Structure

```text
{workspace-root}/research-question-checks/{field-slug}/
|-- source_research_questions.md
|-- checks/
|   `-- {question-slug}/
|       |-- source_card.md
|       |-- interrogation_transcript.md
|       `-- problem_reality_check.md
`-- problem_reality_checks.md
```

## Artifact Roles

- `source_research_questions.md`: Records the source Research Question Workspace and the available cards that can be checked.
- `checks/{question-slug}/source_card.md`: Records the Source Card Gate for exactly one Research Question Card.
- `checks/{question-slug}/interrogation_transcript.md`: Records the turn-by-turn Challenge Questions, provisional recommendations, user responses, and dimension verdicts.
- `checks/{question-slug}/problem_reality_check.md`: Stores the final Problem Reality Check Report for the selected card, derived from the Interrogation Transcript.
- `problem_reality_checks.md`: Summarizes completed single-card checks and open Targeted Evidence Needs.

## Relationship To Research Question Workspace

The Problem Reality Check Workspace reads from the source Research Question Workspace but does not move, rewrite, or merge Research Question Cards.

Each workflow run checks exactly one Research Question Card. If several cards need checking, create or update one per-card folder per separate check run.

Do not write `problem_reality_check.md` before `interrogation_transcript.md` is complete. The final report is a synthesis of the interrogation, not a substitute for it.

## Relationship To Field Map Workspace

The check may cite paper records from the source Field Map Workspace through links already present in the Research Question Card or Research Question Workspace.

If the check reveals that the Field Map Workspace is missing central evidence, record a Targeted Evidence Need instead of expanding the Field Map Workspace inside this workflow.
