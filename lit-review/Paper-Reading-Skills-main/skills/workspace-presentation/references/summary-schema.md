# Presentation Module Summary Schema

`public/generated-summaries/*.json` files contain the Derived Presentation Layer. They are generated from source artifacts, source-linked, and safe to regenerate.

## Shape

```json
{
  "schemaVersion": 1,
  "moduleId": "claim-evidence",
  "title": "Claim-Evidence Map",
  "displayCategory": "summarize-then-link",
  "sourceFileIds": ["claim_evidence_map"],
  "summary": "The current claim-evidence map decomposes the method thesis into three testable claims...",
  "takeaways": [
    "The main mechanism claim needs both benchmark evidence and an ablation route."
  ],
  "structuredItems": [
    {
      "label": "Mechanism claim",
      "kind": "claim",
      "status": "needs-review",
      "value": "The lifecycle-aware memory filter reduces harmful long-term influence.",
      "sourceFileIds": ["claim_evidence_map"]
    }
  ],
  "risks": [
    {
      "label": "Proxy mismatch",
      "severity": "medium",
      "description": "The proposed benchmark may show performance gains without exposing the target failure.",
      "sourceFileIds": ["claim_evidence_map"]
    }
  ],
  "nextActions": [
    {
      "label": "Confirm evidence route for the mechanism claim",
      "status": "open",
      "sourceFileIds": ["claim_evidence_map"]
    }
  ],
  "sourceFileIds": ["claim_evidence_map"]
}
```

## Required Fields

- `schemaVersion`: currently `1`.
- `moduleId`: matches the manifest module id.
- `title`: display title.
- `displayCategory`: `primary-display`, `summarize-then-link`, or `link-only`.
- `summary`: short source-linked prose, usually 2-5 sentences.
- `sourceFileIds`: source files used to produce the summary.

## Optional Fields

- `takeaways`: 3-7 bullets for quick reading.
- `structuredItems`: lightweight extracted fields from stable templates.
- `risks`: unresolved risks, blockers, gaps, fragile claims, proxy risks, or do-not-route warnings.
- `nextActions`: concrete follow-up actions visible to the user.
- `status`: module-level state such as `complete`, `provisional`, `needs-review`, `blocked`, or `missing`.
- `missingSources`: expected source files that were not found.

## Extraction Rules

Prefer stable, user-facing fields over exhaustive parsing. Good extracted fields include:

- claims and evidence routes
- verdicts and statuses
- selected candidates or traditions
- baseline pressures and metric validity risks
- unsafe claims, blockers, evidence needs, weak links, and next workflow routing
- source trace and gate confirmation mode

Do not fabricate fields that are absent from source artifacts. If a field is missing but important, record it as a risk or `missingSources` item.
