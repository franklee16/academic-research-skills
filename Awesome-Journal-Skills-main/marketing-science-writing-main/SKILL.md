---
name: marketing-science-writing
description: Use when writing or revising marketing science papers targeting Marketing Science, JMR, JM, JCR, JAMS, IJRM, QME, Marketing Letters. Covers the full pipeline: substantive problem framing, consumer utility modeling, identification strategy design, structural estimation (BLP, GMM), field/lab experiments, conjoint analysis, counterfactual simulations, and marketing implications with actionable managerial recommendations.
---

# Marketing Science Paper Writing

## Overview

Marketing Science papers follow a distinct pipeline: **Substantive Problem → Consumer + Firm Model → Identification Strategy → Estimation/Experiment → Counterfactual Analysis → Marketing Implications**. Unlike MS&E papers that prioritize analytical derivation, marketing papers are evaluated on the **credibility of the empirical identification** and the **managerial actionability of the counterfactual**.

This skill provides journal-specific guidance for 8 flagship marketing journals, covering structural modeling, causal inference, field experiments, conjoint analysis, and consumer analytics.

**Core Principle**: A marketing paper is an **empirical argument about consumer or firm behavior with testable implications**. Every model, regression, and experiment must answer: "What should a Chief Marketing Officer do differently because of this finding?"

---

## When to Use This Skill

- Drafting a paper targeting Marketing Science, JMR, JM, JCR, JAMS, IJRM, QME, or Marketing Letters
- Designing a structural model of consumer demand (BLP, dynamic structural, discrete choice)
- Planning identification strategy (IV, DID, RDD, field experiment, lab experiment)
- Writing up conjoint analysis, demand estimation, or field experiment results
- Conducting counterfactual policy simulations (merger, tax, product introduction)
- Formulating substantive marketing implications from empirical results
- Addressing endogeneity concerns in observational marketing data

---

## Journal Selection Quick Reference

### Tier 1: Top Marketing Journals

| Journal | Core Identity | Ideal Paper Profile |
|---------|--------------|---------------------|
| **Marketing Science** (MktSci) | Quantitative, model-driven, structural | Structural model + novel data + counterfactual showing substantive managerial impact. ~35 pages. |
| **Journal of Marketing Research** (JMR) | Empirical rigor, identification credibility | Well-identified study (experiment/quasi-experiment) + clear managerial recommendations. ~40 pages. |
| **Journal of Marketing** (JM) | Broad strategy, conceptual + empirical | Conceptual framework + multi-method validation; strong on marketing strategy. ~40 pages. |
| **Journal of Consumer Research** (JCR) | Consumer psychology, behavioral | Theory-driven lab/field experiments testing psychological mechanisms. ~40 pages. |

### Tier 2: Strong Field Journals

| Journal | Core Identity | Ideal Paper Profile |
|---------|--------------|---------------------|
| **JAMS** (J. Academy of Marketing Science) | Broad scope, reviews valued | Conceptual + empirical; strong review papers; AMA-affiliated |
| **IJRM** (Int. J. Research in Marketing) | European tradition, diverse methods | All methods welcomed; strong special issue culture |
| **QME** (Quantitative Marketing & Economics) | Structural IO approach | Rigorous structural econometrics; smaller volume, higher technical bar |
| **Marketing Letters** | Short, sharp empirical | Concise empirical contributions (~20 pages); replication-friendly |

### Decision Flowchart

```
What is your primary method?
├── Structural econometric model (BLP, dynamic) → Marketing Science, QME
├── Field experiment (A/B test, RCT) → JMR, Marketing Science
├── Lab experiment (psychological mechanism) → JCR, JMR
├── Multi-method empirical (survey + secondary) → JM, JAMS
├── Conceptual/theoretical framework → JM, JAMS, JCR
└── Short empirical note → Marketing Letters
```

---

## The Marketing Paper Structure

Unlike IMRAD or MS&E papers, marketing papers have a distinctive structure driven by the identification narrative:

| Section | Typical Pages | Key Content |
|---------|--------------|-------------|
| Abstract | 150-200 words | Substantive problem, method, key finding, substantive marketing implication |
| S1 Introduction | 2-3 pages | Motivating marketing phenomenon → Research gap → Identification approach → Contributions |
| S2 Conceptual Framework / Model | 3-6 pages | Consumer utility specification, firm objective, market equilibrium, hypotheses |
| S3 Data & Identification | 4-8 pages | Data sources, sample construction, identification strategy, institutional context |
| S4 Estimation / Experiment Design | 3-6 pages | Estimator specification, experimental protocol, diagnostic tests, main results |
| S5 Counterfactuals / Robustness | 3-5 pages | Policy simulations, heterogeneity analysis, alternative specifications, placebo tests |
| S6 Discussion & Marketing Implications | 1-2 pages | What should marketers DO differently? Theoretical contributions. Limitations. |
| References | — | 40-80 papers typical |
| Appendix | Unlimited | Additional robustness, alternative specifications, simulation details |

