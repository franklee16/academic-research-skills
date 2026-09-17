# Research Grilling

Use this reference when the user explicitly asks to be grilled, questioned, challenged, stress-tested, or given a mock defense about an econometric paper, research design, identification strategy, dataset, model choice, result interpretation, or empirical plan. If serious unresolved design ambiguity appears without an explicit request, offer grilling; do not force the mode.

## Core Contract

- Investigate evidence before asking questions.
- Ask one question when the answer controls what can be asked next; ask two or three together only when they are independent decisions on the same current frontier.
- Attach an agent-recommended answer to every question.
- Explain the recommendation at a depth matched to the user's demonstrated topic knowledge.
- Find facts from the data, files, code, draft, results, documentation, and available environment instead of asking the user to retrieve them.
- Leave genuine preference, scope, estimand, assumption, and trade-off decisions to the user.
- Do not begin implementation until no material decision ambiguity remains and the user explicitly confirms that implementation may begin.
- Do not create a grill-specific memory, project file, research-design lock, consensus-summary artifact, or persistent session tracker. Rely on the host product's project context and memory.

## Evidence-First Data Grilling

Treat data exploration as part of grilling, not as implementation. Before asking questions that depend on the dataset:

1. Locate and read the relevant dataset, codebook, analysis code, manuscript, prior tables, and project instructions.
2. Inspect variable names, labels, types, values, units, missingness, ranges, category levels, duplicates, keys, time coverage, and sample structure.
3. Determine whether the data appear cross-sectional, repeated cross-sectional, panel, time-series, transaction-level, or event-study shaped.
4. Inspect treatment timing, within-unit variation, outcome support, event-time coverage, sample selection, missingness patterns, and candidate identifying variation.
5. Use focused read-only diagnostics when helpful: descriptive statistics, distributions, trends, correlations among theoretically relevant regressors, VIF, condition number, rank, and treatment-cohort support.
6. Treat semantic roles inferred from data as hypotheses until the user resolves genuinely ambiguous economic meaning or research intent.

Use existing profiling scripts when useful, but keep pre-confirmation outputs temporary. Remove temporary profiles, plots, and scratch files after they have informed the questions unless the user separately requests them as deliverables.

Pre-confirmation exploration may establish facts, but it must not silently lock a sample, estimand, variable role, model, or causal interpretation. Do not run the formal baseline/robustness pipeline, edit the manuscript, generate the final Word report, overwrite results, or make repository changes during grilling.

## Decision Tree

Build a task-specific decision tree rather than reciting a fixed questionnaire. Consider only relevant branches:

- research question and target estimand;
- unit of observation, time index, population, and sample boundary;
- outcome, treatment/main regressor, controls, mechanisms, moderators, instruments, weights, and sample flags;
- measurement, transformation, timing, lag, accumulation, and deflation choices;
- assignment mechanism and source of identifying variation;
- confounding, reverse causality, simultaneity, measurement error, selection, and attrition;
- fixed effects, trends, dynamics, functional form, and estimator;
- standard-error type, clustering level, weights, and finite-sample concerns;
- identifying assumptions and diagnostics;
- robustness checks matched to specific threats;
- heterogeneity and mechanism estimands;
- economic magnitude, uncertainty, and causal-language boundaries;
- required tables, figures, and reproducibility outputs.

Resolve prerequisite decisions before their dependents. If the estimand is unresolved, do not ask the user to choose a final estimator. If the treatment timing is unresolved, do not ask for an event-study window.

## Question Selection

Ask a single question when:

- the next branch depends on its answer;
- the issue is conceptually difficult;
- the user is in guided explanation mode;
- the prior answer was vague, contradictory, or incomplete;
- a blocking identification or measurement issue is being resolved.

Ask two or three questions together only when all are independently answerable from already-established facts. Number them and allow the user to answer them separately. Never dump the entire decision tree.

For each question, use the smallest useful version of this structure:

