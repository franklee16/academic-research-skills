# IRIS-Style Ideation Loop

## Purpose

Use this module when a raw thesis interest needs more than a single review pass. It adapts the useful IRIS loop for economics thesis design:

```text
research goal -> brief -> review scores -> refinement actions -> idea tree -> best branch -> thesis gates
```

This is not a replacement for literature search, data access checks, identification diagnosis, advisor judgment, or empirical validation. It is a bounded exploration engine for candidate thesis directions.

## When To Use

Use this module when:

- the user's input is vague, broad, or only a personal interest;
- several plausible translations or branches exist;
- the topic is crowded and the pivot lab produces multiple nearby options;
- the user wants the AI to explore alternatives before choosing one;
- an initial branch fails and backup branches need systematic comparison.

Skip full tree search for a tiny one-off diagnosis, an urgent deadline with one obvious data path, or a case where the data or theory gate is already red.

## Mandatory Per-Idea And Per-Iteration Review

Every idea, every candidate branch, and every refinement iteration must include at least a one-node IRIS review, even when full MCTS is skipped. A node cannot be selected, expanded, compared, recommended, parked, or killed until it has a five-dimensional score.

Minimum required output:

```markdown
## Mandatory IRIS Review
| Criterion | Score | Feedback |
| --- | --- | --- |
| Novelty | /10 | |
| Clarity | /10 | |
| Feasibility | /10 | |
| Effectiveness | /10 | |
| Impact | /10 | |

- Average score:
- Score change from previous iteration: improved / flat / worse / not available
- Weakest dimensions:
- 小规模分支比较：已使用 / 未使用
- 若未使用，原因：
- Next recommended action:
```

Do not output only a literature summary, revised title, or refined research question. The score table is mandatory for every version being compared or advanced. If multiple branches are shown, score each branch separately. If a branch was refined, score the old and new versions or state the score change.

Each response must include an iteration decision. The decision may recommend freezing the current branch instead of continuing. Ask the user to choose a next action only when continuation is required or useful.

## Brief Format

Each node should contain a compact research brief:

```markdown
# Title

## Core Question
One precise economics question.

## Proposed Design
Data, setting, comparison, model, or theory route.

## Why It Might Work
Economic intuition and why it fits the user's goal.

## Validation Plan
Literature, data, identification, measurement, or theory check.

## Main Risks
Data, identification, novelty, scope, execution, or advisor-defense risks.
```

Keep briefs useful for iteration. Do not polish them as final paper prose.

## Node State

Maintain a compact tree when using multi-round exploration:

```text
node_id | parent | action | depth | title | avg_score | visits | value | gate_status | status
```

Use short IDs:

- `n0`: user's raw interest or initial idea card;
- `n1`, `n2`, `n3`: generated or refined briefs;
- link each node to a candidate ID in the master candidate bank when it becomes viable.

Each node stores:

- `research_goal`;
- `current_brief`;
- `review_scores`;
- `review_feedback`;
- `retrieved_knowledge` if literature or data sources were checked;
- `gate_status`: crowding, paper-type, data, measurement, model, theory, structural, and identification status if known;
- `depth`, `visits`, and `value`.

## Actions

Use these actions:

| Action | Use when | Output |
| --- | --- | --- |
| `generate` | starting from raw interest | first structured brief |
| `review_and_refine` | a node has weak scores but useful core | revised brief improving weakest 2-3 criteria |
| `refresh_idea` | the node is stale, crowded, or too narrow | substantially different branch preserving part of the original interest |
| `retrieve_and_refine` | literature/data grounding is needed | revised brief using inspected sources or clearly marked source tasks |
| `direct_feedback` | user chooses, rejects, or corrects a direction | child node incorporating user feedback |
| `data_gate_refine` | data access or evidence path is weak | brief revised around obtainable or user-confirmable data |
| `identification_refine` | causal credibility is weak | brief revised around usable variation or downgraded claim |
| `type_gate_refine` | the branch is being forced into the wrong paper type | brief revised as empirical, measurement/facts, theory, structural/quantitative, or policy report |

## Review Rubric

Score each node from 0 to 10:

| Criterion | Meaning |
| --- | --- |
| Novelty | Meaningfully different from obvious existing approaches; provisional until literature is checked |
| Clarity | Question, objects, mechanism, and setting are understandable |
| Feasibility | Data, measurement, model, proof, computation, or validation path can realistically be attempted |
| Effectiveness | Proposed design can answer the stated question |
| Impact | Result would matter for economics, policy, thesis defense, or the user's goal |

List the weakest 2-3 dimensions and choose the next action from them.

## Gate-Adjusted Reward

Use the IRIS average as the starting reward:

```text
iris_reward = average(novelty, clarity, feasibility, effectiveness, impact) / 10
```

Then adjust for thesis gates:

```text
reward = iris_reward
```

Apply caps when gate evidence is known:

| Gate result | Reward cap |
| --- | --- |
| Literature `saturated` and no new data/setting/measure/design | 0.35 |
| Data gate `red` for an empirical claim | 0.35 |
| Identification gate `red` for a causal claim | 0.45 |
| Theory gate `red` for a pure theory route | 0.35 |
| Structural/quantitative gate `red` for model-data mapping | 0.40 |
| Major advisor-defense risk unresolved | 0.60 |

Yellow gates do not kill the node, but they should reduce confidence and set the next action to retrieve, data, identification, model, measurement, or theory refinement.

Never let a high IRIS score override a red thesis gate.

## Lightweight MCTS

Use MCTS only when exploring multiple branches. Keep it small by default: 2-5 iterations.

For each iteration:

1. **Select**: choose an unvisited child first. If all children are visited, choose the child with the highest UCT score.
2. **Evaluate**: score the node with the review rubric and gate-adjusted reward.
3. **Expand**: add child nodes using relevant actions, usually `review_and_refine`, `refresh_idea`, `data_gate_refine`, or `identification_refine`; add `retrieve_and_refine` when literature or data grounding is needed.
4. **Backpropagate**: increment visits and update value as a running average reward. Optionally discount parent rewards by `0.9`.
5. **Choose**: report the best current branch, backup branches, and the next recommended action.

UCT formula:

```text
UCT = value + c * sqrt(log(parent_visits + 1) / (child_visits + 1))
```

Use `c = 1.4` by default. Use a lower `c` when the user has a tight deadline and a higher `c` when exploration is the explicit goal.

## Stop-Or-Continue Judgment

Each substantive ideation response must include a stop-or-continue judgment before downstream planning sections. Do not expose internal route codes in user-facing output:

```markdown
## 是否继续打磨
- 判断：建议继续打磨 / 建议冻结当前版本 / 可以推进，也可继续升级 / 建议暂停或更换路线
- 理由：
- 建议下一步：
- 可选项：
```

Use these rules:

- 建议继续打磨: any score is below 6, average score is below 7, the idea lacks a clear question, type route, data/model/proof/design, gates are red or unresolved, or several branches remain without user selection.
- 建议冻结当前版本: average score is about 7.5 or higher, no score is below 6.5, and the type-specific blueprint is concrete enough for the user's thesis level.
- 可以推进，也可继续升级: the idea can proceed, but one more iteration could improve ambition, novelty, data grounding, model, mechanism, identification, or quantification.
- 建议暂停或更换路线: the branch is blocked by saturated literature, unavailable data, unrepairable identification, failed measurement, failed structural mapping, or failed theory route.

When the choice is ambiguous, run a 2-5 step MCTS/UCT comparison and summarize it as "小规模分支比较". If the case is obvious, state why MCTS was skipped. Ask the user to choose an action only when a real choice remains. If the judgment is `建议继续打磨`, stop with the next-iteration options and do not output a first-week validation plan, advisor memo, or full thesis blueprint in the same round. If freezing is recommended, move to thesis blueprint or first-week validation while mentioning that the user may optionally pursue a higher-ambition version.

When MCTS is skipped because there is only one branch and it is clearly data-red, type-gate-red, theory/model-red, or already ready to freeze, do not expose a technical skip label. Use natural language:

- Red or blocked branch: "我没有做树搜索，因为当前只有一个方向，而且阻塞点已经很明确。你要不要调用三维生发模块，从原始 X、Y、机制或反向因果里找 2-3 个相邻新方向？"
- Ready-to-freeze branch: "我没有做树搜索，因为当前版本已经足够冻结。可以直接进入论文蓝图；如果你还想追求更高质量或备选题，也可以调用三维生发模块再找相邻方向。"

## Output Template

```markdown
## 小规模分支比较

我做了小规模分支比较，重点比较每个方向的五维评分、关键 gate、最小可行版本和答辩风险。以下是用户可见摘要；不要默认展示 UCT 分数、visits/value 或节点日志。

| Candidate | Source/action | Research question | N/C/F/E/I | Average | Gate-adjusted reasoning | Main risk | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| c1 | generate / refine / retrieve / refresh | | | | | | |
| c2 | generate / refine / retrieve / refresh | | | | | | |

## Best Branch
- Selected candidate:
- Why this branch:
- Weakest remaining dimensions:
- Next gate:

## Backup Branches
- Backup 1:
- Backup 2:

## Do Not Claim Yet
- Novelty:
- Data:
- Causality:
- Mechanism:

## 是否继续打磨
- Recommended next action:
- 判断:
- User choice needed:
```

After choosing the best branch, return to `references/00_master_router.md`. The selected branch must still pass the literature crowding, data feasibility, and identification gates before a full thesis blueprint.