---

## Methodology Guide by Approach

### 1. Structural Econometric Modeling

See [references/structural-modeling.md](references/structural-modeling.md) for comprehensive guidance.

**The BLP Framework** (Berry-Levinsohn-Pakes, 1995)—the workhorse for aggregate demand estimation:

$u_{ijt} = \alpha_i p_{jt} + \beta_i x_{jt} + \xi_{jt} + \varepsilon_{ijt}$

Key elements:
- Consumer heterogeneity via random coefficients ($\alpha_i, \beta_i$)
- Price endogeneity addressed via instruments (cost shifters, Hausman instruments, BLP differentiation IVs)
- Demand inversion via contraction mapping: $\delta_{jt} \leftarrow \delta_{jt} + \ln s_{jt} - \ln s_{jt}(\delta, \theta)$
- Supply side: Bertrand-Nash FOCs provide additional GMM moments
- Counterfactuals: merger simulation, tax incidence, product entry/exit

**Dynamic Structural Models**:
- State variables: brand loyalty, inventory, advertising stock, learning
- Solution: nested fixed point (Rust) or CCP (Hotz-Miller)
- Applications: brand choice dynamics, new product diffusion, customer relationship management

### 2. Causal Inference / Reduced-Form

See [references/causal-inference.md](references/causal-inference.md) for comprehensive guidance.

**Primary Designs in Marketing**:

| Design | Typical Application | Key Reference |
|--------|-------------------|---------------|
| **Difference-in-Differences** | Ad campaign effects, store entry, policy changes | Callaway & Sant'Anna (2021); Sun & Abraham (2021) |
| **Regression Discontinuity** | Price thresholds, eligibility cutoffs, geographic boundaries | Calonico et al. (2014) |
| **Instrumental Variables** | Price endogeneity, advertising endogeneity | Angrist & Krueger (2001) |
| **Synthetic Control** | Single-market interventions | Abadie et al. (2010) |

**The Identification Narrative**: Every marketing paper must clearly articulate:
1. The causal relationship of interest
2. The source of endogenous variation
3. The source of exogenous variation (the "natural experiment")
4. The identifying assumptions
5. How assumptions are tested (balance tests, placebo tests, falsification)

### 3. Field Experiments

See [references/field-experiments.md](references/field-experiments.md) for comprehensive guidance.

**Design Elements**:
- Randomization unit: individual customer, store, DMA (Designated Market Area)
- Stratification and blocking for balance
- Power analysis to justify sample size
- Pre-registration (AEA Registry, AsPredicted, OSF)

**Reporting Standards**:
- CONSORT-style flow diagram showing participant flow
- Balance table comparing treatment/control on pre-treatment characteristics
- Intent-to-treat (ITT) as primary estimate
- Treatment-on-the-treated (TOT) via instrumental variables for non-compliance
- Multiple testing correction (Bonferroni, Holm, or Benjamini-Hochberg)

### 4. Conjoint Analysis

See [references/conjoint-analysis.md](references/conjoint-analysis.md) for comprehensive guidance.

**Design**: Fractional factorial, random designs; incentive-aligned via BDM mechanism
**Estimation**: Hierarchical Bayes multinomial logit; WTP from part-worths
**Validation**: Holdout prediction accuracy; face validity of attribute importances

---

## Identification: The Make-or-Break Dimension

Marketing Science and JMR reviewers prioritize identification credibility above all else. A paper without a clearly articulated identification strategy is desk-rejected.

### Identification Checklist

- [ ] Source of exogenous variation is clearly described with institutional detail
- [ ] First-stage is strong (F > 10 for IV; visual jump for RDD)
- [ ] Parallel pre-trends are shown visually (event study plot for DID)
- [ ] Balance table compares treatment/control on pre-treatment observables
- [ ] Placebo/falsification tests: fake treatment at different time, different place, different outcome
- [ ] Robustness to: alternative samples, measures, specifications, estimators
- [ ] Threats to identification are explicitly discussed, not hidden
- [ ] Oster (2019) bounds or Altonji et al. (2005) ratio test for selection on unobservables

