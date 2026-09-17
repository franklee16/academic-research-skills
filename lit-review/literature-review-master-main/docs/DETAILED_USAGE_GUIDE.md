# Literature Review Master

## Detailed Usage Guide

This guide explains how to use Literature Review Master as a general literature intelligence skill for academic research. The guide is written for researchers, doctoral students, supervisors, research teams, method developers, and applied scientists who need more than a simple literature summary.

The skill is designed to help with research decisions, literature search, gap discovery, idea validation, project foundation, related-work writing, journal-specific positioning, reviewer-defence preparation, citation verification, and systematic review planning. It is especially useful for quantitative research, theory-driven research, empirical research design, statistical modelling, probabilistic modelling, Bayesian approaches, econometrics, optimisation, computational experiments, simulation, machine learning, AI systems, formal theory, strategic-interaction models, and interdisciplinary work.

The skill does not replace careful human judgement. It is a structured operating system for literature work. It makes the research process more explicit, more auditable, and less dependent on vague impressions.

---

## 1. What the skill does

Literature Review Master is built around modes. Each mode corresponds to a different research situation.

A normal literature-review prompt usually tries to do everything at once. That is unstable. Searching a new field, validating a specific idea, building a manuscript literature section, and verifying citations before submission are different tasks. They require different evidence, different depth, and different risk controls.

This skill separates those tasks.

It can help you answer the following questions.

- Should I enter this topic at all?
- Is this research area too crowded?
- Which journals or communities own this problem?
- What are the main literature streams?
- Which papers are direct predecessors rather than broad background?
- Is my proposed gap real, or is it only a change of setting?
- Is there a killer paper that already does the work?
- Can the gap be addressed without real data?
- What evidence structure is acceptable for the target field?
- What should be cited in the introduction, related work, discussion, limitations, or response letter?
- Which claims in the manuscript are overclaimed?
- Which citations exist but do not actually support the claims attached to them?
- How should the literature positioning change if the target journal changes?
- What would a hostile reviewer say about missing literature?

The skill is deliberately conservative. It should not invent novelty. It should not protect a weak idea. It should not call a search exhaustive unless the search protocol supports that claim. It should state what is known, what is not known, and what would change the verdict.

---

## 2. The operating stance

The skill works best when it is asked to be cold, explicit, and evidence based.

A good instruction is this.

```text
Be cold and evidence based. Do not reassure me unless the literature supports the idea. If the gap is weak, say so. If the idea should be dropped or reframed, give a clear verdict.
```

The skill should distinguish four things that are often confused.

First, it separates topic similarity from framework collision. A paper can be in a different application area but still use the same model, estimation logic, theorem structure, or empirical identification strategy. That paper may be a direct collision.

Second, it separates citation existence from citation support. A cited paper may be real, highly published, and accurately listed in the references, yet still fail to support the sentence in which it is cited.

Third, it separates journal rank from journal fit. A 4* or 4 journal article is not automatically relevant. It must shape the theory, method, mechanism, empirical design, or gap.

Fourth, it separates numerical evidence from empirical evidence. A simulation can illustrate, quantify, stress-test, or map a model. It does not become empirical validation unless it is linked to real observed data.

---

## 3. Quick decision tree

Use this decision tree before invoking the skill.

If you do not have a concrete idea, use Mode A.

If you have a rough idea and want to know whether it is worth doing, use Mode B.

If you are trying to decide whether to enter a topic, whether to target a journal family, or whether to build a working paper first, use Mode 0.

If the project is already chosen and you need a literature tree, use Mode C.

If you are writing the introduction, related work, discussion, limitations, or response material, use Mode D.

If the manuscript is close to submission and you need to check citations, claims, figures, tables, numbers, and internal evidence, use Mode E.

If the project paused, the framing changed, or a deadline is approaching, use Mode F.

If you want to know how reviewers may attack your literature review, use Mode G.

If the same project may be positioned for different journals or communities, use Mode H.

If you are writing a systematic, scoping, bibliometric, or survey review, use Mode I.

If you do not have real data and need to know whether the research gap can still be addressed, use Mode J.

You can combine modes. Common combinations are listed below.

| Combination | Use case |
|---|---|
| Mode A + Mode 0 | Explore a topic and decide whether it is strategically worth entering |
| Mode B + Mode J | Validate an idea under no-data, theory-only, simulation-only, or computation-only constraints |
| Mode C + Mode D | Build the literature foundation and convert it into manuscript material |
| Mode D + Mode H | Rewrite related work for a specific journal family |
| Mode E + Mode G | Check citations and simulate reviewer attacks before submission |
| Mode F + Mode B | Revalidate an old idea after a literature update |
| Mode I + Mode E | Build a review protocol and verify citation traceability |

