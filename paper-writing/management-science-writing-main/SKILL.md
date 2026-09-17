---
name: management-science-writing
description: Use when writing or revising management science & operations research papers targeting MS, OR, MSOM, POM, TS, TRB, DS, OMEGA, TRE, EJOR, IJPE, IJPR, C&IE. Covers the full 0-to-draft pipeline: topic selection, journal targeting, modeling, derivation, algorithm design, numerical experiments, managerial insights, and journal-specific writing patterns. Also use when stuck at any stage of an MS&E paper and needing stage-specific guidance.
---

# Management Science & Operations Research Paper Writing

## Overview

Management Science & Engineering (MS&E) papers follow a distinct pipeline: **Model → Analysis → Algorithm → Numerical Experiment → Managerial Insight**. Unlike ML papers that prioritize empirical results, MS&E papers are evaluated on the **coherence of the analytical chain** — from modeling assumptions through mathematical derivation to computational validation and finally to actionable business implications.

This skill provides journal-specific guidance for 13 flagship MS&E journals across two tiers, covering the full paper lifecycle.

**Core Principle**: An MS&E paper is a **mathematical argument with managerial purpose**. Every equation, lemma, and table must serve the narrative that connects a real problem to a rigorous solution.

---

## When to Use This Skill

- Drafting a paper targeting MS, OR, MSOM, POM, or any MS&E journal
- Deciding which journal best fits a particular model-method-contribution combination
- Structuring a model-analysis-algorithm paper
- Writing proofs, algorithm pseudocode, or numerical experiment sections
- Formulating managerial insights from mathematical results
- Revising based on reviewer feedback from an MS&E journal
- Converting a working paper between MS&E journal formats

---

## Journal Selection Quick Reference

Choosing the right journal is a function of your paper's **methodology depth**, **problem scope**, and **practical relevance**.

### Tier 1 (UTD-24): Top Flagship Journals

| Journal | Core Identity | Ideal Paper Profile |
|---------|--------------|---------------------|
| **MS** (Management Science) | Broad management, high rigor, significant contribution | Novel problem + sharp analytical insight + broad appeal across management disciplines. Length: ~38 pages submission. |
| **OR** (Operations Research) | Methodological depth, optimization focus | Deep theoretical advance in optimization/stochastics. Complete proofs. Methodology-first contribution. |
| **MSOM** (M&SOM) | Empirical OM, behavioral operations | Strong empirical component or behavioral experiment. Managerially relevant. Data-driven modeling. |
| **POM** (Production & Oper. Mgmt) | Data-driven, broad OM scope | Empirical or analytical paper with strong practical relevance to production/service operations. |

### Tier 2: Strong Field Journals

| Journal | Core Identity | Ideal Paper Profile |
|---------|--------------|---------------------|
| **TS** (Transportation Science) | Transportation systems, network models | Transportation-specific problem. Network optimization, traffic equilibrium, logistics. |
| **TRB** (Transportation Research B) | Transportation methodology | Methodological advance in transportation modeling, rigorous proofs. |
| **DS** (Decision Sciences) | Decision-making focus | Decision analysis, multi-criteria methods, judgment under uncertainty. |
| **OMEGA** | Concise, high-impact, managerial | Short, sharp papers (~6000 words max). Strong managerial insights mandatory. |
| **TRE** (Transportation Research E) | Logistics & transportation | Supply chain and logistics modeling. Empirical or analytical. |
| **EJOR** (European J. Operational Research) | Broad methodology, inclusive | Any OR methodology applied to a real problem. Welcomes heuristic methods. Types: Invited Review, Innovative Applications, Theory & Methodology. |
| **IJPE** (Int. J. Production Economics) | Production economics, supply chain | Manufacturing/service operations with economic analysis. Strong on real data. |
| **IJPR** (Int. J. Production Research) | Production engineering | Process design, scheduling, manufacturing systems. Engineering focus. |
| **C&IE** (Computers & Industrial Eng.) | Computational methods, IE | Algorithm-heavy, simulation, AI/ML for industrial engineering. Implementation emphasis. |

