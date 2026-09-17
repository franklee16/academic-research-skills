# Paper-Type Gates

Use this module before data, identification, or blueprint work. Do not force every economics idea into an empirical `X affects Y` regression. Classify the candidate as one primary type and, when needed, one secondary type.

## Types

| Type | Core question | Main gate | Blueprint object |
| --- | --- | --- | --- |
| Empirical causal | Does X affect Y? | data, variation, identification | main regression or comparison |
| Measurement or facts | What is the object, fact, pattern, or index? | concept, measurement, coverage, validation | measurement design and fact figures |
| Theory | What mechanism or equilibrium logic explains the puzzle? | primitives, timing, equilibrium, propositions | model blueprint |
| Structural, quantitative, or computational | What model maps data moments to mechanisms or counterfactuals? | model-data mapping, identification, estimation/calibration | model, moments, fit, counterfactuals |
| Policy report | What decision-relevant facts and options are credible? | evidence strength, feasibility, policy relevance | policy memo and evidence table |

Mixed projects are allowed. For example, a measurement paper can add descriptive regressions, a theory paper can add motivating facts, and a structural project can include reduced-form validation. Still name the primary type first.

## Type-Specific Gates

### Empirical Causal

Require:

- credible data path;
- observable X, Y, unit, time, and sample;
- usable variation before naming DID, IV, RDD, shift-share, or fixed effects;
- assumptions and threats stated in plain language;
- claim downgraded if causal identification is weak.

Blueprint:

- research question;
- data and variable map;
- sample construction;
- main regression or comparison;
- identification assumptions;
- tables, figures, robustness, mechanism or heterogeneity if supported.

### Measurement Or Facts

Do not require causal identification. Require:

- clear concept and why it matters economically;
- measurement rule or index construction;
- unit, coverage, time, and missingness;
- validation against external benchmarks, known facts, or alternative measures;
- facts or figures that would remain useful even without causal claims.

Blueprint:

- concept definition;
- measurement formula or coding rule;
- data coverage and validation checks;
- main descriptive figures or maps;
- decomposition, distribution, trend, or comparison tables;
- what the facts can and cannot imply.

### Theory

Do not require a data path. Require:

- a precise economics puzzle, not just a broad intuition;
- agents, choices, constraints, timing, information, and friction;
- equilibrium or solution concept;
- propositions, comparative statics, or mechanism results not assumed by construction;
- relationship to existing models;
- empirical or policy implications.

Blueprint:

- puzzle and model purpose;
- primitives and timing;
- equilibrium or solution concept;
- main proposition and intuition;
- comparative statics;
- examples or extensions;
- testable or policy implications.

### Structural, Quantitative, Or Computational

Do not reduce this to a simple regression. Require:

- model block and economic mechanism;
- data moments, calibration targets, or estimation sample;
- parameter identification or calibration logic;
- fit diagnostics or validation moments;
- counterfactual or simulation design;
- computational feasibility for the user's deadline and skill.

Blueprint:

- model environment and agents;
- key equations or computational blocks;
- data moments and mapping to model objects;
- estimation or calibration plan;
- fit and validation outputs;
- counterfactuals or simulations;
- sensitivity and robustness checks.

### Policy Report

Require:

- decision-maker and policy question;
- credible facts and evidence strength;
- feasible policy options;
- tradeoffs and implementation constraints;
- clear separation between evidence, interpretation, and recommendation.

Blueprint:

- policy question;
- evidence table;
- descriptive facts;
- options and tradeoffs;
- implementation risks;
- recommendation and uncertainty.

## Scoring Adjustment

Keep the five IRIS-style dimensions for every type, but interpret them by type:

| Criterion | Empirical causal | Measurement/facts | Theory | Structural/quantitative |
| --- | --- | --- | --- | --- |
| Novelty | new question, data, setting, or variation | new object, measure, fact, or coverage | new mechanism or model distinction | new model-data link or counterfactual |
| Clarity | X, Y, sample, variation | concept, unit, measurement rule | primitives, timing, equilibrium | model blocks, moments, counterfactual |
| Feasibility | data and runnable design | data coverage and validation | proof or formal reasoning path | computation, moments, estimation |
| Effectiveness | design answers causal question | facts answer measurement question | model answers puzzle | model identifies mechanism/counterfactual |
| Impact | economics, policy, thesis value | useful fact or measurement value | theory contribution or insight | mechanism and counterfactual value |

## Agent And Human Task Split

For any type using data, separate what the AI agent can verify from what the user must confirm.

Agent-side evidence check:

- inspect papers, abstracts, data sections, appendices, replication pages, public database pages, metadata, codebooks, or local files provided by the user;
- identify likely variables, units, periods, and merge keys;
- mark whether evidence is public, literature-precedent, local-file based, or only a lead;
- state uncertainty and what was not checked.

Human-side access confirmation:

- confirm school, library, advisor-group, research-team, paid database, data-owner, or third-party service access;
- verify actual download, file completeness, legal permission, privacy constraints, citation rules, and thesis-use authorization;
- confirm whether informal platform leads such as 小红书 or 微信公众号 point to legal and reproducible sources.

Never say "the data are available" when only literature precedent or platform leads exist. Say "there is an evidence path, but user-side access must be confirmed."

## Public Stop-Or-Continue Labels

Do not show internal route codes in user-facing output. Use natural labels:

| Meaning | Public label |
| --- | --- |
| more work is required | 建议继续打磨 |
| current version is mature enough | 建议冻结当前版本 |
| usable now, but can be upgraded | 可以推进，也可继续升级 |
| branch should not continue | 建议暂停或更换路线 |

When the stop-or-continue choice is not obvious and several branches remain plausible, run a small MCTS/UCT comparison or clearly state why it is skipped. In user-facing output, summarize it as "小规模分支比较" rather than exposing UCT internals.