---

## 4. The shared research contract

Every serious task should begin with a shared research contract. This prevents the skill from producing a generic answer.

Use this prompt.

```text
Before answering, build a shared research contract. Include mode, primary domain, secondary domain, method family, evidence available, data constraint, target journal family, search scope, closest-collision risk, and requested output.
```

The contract should look like this.

```text
Mode:
Primary domain:
Secondary domain:
Method family:
Evidence available:
Data constraint:
Target journal family:
Search scope:
Closest-collision risk:
Main output requested:
```

A completed contract might look like this.

```text
Mode: B + J
Primary domain: Quantitative marketing
Secondary domain: Information systems
Method family: Game-theoretic model with numerical experiments
Evidence available: Formal analysis and simulation only
Data constraint: No real-world dataset
Target journal family: Marketing, management science, information systems
Search scope: Target-journal core, ABS 4*/4/3 adjacent journals, working papers, game-theory method core
Closest-collision risk: High, because platform pricing and strategic user response are mature literatures
Main output requested: Killer-paper scan, framework-difference test, no-data viability, ROI verdict
```

The contract is not bureaucratic. It is the anchor that keeps the rest of the work coherent.

---

## 5. Mode 0. Meta-decision

Use Mode 0 before committing to a research direction. This mode is strategic rather than technical.

It is suitable for questions such as these.

```text
Should I enter this topic?
Is this area too crowded?
Is the field moving fast enough to justify a working paper?
Should I target a top journal, a specialised journal, a conference, or a review paper?
Should I pursue a theory paper, empirical paper, computational paper, or conceptual paper?
```

A strong Mode 0 output should include these elements.

```text
Strategic decision context
Literature maturity
Crowding level
Evidence requirements
Journal-family feasibility
Data or method constraints
Recent movement in the field
Opportunity cost
Risk of being incremental
Recommended action
Conditions for reversal
```

Recommended prompt.

```text
Use Mode 0. I am considering entering [field or topic]. I have [evidence, method, data, or constraints]. Please assess whether this is strategically worth pursuing. Compare working-paper, journal-paper, review-paper and abandonment options. Give a cold verdict and explain what evidence would change it.
```

Mode 0 should not produce a full literature review. It should produce a research decision.

---

## 6. Mode A. Exploration

Use Mode A when you have a broad topic, keyword set, or intellectual curiosity but no concrete idea.

Mode A is useful when you say things like this.

```text
I am interested in algorithmic pricing and consumer behaviour, but I do not know what to study.
I want to explore Bayesian approaches in public policy research.
I want to find research gaps at the intersection of AI agents and decision support.
I want to understand the literature around digital platforms, governance, and strategic users.
```

A good Mode A output should not merely list papers. It should build a landscape.

Expected components.

```text
Scope definition
Keyword architecture
Search scope ladder
Main literature streams
Boundary literatures
Recent activity map
Foundational works
Methodological foundations
Candidate gaps
Killer-paper risk for each gap
Required evidence structure
No-data viability if relevant
ROI ranking
Reading plan
```

Recommended prompt.

```text
Use Mode A. My broad area is [topic]. I do not yet have a concrete idea. Please map the literature streams, identify possible research gaps, flag killer-paper risks, suggest search queries, and rank candidate directions by expected research ROI.
```

For quantitative research, ask the skill to separate theory, empirics, computation, simulation, and method streams.

```text
Please separate the literature into theory streams, empirical streams, computational streams, methodological streams, and application streams. Identify which streams are essential and which are only background.
```

Mode A should end with ranked research directions, not just a reading list.

---

## 7. Mode B. Idea Validation

Use Mode B when you already have a rough idea and need to know whether it is worth doing.

This is one of the most important modes. It is designed to kill weak ideas early.

Mode B should ask whether the proposed idea is new in a substantive sense. It should not accept superficial changes such as a new context, a new variable name, or a minor empirical setting if the framework remains the same.

A strong Mode B output includes these elements.

```text
Restated idea
Direct predecessor scan
Killer-paper candidates
Framework-versus-cosmetic gap test
Method collision analysis
Evidence-structure feasibility
Journal-family feasibility
No-data viability if relevant
Reviewer risk
ROI score
Pursue, Pivot, or Drop verdict
Minimum condition for reversal
```

