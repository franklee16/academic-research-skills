# Research Design Patterns

Use these patterns as design analogies, not as claims that a method is valid.

## Policy Change Plus Nearby Comparison

Useful for minimum wage, local regulation, pilot zones, or regional policy.

Core:

```text
clear policy shock + comparable control group + pre/post data + simple outcome
```

Check policy timing, treatment definition, comparison group, pre-policy data, and simultaneous policy changes.

## Region Policy Intensity Times Cohort Exposure

Useful for education, infrastructure, public investment, or policy expansion.

Core:

```text
regions differ in policy intensity; cohorts differ in exposure; identify with region by cohort variation
```

Check whether cohort exposure is real, regional intensity is predetermined, and region/cohort fixed effects are possible.

## Local Industry Exposure Or Shift-Share

Useful for trade, automation, AI, industrial shocks, demand shocks, and sectoral policy.

Core:

```text
initial local industry shares x external industry shock = local exposure
```

Check whether initial shares are predetermined, the shock is external, and pre-trends or alternative exposures can be tested.

## Measurement/Facts With Public Statistical Product

Useful for mobility, opportunity, regional inequality, innovation maps, AI exposure, or market integration.

Core:

```text
new data or measure -> stable group/space/industry pattern -> exploratory mechanism -> reusable statistic
```

Check reliability, reproducibility, economics meaning, and avoidance of overclaiming causality.

## Historical Or Institutional Boundary Comparison

Useful for historical institutions, administrative borders, policy boundaries, and geographic discontinuities.

Core:

```text
treatment differs across boundary; nearby units are otherwise comparable enough
```

Check whether the boundary truly determines treatment, whether geography or demographics jump at the same place, and whether enough near-boundary observations exist.

## Threshold Or Eligibility Rule

Useful for subsidies, school admission, firm regulation, poverty programs, or tax rules.

Core:

```text
eligibility cutoff changes treatment probability around a known threshold
```

Check manipulation, density around cutoff, covariate continuity, enough observations, and robustness to bandwidth.

## When No Pattern Fits

Do not force a causal design. Consider:

- measurement/facts paper;
- descriptive thesis with careful limits;
- theory version;
- policy report;
- changing topic or data path.
