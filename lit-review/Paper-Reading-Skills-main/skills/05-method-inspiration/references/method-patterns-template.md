# Method Patterns: {Short Name}

Status: Draft / Complete

Method Inspiration Workspace: `{workspace-root}/method-inspirations/{field-slug}/`

Inspiration Folder: `inspirations/{problem-slug}/`

Source Search: `targeted_method_search.md`

## Pattern Extraction Rule

Extract reusable method design patterns, not paper summaries. Every pattern must include a source URL.

## Method Patterns

| ID | Pattern Name | Source Paper Type | Source Paper | Source URL | Matched Method Need | Original Setting | Core Mechanism | Transferable Unit | Required Assumptions | Inputs | Outputs | Integration Cost | Transfer Risk | Evidence Strength |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MP-1 | {Name} | Same-Problem / Adjacent-Problem / Far-Analogy | {Title, year} | {URL} | MN-1 | {Setting} | {Mechanism} | module / objective / training flow / inference flow / data construction / filter / router / memory update / critic / controller / other | {Assumptions} | {Inputs} | {Outputs} | low / medium / high | {Risk} | strong / moderate / weak / unknown |
| MP-2 | {Name} | Same-Problem / Adjacent-Problem / Far-Analogy | {Title, year} | {URL} | MN-2 | {Setting} | {Mechanism} | {Unit} | {Assumptions} | {Inputs} | {Outputs} | low / medium / high | {Risk} | strong / moderate / weak / unknown |

## Pattern Notes

### MP-1: {Pattern Name}

What the paper actually showed:

- {Evidence summary}

What can transfer:

- {Transferable piece}

What must not be copied directly:

- {Boundary}

## Evidence Strength Summary

| Evidence Strength | Patterns | Main Concern |
| --- | --- | --- |
| strong | MP-{n} | {Concern or None} |
| moderate | MP-{n} | {Concern} |
| weak | MP-{n} | {Concern} |
| unknown | MP-{n} | {Concern} |

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial Method Patterns | Extracted from Targeted Method Search |