Recommended prompt.

```text
Use Mode B. My rough idea is [idea]. Please search for killer-paper risks, identify closest predecessors, test whether the gap is framework-level or cosmetic, assess target-journal feasibility, and give a Pursue, Pivot, or Drop verdict with an ROI score.
```

If the idea is theory-driven, add this.

```text
Also check whether the model changes primitives, timing, information, constraints, equilibrium object, proof structure, comparative statics, or decision rules relative to the closest papers.
```

If the idea is empirical, add this.

```text
Also check whether the identification strategy, measurement, dataset, construct, treatment, population, and causal claim are meaningfully different from existing work.
```

If the idea is computational or methodological, add this.

```text
Also check whether the method changes the algorithmic object, benchmark class, theoretical guarantee, computational complexity, uncertainty treatment, scalability, or downstream decision value.
```

Mode B should not be polite. A weak idea should be marked as weak.

---

## 8. Mode C. Project Foundation

Use Mode C after the project is selected and you need a defensible literature foundation.

Mode C builds the literature tree. It is not the same as writing the related-work section. It is the research infrastructure behind the related-work section.

Expected output.

```text
Direct predecessors
Theoretical foundations
Methodological foundations
Application or phenomenon stream
Adjacent streams
Recent activity
Historical baseline
Closest-paper matrix
Gap matrix
Claim-citation map
Known unknowns
Reading priorities
```

Recommended prompt.

```text
Use Mode C. The project is [project]. Please build a literature tree with direct predecessors, theoretical foundations, methodological foundations, application context, adjacent streams, recent activity, historical baseline, closest-paper matrix, gap matrix and claim-citation map.
```

For quantitative research, include method and evidence categories.

```text
Please classify each paper by method, evidence type, model or empirical design, central claim, and risk to my contribution.
```

Mode C is where paper notes, corpus triage, three-pass reading and cross-paper synthesis become important.

---

## 9. Mode D. Manuscript Support

Use Mode D when you are writing a manuscript. It can support introductions, related work, discussion, limitations, contribution statements, response letters, or revision memos.

Mode D should not invent literature. It should only write from verified or clearly marked materials.

Common sub-tasks.

```text
Introduction evidence pack
Related-work stream map
Contribution-positioning paragraph
Discussion contrast pack
Limitations and boundary conditions
Response-to-reviewer literature defence
Claim-citation alignment
Target-journal versioning
```

Recommended prompt.

```text
Use Mode D. I am writing [section]. My target journal family is [target]. Please convert the literature map into manuscript-ready material. Use British English. Minimise colons and semicolons. Preserve paragraph integrity. Mark any unverified claims.
```

For related work, ask for stream-level organisation.

```text
Please organise related work by intellectual stream rather than by chronology. For each stream, state what it knows, what it assumes, what it misses, and how my paper differs.
```

For discussion, ask for boundary-aware language.

```text
Please prepare discussion material that states what the results imply, what they do not imply, and which literature streams the findings revise or qualify.
```

Mode D should produce writing that is careful, not promotional.

---

## 10. Mode E. Citation and Evidence Verification

Mode E is a pre-submission evidence gate. It is stricter than proofreading.

It checks whether claims are supported by citations, internal evidence, appendices, proofs, tables, figures, code outputs, simulation logs, empirical results, qualitative materials, or a fixed corpus of sources.

Mode E uses a two-pass structure.

Pass 1 extracts claims. It does not verify them.

Pass 2 verifies the fixed claim list. It should not quietly rewrite claims while verifying them.

Recommended prompt.

```text
Use Mode E. First extract all citation-bearing and evidence-bearing claims from the manuscript. Do not verify anything in the first pass. Then verify the fixed claim list. Check source existence, metadata, version risk, retraction risk, claim support, overclaiming, numerical values, tables, figures and internal evidence. End with PASS, PASS WITH MINOR FIXES, MAJOR REPAIR REQUIRED, or UNSAFE FOR SUBMISSION.
```

Mode E should classify evidence-support status.

| Status | Meaning |
|---|---|
| Verified | The source exists and supports the claim |
| Verified with rounding | The rounded number is correct and does not alter interpretation |
| Metadata verified only | The source exists but full claim support has not been checked |
| Partially supported | The source supports a weaker version of the claim |
| Misleading | The source is selectively or contextually misused |
| Overclaimed | The manuscript states more than the source supports |
| Citation not found | The cited source cannot be located |
| Wrong version risk | The cited version may not match the manuscript claim |
| Numerical error | Number, unit, sign, benchmark, or magnitude is wrong |
| Not in corpus | The claim is not traceable under source-only mode |
| Contradicted | The source contradicts the claim |
| Manual check required | Full verification requires human reading or inaccessible materials |

