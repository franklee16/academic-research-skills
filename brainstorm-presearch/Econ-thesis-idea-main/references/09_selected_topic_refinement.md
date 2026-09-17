# Selected Topic Refinement

Use this module after the user has chosen one candidate topic from the literature crowding gate or the crowded topic pivot lab. The goal is not to generate more topics. The goal is to turn the selected candidate into the smallest credible economics research design.

This module is called by `references/00_master_router.md`. It should freeze one selected candidate, refine that branch, and return gate statuses to the router. If the selected branch fails, return to the candidate bank rather than restarting broad topic search.

The selected candidate and each refined version must retain the five-dimensional score record: novelty, clarity, feasibility, effectiveness, and impact. When a refinement changes the idea, report the score change from the previous version and the next route. First classify the paper type and use `references/11_paper_type_gates.md`; do not force measurement, theory, or structural/quantitative branches into an empirical main-regression template.

## When To Trigger

Trigger this module when the user says things like:

- "就选这个方向";
- "把这个压成一个最小可行设计";
- "先不要继续找题，帮我把这个做成 paper";
- "把 n2 / branch 2 / 这个候选题继续 refine";
- "我想知道这个题能不能启动".

If the user has not selected a candidate yet, continue screening or ask them to choose one branch.

## Freeze The Candidate

Start by restating the chosen candidate:

```text
selected_candidate:
original_interest:
candidate_question:
setting:
claim_type: causal / descriptive / measurement / theory / structural-quantitative / policy report / mixed
known_data_path:
biggest_uncertainty:
```

Do not re-open broad ideation unless the data or identification gate fails.

Immediately after freezing the candidate, include:

```markdown
## Selected Branch IRIS Review
| Criterion | Score | Feedback |
| --- | --- | --- |
| Novelty | /10 | |
| Clarity | /10 | |
| Feasibility | /10 | |
| Effectiveness | /10 | |
| Impact | /10 | |

- Average score:
- Score change from previous iteration:
- Weakest dimensions:
- Next route:
```

## Refinement Sequence

1. **Question compression**: write the question in the right form for the paper type. Empirical causal may use `Does X affect Y...`; measurement/facts should define the object or pattern; theory should state the puzzle; structural/quantitative should state the model-counterfactual question.
2. **Type gate**: apply empirical, measurement, theory, structural/quantitative, policy report, or mixed gates.
3. **Data or model availability gate**: for data-using projects, separate agent-side evidence from user-side access confirmation; for theory, verify primitives and proof path; for structural/quantitative, verify moments, calibration/estimation, and computation.
4. **Identification or validation diagnosis**: name usable variation for causal work, validation checks for measurement/facts, equilibrium/proposition logic for theory, or moment/parameter identification for structural/quantitative work.
5. **Object mapping**: define variables, measures, primitives, moments, parameters, mechanisms, and labels as relevant.
6. **Minimum viable model/design**: write the baseline comparison, measurement rule, theoretical setup, or quantitative model in words first; formula only after the objects are clear.
7. **Table, figure, proposition, or counterfactual plan**: decide which 3-5 outputs are necessary for the first version.
8. **Unsupported claims**: list causal, mechanism, policy, external-validity, and novelty claims the current design cannot yet support.
9. **Validation plan**: give 3-7 checks that can be done before committing to full data work.

## Required Tables

### Data / Model / Measurement Map

| Component | Object | Candidate source or model role | Agent-side evidence | User-side confirmation | Difficulty | Missing check |
| --- | --- | --- | --- | --- | --- | --- |
| Outcome / fact / target moment |  |  |  |  |  |  |
| Treatment / key variable / primitive |  |  |  |  |  |  |
| Mechanism / parameter / friction |  |  |  |  |  |  |
| Controls / validation / benchmark |  |  |  |  |  |  |
| Merge keys / model mapping |  |  |  |  |  |  |

### Identification Screen

| Route | Needed object | Main assumption | Main threat | First validation |
| --- | --- | --- | --- | --- |
| DID/event study | policy timing or intensity | parallel trends / no anticipation | differential trends | pre-trend plot |
| IV | excluded source of X variation | relevance and exclusion | direct effect / weak IV | first stage and exclusion story |
| RDD | cutoff assignment | continuity near threshold | manipulation or sorting | density and balance checks |
| Shift-share | exposure times shock | shock exogeneity | endogenous exposure | pre-trend and leave-one-out checks |
| Panel FE | within-unit changes | no omitted time-varying confounder | reverse causality | placebo timing or lag structure |
| Descriptive facts | measurement variation | valid and stable measurement | composition shifts | sample audit and definitions |
| Theory | primitives and timing | equilibrium logic | result assumed by construction | proposition or comparative static |
| Structural/quantitative | moments and parameters | identification/calibration | weak mapping or poor fit | fit and sensitivity checks |

## Minimum Viable Result Package

Prefer a small first version:

- Table 1: sample construction and descriptive statistics.
- Table 2: main effect or core descriptive fact.
- Table 3: robustness checks or alternative definitions.
- Table 4: mechanism or heterogeneity only if data support it.
- Figure 1: policy timeline, data distribution, map, event-study plot, or validation figure.
- Theory version: model setup, main proposition, comparative static, example, extension.
- Structural/quantitative version: model block, target moments, fit table, counterfactual figure, sensitivity table.

Avoid adding mechanism or heterogeneity tables before the outcome, key X, and main comparison are credible.

## Verdict

End with:

```text
data_gate: green / yellow / red
identification_gate: green / yellow / red
decision: proceed / refine / retrieve_sources / pivot / park
next_action:
```

Then give a user-facing iteration decision:

```text
判断: 建议继续打磨 / 建议冻结当前版本 / 可以推进，也可继续升级 / 建议暂停或更换路线
建议下一步:
可选项:
是否需要用户选择:
```

Only `green + green` with a `建议冻结当前版本` or `可以推进，也可继续升级` iteration judgment should proceed directly to a full blueprint. Yellow requires another validation or refinement choice first unless the judgment explicitly says the thesis can proceed. Red requires repair, downgrade, pivot, or park.

Return to `references/00_master_router.md` with: score state, paper-type gate, data/model/measurement/theory gate, identification gate if relevant, decision, next action, and whether to use a backup branch.