### Decision Flowchart

```
Is your contribution primarily methodological?
├── YES → Is it a deep theoretical advance in optimization?
│   ├── YES → OR, possibly MS (Optimization dept)
│   └── NO → Is the method heuristic/computational?
│       ├── YES → EJOR, C&IE, IJPR
│       └── NO → MS, DS
└── NO → Is your contribution primarily empirical/applied?
    ├── YES → Does it have broad managerial appeal?
    │   ├── YES → MS, MSOM, POM, OMEGA
    │   └── NO → IJPE, IJPR, TRE, C&IE
    └── NO → Hybrid (model + data) → MSOM, POM, EJOR
```

---

## The MS&E Paper Structure

Unlike IMRAD for biomedical sciences or the systems paper blueprint, an MS&E paper typically follows this structure:

| Section | Typical Pages | Key Content |
|---------|--------------|-------------|
| Abstract | 150-250 words | Problem, methodology, key results, managerial implication |
| S1 Introduction | 2-3 pages | Motivation, gap, contributions (numbered), paper organization |
| S2 Literature Review | 2-4 pages | Organized by stream, explicit differentiation table |
| S3 Model | 4-8 pages | Notation, assumptions, base model, extensions |
| S4 Analysis / Derivation | 4-10 pages | Lemmas, propositions, theorems with proofs |
| S5 Algorithm / Solution Method | 2-5 pages | Pseudocode, complexity, approximation guarantees |
| S6 Numerical Experiments | 4-8 pages | Setup, parameter settings, main results, sensitivity analysis |
| S7 Managerial Insights / Discussion | 1-3 pages | Actionable implications, connected to practice |
| S8 Conclusion | 0.5-1 page | Summary, limitations, future work |
| References | — | 30-60 papers typical |
| Appendix | Unlimited | Long proofs, additional experiments, robustness checks |

**Key structural difference from ML/CS papers**: The **Model section is the backbone**. It occupies the most central real estate. If your model is unclear, the rest of the paper collapses. Reviewers read the model section before anything else after the introduction.

---

## Modeling Conventions

See [references/modeling-conventions.md](references/modeling-conventions.md) for comprehensive guidance. Key principles:

### Notation System
- Use a **consistent three-tier notation**: sets (calligraphic), parameters (lowercase), decision variables (uppercase or bold), dual variables (Greek)
- Present a **notation table** (for papers with 15+ symbols)
- Define all symbols at first use; never assume the reader infers from context

### Assumption Presentation
- List assumptions as **numbered statements** (Assumption 1, 2, 3...)
- For each assumption, state: (a) what it is, (b) why it is needed, (c) whether it is restrictive and what happens if relaxed
- **Assumption defense**: Explain why each assumption is reasonable in the target application context
- Use **assumption-relaxation extensions** ($4-6 pages) to demonstrate robustness

### Model Types by Journal Preference

| Model Type | MS | OR | MSOM | POM | EJOR | IJPE |
|-----------|-----|-----|------|-----|------|------|
| Analytical (optimization/game theory) | ✓✓✓ | ✓✓✓ | ✓✓ | ✓ | ✓✓✓ | ✓✓ |
| Stylized analytical + numerical | ✓✓ | ✓✓ | ✓✓✓ | ✓✓ | ✓✓ | ✓✓ |
| Data-driven empirical | ✓✓ | — | ✓✓✓ | ✓✓✓ | ✓ | ✓✓✓ |
| Simulation-based | ✓ | — | ✓ | ✓ | ✓✓ | ✓✓✓ |
| Heuristic/metaheuristic | — | — | — | ✓ | ✓✓✓ | ✓✓✓ |

---

## Proof and Derivation Standards

See [references/proof-derivation-guide.md](references/proof-derivation-guide.md) for comprehensive guidance. Key principles:

### Proof Presentation Hierarchy
```
Lemma 1 (Technical result) → Proposition 1 (Structural property) → Theorem 1 (Main result) → Corollary 1 (Special case)
```

### Journal-Specific Proof Expectations

| Journal | Full Proof in Body | Proof Sketch Tolerated | Appendix Proofs | Proof Length Tolerance |
|---------|-------------------|----------------------|-----------------|----------------------|
| MS | Short proofs in body; long ones appendix | For non-central results only | Yes, unlimited | Concise proofs preferred |
| OR | Complete proofs in body | Rarely | Yes | No length constraint on proofs |
| MSOM | Streamlined in body; full in appendix | Yes, for some results | Yes | Condensed preferred |
| POM | Streamlined in body | Yes | Yes | Condensed preferred |
| EJOR | Complete in body or appendix | Yes | Yes | Moderate |
| IJPE/IJPR | Minimal in body | Yes, often | Yes | Short |
| C&IE | Minimal | Yes, frequently | Optional | Very short |

### Proof Writing Guidelines
1. **State the result before proving it.** Use "We next establish that..." or "The following proposition characterizes..."
2. **Begin each proof with the proof technique** ("By induction on N", "We construct a coupling...", "By contradiction, assume...")
3. **End each proof with a clear marker** (∎ or □)
4. **Connect proofs to intuition**: Before a long proof, give a one-sentence intuitive explanation
5. **All proofs in the main body must be self-contained**; do not reference appendix derivations from body proofs

---

## Algorithm and Solution Method Presentation

See [references/algorithm-solving-guide.md](references/algorithm-solving-guide.md) for comprehensive guidance.

### Pseudocode Standards
- Use the `algorithm2e` or `algorithmicx` LaTeX packages
- Every algorithm must have: input, output, and numbered steps
- Include **computational complexity** (worst-case time and space) for every algorithm
- If applicable, state **approximation ratio** and **tightness**

### Algorithm vs. Heuristic
- **Algorithm**: Provable optimality or approximation guarantee → label as "Algorithm"
- **Heuristic**: No theoretical guarantee, validated numerically → label as "Heuristic" or "Solution Procedure"
- C&IE and IJPR accept pure heuristics; MS/OR expect optimality or approximation guarantees

---

## Numerical Experiment Design

See [references/numerical-experiments.md](references/numerical-experiments.md) for comprehensive guidance.

### Standard Experiment Structure
1. **Experimental Setup** (§X.1): Hardware, software, solver versions, random seeds
2. **Parameter Settings** (§X.2): Table of all parameters with default values and justification
3. **Benchmark Instances** (§X.3): Data source, generation method, instance sizes
4. **Main Results** (§X.4): Performance comparison tables with statistical tests
5. **Sensitivity Analysis** (§X.5): One-at-a-time or factorial design varying key parameters
6. **Managerial Implications of Experiments** (§X.6): What the numbers mean for practice

### MS&E-Specific Experiment Requirements

| Requirement | MS/OR | MSOM/POM | EJOR/IJPE | C&IE/IJPR |
|-------------|-------|----------|-----------|-----------|
| Real data instances | Preferred | Required | Strongly preferred | Optional |
| Statistical tests | Yes | Yes | Preferred | Optional |
| Sensitivity analysis | Required | Required | Required | Preferred |
| CPU time reporting | Required | Optional | Required | Required |
| Benchmark comparison | Required | Required | Required | Required |
| Instance size variety | Required | Required | Required | Required |
| Parameter justification | Required | Required | Required | Optional |

---

## Managerial Insights

See [references/managerial-insights.md](references/managerial-insights.md) for comprehensive guidance.

This is the **most distinctive feature** of MS&E papers. Managerial Insights (MIs) translate mathematical results into actionable business recommendations.