Mode E is useful beyond reference lists. It can verify tables, figures, appendices, theorem claims, empirical claims, simulation claims, qualitative claims, and response-letter claims.

---

## 11. Mode F. Rolling Update

Use Mode F when the literature may have changed.

Triggers include these.

```text
The project paused for several months.
The paper framing changed.
The target journal changed.
A submission deadline is approaching.
A reviewer asked for new literature.
A new technology, dataset, law, policy, or method appeared.
A working paper may have been published or superseded.
```

Recommended prompt.

```text
Use Mode F. The project was last checked on [date]. The current framing is [framing]. Please identify new papers, new working papers, new terminology, new killer-paper risks, outdated claims and literature-positioning changes.
```

Mode F should not redo everything. It should focus on what changed.

---

## 12. Mode G. Reviewer Attack and Literature Defence

Use Mode G to simulate hostile reviewer objections.

A reviewer may attack the literature review in several ways.

```text
Missing direct predecessor
Misread closest paper
Weak novelty claim
Wrong journal identity
Ignored method literature
Ignored construct literature
Ignored empirical evidence
Overstated gap
Cosmetic difference
Unjustified no-data evidence structure
```

Recommended prompt.

```text
Use Mode G. Act as a hostile reviewer. Attack my literature review, missing citations, gap statement and journal positioning. Then provide a defence strategy, including which papers to cite, which claims to weaken, and which framing to change.
```

A good Mode G output contains likely reviewer lines, not vague suggestions.

---

## 13. Mode H. Journal-Specific Literature Positioning

Use Mode H when the same paper may be submitted to different journal families.

A project rarely has only one possible identity. A study about AI decision support may be a computer-science paper, an information-systems paper, a management paper, a marketing paper, a public-policy paper, or a healthcare paper depending on the contribution.

Mode H asks what the paper becomes when read by different communities.

Recommended prompt.

```text
Use Mode H. My project is [project]. Compare literature positioning for [journal families]. For each route, identify must-cite streams, bridge streams, literature to downplay, dangerous missing literature, preferred gap language, evidence-structure feasibility and likely reviewer profile.
```

Mode H should never say that a paper fits a journal merely because it uses the journal's vocabulary. It must explain the central contribution.

---

## 14. Mode I. Systematic Survey or Review Paper

Use Mode I when the output is itself a review paper, not merely a literature section inside a research paper.

Mode I supports systematic reviews, scoping reviews, bibliometric reviews, meta-analyses, narrative reviews, framework reviews, method surveys and literature-mapping papers.

Expected components.

```text
Review question
Database list
Search strings
Inclusion criteria
Exclusion criteria
Screening protocol
Coding scheme
Quality appraisal
Evidence-extraction table
Synthesis strategy
Limitations
Reproducibility notes
```

Recommended prompt.

```text
Use Mode I. I want to write a [systematic, scoping, bibliometric, narrative, or method] review on [topic]. Please design the search protocol, inclusion and exclusion criteria, screening stages, coding scheme, synthesis plan and reporting structure.
```

If the review is not truly systematic, do not call it systematic. Use a more accurate label such as narrative review, structured literature review, scoping review, or thematic survey.

---

## 15. Mode J. Theory-only and simulation-only gap viability

Use Mode J when no real data are available, or when the research contribution is formal, computational, conceptual, or simulation-supported.

This mode is essential for projects where the evidence comes from the model, proof, numerical experiment, algorithm, simulation, or conceptual synthesis rather than a field dataset.

Recommended prompt.

```text
Use Mode J. I do not have real data. My proposed gap is [gap]. Please classify whether it is viable as pure theory, theory plus numerical experiments, algorithmic work, computational simulation, or conceptual synthesis. Identify target journal feasibility and the minimum evidence required.
```

Mode J should classify the gap.

```text
Theory-viable gap
Theory plus simulation viable gap
Algorithmic or computational gap
Empirical gap not viable without data
Conceptual review or synthesis gap
```

A project with no real data can still be strong. It must be honest about its evidence.

Use these phrases when appropriate.

```text
The model predicts...
The numerical experiments illustrate...
The simulation quantifies...
The comparative statics show...
The regime map indicates...
```

