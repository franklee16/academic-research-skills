# Ablation And Controls Plan: {Method Or Question Name}

Experiment Folder: `{workspace-root}/experiment-designs/{field-slug}/{method-or-question-slug}/`

Claim-Evidence Map: `claim_evidence_map.md`

## Ablation Principle

Ablations and controls must test the Mechanistic Claim or a named assumption. Do not include decorative component removals that cannot change claim interpretation.

## Ablation And Control Matrix

| Test ID | Test Type | Mechanism Or Assumption Tested | Claim IDs | Expected Result If Mechanistic Claim Holds | Interpretation If Performance Does Not Change | Interpretation If Performance Drops | Confound Controlled | Supports Mechanism Or Changes Access? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | component removal / intervention-point ablation / data-source ablation / objective ablation / stress test / negative control / sanity check / confound check | {Mechanism or assumption} | {Claim IDs} | {Expected result} | {Interpretation} | {Interpretation} | {Confound} | mechanism support / information access / compute / strictness / utility / unclear |

## Required Ablations

### A1. {Ablation Name}

Mechanism or assumption tested:

- {Mechanism or assumption}

Experimental change:

- {What changes compared with the full method}

Expected result if the Mechanistic Claim holds:

- {Expected result}

Interpretation if performance does not change:

- {Interpretation}

Interpretation if performance drops:

- {Interpretation}

Risk of misleading interpretation:

- {Risk}

## Stress Tests

| Stress Test | Weakest Link Tested | Claim IDs | Failure Boundary Exposed | Expected Interpretation |
| --- | --- | --- | --- | --- |
| {Stress test} | {Weakest link} | {Claim IDs} | {Boundary} | {Interpretation} |

## Negative Controls And Sanity Checks

| Check | Purpose | Expected Result | Interpretation If Failed |
| --- | --- | --- | --- |
| {Check} | leakage / prompt sensitivity / annotation bias / unfair baseline access / data contamination / other | {Expected result} | {Interpretation} |

## Confound Checklist

| Confound | Checked? | Control Or Mitigation | Remaining Risk |
| --- | --- | --- | --- |
| Data leakage | Yes / No / N/A | {Control} | {Risk} |
| Prompt sensitivity | Yes / No / N/A | {Control} | {Risk} |
| Annotation bias | Yes / No / N/A | {Control} | {Risk} |
| Unfair baseline access | Yes / No / N/A | {Control} | {Risk} |
| Compute or tool budget mismatch | Yes / No / N/A | {Control} | {Risk} |
| Distribution mismatch | Yes / No / N/A | {Control} | {Risk} |

## Ablation And Control Review Record

Review status:

- draft / needs revision / accepted / provisional

User decision:

- not reviewed / confirmed / explicitly delegated / mixed

Open issues:

- None / {Issue}

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial Ablation And Controls Plan | Created from Claim-Evidence Map |