---

## Common Rejection Reasons in Marketing Journals

| Reason | Frequency | Prevention |
|--------|-----------|------------|
| Weak identification / unconvincing instruments | Very High | Show first-stage F, discuss excludability, multiple instruments |
| Endogeneity not adequately addressed | Very High | Explicit identification section; don't rely on fixed effects alone |
| "So what?"—no substantive marketing implication | High | Concrete counterfactual; what changes in practice? |
| Incremental over existing literature | High | Clear differentiation table; novel data or context |
| Model not connected to data | Medium | Model should motivate specification; don't estimate a kitchen sink |
| Mechanical application of method | Medium | Method serves the question; contribution is insight, not technique |

---

## 0-to-Draft Pipeline: Five-Stage Workflow

### Stage 1: Substantive Problem & Positioning

**Goal**: Identify the marketing problem, articulate the gap, select target journal.

**Agent actions**:

```
1.1 Understand the marketing phenomenon
    - Ask: What is the substantive marketing problem? What decision does it inform?
    - Identify the core consumer/firm trade-off
    - Classify: Structural / Reduced-form / Experimental / Conceptual

1.2 Literature gap analysis
    - Search for 10-15 closest papers in target journals
    - Build a Gap Table: rows = key references, columns = dimensions (data, method, context, finding)
    - Identify the empty cell this paper fills
    - Output: draft gap table with explicit differentiation

1.3 Journal selection
    - Match paper profile to journal identity
    - Consider: MktSci (structural + novel data) vs. JMR (identification + relevance) vs. JM (strategy + multi-method)
    - Output: recommended journal + 1-2 fallback options

1.4 Contribution statement
    - One sentence: "Using [data/method], we study [phenomenon] and find [key insight]. For marketers, this means [implication]."
    - Draft 3-5 numbered contributions
    - Output: contribution list

1.5 Writing plan
    - Outline paper structure with estimated page allocation
    - Identify reference files to load at each stage
```

**Reference to load**: `references/journal-characteristics.md`

### Stage 2: Model & Identification Design

**Goal**: Specify consumer/firm model and articulate empirical identification.

**Agent actions**:

```
2.1 Consumer utility specification
    - Specify indirect utility: u_ijt = f(price, characteristics, heterogeneity)
    - For structural: random coefficients, outside good, market definition
    - For reduced-form: outcome equation, treatment definition

2.2 Firm behavior (if applicable)
    - Pricing: Bertrand-Nash, uniform pricing, price discrimination
    - Advertising, entry, product line decisions

2.3 Identification strategy
    - Source of exogenous variation: what quasi-experiment or instrument?
    - Identifying assumptions and how they're tested
    - Institutional details that make the strategy credible
    - Output: identification narrative (~1 page)

2.4 Data description
    - Data sources, sample construction, summary statistics
    - Key variables: construction, sources, limitations
    - Output: §3 Data & Identification draft
```

**Reference to load**: `references/structural-modeling.md` or `references/causal-inference.md`

### Stage 3: Estimation & Results

**Goal**: Implement estimator, present results with diagnostics.

**Agent actions**:

```
3.1 Estimator specification
    - Structural: GMM objective, instruments, weighting matrix, optimization
    - Reduced-form: regression specification, fixed effects, standard error clustering
    - Experimental: ITT specification, randomization check

3.2 Results presentation
    - Main results table with diagnostics
    - Economic significance: elasticities, WTP, treatment effect magnitude
    - Not just statistical significance (p-values)
    - Output: §4 Estimation / Results draft

3.3 Diagnostic tests
    - First-stage F, overidentification J-test, DWH endogeneity test
    - Balance table, attrition analysis, parallel trends
```

### Stage 4: Counterfactuals & Robustness

**Goal**: Conduct policy simulations, demonstrate robustness, show mechanism.

**Agent actions**:

```
4.1 Counterfactual simulations (structural papers)
    - Merger: change ownership matrix, recompute equilibrium
    - Tax/subsidy: add per-unit tax, compute pass-through
    - Product introduction/removal: change choice set
    - Report: compensating variation, profit changes, bootstrap CIs
    - Output: §5 Counterfactuals draft

4.2 Robustness analysis (all papers)
    - Alternative DV, IV, sample, specification, estimator
    - Placebo tests
    - Oster bounds for selection on unobservables
    - Output: §5 Robustness draft

4.3 Heterogeneity / Mechanism
    - Who is most affected? (demographic, behavioral, contextual)
    - Through what channel? (mediation, moderation, process evidence)
```

