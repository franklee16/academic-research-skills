# Master Router

## Purpose

Use this file as the total controller for multi-step `thesis-idea` work. It decides the current stage, what reference module to load next, which candidate branch is active, and when to stop, pivot, or return to a backup branch.

The router should keep the process ordered:

```text
raw interest -> per-idea ideation review -> IRIS tree when useful -> paper-type route -> cognitive transfer search when triggered -> literature crowding gate -> pivot lab if needed -> user selection -> selected-topic refinement -> type-specific gates -> verdict -> thesis blueprint
```

## Routing Architecture

Use a star-shaped architecture:

- `00_master_router.md` owns stage order, candidate-bank state, and handoffs.
- Other reference files define local diagnostics and return a compact status.
- Do not build a mesh where every module routes to every other module.
- When a module finishes, return to the master router to decide the next step.

This keeps the skill from forgetting earlier gates or overloading the context window.

## Project State

Maintain a compact state table when the task spans more than one exchange:

```text
stage | active_candidate | selected? | crowding | transfer_gate | data_gate | identification_gate | decision | next_route
```

Use short candidate IDs:

```text
c0 = user's raw interest
c1, c2, c3 = generated or refined candidate branches
```

Candidate records should contain:

- `raw_interest`: user's original wording;
- `academic_translation`: provisional research-language version;
- `source`: original / horizontal-X / horizontal-Y / vertical / reverse-X / reverse-Y / user feedback;
- `question`: one-sentence candidate question;
- `paper_type`: empirical causal / measurement-facts / theory / structural-quantitative / policy report / mixed / unclear;
- `crowding`: low / medium / high / saturated / not checked;
- `data_gate`: green / yellow / red / not applicable / not checked;
- `identification_gate`: green / yellow / red / not applicable / not checked;
- `type_gate`: green / yellow / red / not checked;
- `transfer_gate`: green / yellow / red / not applicable / not checked;
- `transfer_route`: source-domain transfer path if Cognitive Transfer Search is used;
- `ideation_score`: average of novelty, clarity, feasibility, effectiveness, and impact when scored;
- `tree_node`: linked IRIS-style node ID if tree exploration is used;
- `visits` and `value`: lightweight MCTS state when relevant;
- `candidate_state`: active / backup / rejected / parked / killed;
- `next_action`: literature check, cognitive transfer search, data check, user choice, refinement, pivot, blueprint, or stop.

## Stage 1: Raw Interest Intake

Accept rough inputs such as:

- personal interest;
- advisor direction;
- policy name;
- variable or index;
- observed phenomenon;
- vague sentence;
- several disconnected keywords.

First preserve the raw wording. Then create a provisional academic translation as an idea card:

```markdown
## Raw Interest Card
- Raw wording:
- Possible economic object:
- Possible X:
- Possible Y:
- Possible mechanism:
- Possible setting:
- Claim type: causal / descriptive / measurement / theory / unclear
- Missing key information:
```

Do not lock the final title at this stage. If the input is too vague, still produce the card and ask at most one high-impact question.

## Stage 2: Mandatory Ideation Review

Review the idea card before literature and data gates. This is mandatory for the first idea, but it is not limited to the first pass.

Every idea, every candidate branch, and every refinement iteration must be scored from 0 to 10:

| Criterion | Question |
| --- | --- |
| Novelty | Is there a plausible margin beyond obvious existing work? Mark as provisional until literature is checked. |
| Clarity | Can the idea be stated as an object, relationship, or fact? |
| Feasibility | Is there a plausible path to data, measurement, model, proof, or evidence? |
| Effectiveness | Would the design answer the user's intended question? |
| Impact | Would the answer matter for economics, policy, or thesis defense? |

Then report:

- average score;
- score change from the previous iteration when available;
- weakest 2-3 dimensions;
- whether MCTS/tree exploration was run or skipped;
- next route.

Then route by the weakest dimensions:

| Weakest dimension | Next route |
| --- | --- |
| Clarity | refine the idea card, ask one question, or generate 2-3 candidate translations |
| Novelty | run `references/07_literature_crowding_gate.md` |
| Feasibility | run `references/11_paper_type_gates.md`, then the relevant data, measurement, theory, or structural gate |
| Effectiveness | run `references/04_identification_diagnostics.md` for empirical causal ideas or `references/11_paper_type_gates.md` for other types |
| Impact | narrow the welfare object, mechanism, or setting before full design |

Do not claim true novelty without literature search.

Do not output only a literature summary, revised topic sentence, or verdict. Any branch that is introduced, compared, advanced, selected, or refined must carry its own score table or compact score row. End with an iteration decision that says whether to continue, freeze, optionally continue, or stop/park.

