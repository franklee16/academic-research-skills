# Claim-Evidence Map: {Method Or Question Name}

Experiment Folder: `{workspace-root}/experiment-designs/{field-slug}/{method-or-question-slug}/`

Source Context: `source_experiment_context.md`

Map Status: draft / needs-revision / review-gate-passed / provisional-sketch

Claim-Evidence Review User Decision: not reviewed / confirmed / explicitly delegated / mixed

## Key Claims

| Claim ID | Claim | Claim Type | Source | Core Claim? | Current Status |
| --- | --- | --- | --- | --- | --- |
| C1 | {Claim} | problem / mechanism / performance / robustness / safety / usability / efficiency / generalization | {Source section} | Yes / No | stable / provisional / weak |

## Claim To Evidence Routes

| Claim ID | Observable Evidence Needed | Evidence Route | Task Or Scenario | Baseline Pressure Needed | Metric Signal Needed | Ablation Or Control Needed | Evidence Strength | Reviewer Objection Answered | Likely Failure Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | {Evidence} | standard benchmark / targeted workload / synthetic controlled task / real-world case study / ablation study / stress test / human evaluation / user study / error analysis | {Task or scenario} | {Pressure} | {Signal} | {Ablation or control} | direct evidence / strong proxy / weak proxy / anecdotal evidence / speculative | {Objection} | {Interpretation} |

## Claim-Evidence Decision Packets

Use one row per core claim or low-risk grouped claim packet.

| Packet ID | Claim IDs | Recommended Decision | User Decision | Resulting Update | Packet Status |
| --- | --- | --- | --- | --- | --- |
| P1 | C1 | accept route / narrow claim / change route / mark evidence gap / ask high-risk challenge | confirmed / explicitly delegated / revised / not reviewed | {Update made after user response} | draft / needs revision / accepted / provisional |

## Evidence Route Rationale

For each core claim, explain why the route is appropriate and what it cannot prove.

### C1: {Short Claim Name}

Why this evidence route fits:

- {Rationale}

What this route cannot prove:

- {Boundary}

Main construct mismatch or proxy risk:

- None / {Risk}

## High-Risk Claim Challenges

Use this section for live challenge questions before the Claim-Evidence Review Gate passes.

| Challenge ID | Skeptical Claim | Hidden Assumption Tested | Why The Current Route May Fail | Evidence Or Design Change Needed | Provisional Recommendation | User Response Or Delegation | Resulting Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | {Skeptical claim} | {Assumption} | {Risk} | {Needed evidence or change} | {Recommendation} | {Response} | {Decision} |

## Claim-Evidence Review Gate

Gate status:

- draft / needs revision / blocked / passed

User decision:

- not reviewed / confirmed / explicitly delegated / mixed

Accepted or delegated decisions:

- Key claim decomposition: Yes / No
- Evidence route for each core claim: Yes / No
- Evidence-strength label for each core claim: Yes / No
- Reviewer-objection mapping: Yes / No
- High-risk proxy decisions answered or delegated: Yes / No / N/A

Open issues:

- None / {Issue}

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial Claim-Evidence Map | Created before benchmark, baseline, or metric selection |
