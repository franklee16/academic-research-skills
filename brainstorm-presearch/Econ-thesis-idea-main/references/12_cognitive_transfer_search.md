# Cognitive Transfer Search

## Purpose

Use Cognitive Transfer Search / 认知迁移搜索 when an economics thesis idea may benefit from tools, structures, proof strategies, measurement ideas, or model patterns from another field. This is not ordinary brainstorming and not decorative analogy. The goal is to translate an economics problem into a structure card, search for transferable source-domain structures, then keep only transfers that can produce variables, facts, propositions, model blocks, figures, tables, proofs, or testable claims.

Do not run this module for every routine thesis idea. Treat it as an enhancement module for novelty, mechanism, theory, measurement, or model bottlenecks.

## Triggers

Call this module when at least one condition holds:

- the user explicitly asks for cross-field transfer, cognitive migration, interdisciplinary search, or inspiration from other domains;
- the ordinary ideation review finds weak novelty or weak impact, but the core economic object is still interesting;
- the theory, structural, quantitative, measurement, or mechanism route is stuck;
- the idea has a descriptive pattern but lacks a deeper mechanism or model;
- the literature crowding gate or crowded-topic pivot lab leaves only low-quality branches;
- selected-topic refinement shows that the empirical route is thin, but a model, measurement, or mechanism route might still rescue the idea;
- the user wants a higher-ambition branch after a thesis-feasible version already exists.

## Workflow

### 1. Problem Structure Card

First abstract the economics idea away from its topic labels:

```markdown
## Problem Structure Card
- Economic object:
- Unit or agent:
- Relationship, mechanism, or pattern:
- Constraint, friction, or scarce resource:
- Time/order/process:
- Network, spatial, strategic, informational, dynamic, or measurement structure:
- Desired output: variable / fact / proposition / model block / figure / table / proof / counterfactual
- Current bottleneck:
- Claims not yet supported:
```

Keep the original economics language visible. Do not let source-domain terminology replace the economic question.

### 2. Source-Domain Candidate Search

Search for structures and tools, not just topical keywords. Useful source domains include:

- mathematics and proof strategies: extremal examples, bounds, duality, fixed points, graph theory, topology, optimization;
- network science: centrality, diffusion, multiplex networks, percolation, community detection, brokerage, robustness;
- information theory: entropy, compression, coding, signal extraction, noise, mutual information, attention limits;
- ecology and evolution: niche, competition, adaptation, invasion, resilience, carrying capacity, coevolution;
- epidemiology: contagion, exposure, susceptible-infected-recovered structures, thresholds, superspreading, contact networks;
- computer science and algorithms: search, matching, routing, recommendation, complexity, exploration-exploitation, bandits;
- physics and complex systems: phase transition, criticality, cascades, synchronization, hysteresis, scaling laws;
- operations research: queues, congestion, inventory, allocation, scheduling, bottlenecks, stochastic control;
- cognitive science and psychology: attention, memory, categorization, learning, heuristics, representation.

For each source candidate, name the transferable structure or tool and the economics object it might map to.

### 3. Transfer Hypothesis

Write each transfer as a hypothesis, not as a metaphor:

```markdown
Source-domain structure/tool:
Economics mapping:
- source object -> economics object
- source relation/process -> economics relation/process
- source constraint/friction -> economics constraint/friction
Potential thesis output:
What the transfer newly lets us measure, model, prove, compare, or visualize:
```

### 4. Transfer Scoring

Score every transfer candidate from 0 to 10:

| Dimension | Question |
| --- | --- |
| Structural fit | Does the source structure match the economic object beyond surface resemblance? |
| Economic meaning | Does the mapping preserve meaningful economic incentives, constraints, agents, or institutions? |
| Operationality | Can it become a variable, proposition, model block, table, figure, proof step, or testable fact? |
| Data/model/proof feasibility | Is there a realistic path to data, computation, calibration, formalization, or proof? |
| Paper contribution | Would the transfer strengthen novelty, mechanism, measurement, identification, or theory contribution? |
| Misleading metaphor risk | Could the analogy seduce the paper into false precision or non-economic claims? Higher is worse. |