## Stage 2b: IRIS-Style Tree Exploration

Route to `references/10_iris_ideation_loop.md` when the first review creates several plausible translations, the user wants exploration, the idea is broad, or the pivot lab produces multiple viable branches.

Use a small tree, not open-ended brainstorming:

- generate or refine research briefs;
- score every node on novelty, clarity, feasibility, effectiveness, and impact before selection, expansion, or comparison;
- use `generate`, `review_and_refine`, `refresh_idea`, `retrieve_and_refine`, `data_gate_refine`, `identification_refine`, or `direct_feedback`;
- run 2-5 MCTS/UCT iterations by default;
- track node visits and value;
- apply thesis-gate penalties when literature, data, identification, or theory gates are known.

Tree search is only a candidate-exploration method. After a best branch is chosen, return to the router and run literature, data, and identification gates before a thesis blueprint.

When deciding whether a branch should continue, freeze, or stop is ambiguous, run a small MCTS/UCT comparison unless the case is obvious or the user has a tight deadline. In user-facing output, summarize this as a "小规模分支比较"; do not expose UCT formulas, internal status codes, or tree bookkeeping unless the user asks for technical details.

If MCTS is skipped because there is only one branch and the decision is obvious, still handle the user's choice space explicitly:

- If the branch is clearly red or not worth continuing, state why tree search was unnecessary, then ask whether to call the three-dimensional branching module in Stage 4 to look for adjacent new ideas from the original X, Y, mechanism, or reverse causal direction.
- If the branch is clearly ready to freeze, recommend freezing and moving to blueprint or first-week validation, then offer optional three-dimensional branching only if the user still wants alternative or higher-ambition directions.

## Stage 2c: Paper-Type Route

Route to `references/11_paper_type_gates.md` before diagnosing data, identification, or blueprint.

Classify each candidate as:

- empirical causal;
- measurement/facts/descriptive;
- theory;
- structural/quantitative/computational;
- policy report;
- mixed.

Do not force a theory, measurement, or structural idea into a main regression. For non-empirical types, replace data/identification gates with the relevant measurement, model, proof, moment, calibration, or policy-evidence gate.

## Stage 2d: Cognitive Transfer Search

Route to `references/12_cognitive_transfer_search.md` when cross-field transfer is explicitly requested or when ordinary review, literature crowding, pivot lab, selected-topic refinement, theory gate, structural gate, measurement gate, or mechanism diagnosis suggests that novelty, model structure, proof strategy, measurement, or explanation is stuck but still salvageable.

This stage can appear after ordinary ideation review, after literature crowding, after the crowded-topic pivot lab, after user selection, or after a type-specific gate. It must still return to this router before any thesis blueprint.

Required behavior:

- abstract the economics idea into a problem structure card;
- search source-domain tools, structures, proof strategies, measurement ideas, or model patterns;
- score each transfer on structural fit, economic meaning, operationality, data/model/proof feasibility, paper contribution, and misleading metaphor risk;
- apply structure, operation, and economics-contribution gates;
- use small MCTS/UCT branch comparison only when several transfer routes are close or the best route is unclear;
- downgrade or reject transfers that are only metaphors and do not produce variables, propositions, model blocks, tables, figures, proof steps, or testable facts.

After the recommended transfer route is chosen, return to the relevant paper-type gate. A cognitive-transfer branch still needs the usual `是否继续打磨` judgment before any first-week validation plan, advisor memo, or full thesis blueprint.

## Stage 3: Literature Crowding Gate

Route to `references/07_literature_crowding_gate.md` when:

- the user is in thesis rescue mode;
- the topic is a crowded China or applied-economics theme;
- the idea uses standard public data and standard panel FE/DID/mediation patterns;
- the mandatory ideation review suggests novelty is the binding risk.

If crowding is `low` or `medium`, continue to data and identification gates. If crowding is `high` or `saturated`, route to the pivot lab or recommend `park`/`kill`.

## Stage 4: Crowded Topic Pivot Lab

Route to `references/08_crowded_topic_pivot_lab.md` when the exact topic is crowded but the user's underlying interest is still worth preserving.

The pivot lab should generate branches from the original idea:

- horizontal from X;
- horizontal from Y;
- vertical through mechanisms;
- reverse from X adoption, diffusion, or capacity;
- reverse from Y as a cause of later behavior or policy response.

Screen each branch on literature crowding, data path, design, defense risk, and user fit. Put viable branches into the candidate bank.

In this stage, do not force each branch into an over-compressed one-sentence question. Use a readable candidate question and, when needed, a separate key-object note that names the unit, X/object, Y/outcome or fact, mechanism/comparison, and claim type. The formal one-sentence research question can be produced after the user selects a branch.

