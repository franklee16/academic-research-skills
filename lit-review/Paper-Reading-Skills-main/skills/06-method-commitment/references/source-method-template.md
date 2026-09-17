# Source Method: {Method Name}

Status: Pending / Confirmed / Blocked

Method Commitment Workspace: `{workspace-root}/method-commitments/{field-slug}/`

Method Folder: `{method-slug}/`

## Method Commitment Source Gate

Use this source for the current Method Commitment Workflow: Yes / No

Method Source Mode: `selected-candidate-method` / `user-authored-method` / `hybrid-method` / `reconstructed-from-chat`

Method Commitment Source Problem:

- {Exactly one Research Question Card, Source Problem Brief, or confirmed problem statement}

Gate confirmation mode:

- Confirmed by user / Explicitly delegated / Blocked

Reason method commitment is being run now:

- {User goal, proposal need, downstream workflow need, or other reason}

## Source Method Summary

Current method summary:

- {One-paragraph method description}

Expected improvement:

- {Target outcome or effect}

Core mechanism:

- {Mechanism as currently understood}

Target failure:

- {Failure the method intervenes on}

Intervention point:

- {Where the method acts}

Inputs:

- {Inputs}

Outputs:

- {Outputs}

## Source Artifacts

| Artifact Type | Path Or Source | Found? | Notes |
| --- | --- | --- | --- |
| Source Research Question Card | `{path}` / N/A | Yes / No / N/A |  |
| Source Problem Brief | `{path}` / N/A | Yes / No / N/A |  |
| Candidate Method | `{path}#CM-n` / N/A | Yes / No / N/A |  |
| Method Candidate Library | `{path}` / N/A | Yes / No / N/A |  |
| User-authored description | Current chat / `{path}` / N/A | Yes / No / N/A |  |
| Other source | `{path or citation}` / N/A | Yes / No / N/A |  |

## Hybrid Source Details

Use when Method Source Mode is `hybrid-method`.

| Source Piece | Borrowed? | Discarded? | Role In Source Method | Reason |
| --- | --- | --- | --- | --- |
| CM-1 / paper / pattern / user idea | Yes / No | Yes / No | {Role} | {Rationale} |

Merge rationale:

- {Why the merged method is coherent}

New weakest link created by the merge:

- {Weakest link}

## Constraints And Non-Goals

Known constraints:

- {Data, compute, engineering, time, venue, ethical, or deployment constraints}

Non-goals:

- {What this method should not try to solve}

Evidence status:

- sufficient / needs-evidence / thin / unknown

Open decisions:

- {Open decision or None}

## Minimal Method Brief Completeness

Use when the source is user-authored or reconstructed from chat.

| Required Field | Present? | Notes |
| --- | --- | --- |
| Problem addressed | Yes / No |  |
| Failure intervened on | Yes / No |  |
| Input consumed | Yes / No |  |
| Output produced | Yes / No |  |
| Core mechanism | Yes / No |  |
| Expected improvement | Yes / No |  |
| Non-goals | Yes / No |  |

## Source Gate Decision

Method Commitment Source Gate passed: Yes / No

Decision rationale:

- {Why this is exactly one Source Method bound to exactly one source problem, or what blocks the gate}

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial Source Method record | Created for Method Commitment Workflow |