Avoid these unless real data exist.

```text
The data show...
We empirically validate...
The empirical results demonstrate...
The causal effect is...
```

---

## 16. Specialist agents

The skill includes specialist agents. They can be run as true parallel agents if the environment supports it. If not, run them sequentially with clear labels.

| Agent | Function |
|---|---|
| Literature Orchestrator Agent | Selects modes, builds the contract and coordinates outputs |
| Search Query Architect Agent | Builds search strings, terminology variants and collision queries |
| Corpus Triage Agent | Classifies papers into tiers and reading priorities |
| Deep Reading Agent | Extracts claims, assumptions, evidence, methods and limitations |
| Gap Hunter Agent | Identifies real gaps and rejects cosmetic gaps |
| Killer Paper Agent | Searches for direct collisions and closest predecessors |
| Journal Scope Agent | Adjusts literature search and positioning by target journal family |
| Equilibrium Agent | Handles solution concepts and equilibrium structure for strategic models |
| No-Data Viability Agent | Checks whether a gap can be addressed without real data |
| Related Work Writer Agent | Converts literature maps into manuscript material |
| Claim Extraction Agent | Extracts citation-bearing and evidence-bearing claims |
| Citation Verification Agent | Checks source existence, metadata, versions and status |
| Evidence Gate Agent | Checks whether sources support claims |
| Numerical and Table Verification Agent | Checks numerical values, tables, figures and simulation claims |
| Source-Only Verification Agent | Restricts verification to uploaded or fixed corpus sources |
| Red Team Literature Reviewer Agent | Simulates hostile reviewer attacks |
| Integration Editor Agent | Merges agent outputs and resolves conflicts |

A useful multi-agent request looks like this.

```text
Use agent mode. Activate Search Query Architect, Corpus Triage, Killer Paper, Deep Reading, Gap Hunter, Journal Scope and Integration Editor. If true parallel execution is unavailable, run them sequentially and label each output.
```

---

## 17. Search scope and the ABS database

The embedded ABS AJG 2024 database is useful for business, management and adjacent social-science fields. It covers all 4*, 4 and 3 journals in the bundled data.

Use it for these tasks.

```text
Journal-family scanning
Missing-citation risk
ABS 4*/4/3 search prioritisation
Target-journal comparison
Adjacent-stream identification
Reviewer-risk coverage
```

Do not use it blindly. A highly rated paper outside the intellectual stream can be noise. A lower-ranked but direct predecessor can be essential.

The search scope ladder is more important than raw journal rank.

Search first where the paper's home discipline lives. Then search adjacent high-quality literatures. Then search method foundations. Then search interdisciplinary prestige outlets when relevant. Then search working papers and preprints.

---

## 18. How to judge a research gap

The skill should reject cosmetic gaps. A real gap changes the research object, mechanism, evidence, method, or theory.

A strong gap may involve these.

```text
New mechanism
New information structure
New timing
New constraint
New population or institutional setting with theoretical consequences
New estimation or identification strategy
New measurement of a construct
New model primitive
New equilibrium object
New algorithmic object
New uncertainty structure
New boundary condition
New synthesis of conflicting literatures
```

A weak gap often looks like this.

```text
Same framework, new context only
Same method, new dataset only without a theoretical reason
Same variables under new names
Same result with a minor parameter change
Same literature split with no new synthesis
Same setting with only a fashionable label added
```

Ask the skill to run the framework-versus-cosmetic test.

```text
Please test whether the gap is framework-level or cosmetic. Compare primitives, assumptions, mechanism, evidence, method, solution concept, identification strategy, and core result.
```

---

## 19. How to use the skill for quantitative research

For quantitative research, always ask the skill to classify papers by method and evidence.

Useful categories include these.

```text
Formal theory
Game-theoretic modelling
Optimisation
Simulation
Numerical experiments
Computational experiments
Econometrics
Statistical modelling
Bayesian modelling
Machine learning
Causal inference
Experiment
Survey
Panel data
Structural estimation
Text analysis
Network analysis
Qualitative or mixed evidence
```

Quantitative literature review should not only list dependent and independent variables. It should inspect design choices.

For empirical papers, ask for this.

```text
Data source
Sample
Construct measurement
Identification strategy
Estimator
Robustness checks
Threats to validity
Main claim
Boundary condition
```

For formal papers, ask for this.

```text
Actors
Timing
Information
State variables
Controls
Objectives
Constraints
Solution concept
Assumptions
Main result
Proof object
Comparative statics
Boundary cases
```