### MI Structure
Each managerial insight should follow the **SAR format**:
- **Setting**: Remind the reader of the context
- **Analytical finding**: State the mathematical result in plain language
- **Recommendation**: What a manager should DO differently

### MI Checklist
- [ ] Each MI is traceable to a specific theorem, proposition, or numerical result
- [ ] MIs use **zero mathematical notation**
- [ ] MIs are numbered for clarity (Managerial Insight 1, 2, 3...)
- [ ] Counterintuitive findings are explicitly highlighted
- [ ] Boundary conditions ("this insight holds only when...") are stated
- [ ] At least one MI connects to a real company or industry context

**Journals requiring mandatory MI**: MS, MSOM, OMEGA (critical), POM, IJPE.
**Journals where MI is optional but valued**: OR, TS, DS, EJOR.

---

## Writing Patterns

### Pattern 1: The Motivating Example
Open the introduction with a concrete mini-case from industry. Cite a real company, real numbers, real dilemma. This grounds the abstract model in practice. **Required by MS, MSOM, OMEGA.**

### Pattern 2: The Gap Table
Use a structured table comparing your paper against 8-12 key references on dimensions like: modeling approach, demand model, solution method, numerical validation, managerial insights. Explicitly mark your contribution. **Standard for MS, OR, EJOR.**

### Pattern 3: The Assumption-Relaxation Ladder
Present the base model → analyze → relax one assumption → re-analyze → relax another → re-analyze. Demonstrates robustness of the core insight. **Standard for MS, OR.**