```markdown
### Question [number]: [decision]

Evidence already established:
- [facts found by the agent]

Decision needed:
[the choice only the user can make]

Recommended answer:
[the agent's recommendation]

Why:
[reasoning matched to the user's knowledge]

Benefits:
- [main benefit]

Costs or risks:
- [main trade-off]
```

For a straightforward expert exchange, compress the headings into a short paragraph while preserving the recommendation and material trade-offs. A recommendation is advice, not a decision: wait for the user to accept, reject, modify, or defer it.

## Topic-Knowledge Calibration

Infer knowledge from the user's answers during the current topic; do not administer an unrelated entrance quiz and do not assign a permanent label. Reassess continuously.

Use guided explanation when the user repeatedly:

- asks for definitions of foundational concepts;
- confuses outcomes, treatments, controls, mechanisms, fixed effects, or instruments;
- treats correlation, fixed effects, Granger precedence, or cointegration as automatic causal proof;
- cannot distinguish basic timing, estimator, inference, or interpretation alternatives;
- gives answers that cannot be converted into an operational research decision;
- returns to the same foundational misunderstanding after it was discussed.

Once guided explanation is warranted, every recommended answer must include:

1. a plain-language explanation of the relevant concept;
2. why the recommendation fits the observed data and research goal;
3. its main benefits;
4. its main costs, assumptions, and failure risks;
5. a concrete example when abstraction is still blocking understanding.

For users demonstrating standard knowledge, explain identification assumptions and the principal trade-off. For users demonstrating advanced knowledge, stay concise but still state non-obvious assumptions, inferential consequences, and material alternatives. Never become condescending, and never infer general ability from unfamiliarity with one method.

## Facts Versus Decisions

Do not ask the user for facts the environment can answer. Replace generic questions with evidence-backed decision questions.

Avoid:

> Is `firm_code` the panel identifier, and does treatment vary over time?

Prefer:

> `firm_code` repeats across years and uniquely identifies 1,842 longitudinal units; treatment changes within 37% of them. The codebook describes it as a group code rather than a legal-entity code. Should the estimand apply to corporate groups or legal entities? I recommend confirming the group-level estimand because the available key cannot support legal-entity fixed effects without another identifier. The benefit is a reproducible panel; the cost is a broader unit of interpretation.

The agent may recommend a choice strongly when evidence supports it, but must not present an assumption-dependent recommendation as a discovered fact.

## Implementation Gate

Remain in grilling mode while a material decision is unresolved. Nonmaterial items may be explicitly deferred by the user. When the decision tree has no meaningful open branch, ask only for direct permission to proceed, for example:

> I have no further material decision questions. May I begin the agreed analysis or writing work?

Do not produce a consensus recap or save a special summary before asking. A clear user instruction such as "proceed", "implement it", "run the analysis", or "start writing" opens the gate only when it follows the resolved discussion. If the user requests implementation while a blocking ambiguity remains, surface that specific blocker and resolve it first.

After the gate opens, leave grilling mode and follow the relevant data-analysis, empirical, writing, citation, figure/table, or DOCX workflow. Create only the normal deliverables that workflow requires.

## Stop Conditions

Stop grilling when:

- the user explicitly ends the session;
- no material question remains and the user either permits implementation or chooses to stop;
- remaining questions require unavailable external information, in which case state the blocker without inventing an answer.

If the user stops without opening the implementation gate, do not implement.

## Failure Modes

- Asking the user to inspect a dataset or file the agent can inspect itself.
- Asking several questions whose answers depend on one another.
- Hiding the recommendation so the user cannot evaluate the trade-off.
- Giving a novice only unexplained jargon or giving an expert repetitive textbook exposition.
- Treating a recommended answer as user consent.
- Running formal regressions early and allowing preliminary coefficients to dictate the research question.
- Writing a persistent grilling summary or duplicating the host product's project-memory features.
- Continuing to grill after all material decisions are resolved and implementation has been authorized.
