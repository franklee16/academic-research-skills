# Research Question Workspace Structure

A Research Question Workspace is derived from exactly one Field Map Workspace and lives at:

```text
{workspace-root}/research-questions/{field-slug}/
```

## Required Structure

```text
{workspace-root}/research-questions/{field-slug}/
|-- source_field_map.md
|-- writing_intent.md
|-- candidate_angles.md
|-- evidence/
|   `-- {angle-or-question-slug}.md
|-- cards/
|   `-- {question-slug}.md
`-- research_question_cards.md
```

## Artifact Roles

- `source_field_map.md`: Records the source Field Map Workspace, completeness check, imported Research Opportunity Candidates, and known limits.
- `writing_intent.md`: Records the user's primary writing goal, secondary goals, practical constraints, and target research direction or venue.
- `candidate_angles.md`: Lists Candidate Angles derived from Research Opportunity Candidates and ranks them against the Writing Intent.
- `evidence/`: Stores Supporting Evidence collected when the source Field Map Workspace is not sufficient for a selected Candidate Angle.
- `cards/`: Stores one Research Question Card per supported selected Candidate Angle.
- `research_question_cards.md`: Summarizes, compares, and records decisions across Research Question Cards.

## Relationship To Field Map Workspace

The Research Question Workspace must link back to the source Field Map Workspace. It may cite paper records from the Field Map Workspace, but it should not move or rewrite Field Map artifacts.

If Supporting Evidence reveals that the Field Map Workspace is missing central papers, note that in the relevant evidence file and Research Question Card.
