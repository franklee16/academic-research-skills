# Output Templates

## Single Idea Diagnosis

```markdown
# Idea Diagnosis

## 0a. Router State
- Current stage:
- Active candidate:
- Backup candidates:
- Binding risk:
- Next route:

## 0b. Per-Idea And Per-Iteration IRIS Review
Required for every idea, every candidate branch, and every refinement iteration. If multiple branches are listed, score each branch separately before recommending or rejecting it.

| Criterion | Score | Feedback |
| --- | --- | --- |
| Novelty | /10 | Provisional until literature is checked. |
| Clarity | /10 | |
| Feasibility | /10 | |
| Effectiveness | /10 | |
| Impact | /10 | |

- Average score:
- Score change from previous iteration: improved / flat / worse / not available
- Weakest dimensions:
- 小规模分支比较：已使用 / 未使用
- 若未使用，原因：
- Next route:

## 0c. 小规模分支比较
Use this section only when branch exploration is used. Do not show node visits/value, UCT scores, or tree bookkeeping unless the user explicitly asks for technical details.

| Candidate | Source/action | Research question | N/C/F/E/I | Average | Gate-adjusted reasoning | Main risk | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| c1 | generate / refine / retrieve / refresh | | | | | | |
| c2 | generate / refine / retrieve / refresh | | | | | | |

- Best branch:
- Backup branches:
- Weakest remaining dimensions:
- Next gate:

## 0d. 认知迁移搜索 / Cognitive Transfer Search
Use this section only when cross-field transfer is triggered by the user, weak novelty, a stuck theory/model/measurement/mechanism route, or thin ordinary pivot branches.

### Problem Structure Card
- Economic object:
- Unit or agent:
- Core relationship / mechanism / pattern:
- Constraint, friction, or scarce resource:
- Time, order, or process:
- Network / spatial / strategic / informational / dynamic / measurement structure:
- Desired thesis object: variable / fact / proposition / model block / table / figure / proof / counterfactual
- Current bottleneck:

### Source-Domain Transfer Candidates
| Source domain | Transferable tool/structure | Economics mapping | Possible output | Fit/Meaning/Operation/Feasibility/Contribution | Metaphor risk | Gate result | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mathematics / network science / information theory / ecology / epidemiology / CS / physics / OR / cognitive science | | | variable / proposition / model block / fact / figure / table / proof | | | structure / operation / contribution | recommend / backup / downgrade / reject |

- Recommended route:
- Backup route(s):
- Main risk:
- Why this is more than a metaphor:
- Return to router:

## 0e. Literature Crowding Gate
- Literature crowding: low / medium / high / saturated / not checked
- Closest literature pattern:
- Defense risk:
- Decision before focusing: proceed / pivot / park / kill / downgrade
- Why continue or stop:

## 0f. Candidate Bank
| ID | Candidate | Source | Status | Why keep or reject | Return if |
| --- | --- | --- | --- | --- | --- |
| c0 | original interest | raw input | active / rejected / parked | | |
| c1 | | horizontal / vertical / reverse / user feedback | primary / backup / rejected | | |
| c2 | | horizontal / vertical / reverse / user feedback | primary / backup / rejected | | |

## 1. One-Sentence Rewrite
[Turn the raw idea into a testable economics question.]

## 2. Paper Type And Mode
- Type: empirical causal / measurement-facts / theory / structural-quantitative / policy report / mixed
- Mode: thesis rescue / research-design strengthening / top-field or top-journal
- Why:

## 3. Feasibility Verdict
- Feasibility: green / yellow / red
- Decision: proceed / pivot / park / kill / upgrade / downgrade
- Binding constraint:

## 4. 是否继续打磨
Required for every substantive output. Put this section here, before any thesis blueprint, first-week validation plan, or advisor memo.

- 判断：建议继续打磨 / 建议冻结当前版本 / 可以推进，也可继续升级 / 建议暂停或更换路线
- 理由：
- 建议下一步：
- 若判断为“建议继续打磨”：stop the output after this section and give 2-4 next-iteration options. Do not output sections 5-12 in this round unless the user explicitly asks for a provisional sketch.
- 若判断为“建议冻结当前版本”或“可以推进，也可继续升级”：continue to sections 5-12.
- 若判断为“建议暂停或更换路线”：do not output a full blueprint for the current branch; offer pivot, downgrade, park/kill, or candidate-bank options.
- 若因单一方向明显红灯或明显可冻结而跳过 MCTS：说明跳过原因，并询问是否调用三维生发模块，沿原始 X、Y、机制或反向因果寻找相邻新方向；若当前版本可冻结，把该询问写成可选升级，而不是强制继续。

## 5. Minimum Viable Thesis Version
- Title:
- Core question:
- Type-specific minimum version:
- Empirical causal: sample, period, outcome, treatment/key variable, baseline method.
- Measurement/facts: concept, measurement rule, coverage, validation fact, main figures.
- Theory: agents, choices, constraints, timing, friction, equilibrium, proposition.
- Structural/quantitative: model block, data moments, estimation/calibration, fit, counterfactual.

## 6. Data / Model / Measurement Map
| Component | Object | Source or model role | Agent-side evidence | User-side confirmation | Difficulty | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Outcome / fact / target moment | | | | | | |
| Treatment / key variable / primitive | | | | | | |
| Mechanism / parameter / friction | | | | | | |
| Controls / validation / benchmark | | | | | | |
| Unit / agent / state | | | | | | |
| Time / timing / horizon | | | | | | |

## 7. Design Options
| Route | Required object | Main assumption | Main threat | Feasibility |
| --- | --- | --- | --- | --- |
| Empirical causal | variation / comparison | | | |
| Measurement/facts | concept / measurement / validation | | | |
| Theory | primitives / equilibrium / proposition | | | |
| Structural/quantitative | moments / parameters / counterfactual | | | |
| Policy report | evidence / option / implementation | | | |

## 8. What Not To Claim
[Unsupported causal, mechanism, policy, novelty, or external-validity claims.]

## 9. Thesis Blueprint
- Section plan:
- Main regression, measurement design, model proposition, or structural block:
- Main table, figure, proposition, or counterfactual:
- Robustness, validation, comparative statics, sensitivity, or fit checks:
- Mechanism, heterogeneity, decomposition, extension, or policy exercise:
- Figures:
- Appendix:

## 10. First-Week Validation Plan
Day 1:
Day 2:
Day 3:
Day 4:
Day 5:
Day 6:
Day 7:

## 11. Advisor Memo
[200-300 Chinese characters or a concise English paragraph, depending on the user's language.]

## 12. Upgrade And Downgrade Path
- Thesis version:
- Excellent thesis version:
- Working paper version:
- Top-field/top-journal version:
```