Report the first five dimensions as value dimensions. Report misleading metaphor risk separately and use it as a penalty. A simple rule is:

```text
transfer_value = average(structural fit, economic meaning, operationality, feasibility, paper contribution)
```

If misleading metaphor risk is 7 or higher, downgrade the transfer unless the output object is unusually concrete and defensible.

## Three Gates

### Structure Gate

Pass only if the mapping preserves a real relation, process, constraint, or formal object. Surface word similarity is not enough.

Fail or downgrade when the transfer only says "this is like that" without a structural mapping.

### Operation Gate

Pass only if the transfer produces at least one concrete output:

- measurable variable or index;
- descriptive fact or comparison;
- model primitive, state variable, constraint, timing, or equilibrium object;
- proposition, lemma, comparative static, or proof strategy;
- estimation/calibration moment or counterfactual;
- table, figure, network object, or validation exercise.

If the transfer cannot produce any of these, label it as a metaphor and do not let it drive the thesis.

### Economics Contribution Gate

Pass only if the transfer clarifies an economic mechanism, improves measurement, creates a sharper model, suggests a new empirical fact, or changes the paper's contribution relative to close literature.

Fail or downgrade when the transfer is technically interesting but does not help answer an economics question.

## Lightweight MCTS/UCT Position

Do not mechanically run MCTS for every transfer. Use small MCTS/UCT branch comparison when:

- several source-domain transfers have similar scores;
- the best source domain is unclear;
- one transfer has high novelty but weak feasibility while another has lower novelty but stronger feasibility;
- the user wants higher ambition and can tolerate exploration;
- previous iterations improved little but the gates are not fatal.

Use transfer candidates as nodes. Possible actions:

- retrieve source-domain concept;
- remap the economics object;
- simplify the tool;
- combine two source domains;
- downgrade from causal empirical design to measurement, theory, or structural/quantitative design;
- reject misleading metaphor;
- return to ordinary selected-topic refinement.

Reward should combine the normal five-dimensional idea score with transfer gates:

```text
transfer_reward = idea_reward adjusted by structure gate, operation gate, economics contribution gate, and metaphor-risk penalty
```

User-facing output should say "我做了小规模跨领域分支比较" or "I ran a small cross-field branch comparison." Do not expose visits/value, UCT logs, or internal status codes unless the user explicitly asks for technical details.

## Output Template

Use this block when Cognitive Transfer Search is triggered:

```markdown
## 认知迁移搜索 / Cognitive Transfer Search

### 问题结构卡片
- 经济学对象：
- 单位或主体：
- 核心关系/机制/模式：
- 约束、摩擦或稀缺资源：
- 时间、顺序或过程：
- 网络/空间/策略/信息/动态/测度结构：
- 想得到的论文对象：
- 当前卡点：

### 源领域候选与迁移评分
| Source domain | Transferable tool/structure | Economics mapping | Possible output | Fit/Meaning/Operation/Feasibility/Contribution | Metaphor risk | Gate result | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | variable / proposition / model block / fact / figure / table / proof | | | structure / operation / contribution | recommend / backup / downgrade / reject |

### 推荐路线
- 主推迁移：
- 为什么它不是单纯比喻：
- 它能产出的变量、命题、模型、图表或事实：
- 主要风险：

### 备选路线
- 备选 1：
- 备选 2：

### 返回总控路由
- 下一步 gate：
- 是否需要小规模分支比较：
- 是否继续打磨：
```

## Handoff Rules

After Cognitive Transfer Search, always return to the master router. The selected transfer route must still pass the relevant paper-type gate:

- empirical causal: data and identification gates;
- measurement/facts: concept, measurement, coverage, validation, and reproducibility gates;
- theory: primitives, timing, equilibrium, proposition, and comparative-statics gates;
- structural/quantitative: model-data mapping, moments, estimation/calibration, fit, and counterfactual gates;
- policy report: evidence, implementability, and policy-risk gates.

Preserve the v34 stop-or-continue rule. Cognitive transfer output must still include `是否继续打磨` before any first-week validation plan, advisor memo, or full thesis blueprint. If the judgment is `建议继续打磨`, stop with next-iteration choices and do not output those downstream planning sections in the same round unless the user explicitly asks for a provisional sketch.