## Stage 5: User Selection

When there are several viable branches, ask the user to choose one primary branch unless the best choice is obvious and low risk.

Keep other viable branches as backups:

```markdown
## Candidate Bank
| ID | Candidate | Why keep it | Current risk | Return if |
| --- | --- | --- | --- | --- |
| c1 | | primary | | |
| c2 | | backup | | c1 fails data, model, or measurement gate |
| c3 | | backup | | c1 fails identification, theory, or structural gate |
```

Do not refine every branch into a full blueprint. Refine only the selected branch.

## Stage 6: Selected-Topic Refinement

Route to `references/09_selected_topic_refinement.md` after the user chooses a branch.

Freeze the selected candidate. Convert it into:

- one-sentence research question;
- data, model, measurement, or theory object map;
- sample construction, model setup, measurement coverage, or theory primitives;
- identification, validation, theoretical, structural, or descriptive strategy;
- main regression, comparison, measurement rule, proposition, or model block;
- table, figure, proposition, fit, or counterfactual plan;
- unsupported claims;
- first validation tasks.

If the relevant type-specific gate becomes red, return to the candidate bank and test the next backup branch.

## Stage 7: Gates And Verdict

Use these gates before a full blueprint:

1. Paper-type gate: `references/11_paper_type_gates.md`.
2. Cognitive transfer gate when cross-field transfer is triggered: `references/12_cognitive_transfer_search.md`.
3. Data gate when the type uses data: `references/03_data_feasibility.md`.
4. Identification gate for empirical causal claims: `references/04_identification_diagnostics.md`.
5. Verdict rules: `references/02_verdict_rules.md`.
6. Research design patterns when useful: `references/06_research_design_patterns.md`.

Only move to a full thesis blueprint when the idea is green or repairable yellow and the `是否继续打磨` judgment says `建议冻结当前版本` or `可以推进，也可继续升级`. If the judgment says `建议继续打磨`, stop with next-iteration options. For red ideas, recommend pivot, park, kill, downgrade, or a strict theory route.

## Stage 8: Thesis Blueprint

Route to `references/05_output_templates.md` for downstream planning only after the stop-or-continue gate allows it:

- single idea diagnosis;
- batch screening;
- first-week validation plan;
- advisor memo;
- thesis blueprint.

The final blueprint should match the paper type. Empirical ideas need main regression or comparison, variables, data, tables, and figures. Measurement/facts ideas need concept, measurement rule, validation, fact tables, and figures. Theory ideas need primitives, timing, equilibrium, propositions, and comparative statics. Structural/quantitative ideas need model blocks, moments, estimation or calibration, fit, counterfactuals, and computation checks.

## Router Output

At the end of each substantive exchange, include a compact routing state when useful:

```markdown
## Router State
- Current stage:
- Active candidate:
- Backup candidates:
- Binding risk:
- Next route:
```

Use this state to keep long conversations from drifting away from the skill.

For every substantive exchange, also include a compact iteration decision:

```markdown
## 是否继续打磨
- 判断：建议继续打磨 / 建议冻结当前版本 / 可以推进，也可继续升级 / 建议暂停或更换路线
- 理由：
- 建议下一步：
- 可选项：
```

Use these status rules:

- 建议继续打磨: any score is below 6, average score is below 7, the question/data/model/identification is still underspecified, gates are red or unresolved, or meaningful branches remain but the user has not selected one.
- 建议冻结当前版本: average score is about 7.5 or higher, no dimension is below 6.5, type-specific gates are concrete enough, the closest-literature risk is not fatal, and the one-sentence question plus blueprint objects are clear.
- 可以推进，也可继续升级: the idea can proceed as a thesis, but one more iteration could improve ambition, novelty, data grounding, model, mechanism, identification, or quantification.
- 建议暂停或更换路线: data, literature, identification, measurement, structural, or theory gates make the current branch not worth further iteration; offer backup, downgrade, park, kill, or a different paper type.

Do not show internal route codes. Treat this section as the routing gate before downstream planning. If the judgment is `建议继续打磨`, stop the response here with concrete next-iteration options; do not output a first-week validation plan, advisor memo, or full thesis blueprint in the same round unless the user explicitly asks for a provisional sketch. If freezing is recommended, say so directly and then move to blueprint or first-week validation.

When MCTS was skipped because one branch was obviously blocked or obviously freezable, include a natural-language question about whether to use the three-dimensional branching module. Do this even when no further MCTS choice is needed, because the real user choice may be whether to accept the verdict or search for adjacent alternatives.