For crowded master's topics, output section 0 first and stop there if the idea is `high`/`saturated` and the student has no new data, setting, measurement, mechanism, or identification. Do not produce sections 5-12 unless the idea passes the crowding gate or the user explicitly chooses to proceed despite the risk.

If the original idea is `high`/`saturated` but the user wants nearby alternatives, output the pivot lab before sections 1-11:

```markdown
## 0b. Crowded Topic Pivot Lab

Do not over-compress branch questions. The branch table should use readable candidate questions; if the question needs more context, keep the table cell concise and add key objects below it.

| Branch | Source from original topic | Dimension | Candidate idea | Readable candidate question | Key objects | Closest literature pattern | Data path | Main design | Defense risk | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | X-side / Y-side / mechanism / reverse-X / reverse-Y | horizontal / vertical / reverse | | | unit; X/object; Y/fact; mechanism/comparison; claim type | | | | | proceed / verify / pivot / park / kill |

Recommended branch:
Backup branch:
Why not the others:
First verification task:
Do not claim yet:
If the recommended branch is selected, then rewrite it into a formal one-sentence research question.
```

Only continue to a full thesis blueprint for a branch with `proceed` or `verify` and a `是否继续打磨` judgment of `建议冻结当前版本` or `可以推进，也可继续升级`.

After the user selects one branch, update the candidate bank and mark non-selected viable branches as `backup`. If the selected branch fails the data or identification gate, return to the highest-quality backup rather than restarting from zero.

## Batch Screening Table

```markdown
# Idea Screening Table

| Rank | Candidate idea | Readable research question | N/C/F/E/I score | Average | Data access | Identification | Advisor acceptance | Overall | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |

## Recommended Choice
[Pick the best fit for the user's deadline, data access, and ambition.]

## Why Not The Others
[State the binding risk for each rejected idea.]

## 是否继续打磨
[State in natural language whether to continue, freeze, optionally upgrade, or stop/change route; ask for a choice only when the user must choose among branches or continuation actions.]
```

## First-Week Validation Plan

Use this only after the output has already judged `是否继续打磨` as `建议冻结当前版本` or `可以推进，也可继续升级`. If the judgment is `建议继续打磨`, do not produce this plan yet; ask the user to choose the next refinement action first.

Default plan:

- Day 1: find 5 closest Chinese and English papers and inspect data, identification, mechanism, and novelty claims.
- Day 2: confirm or download the core data source or metadata.
- Day 3: build rough treatment/key variable and outcome definitions.
- Day 4: plot treatment intensity, time trend, sample coverage, or basic distribution.
- Day 5: run a baseline descriptive relation or feasibility regression if data exist.
- Day 6: inspect the most fatal identification threat.
- Day 7: write an advisor memo with decision, data status, and next action.

Short deadlines can compress this to 3 days; long projects can expand it into two weeks.

## Advisor Memo

The memo should include:

- topic and one-sentence question;
- why the question matters;
- data path and current access status;
- identification or descriptive strategy;
- main risk;
- first validation result needed;
- requested advisor decision.

Avoid grand claims. The memo is for decision-making, not selling a finished paper.
