# Committed Method Design: {Method Name}

Status: committed

Downstream-ready: Yes

Method Commitment Workspace: `{workspace-root}/method-commitments/{field-slug}/`

Method Folder: `{method-slug}/`

Source Method: `source_method.md`

Method Reconstruction: `method_reconstruction.md`

Method Attack Transcript: `method_attack_transcript.md`

Method Decision Log: `method_decision_log.md`

## Explicit Method Commitment Confirmation

Researcher explicitly confirmed commitment: Yes

Confirmation text or turn:

- {User confirmation}

## Source Problem

{Exactly one Method Commitment Source Problem}

## Method Thesis

By introducing {mechanism} at {intervention point}, the method aims to improve {target outcome} under {scope}, because {reason it should work}.

## Mechanistic Claim

{Attackable causal hypothesis}

## Method Boundary

In scope:

- {In-scope boundary}

Out of scope:

- {Out-of-scope boundary}

## Target Failure And Intervention Point

Target failure:

- {Failure}

Intervention point:

- {Point}

## Inputs And Outputs

Inputs:

- {Input}

Outputs:

- {Output}

## Core Mechanism And Modules

Core mechanism:

- {Mechanism}

Modules:

| Module | Role | Necessary? | Replaceable? |
| --- | --- | --- | --- |
| {Module} | {Role} | Yes / No | Yes / No |

## Training Or Inference Flow

1. {Step}
2. {Step}
3. {Step}

## Data Requirements

- {Data requirement}

## Objective, Decision Rule, Or Control Policy

- {Objective, decision rule, control policy, or N/A}

## Borrowed Inspirations And Novelty Boundary

Borrowed inspirations:

- {Borrowed element and source}

Novelty boundary:

- {What is new}
- {What is borrowed}
- {What is not claimed}

## Assumptions

| Assumption | Evidence Status | Pressure Test |
| --- | --- | --- |
| {Assumption} | supported / plausible / assumed / needs-evidence | {How later work should test it} |

## Non-Goals

- {Non-goal}

## Replaceable Components

| Component | Replacement Candidate | Invariant |
| --- | --- | --- |
| {Component} | {Alternative} | {Invariant} |

## Method Commitment Downstream Pressure Points

Required ablations:

- {Ablation}

Implied baseline pressures:

- {Baseline pressure}

Implied metric signals:

- {Metric signal}

## Weakest Link

- {Weakest link}

## Intentionally Unfrozen Open Decisions

These must be non-blocking for downstream routing.

| Decision | Why Non-Blocking | Later Owner |
| --- | --- | --- |
| {Decision or None} | {Reason} | {Workflow or person} |

## Downstream Routing

Recommended next workflow:

- paper-reading-experiment-design / paper-reading-research-framing / other

Routing rationale:

- {Why}

Do-not-route warnings:

- None / {Warning}

## Commitment Gate Check

| Required Item | Confirmed? | Notes |
| --- | --- | --- |
| Method Thesis | Yes / No |  |
| Mechanistic Claim | Yes / No |  |
| Source Problem | Yes / No |  |
| Core mechanism | Yes / No |  |
| Method boundary | Yes / No |  |
| Inputs and outputs | Yes / No |  |
| Major modules | Yes / No |  |
| Training or inference flow | Yes / No |  |
| Novelty boundary | Yes / No |  |
| Strongest assumptions | Yes / No |  |
| Weakest link | Yes / No |  |
| Downstream pressure points | Yes / No |  |
| Explicit Method Commitment Confirmation | Yes |  |

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial Committed Method Design | Created after Method Commitment Gate |
