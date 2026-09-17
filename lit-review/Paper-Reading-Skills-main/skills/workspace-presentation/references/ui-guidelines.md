# Workspace Presentation UI Guidelines

Build a research-material reader, not a landing page, marketing site, or slide deck.

## Information Architecture

The first screen is `Research State Overview`. It should show the source, workflow status, 3-7 takeaways, unresolved risks or blockers, next actions, and navigation into modules.

Use the standard page sections:

1. Research State Overview
2. Source Trace
3. Main Artifacts
4. Decisions & Evidence
5. Risks & Gaps
6. Next Actions
7. Source Files

## Layout

Use a dense but calm three-zone layout on desktop:

- left navigation for sections and modules
- central reading area for summaries, structured fields, and markdown previews
- right panel for source metadata, source links, risks, and selected module details

On narrow screens, collapse navigation and metadata into stacked sections. Text and controls must not overlap or resize the layout unexpectedly.

## Interaction

Expected controls:

- tabs or segmented controls for sections
- search for module titles and source files
- filters for display category, status, risk severity, and workflow
- expandable markdown preview for source files
- source links visible from every derived summary
- badges for status, workflow, risk, and display category

Do not make the app editable. Source artifacts are changed through the user's editor or agent conversation, not through the presentation.

## Visual Style

Use a quiet, work-focused interface suitable for long reading:

- restrained neutral background
- clear type hierarchy
- compact panels with stable spacing
- icons for actions and categories where useful
- no hero section, decorative gradients, oversized marketing copy, or ornamental backgrounds
- no nested UI cards

Primary content should be scannable: summaries first, structured fields next, source preview on demand.
