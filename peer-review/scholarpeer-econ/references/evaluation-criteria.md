# Evaluation Criteria for Finance and Economics

## Overview

Finance and economics manuscripts are evaluated on five core dimensions, each scored on a 1-5 scale. The overall score is a weighted average converted to a 100-point scale.

---

## Dimension 1: Identification Strategy (30% weight)

**Definition:** The validity and appropriateness of the causal identification approach.

### Key Elements

**For DiD:**
- [ ] Parallel trends assumption stated and tested
- [ ] Pre-trends visualization
- [ ] Staggered timing addressed if applicable (Callaway-Sant'Anna, Sun-Abraham, etc.)
- [ ] Event study specification

**For IV:**
- [ ] Instrument relevance (first stage F-stat > 10)
- [ ] Exclusion restriction discussed and justified
- [ ] Overidentification test if multiple instruments

**For RDD:**
- [ ] Bandwidth choice justified
- [ ] Continuity assumption discussed
- [ ] Manipulation test (McCrary density test)
- [ ] Polynomial order selection

**For Synthetic Control:**
- [ ] Pre-treatment fit (RMSPE)
- [ ] Inference (placebo tests, permutation)
- [ ] Donor pool construction

**For Event Studies:**
- [ ] Event window justification
- [ ] Benchmark model specification
- [ ] Announcement vs. implementation effects

### Scoring

| Score | Criteria |
|-------|----------|
| 5 | Innovative identification; thoroughly validated; sets new standard |
| 4 | Solid identification with appropriate robustness and falsification |
| 3 | Acceptable identification; minor concerns in assumptions or tests |
| 2 | Identification gaps; key assumptions untested or implausible |
| 1 | No credible identification; results likely confounded |

---

## Dimension 2: Data Quality (20% weight)

**Definition:** The appropriateness, construction, and documentation of data.

### Key Elements

- [ ] Data source is appropriate for research question
- [ ] Sample construction is clearly described
- [ ] Key variables are properly measured and validated
- [ ] Attrition and missing data are addressed
- [ ] Summary statistics are comprehensive
- [ ] Data will be available for replication

### Common Issues

| Issue | Severity |
|-------|----------|
| Opaque data construction | Major |
| Unvalidated proxy variables | Major |
| Arbitrary sample restrictions | Major |
| Missing summary statistics | Minor |
| No discussion of measurement error | Minor |

### Scoring

| Score | Criteria |
|-------|----------|
| 5 | Exemplary data; model for transparency |
| 4 | High-quality data; replication straightforward |
| 3 | Adequate data; some documentation gaps |
| 2 | Data quality concerns; replication difficult |
| 1 | Serious data problems; results not credible |

---

## Dimension 3: Robustness (20% weight)

**Definition:** The comprehensiveness of sensitivity analysis and robustness checks.

### Standard Robustness Categories

1. **Specification robustness**
   - Alternative control variables
   - Alternative functional forms
   - Alternative clustering

2. **Sample robustness**
   - Alternative sample periods
   - Alternative sample restrictions
   - Leave-one-out analysis

3. **Measurement robustness**
   - Alternative variable definitions
   - Alternative data sources

4. **Method robustness**
   - Alternative estimators
   - Alternative bandwidths (RDD)
   - Alternative instruments (IV)

5. **Falsification tests**
   - Placebo outcomes
   - Placebo treatments
   - Pre-treatment periods

### Minimum Requirements by Journal

| Journal | Minimum Robustness |
|---------|-------------------|
| JF | 4+ robustness categories + falsification |
| RFS | 3+ robustness categories |
| JFE | 3+ robustness categories |
| AER | 4+ robustness categories + falsification |

### Scoring

| Score | Criteria |
|-------|----------|
| 5 | Comprehensive robustness; results ironclad |
| 4 | Solid robustness with falsification tests |
| 3 | Standard robustness; results generally stable |
| 2 | Limited robustness; sensitivity unclear |
| 1 | No robustness checks; results fragile |

---

## Dimension 4: Contribution (20% weight)

**Definition:** The novelty and importance of the research contribution.

### Assessment Framework

1. **Literature gap**
   - Is the gap clearly identified?
   - Is the gap meaningful?

2. **Contribution type**
   - New question?
   - New identification?
   - New data?
   - New setting?
   - New mechanism?

3. **Magnitude of contribution**
   - Transformative (opens new agenda)
   - Important (fills major gap)
   - Incremental (adds to literature)
   - Marginal (minor extension)

### Journal-Specific Standards

| Journal | Contribution Threshold |
|---------|----------------------|
| JF | Important + identification innovation |
| RFS | Important + theoretical grounding |
| JFE | Important + empirical contribution |
| AER | Important + broad interest |

### Scoring

| Score | Criteria |
|-------|----------|
| 5 | Transformative; opens new research agenda |
| 4 | Important; fills major gap in literature |
| 3 | Solid; clear incremental contribution |
| 2 | Marginal; minor extension of existing work |
| 1 | No contribution; duplicates existing research |

---

## Dimension 5: Clarity (10% weight)

**Definition:** The clarity of writing, organization, and exposition.

### Key Elements

- [ ] Research question is clearly stated
- [ ] Hypotheses/predictions are testable
- [ ] Methods are comprehensible to non-specialists
- [ ] Results are presented clearly
- [ ] Discussion is balanced and appropriately caveated
- [ ] Writing is concise and well-organized

### Common Issues

| Issue | Deduction |
|-------|-----------|
| Unclear research question | -1 |
| Missing intuition for mechanism | -1 |
| Over-technical exposition | -1 |
| Overstated conclusions | -1 |
| Poor organization | -1 |
| Hedging language | -0.5 |

### Scoring

| Score | Criteria |
|-------|----------|
| 5 | Exemplary clarity; could be teaching example |
| 4 | Clear and well-organized; minor improvements possible |
| 3 | Adequately clear; some passages need revision |
| 2 | Unclear in places; substantial revision needed |
| 1 | Poorly written; difficult to follow |

---

## Overall Score Calculation

```
Overall Score = 
  Identification (30%) × 20 +
  Data Quality (20%) × 20 +
  Robustness (20%) × 20 +
  Contribution (20%) × 20 +
  Clarity (10%) × 20
```

**Scale:**
- 95-100: Ready for submission
- 90-94: Minor revisions recommended
- 80-89: Major revisions recommended
- 70-79: Fundamental issues; rethink approach
- < 70: Not ready for submission
