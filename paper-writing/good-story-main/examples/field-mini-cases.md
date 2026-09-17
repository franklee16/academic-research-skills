# Field Mini Cases

These examples show how different fields can use the same story logic while respecting different evidence standards.

The shared logic is:

`what readers assume or need -> what remains blocked -> what evidence changes -> what can now be claimed -> why it matters`

## Ecology

### Loose Material

Plant diversity increased productivity in one grassland experiment, but the effect was strongest during dry years.

### Weak Story

> Biodiversity improves ecosystem productivity.

### Better Story

> Biodiversity matters most when the system is stressed: in this grassland experiment, diverse plots maintained productivity better during dry years, suggesting that diversity can buffer function under climatic stress.

### Calibration

- Evidence standard: field experiment, site context, treatment design, year-to-year variation.
- Strongest claim: conditional buffering effect in this system.
- Main risk: turning one grassland experiment into universal ecosystem law.

## Remote Sensing

### Loose Material

A satellite-derived vegetation product detects drought stress earlier than a standard index in two validation regions.

### Weak Story

> Our product enables global drought prediction.

### Better Story

> The product improves early detection of vegetation stress in validated regions by capturing canopy change before the standard index responds.

### Calibration

- Evidence standard: ground validation, sensor uncertainty, temporal transfer, regional coverage.
- Strongest claim: earlier detection in validated regions.
- Main risk: treating a product signal as global prediction or causal drought attribution.

## AI4Science

### Loose Material

A model predicts candidate catalysts faster than simulation and finds several high-scoring candidates in retrospective benchmarks.

### Weak Story

> The model discovers new catalysts.

### Better Story

> The model reduces the catalyst search space by identifying candidates that reproduce known simulation rankings and should be prioritized for prospective validation.

### Calibration

- Evidence standard: leakage checks, out-of-distribution tests, physics constraints, prospective validation.
- Strongest claim: search-space reduction and candidate prioritization.
- Main risk: calling benchmark success a scientific discovery before validation.

## Social Science

### Loose Material

Survey and interview data show that a policy is experienced differently by urban and rural households.

### Weak Story

> The policy fails rural households.

### Better Story

> The policy produces uneven burdens because rural households face access constraints that the policy design assumes away.

### Calibration

- Evidence standard: construct validity, sampling, identification strategy, interview triangulation.
- Strongest claim: mechanism of uneven burden in the studied population.
- Main risk: universalizing a situated sample or using causal language without support.

## Biomedical Research

### Loose Material

A biomarker correlates with treatment response in a retrospective cohort and is supported by cell-line mechanism experiments.

### Weak Story

> The biomarker predicts clinical benefit and can guide treatment.

### Better Story

> The biomarker is a candidate stratification signal that links a plausible mechanism to retrospective treatment response and warrants prospective validation.

### Calibration

- Evidence standard: cohort design, confounding, endpoint relevance, mechanism, prospective validation.
- Strongest claim: candidate biomarker for stratification.
- Main risk: jumping from association and cell-line mechanism to clinical decision-making.

## How To Make Your Own Field Case

Use this schema:

```markdown
## Field

### Loose Material

### Weak Story

### Better Story

### Calibration

- Evidence standard:
- Strongest claim:
- Main risk:
```

The field can be materials science, geoscience, education, economics, history, law, public health, or anything else. The point is to make the evidence contract visible before improving the prose.
