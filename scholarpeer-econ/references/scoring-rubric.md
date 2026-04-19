# Scoring Rubric

## Overview

This rubric ensures consistent scoring across reviewer personas and manuscripts. All reviewers use the same 1-5 scale for each dimension, with detailed criteria for each score level.

---

## Score Definitions

| Score | Label | Interpretation |
|-------|-------|----------------|
| 5 | Excellent | Exceeds journal standards; could be model for field |
| 4 | Good | Meets journal standards; minor improvements possible |
| 3 | Adequate | Meets minimum standards; some concerns exist |
| 2 | Weak | Below journal standards; substantial revision needed |
| 1 | Poor | Serious deficiencies; fundamental rethink required |

---

## Dimension-by-Dimension Rubric

### 1. Identification Strategy

| Score | Criteria | Evidence |
|-------|----------|----------|
| **5** | Innovative, thoroughly validated, sets new standard | Multiple falsification tests; addresses all assumptions; robustness to alternative specifications |
| **4** | Solid identification with appropriate validation | Key assumptions tested; robustness checks; at least one falsification |
| **3** | Acceptable but with concerns | Assumptions stated but not fully tested; robustness incomplete |
| **2** | Gaps in identification | Key assumptions unaddressed; no falsification; specification concerns |
| **1** | No credible identification | Confounded design; results not interpretable as causal |

**Common Deductions:**
- No parallel trends test (DiD): -1 to -2
- No instrument validity discussion (IV): -2
- Staggered timing not addressed: -1
- Missing event study: -0.5

### 2. Data Quality

| Score | Criteria | Evidence |
|-------|----------|----------|
| **5** | Exemplary; model for field | Data construction fully documented; replication package complete; novel high-quality data |
| **4** | High quality; replication straightforward | Clear documentation; standard data quality; data available |
| **3** | Adequate; some gaps | Basic documentation; minor quality concerns; replication possible |
| **2** | Concerns present | Opaque construction; quality issues; replication difficult |
| **1** | Serious problems | Data unsuitable; measurement issues; results not credible |

**Common Deductions:**
- No variable construction details: -1 to -2
- No discussion of measurement error: -0.5
- Sample selection unexplained: -1
- No data availability statement: -0.5

### 3. Robustness

| Score | Criteria | Evidence |
|-------|----------|----------|
| **5** | Comprehensive; results ironclad | All major robustness categories; falsification tests; sensitivity analysis |
| **4** | Solid; includes falsification | 4+ robustness checks; at least one falsification; results stable |
| **3** | Standard; results generally stable | 2-3 robustness checks; limited falsification |
| **2** | Limited; sensitivity unclear | 1-2 checks; no falsification; results sensitive |
| **1** | None; results fragile | No robustness checks; results highly sensitive |

**Minimum Requirements by Journal:**

| Journal | Robustness Expectation |
|---------|----------------------|
| JF | 4+ categories + falsification |
| RFS | 3+ categories |
| JFE | 3+ categories |
| AER | 4+ categories + falsification |

### 4. Contribution

| Score | Criteria | Evidence |
|-------|----------|----------|
| **5** | Transformative; opens new agenda | Novel question/method/setting; theoretical and empirical contribution; broad impact |
| **4** | Important; fills major gap | Clear contribution; literature properly positioned; advances field |
| **3** | Solid; incremental contribution | Adds to literature; properly positioned; not breakthrough |
| **2** | Marginal; minor extension | Small step beyond existing work; positioning unclear |
| **1** | No contribution | Duplicates existing research; no clear advancement |

**Contribution Types (in order of typical value):**
1. New research question + new identification
2. New identification for existing question
3. New data/setting for existing question
4. New mechanism for existing relationship
5. Replication in new setting

### 5. Clarity

| Score | Criteria | Evidence |
|-------|----------|----------|
| **5** | Exemplary; teaching quality | Clear question; intuitive mechanism; accessible methods; balanced discussion |
| **4** | Clear; minor improvements | Well-organized; mostly clear; small passages need work |
| **3** | Adequate; needs revision | Generally clear; some unclear passages; organization issues |
| **2** | Unclear; substantial revision | Hard to follow; poor organization; technical jargon |
| **1** | Poorly written | Incomprehensible; no structure; unusable |

**Common Deductions:**
- Unclear research question: -1
- Missing intuition: -1
- Overstated conclusions: -1
- Hedging language: -0.5 per instance
- Poor organization: -1

---

## Confidence Levels

Each dimension score includes a confidence level indicating reviewer certainty.

| Confidence | Interpretation |
|------------|----------------|
| **High** | Score is definitive; reviewer is certain |
| **Medium** | Score is tentative; additional information could change it |
| **Low** | Score is preliminary; major uncertainty exists |

**When to use Low/Medium:**
- Missing information prevents definitive assessment
- Reviewer lacks expertise in specific area
- Disagreement between reviewers

---

## Disagreement Resolution

When reviewers differ by >1 point:

1. **Identify source:**
   - Different information?
   - Different expertise?
   - Different standards?

2. **Seek common ground:**
   - What evidence would resolve the disagreement?
   - Is there a factual basis for one position?

3. **Document outcome:**
   - Consensus: Note resolution in discussion transcript
   - Disagreement: Document both positions with confidence levels

---

## Overall Score Calculation

```
Overall = (Identification × 0.30 + Data × 0.20 + Robustness × 0.20 + Contribution × 0.20 + Clarity × 0.10) × 20
```

**Example:**
- Identification: 4
- Data: 4
- Robustness: 3
- Contribution: 4
- Clarity: 4

```
Overall = (4×0.30 + 4×0.20 + 3×0.20 + 4×0.20 + 4×0.10) × 20
        = (1.2 + 0.8 + 0.6 + 0.8 + 0.4) × 20
        = 3.8 × 20
        = 76
```

**Interpretation:** Major revisions recommended (70-79 range)

---

## Threshold Guidelines

| Overall Score | Recommendation | Next Steps |
|---------------|----------------|------------|
| 95-100 | Accept / Ready for submission | Proceed to submission |
| 90-94 | Minor revision | Address minor issues; resubmit |
| 80-89 | Major revision | Address major issues; re-review recommended |
| 70-79 | Revise and resubmit | Fundamental issues; rethink approach |
| <70 | Reject | Not ready for publication |
