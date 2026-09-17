# Experiment Design Workspace Structure

Experiment Design artifacts live at:

```text
{workspace-root}/experiment-designs/{field-slug}/
```

Each run creates or resumes exactly one method or question folder:

```text
{workspace-root}/experiment-designs/{field-slug}/{method-or-question-slug}/
```

## Required Structure

```text
{workspace-root}/experiment-designs/{field-slug}/
`-- {method-or-question-slug}/
    |-- source_experiment_context.md
    |-- claim_evidence_map.md
    |-- experiment_design.md
    |-- baseline_pressure_matrix.md
    |-- claim_metric_map.md
    `-- ablation_and_controls.md
```

## Artifact Roles

- `source_experiment_context.md`: Records the Experiment Design Source Gate, source status, Method Thesis or research question, Mechanistic Claim when available, target failure, intervention point, target outcome, scope, non-goals, inherited warnings, and Minimal Experiment Brief when needed.
- `claim_evidence_map.md`: Decomposes claims into observable evidence, evidence routes, evidence-strength labels, baseline pressure, metric signals, ablation needs, reviewer objections, and the Claim-Evidence Review Gate record.
- `experiment_design.md`: Defines the Experiment Stack, tasks, datasets, workloads, protocols, human evaluation or user study plan when needed, expected evidence, failure analysis, and Result Interpretation Contract.
- `baseline_pressure_matrix.md`: Selects baselines by the pressure they apply to claims and reviewer objections, including fairness, reproducibility, inclusion status, and remaining weakness.
- `claim_metric_map.md`: Maps claims to observable constructs, metrics, measurement protocols, success criteria, validity risks, proxy strength, and failure interpretation.
- `ablation_and_controls.md`: Specifies mechanism-linked ablations, controls, stress tests, sanity checks, confound checks, and what each result would mean.

## Relationship To Upstream Workflows

A `committed_method_design.md` from Method Commitment is the normal source for a final experiment plan.

If the source is a Research Question Card, Source Problem Brief, rough method, or non-committed method, the folder may still be created, but downstream artifacts must be marked `provisional` until the source method is stabilized.

Do not treat Method Commitment Downstream Pressure Points as a final experiment protocol. Use them as inputs to the Claim-Evidence Map, then decide tasks, baselines, metrics, ablations, and result interpretations inside this workflow.