### Pattern 4: The SAR Managerial Insight
Each MI is a self-contained mini-section: Setting → Analytical Finding → Recommendation. See [Managerial Insights](#managerial-insights) above.

---

## Venue-Specific Page Budgets

| Journal | Typical Submission Length | References | Appendix | Abstract Word Limit |
|---------|--------------------------|------------|----------|---------------------|
| MS | 38 pages | Unlimited | Unlimited | 200 |
| OR | 35 pages | Unlimited | Unlimited | 200 |
| MSOM | 32 pages | Unlimited | Unlimited | 200 |
| POM | 35 pages | Unlimited | Unlimited | 200 |
| TS | 32 pages | Unlimited | Unlimited | 200 |
| TRB | 32 pages | Unlimited | Unlimited | 150 |
| DS | 30 pages | Unlimited | Unlimited | 150 |
| OMEGA | ~6000 words | Unlimited | Limited | 150 |
| TRE | 30 pages | Unlimited | Unlimited | 200 |
| EJOR | 30 pages | Unlimited | Unlimited | 200 |
| IJPE | 30 pages | Unlimited | Unlimited | 200 |
| IJPR | 25 pages | Unlimited | Limited | 200 |
| C&IE | 25 pages | Unlimited | Limited | 200 |

---

## Cross-Referencing with Other Skills

This skill works with:
- **scientific-writing**: General IMRAD principles, clarity, citation formatting
- **literature-review**: Systematic literature search for MS&E topics
- **ppw:polish**: English polishing for non-native speakers (common in MS&E)
- **matlab** / **sympy**: For deriving and verifying mathematical results

---

## Common Rejection Reasons in MS&E Journals

| Reason | Frequency | Prevention |
|--------|-----------|------------|
| Insufficient contribution over existing literature | Very High | Explicit gap table in introduction |
| Unrealistic or undefended assumptions | High | Assumption defense section + relaxation |
| Managerial insights too generic | High | Specific, numbered, traceable to results |
| Numerical experiments not reproducible | Medium | Provide code, data, parameter justification |
| Proof errors or incomplete derivation | Medium | Have a colleague verify the proof chain |
| Poor motivation — why should anyone care? | High | Real-world motivating example |
| Wrong journal fit | Medium | Use the journal selection guide above |
| Paper too long for contribution size | Medium | Respect page budgets; move to appendix |

---

## 0-to-Draft Pipeline: Five-Stage Workflow

This is the core workflow of this skill. Each stage builds on the previous. Stages 1-3 are sequential; Stages 4-5 can partially overlap. At each stage, ask the user for their current materials before proceeding.

---

### Stage 1: Topic Positioning & Journal Selection

**Goal**: Define the paper's contribution gap, select a target journal, and establish the writing plan.

**Input needed from user**: Research area, preliminary idea, any existing notes or literature.

**Agent actions**:

```
1.1 Understand the research idea
    - Ask: What is the managerial problem? What methodology? Any preliminary results?
    - Identify the core trade-off or mechanism the paper will study
    - Classify: Analytical / Empirical / Computational / Hybrid

1.2 Literature gap analysis
    - Search for 8-12 closest papers using research-lookup or paper-lookup
    - Build a Gap Table draft: rows = key references, columns = dimensions (methodology, demand model, solution approach, etc.)
    - Identify the empty cell that this paper fills
    - Output: draft gap table with explicit differentiation

1.3 Journal selection
    - Use the Journal Selection Quick Reference and Decision Flowchart above
    - Match paper profile (methodology, scope, contribution type) to journal identity
    - Consider: MS (broad impact) vs. OR (method depth) vs. MSOM (empirical) vs. EJOR (method-inclusive)
    - Output: recommended journal + 1-2 fallback options with rationale

1.4 Contribution statement
    - Formulate the one-sentence contribution: "We [action] [what] using [method] and find that [key insight]."
    - Draft 3-5 numbered contributions
    - Output: contribution list

1.5 Writing plan
    - Outline the paper structure with estimated page allocation per section
    - Identify which reference files to load at each stage
    - Output: section-by-section writing plan
```

**Stage 1 exit criteria**: Target journal chosen, gap table drafted, contribution list written, writing plan ready.

**Reference to load**: `references/journal-characteristics.md` (for chosen journal)

---

### Stage 2: Model Building

**Goal**: Design the mathematical model — the backbone of the paper.

**Input needed from user**: Problem description, decision variables, constraints, objective.

**Agent actions**:

```
2.1 Problem formalization
    - Translate the verbal problem into mathematical structure
    - Define: decision-maker, timeline (if dynamic), information structure (if stochastic)
    - Output: verbal model description + event sequence

2.2 Notation system design
    - Establish three-tier notation: sets (calligraphic), parameters (lowercase), variables (uppercase/bold)
    - Check for symbol conflicts across sections
    - Output: draft notation table

2.3 Assumption framework
    - Enumerate assumptions as numbered statements
    - For each: state the assumption, justify it, note what happens if relaxed
    - Identify which assumptions are standard vs. novel to this paper
    - Output: numbered assumption list with defenses

2.4 Model formulation
    - Write objective function
    - Write constraint set
    - Write compact formulation: min/max {obj | constraints}
    - Check: all symbols defined, all constraints numbered, boundary conditions explicit
    - Output: §3 Model Formulation draft

2.5 Extensions planning
    - Plan assumption-relaxation ladder: Base Model → Extension 1 → Extension 2 → ...
    - Decide which extensions go in body vs. appendix
    - Output: extensions outline
```

**Stage 2 exit criteria**: Complete model section draft with notation table, assumption list, base formulation, and extensions plan.

**Reference to load**: `references/modeling-conventions.md`

---

### Stage 3: Derivation & Analysis

**Goal**: Derive structural properties, prove main results, establish the analytical contribution.

**Input needed from user**: Model formulation (from Stage 2), any preliminary derivations.

**Agent actions**:

```
3.1 Structural property identification
    - What properties should the optimal solution have? (convexity, monotonicity, threshold structure, etc.)
    - Design the proof hierarchy: Lemma → Proposition → Theorem → Corollary
    - Output: proof plan (what to prove, in what order)

3.2 Proof drafting
    - For each result: state the theorem/proposition → provide intuition → proof/proof sketch
    - Name the proof technique in the first sentence of each proof
    - Check: all assumptions referenced, all steps justified, edge cases handled
    - Decide body vs. appendix placement based on proof length and centrality
    - Output: §4 Analysis section draft

3.3 Closed-form solutions (if applicable)
    - Derive closed-form expressions for optimal decisions
    - Verify boundary behavior (what happens at parameter limits?)
    - Output: closed-form results with interpretation

3.4 Comparative statics
    - How does the optimal solution change with key parameters?
    - Use implicit function theorem, monotone comparative statics, or numerical exploration
    - Output: comparative statics results

3.5 Proof verification checklist
    - Every theorem stated (even if proof in appendix)
    - Every statement has proof or proof sketch somewhere
    - All "Proof." claims are verified
    - No circular reasoning
```

**Stage 3 exit criteria**: Complete proof chain with all theorems/propositions/lemmas stated and proved.

**Reference to load**: `references/proof-derivation-guide.md`

---

### Stage 4: Algorithm & Numerical Experiments

**Goal**: Design solution method (if needed), run numerical experiments, generate figures and tables.

**Input needed from user**: Analytical results (from Stage 3), computational resources, data sources.

**Agent actions**:

```
4.1 Solution method design
    - If model has closed-form solution → skip to 4.2
    - If exact method: design algorithm, state complexity, prove optimality
    - If heuristic: design procedure, calibrate parameters, validate on small instances
    - Output: pseudocode + complexity analysis OR heuristic description

4.2 Experimental design
    - Design parameter table: all parameters, base values, ranges, sources
    - Determine benchmark instances: real data, literature instances, or generated
    - Plan instance sizes: small/medium/large categories
    - Design sensitivity analysis: which parameters, what ranges
    - Output: experimental plan document

4.3 Code implementation guidance
    - Suggest implementation approach (language, solver, key libraries)
    - Provide pseudocode-to-code mapping for complex algorithms
    - Remind: set random seeds, record solver versions, save all outputs

4.4 Results presentation
    - Design performance comparison tables
    - Design sensitivity analysis figures (line plots, heatmaps)
    - Compute: optimality gaps, CPU times, statistical significance
    - Draft figure captions that are self-contained
    - Output: §6 Numerical Experiments draft with tables and figures

4.5 Managerial implications of experiments
    - Connect numerical results back to analytical findings
    - Translate numerical patterns into actionable recommendations
    - Draft SAR-format insights from the experimental results
```

**Stage 4 exit criteria**: Complete experimental section with parameter table, benchmark description, results tables, sensitivity analysis, and experiment-derived insights.

**References to load**: `references/numerical-experiments.md`, `references/algorithm-solving-guide.md`

---

### Stage 5: Writing & Assembly

**Goal**: Write the full paper from Introduction to Conclusion, assemble all sections, polish.

**Input needed from user**: All prior stage outputs, target journal selection.

**Agent actions**:

```
5.1 Introduction drafting
    - P1: Motivating example (real company, real numbers) — see Writing Pattern 1
    - P2: Generalization to broader industry context
    - P3-P4: Literature gap → "Despite its importance, the literature has..."
    - P5: Our approach (one paragraph, no math)
    - P6: Contributions (numbered, 3-5 items)
    - P7: Paper organization ("The remainder of this paper is organized as follows...")
    - Output: §1 Introduction draft

5.2 Literature review
    - Organize by research stream, not paper-by-paper
    - Include the Gap Table from Stage 1
    - End each stream with: what's been done + what's missing
    - Conclude with: how this paper bridges the gaps
    - Output: §2 Literature Review draft

5.3 Managerial insights (standalone section)
    - Distill analytical and numerical results into 3-6 SAR-format insights
    - Each insight: Setting → Analytical Finding → Recommendation
    - Zero mathematical notation
    - Numbered, traceable to specific results
    - Counterintuitive findings highlighted
    - Output: §7 Managerial Insights draft

5.4 Conclusion
    - Summary (2-3 sentences): problem, approach, key result
    - Limitations (honest, specific): "Our analysis assumes X; relaxing this is future work."
    - Future research directions (2-4 concrete directions)
    - Output: §8 Conclusion draft

5.5 Abstract
    - Write LAST, after the full paper is drafted
    - Follow 5-sentence formula: (1) what achieved, (2) why hard/important, 
      (3) how done, (4) evidence, (5) key number/insight
    - Max 200 words for MS/OR/MSOM; 150 for OMEGA/DS
    - Output: Abstract

5.6 Cross-section consistency check
    - Contributions list ↔ body sections (1:1 mapping)
    - Notation: consistent across all sections
    - All figures/tables referenced in text
    - All citations in References section
    - Managerial insights traceable to theorems/experiments
    - Abstract claims substantiated in body

5.7 Formatting
    - Apply journal-specific page budget (see table above)
    - Move long proofs to appendix; keep proof sketches in body
    - Format tables with booktabs; format algorithms with algorithm2e/algorithmicx
    - Verify all citations programmatically (no hallucinated references)
```

**Stage 5 exit criteria**: Complete first draft with all sections, cross-checked for consistency, within page budget.

**References to load**: `references/writing-patterns.md`, `references/managerial-insights.md`, `references/reviewer-expectations.md`

---

### Pipeline Interaction Protocol

When the user invokes this skill, the agent should:

1. **Determine the current stage**: Ask what the user has so far (idea only? model built? results in hand?)
2. **Start at the appropriate stage**: Don't force users back to Stage 1 if they're ready for Stage 4
3. **At each stage**: Load the relevant reference file, then execute the agent actions
4. **Stage gate**: Confirm with user before proceeding to the next stage
5. **Iterate within stage**: Draft → get feedback → revise until the stage exit criteria are met

### Quick-Start Prompts

Users can jump to any stage:

- "I have a research idea about [topic]. Help me position it and pick a journal." → Stage 1
- "I have my model formulated. Help me derive structural properties." → Stage 3
- "I have analytical results. Help me design numerical experiments." → Stage 4
- "I have all my results. Help me write the full paper for MS." → Stage 5
- "Take me through the full pipeline from scratch." → Stage 1 → 5

---

## Quick Checklist Before Submission

- [ ] Target journal fits the paper's methodology-contribution profile
- [ ] Model section: all notation defined, assumptions stated and defended, extensions present
- [ ] Proofs: complete in body or appendix, proof techniques stated, markers (∎) present
- [ ] Algorithms: pseudocode present, complexity stated, approximation ratio if applicable
- [ ] Numerical experiments: parameter table, benchmark description, sensitivity analysis, CPU times
- [ ] Managerial insights: numbered, math-free, traceable to results, actionable
- [ ] Introduction: motivating example, gap table, numbered contributions, road map
- [ ] Literature review: organized by stream, not paper-by-paper; differentiation explicit
- [ ] Page budget: within journal limits (body only)
- [ ] All citations verified via DOI/programmatic fetch (no hallucinated references)

---

## References

- [references/journal-characteristics.md](references/journal-characteristics.md): Detailed per-journal characteristics, reviewer expectations, departmental editorial statements
- [references/modeling-conventions.md](references/modeling-conventions.md): Notation systems, assumption frameworks, model types, model section structure
- [references/proof-derivation-guide.md](references/proof-derivation-guide.md): Proof hierarchy, journal-specific proof standards, common proof techniques
- [references/numerical-experiments.md](references/numerical-experiments.md): Experiment design, parameter calibration, sensitivity analysis, benchmark instances
- [references/managerial-insights.md](references/managerial-insights.md): SAR framework, MI writing patterns, journal-specific MI expectations
- [references/reviewer-expectations.md](references/reviewer-expectations.md): What reviewers look for by journal, common criticisms, rebuttal strategies
- [references/writing-patterns.md](references/writing-patterns.md): Reusable writing patterns from published MS&E papers
