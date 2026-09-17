# Presentation Manifest Schema

`public/presentation-manifest.json` records the presentation structure. It is generated metadata owned by the Workspace Presentation skill.

## Shape

```json
{
  "schemaVersion": 1,
  "presentation": {
    "title": "Agent Memory Experiment Design",
    "slug": "agent-memory-experiment-design",
    "generatedAt": "2026-06-23T12:00:00+08:00",
    "sourceKind": "experiment-design-workspace",
    "sourcePath": "/absolute/path/to/workspace/experiment-designs/field/method",
    "sourceLabel": "workspace/experiment-designs/field/method",
    "status": "provisional",
    "description": "Interactive presentation of the current experiment design artifacts."
  },
  "sections": [
    {
      "id": "overview",
      "title": "Research State Overview",
      "kind": "overview",
      "summaryFile": "generated-summaries/overview.json"
    }
  ],
  "modules": [
    {
      "id": "claim-evidence",
      "sectionId": "decisions-evidence",
      "title": "Claim-Evidence Map",
      "workflow": "experiment-design",
      "displayCategory": "summarize-then-link",
      "summaryFile": "generated-summaries/claim-evidence.json",
      "sourceFileIds": ["claim_evidence_map"]
    }
  ],
  "sourceFileIds": ["claim_evidence_map", "experiment_design"],
  "warnings": []
}
```

## Required Fields

- `schemaVersion`: currently `1`.
- `presentation.title`: human-readable title.
- `presentation.slug`: output directory slug.
- `presentation.generatedAt`: ISO timestamp.
- `presentation.sourceKind`: one of the source kinds in `presentation-display-map.md`.
- `presentation.sourcePath`: absolute path to the selected source workspace or chain root.
- `sections`: global page sections in display order.
- `modules`: presentation modules in display order.
- `sourceFileIds`: source files included in `source-index.json`.

## Standard Sections

Use this order unless the source workspace genuinely lacks a section:

1. `overview` - Research State Overview
2. `source-trace` - Source Trace
3. `main-artifacts` - Main Artifacts
4. `decisions-evidence` - Decisions & Evidence
5. `risks-gaps` - Risks & Gaps
6. `next-actions` - Next Actions
7. `source-files` - Source Files

## Module Rules

Each module must include:

- stable `id`
- `sectionId`
- `title`
- `workflow`
- `displayCategory`: `primary-display`, `summarize-then-link`, or `link-only`
- `sourceFileIds`

Use `summaryFile` for every Primary Display and Summarize-Then-Link module. Link-Only modules may omit summaries unless a short audit note is useful.