For computational papers, ask for this.

```text
Problem class
Algorithmic object
Benchmark
Instance generation
Performance metric
Complexity or guarantee
Robustness
Reproducibility
Decision value
```

---

## 20. Citation verification in practice

Before submission, use Mode E. Do not wait until the final hour. Citation verification often reveals structural problems in the manuscript.

The most dangerous claims are often not the obvious factual statements. They are literature-positioning claims.

Examples.

```text
Prior work has largely focused on...
Few papers examine...
This is the first study to...
The literature assumes...
Existing methods cannot handle...
The closest papers do not consider...
```

These claims need evidence. They should be weakened if support is partial.

A good Mode E report should identify three kinds of fixes.

```text
Citation fixes, where the citation or metadata is wrong.
Claim fixes, where the sentence is too strong.
Structural fixes, where the literature positioning itself is unsafe.
```

The safest final verdict is not always PASS. A Major Repair Required verdict is useful if it prevents a desk rejection or hostile review.

---

## 21. Manuscript prose style

Generated manuscript prose should use British English unless the target outlet requires another convention.

For manuscript prose, minimise colons and semicolons. If a colon or semicolon appears, rewrite the sentence into a more natural form when possible.

Instead of this.

```text
The study has three aims: to explore X, analyse Y, and evaluate Z.
```

Prefer this.

```text
The study aims to explore X, analyse Y, and evaluate Z.
```

Instead of this.

```text
The results showed a positive trend; however, the sample size was small.
```

Prefer this.

```text
The results showed a positive trend. However, the sample size was small.
```

Do not split paragraphs mechanically. Academic paragraphs should preserve a complete thought, a full contrast, or a coherent literature move. Do not create a new paragraph merely because three or four sentences have passed.

---

## 22. Common mistakes and how to avoid them

Do not ask for a literature review without a mode. The output will become generic.

Do not ask for exhaustive coverage unless you provide a protocol, databases, time span, inclusion criteria and screening method.

Do not ask the skill to write related work before Mode C has identified direct predecessors.

Do not treat a high journal rating as a substitute for relevance.

Do not let Mode D produce final manuscript prose from unverified citation claims.

Do not treat simulated evidence as empirical evidence.

Do not claim novelty from absence. A search that did not find a paper is not proof that no paper exists.

Do not ignore working papers in fast-moving fields.

Do not skip Mode E before submission.

---

## 23. Contribution workflow for teams

For a research team, a stable workflow is this.

1. Use Mode 0 or Mode A to decide whether the area is worth entering.
2. Use Mode B to test each candidate idea.
3. Use Mode C to build the literature tree for the chosen idea.
4. Use Mode H to choose journal positioning.
5. Use Mode D to prepare literature material for the manuscript.
6. Use Mode G to attack the manuscript before external review.
7. Use Mode E to verify citations, claims and internal evidence.
8. Use Mode F every time framing changes or several months pass.

Keep a corpus log, search log, gap matrix and claim-citation map. These artefacts are more valuable than a one-time list of papers.

---

## 24. Repository structure

The main files and folders are as follows.

```text
SKILL.md
README.md
QUICK_START.md
QUICK_START_CN.md
THIRD_PARTY_NOTICE.md
LICENSING_NOTE.md
CONTRIBUTING.md
references/
agents/
templates/
database/
scripts/
examples/
docs/
```

The `references` folder contains the protocols. The `agents` folder contains role briefs. The `templates` folder contains output scaffolds. The `database` folder contains the AJG 2024 4*, 4 and 3 journal database and citation-status schema. The `scripts` folder contains lightweight utilities. The `examples` folder gives sample workflows. The `docs` folder contains public-facing guidance.

---

## 25. Extending the skill

Contributors should preserve the mode structure. Do not replace Mode 0 to Mode E. Add new modes only when a genuinely new research situation appears.

Good contributions include these.

```text
New journal-family routing cards
Improved search strings for a field
Additional evidence-status labels
Better citation-verification schema
New systematic-review templates
Domain-specific gap taxonomies
More precise no-data viability rules
Examples from underrepresented fields
Workflow examples for teams
```

Poor contributions include these.

```text
Generic advice without operational output
Overbroad claims about exhaustive search
Promotional language
Rules that assume every field uses the same evidence standard
Hard-coded journal recommendations without fit logic
Templates that encourage unsupported novelty claims
```

The skill should remain cold, explicit and evidence based.
