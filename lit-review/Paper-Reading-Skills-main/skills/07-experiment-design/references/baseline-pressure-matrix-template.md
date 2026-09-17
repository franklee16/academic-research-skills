# Baseline Pressure Matrix: {Method Or Question Name}

Experiment Folder: `{workspace-root}/experiment-designs/{field-slug}/{method-or-question-slug}/`

Claim-Evidence Map: `claim_evidence_map.md`

## Baseline Selection Principle

Baselines are selected by the pressure they apply to a claim or reviewer objection, not by popularity alone.

## Baseline Matrix

| Baseline | Pressure Type | Claim IDs | Reviewer Objection Answered | Why Fair | Reproducibility Status | Inclusion Status | Advantage Or Disadvantage | Remaining Weakness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {Baseline} | lower-bound / classic expected / strongest recent / closest prior work / component-equivalent / ablated proposed method / oracle or upper-bound / human reference | {Claim IDs} | {Objection} | {Fairness rationale} | available / reimplemented / unavailable / unclear | required / optional / rejected | {Advantage or disadvantage} | {Weakness} |

## Required Baselines

### {Baseline Name}

Pressure type:

- {Type}

Claim pressured:

- {Claim ID and claim}

Reviewer objection answered:

- {Objection}

Fair comparison protocol:

- {Protocol}

Known unfairness or limitation:

- None / {Limitation}

Reproducibility status:

- {Code, data, implementation, or citation status}

## Optional Baselines

| Baseline | Why Optional | Condition For Inclusion |
| --- | --- | --- |
| {Baseline} | {Reason} | {Condition} |

## Rejected Baselines

Record rejected baselines when a future reviewer may expect them.

| Baseline | Why It Was Considered | Rejection Reason | Risk Of Exclusion |
| --- | --- | --- | --- |
| {Baseline} | {Reason} | mismatch / unfair access / unreproducible / not relevant / superseded / outside scope | {Risk} |

## Baseline Coverage Check

| Pressure Type | Covered? | Baseline Or Gap |
| --- | --- | --- |
| Lower-bound or trivial baseline | Yes / No / N/A | {Baseline or gap} |
| Classic or reviewer-expected baseline | Yes / No / N/A | {Baseline or gap} |
| Strongest recent baseline | Yes / No / N/A | {Baseline or gap} |
| Closest prior work | Yes / No / N/A | {Baseline or gap} |
| Component-equivalent baseline | Yes / No / N/A | {Baseline or gap} |
| Ablated proposed method | Yes / No / N/A | {Baseline or gap} |
| Oracle, upper-bound, or human reference | Yes / No / N/A | {Baseline or gap} |

## Baseline Review Record

Review status:

- draft / needs revision / accepted / provisional

User decision:

- not reviewed / confirmed / explicitly delegated / mixed

Open issues:

- None / {Issue}

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial Baseline Pressure Matrix | Created from Claim-Evidence Map |
