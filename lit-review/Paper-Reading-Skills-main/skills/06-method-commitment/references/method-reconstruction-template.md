# Method Reconstruction: {Method Name}

Status: Draft / Revised / Ready For Attack / Blocked

Method Commitment Workspace: `{workspace-root}/method-commitments/{field-slug}/`

Method Folder: `{method-slug}/`

Source Method: `source_method.md`

## Method Anatomy

### Method Name

{Name}

### Source Problem

{Exactly one Method Commitment Source Problem}

### Method Thesis

By introducing {mechanism} at {intervention point}, the method aims to improve {target outcome} under {scope}, because {reason it should work}.

### Mechanistic Claim

{Attackable causal hypothesis explaining why the mechanism should work}

### Target Failure

{Failure being addressed}

### Intervention Point

{Write, retrieval, planning, training, inference, tool-call, data construction, or other point}

### Inputs

- {Input}

### Outputs

- {Output}

### Core Mechanism

{Core mechanism}

### Module Breakdown

| Module | Role | Input | Output | Necessary? | Replaceable? |
| --- | --- | --- | --- | --- | --- |
| {Module} | {Role} | {Input} | {Output} | Yes / No / Unclear | Yes / No / Unclear |

### Training Flow Or Inference Flow

1. {Step}
2. {Step}
3. {Step}

### Data Requirements

- {Data, labels, logs, environments, demonstrations, or other requirements}

### Objective, Decision Rule, Or Control Policy

- {Objective, rule, policy, threshold, controller, or N/A}

### Borrowed Inspirations

| Source | Borrowed Element | Role | Boundary |
| --- | --- | --- | --- |
| {Candidate Method, Method Pattern, paper, or user idea} | {Element} | {Role} | {What is not borrowed} |

### Novelty Boundary

- {What is claimed as new}
- {What is explicitly borrowed or close to prior work}
- {What is not claimed}

### Assumptions

| Assumption | Evidence Status | If False |
| --- | --- | --- |
| {Assumption} | supported / plausible / assumed / needs-evidence | {Consequence} |

### Non-Goals

- {Non-goal}

### Replaceable Components

| Component | Replacement Candidate | What Must Stay Invariant |
| --- | --- | --- |
| {Component} | {Alternative} | {Invariant} |

### Method Commitment Downstream Pressure Points

Required ablations:

- {Ablation required to test the Mechanistic Claim}

Implied baseline pressures:

- {Baseline pressure, not a final baseline set}

Implied metric signals:

- {Metric signal, not a final metric formula}

### Weakest Link

- {Most likely point of failure}

### Intentionally Unfrozen Open Decisions

| Decision | Why Left Unfrozen | Blocks Downstream? | Owner / Next Workflow |
| --- | --- | --- | --- |
| {Decision} | {Reason} | Yes / No | {Workflow or person} |

### Candidate Blockers

| Blocker | Why It Blocks | Possible Resolution |
| --- | --- | --- |
| {Blocker or None} | {Reason} | {Resolution} |

## Missing Or Vague Fields

| Field | Issue | Recommended Fix |
| --- | --- | --- |
| {Field} | {Issue} | {Fix} |

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial method reconstruction | Created from Source Method and context review |
