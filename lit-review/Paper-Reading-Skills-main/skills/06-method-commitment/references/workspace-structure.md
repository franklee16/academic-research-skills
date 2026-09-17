# Method Commitment Workspace Structure

A Method Commitment Workspace contains convergence artifacts for one method outcome. It lives at:

```text
{workspace-root}/method-commitments/{field-slug}/
```

Each run creates or resumes exactly one method folder:

```text
{workspace-root}/method-commitments/{field-slug}/{method-slug}/
```

## Required Structure

```text
{workspace-root}/method-commitments/{field-slug}/
`-- {method-slug}/
    |-- source_method.md
    |-- method_reconstruction.md
    |-- method_attack_transcript.md
    |-- method_decision_log.md
    |-- committed_method_design.md              # only when status is committed
    |-- provisional_method_design.md            # only when status is provisionally-committed
    |-- method_redesign_brief.md                # only when status is needs-redesign
    |-- method_rejection_note.md                # only when status is reject-current-method
    `-- method_commitment_summary.md            # always present
```

Only one status-specific output artifact should exist for the current final status.

## Artifact Roles

- `source_method.md`: Records the Method Commitment Source Gate for exactly one Source Method and one Method Commitment Source Problem.
- `method_reconstruction.md`: Reconstructs the method anatomy before attack.
- `method_attack_transcript.md`: Records high-risk Challenge Questions, user responses or explicit delegations, and resulting design decisions.
- `method_decision_log.md`: Records only structure-changing method decisions.
- `committed_method_design.md`: Stores the downstream-ready method design when status is `committed`.
- `provisional_method_design.md`: Stores a nearly stable but blocked design when status is `provisionally-committed`.
- `method_redesign_brief.md`: Records why the current method needs redesign and what can be salvaged.
- `method_rejection_note.md`: Records why the current method should not proceed.
- `method_commitment_summary.md`: Always-present routing index with status, output artifact, blockers, next workflow, and do-not-route warnings.

## Relationship To Later Workflows

Only `committed_method_design.md` is a normal source for experiment design or research-framing workflows. Baseline and metric selection are part of experiment design.

If the status is `provisionally-committed`, `needs-redesign`, or `reject-current-method`, the summary must include do-not-route warnings and the blocking reason.
