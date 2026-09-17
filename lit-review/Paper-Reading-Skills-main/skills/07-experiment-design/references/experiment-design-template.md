# Experiment Design: {Method Or Question Name}

Experiment Folder: `{workspace-root}/experiment-designs/{field-slug}/{method-or-question-slug}/`

Source Context: `source_experiment_context.md`

Claim-Evidence Map: `claim_evidence_map.md`

Design Status: committed / research-question-level / provisional

Experiment Design Review User Decision: not reviewed / confirmed / explicitly delegated / mixed

## Experiment Stack

| Layer | Included? | Claim IDs | Rationale | Artifact Sections |
| --- | --- | --- | --- | --- |
| Main Effect Experiment | Yes / No | {Claim IDs} | {Why included or omitted} | {Section} |
| Mechanism / Ablation Experiment | Yes / No | {Claim IDs} | {Why included or omitted} | `ablation_and_controls.md` |
| Robustness or Stress Test | Yes / No | {Claim IDs} | {Why included or omitted} | {Section} |
| Generalization Test | Yes / No | {Claim IDs} | {Why included or omitted} | {Section} |
| Human Evaluation or User Study | Yes / No | {Claim IDs} | {Why included or omitted} | {Section} |
| Cost / Efficiency Analysis | Yes / No | {Claim IDs} | {Why included or omitted} | {Section} |
| Failure Analysis | Yes / No | {Claim IDs} | {Why included or omitted} | {Section} |

## Proposed Experiments

### E1. {Experiment Name}

Claim IDs:

- {C1}

Evidence route:

- standard benchmark / targeted workload / synthetic controlled task / real-world case study / ablation study / stress test / human evaluation / user study / error analysis

Task, dataset, workload, or scenario:

- {Setting}

Why this setting matches the target failure:

- {Rationale}

What this setting cannot test:

- {Boundary}

Data availability and reproducibility:

- {Availability}

Protocol:

1. {Step}
2. {Step}
3. {Step}

Comparisons:

- See `baseline_pressure_matrix.md`

Metrics:

- See `claim_metric_map.md`

Ablations and controls:

- See `ablation_and_controls.md`

Expected evidence:

- {What result would support the claim}

Reviewer objection covered:

- {Objection}

Failure interpretation:

- {What different results would mean}

Known validity risks:

- leakage / saturation / distribution mismatch / annotation ambiguity / construct mismatch / prompt sensitivity / other

## Human Evaluation Or User Study Plan

Use only when needed by the claims.

Study purpose:

- {What claim requires human evidence}

Participants or annotators:

- {Population}

Task:

- {Task}

Instrument, rubric, or measurement:

- {Validated instrument, prior-paper rubric, or proposed rubric}

Comparison conditions:

- {Conditions}

Main validity risks:

- {Risks}

Ethics or privacy notes:

- None / {Notes}

## Result Interpretation Contract

| Result Pattern | Interpretation | Required Claim Or Method Update |
| --- | --- | --- |
| Main metric improves but ablation does not drop | Performance claim may hold, mechanism claim is weak | Narrow mechanism claim or redesign ablation |
| Safety improves but task success drops sharply | Method may be over-conservative | Report tradeoff and revise target outcome |
| Strong benchmark result but weak targeted workload result | General performance may hold, target failure may not be solved | Narrow claim or add targeted evidence |
| Human evaluation improves but automatic metric does not | Construct difference may explain mismatch | Downgrade automatic metric or explain construct boundary |
| Close-work baseline matches the method | Novelty or mechanism boundary needs revision | Revisit positioning and method claim |
| Proxy metric improves but direct evidence is missing | Claim remains under-evidenced | Keep claim narrow or record evidence gap |

## Failure Analysis Plan

Failure slices:

- {Slice}

Error categories:

- {Category}

What failure analysis can change:

- claim wording / method boundary / ablation interpretation / baseline inclusion / metric validity / future work

## Experiment Design Review Packets

Use one row per reviewed design decision.

| Packet ID | Decision Area | Claim Or Experiment IDs | Recommendation | User Decision | Resulting Update | Packet Status |
| --- | --- | --- | --- | --- | --- | --- |
| RP1 | Experiment Stack / task or protocol / baseline pressure / metric validity / ablation or control / Result Interpretation Contract | {IDs} | {Recommendation} | confirmed / explicitly delegated / revised / not reviewed | {Update made after user response} | draft / needs revision / accepted / provisional |

## Experiment Design Review Gate

Gate status:

- draft / needs revision / blocked / passed

User decision:

- not reviewed / confirmed / explicitly delegated / mixed

Accepted or delegated decisions:

- Claim decomposition: Yes / No
- Evidence routes: Yes / No
- Experiment Stack: Yes / No
- Required baselines: Yes / No
- Primary metrics: Yes / No
- Ablations, controls, and stress tests: Yes / No
- Result Interpretation Contract: Yes / No

Open issues:

- None / {Issue}

## Revision Log

| Version | Change | Reason |
| --- | --- | --- |
| v1 | Initial Experiment Design | Created after Claim-Evidence Review Gate |