**Reference to load**: `references/structural-modeling.md` (counterfactuals) or `references/causal-inference.md` (robustness)

### Stage 5: Writing & Assembly

**Goal**: Write the full paper with marketing implications.

**Agent actions**:

```
5.1 Introduction drafting
    - P1: Motivating marketing phenomenon (real company, real numbers)
    - P2: Why existing literature/approaches fail
    - P3: Our approach and identification strategy
    - P4: Contributions (numbered, 3-5 items)
    - P5: Paper organization

5.2 Literature review
    - Organize by substantive domain, not paper-by-paper
    - Include Gap Table from Stage 1
    - End each stream: what's known + what's missing

5.3 Marketing implications
    - What should a CMO/marketing manager DO differently?
    - Connect to specific results (robust to X, not just significant)
    - Quantify where possible: "A 10% increase in X leads to Y% change in sales"
    - Distinguish: statistical significance vs. economic significance vs. managerial significance

5.4 Abstract
    - Write LAST
    - Substantive problem → Method → Key finding → Marketing implication
    - Max 200 words for MktSci, JMR, JM, JCR

5.5 Cross-section consistency check
    - Contributions list ↔ body sections (1:1)
    - All variables defined at first use
    - All tables/figures referenced in text
```

**References to load**: `references/writing-patterns.md`, `references/reviewer-expectations.md`

---

## Writing Patterns

### Pattern 1: The Managerial Motivating Example
Open with a concrete marketing decision faced by a real company. "In 2023, P&G allocated $7.1B to advertising across 40 brands, yet had no systematic way to measure cross-brand spillover effects..."

### Pattern 2: The Identification Narrative
Devote an entire section to explaining the source of exogenous variation. The best marketing papers make the identification strategy feel like a detective story.

### Pattern 3: The Elasticity Table
For demand estimation papers, the own- and cross-price elasticity matrix is the central result. Present a representative subset with standard errors.

### Pattern 4: The Counterfactual Triplet
For each counterfactual: Baseline → Counterfactual → Difference. Always report consumer welfare (compensating variation) alongside firm profit.

---

## Venue-Specific Page Budgets

| Journal | Submission Length | References | Appendix | Abstract |
|---------|:---:|:---:|:---:|:---:|
| Marketing Science | 35 pages | Unlimited | Unlimited | 200 words |
| JMR | 40 pages | Unlimited | Unlimited | 200 words |
| JM | 40 pages | Unlimited | Unlimited | 200 words |
| JCR | 40 pages | Unlimited | Unlimited | 150 words |
| JAMS | 40 pages | Unlimited | Unlimited | 200 words |
| IJRM | 35 pages | Unlimited | Unlimited | 200 words |
| QME | 40 pages | Unlimited | Unlimited | 200 words |
| Marketing Letters | 20 pages | Unlimited | Limited | 150 words |

---

## Quick Checklist Before Submission

- [ ] Target journal fits the paper's method-contribution profile
- [ ] Identification strategy is clearly articulated and credible
- [ ] First-stage (if IV) or parallel trends (if DID) convincingly shown
- [ ] Results table: coefficients + SE + economic significance + diagnostics
- [ ] Robustness: 8+ checks covering alternative measures, samples, specifications
- [ ] Counterfactuals (if structural): baseline vs. counterfactual with welfare
- [ ] Marketing implications: specific, actionable, connected to results
- [ ] Introduction: motivating example + gap + numbered contributions
- [ ] All citations verified programmatically (no hallucinated references)
- [ ] Page budget within limits; long proofs/materials in appendix

---

## References

- [references/journal-characteristics.md](references/journal-characteristics.md): Detailed per-journal characteristics, editorial philosophy, reviewer expectations
- [references/structural-modeling.md](references/structural-modeling.md): BLP framework, demand estimation, supply side, counterfactuals, diagnostics
- [references/causal-inference.md](references/causal-inference.md): DID, RDD, IV, synthetic control, matching—implementation and reporting
- [references/field-experiments.md](references/field-experiments.md): Design, power analysis, pre-registration, CONSORT, analysis
- [references/conjoint-analysis.md](references/conjoint-analysis.md): Fractional factorial design, HB estimation, WTP, validation
- [references/reviewer-expectations.md](references/reviewer-expectations.md): What MktSci/JMR/JM/JCR reviewers look for, common criticisms, rebuttal strategies
- [references/writing-patterns.md](references/writing-patterns.md): Reusable writing patterns from published marketing science papers
