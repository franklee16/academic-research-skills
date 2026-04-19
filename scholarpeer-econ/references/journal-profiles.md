# Journal Profiles

## Overview

Each finance and economics journal has distinct expectations for manuscripts. These profiles calibrate reviewer personas to journal-specific standards.

---

## Journal of Finance (JF)

**Emphasis:** Identification rigor, causal inference

### Reviewer Calibration

| Dimension | JF Expectation |
|-----------|----------------|
| Identification | Central focus; must be innovative and thoroughly validated |
| Data Quality | High; must support causal claims |
| Robustness | Comprehensive; falsification tests expected |
| Contribution | Important; theoretical grounding valued |
| Clarity | High; accessible to broad finance audience |

### Key Criteria

1. **Identification (Critical)**
   - Innovative design strongly valued
   - DiD: Must address staggered timing (Sun-Abraham, Callaway-Sant'Anna)
   - IV: Must defend exclusion restriction with institutional knowledge
   - RDD: Must show smoothness at cutoff

2. **Robustness (Critical)**
   - Minimum 4 robustness categories
   - Falsification tests expected
   - Event study visualization for DiD

3. **Contribution (Important)**
   - Theoretical motivation strengthens paper
   - Novel question or setting valued
   - Must address "why finance readers care"

### Typical Thresholds

| Score | JF Interpretation |
|-------|-------------------|
| 95+ | Likely accept after revision |
| 90-94 | Borderline; strong identification needed |
| 80-89 | Reject; identification concerns |
| <80 | Desk reject territory |

### Common Rejection Reasons

- Parallel trends violated or untested
- No theoretical motivation
- Marginal contribution
- Robustness incomplete

---

## Review of Financial Studies (RFS)

**Emphasis:** Theoretical contribution, novelty

### Reviewer Calibration

| Dimension | RFS Expectation |
|-----------|-----------------|
| Identification | High; must support theoretical predictions |
| Data Quality | High; institutional detail valued |
| Robustness | Comprehensive; mechanism tests expected |
| Contribution | Critical; theoretical contribution essential |
| Clarity | High; model exposition must be clear |

### Key Criteria

1. **Contribution (Critical)**
   - Theoretical contribution strongly valued
   - Model must be clean and insightful
   - Empirical tests of model predictions expected
   - Novel mechanism valued

2. **Identification (Important)**
   - Must test theoretical predictions
   - Mechanism identification valued
   - Not necessarily causal reduced-form

3. **Novelty (Critical)**
   - New question highly valued
   - New setting if theoretically motivated
   - Cross-disciplinary contributions welcome

### Typical Thresholds

| Score | RFS Interpretation |
|-------|-------------------|
| 95+ | Likely accept; strong contribution |
| 90-94 | Borderline; needs stronger theory |
| 80-89 | Reject; contribution unclear |
| <80 | Desk reject territory |

### Common Rejection Reasons

- No theoretical contribution
- Contribution unclear or marginal
- Model not well-connected to empirics
- Missing mechanism tests

---

## Journal of Financial Economics (JFE)

**Emphasis:** Empirical contribution, data quality

### Reviewer Calibration

| Dimension | JFE Expectation |
|-----------|-----------------|
| Identification | High; standard causal design expected |
| Data Quality | Critical; institutional detail valued |
| Robustness | Comprehensive; standard checks expected |
| Contribution | Important; empirical contribution valued |
| Clarity | High; institutional context must be clear |

### Key Criteria

1. **Data Quality (Critical)**
   - Institutional detail highly valued
   - Novel data sources valued
   - Data construction must be transparent
   - Measurement validation expected

2. **Identification (Important)**
   - Standard causal designs accepted
   - Not as demanding as JF on innovation
   - Must be solid and validated

3. **Empirical Contribution (Important)**
   - New empirical facts valued
   - Detailed institutional knowledge valued
   - Practical relevance valued

### Typical Thresholds

| Score | JFE Interpretation |
|-------|-------------------|
| 92+ | Likely accept |
| 88-91 | Borderline; needs better data/identification |
| 80-87 | Reject; data or identification concerns |
| <80 | Desk reject territory |

### Common Rejection Reasons

- Institutional detail missing
- Data quality concerns
- Standard identification without contribution
- No practical relevance

---

## American Economic Review (AER)

**Emphasis:** General interest, methodology

### Reviewer Calibration

| Dimension | AER Expectation |
|-----------|-----------------|
| Identification | Critical; must be exemplary |
| Data Quality | Critical; replication expected |
| Robustness | Comprehensive; falsification required |
| Contribution | Critical; broad interest required |
| Clarity | Critical; accessible to all economists |

### Key Criteria

1. **Broad Interest (Critical)**
   - Must interest economists outside finance
   - Methodological innovation valued
   - Policy relevance strengthens

2. **Identification (Critical)**
   - Must be exemplary
   - Innovation valued
   - All assumptions tested

3. **Replication (Critical)**
   - Data and code expected
   - Documentation must be complete
   - Replication package required

### Typical Thresholds

| Score | AER Interpretation |
|-------|-------------------|
| 95+ | Likely R&R |
| 90-94 | Borderline; needs broader appeal |
| 80-89 | Reject; narrow contribution |
| <80 | Desk reject territory |

### Common Rejection Reasons

- Too narrow for AER audience
- Identification not exemplary
- Missing replication package
- Contribution not clear to general economists

---

## Quick Reference Table

| Criterion | JF | RFS | JFE | AER |
|-----------|-----|-----|-----|-----|
| **Top Priority** | Identification | Theory | Data | Broad interest |
| **Innovation** | Critical | Critical | Valued | Critical |
| **Robustness** | 4+ categories | 3+ categories | 3+ categories | 4+ categories |
| **Falsification** | Required | Expected | Expected | Required |
| **Theory** | Valued | Essential | Optional | Valued |
| **Institutional Detail** | Important | Important | Critical | Valued |
| **Replication Package** | Expected | Expected | Expected | Required |
| **Accept Threshold** | 95+ | 95+ | 92+ | 95+ |

---

## Applying Journal Profiles

When invoking ScholarPeer-Econ with a journal target:

1. **Load the profile** into reviewer prompts
2. **Weight dimensions** according to journal emphasis
3. **Apply journal-specific criteria** in scoring
4. **Note journal-specific red flags** in review

**Example JF Review:**
- Econometrician focuses heavily on identification validity
- Domain Expert checks theoretical motivation
- Methodologist checks robustness comprehensiveness

**Example RFS Review:**
- Domain Expert focuses on theoretical contribution
- Econometrician checks tests of model predictions
- Methodologist checks mechanism identification
