# 毕业论文 idea 打磨器 🎓

`thesis-idea` 是一个面向经济学毕业论文选题和早期研究设计的 Codex skill。它帮助研究生和研究初学者把模糊兴趣、导师给的题目、政策、变量或现象，转化为更清楚、更可验证、更适合继续推进的研究问题。它会先检查题目是否太拥挤、数据或模型路径是否现实、识别和测度是否站得住，并先判断是否还需要继续打磨；只有当 idea 足够成熟时，才继续整理论文结构、变量/命题、数据、图表和第一周验证计划。它想做的事很简单：少一点空泛题目，多一点能真的往前走的研究设计。

# Thesis Idea Builder 🎓

`thesis-idea` is a Codex skill for economics thesis topic selection and early research design. It helps graduate students and early-stage researchers turn vague interests, advisor-given topics, policies, variables, or phenomena into clearer, more testable research questions. It first checks whether a topic is too crowded, whether the data or model path is realistic, and whether the identification or measurement logic is defensible, then decides whether the idea still needs polishing. Only mature ideas move on to thesis structures, variables or propositions, data plans, tables and figures, and first-week validation tasks. The goal is simple: fewer empty topic lists, more research designs that can actually move forward.

## 模型要求提示 🧠

AI 选题和研究设计对大模型的推理、知识组织、识别诊断和不确定性处理要求很高。建议优先使用当前最强的大模型：优先使用 GPT-5.5 Thinking 以上模型，以及 Claude 4.7 以上模型。DeepSeek 可以在中国大陆内部无法使用前两个模型时作为备选，但目前效果仍然不够好，尤其是在数据可行性、识别压力测试和论文蓝图细化上需要更谨慎地人工核查。

## Model Recommendation 🧠

AI-assisted topic selection and research design place high demands on a model's reasoning, knowledge organization, identification diagnostics, and uncertainty handling. Prefer the strongest available models: currently GPT-5.5 Thinking or above, and Claude 4.7 or above. DeepSeek can be used as a fallback when the first two model families are not accessible in mainland China, but its results are still not strong enough for this task; data feasibility, identification pressure-testing, and thesis-blueprint details require especially careful human checking.

## 不使用 AI Agent 时 🌐

如果你不使用 Codex skill 或其他 AI agent，也可以直接复制主目录里的 [`WEB_AI_PROMPT.md`](WEB_AI_PROMPT.md) 到网页版 AI 中使用。

网页版 AI 有上下文限制。更稳妥的做法是把这份 prompt 放进 AI 的背景、个性化设置、项目说明或 Custom instructions 中；如果平台不支持，就在每次开始新的 idea 打磨前粘贴一次。长对话后、隔了一段时间后、换窗口后，或模型输出开始偏离规则时，请重新上传或粘贴这份 prompt。

## Without An AI Agent 🌐

If you do not use the Codex skill or another AI agent, you can copy [`WEB_AI_PROMPT.md`](WEB_AI_PROMPT.md) from the repository root into a web AI chat and use it directly.

Web AI tools have context limits. A safer approach is to put this prompt into the AI tool's background, custom instructions, project instructions, or similar settings. If the platform does not support that, paste the prompt before starting a new idea-polishing session. After a long conversation, a long break, a new chat window, or when the model starts drifting from the rules, upload or paste the prompt again.

## 核心功能 ✨

- 面向经济学毕业论文选题和研究设计。
- 把模糊直觉、导师题目、政策、变量或现象，打磨成更清晰的研究问题。
- 检查题目是否太拥挤、数据是否现实可得、识别或模型路径是否站得住。
- 每轮给出五维评分：新意、清晰度、可行性、有效性和影响。
- 支持经验因果、测度/事实、理论、结构/量化、政策报告和混合型论文。
- 支持从其他学科寻找可迁移的工具、结构或模型思路。
- 先判断是否继续打磨；成熟后再输出第一周验证计划、导师 memo 和论文蓝图。

## Core Features ✨

- Serves economics thesis topic selection and research design.
- Turns vague intuitions, advisor-given topics, policies, variables, or phenomena into clearer research questions.
- Checks whether a topic is too crowded, whether data access is realistic, and whether the identification or model path is defensible.
- Gives five-dimensional scores in each round: novelty, clarity, feasibility, effectiveness, and impact.
- Supports empirical causal, measurement/facts, theory, structural/quantitative, policy report, and mixed thesis designs.
- Looks for transferable tools, structures, or model ideas from other fields.
- Decides whether to keep polishing first; mature ideas then receive first-week validation plans, advisor memos, and thesis blueprints.

## 安装 🚀

### 方法一（推荐）：让你的 agent 帮你安装

把这个项目网站发给你的 Codex 或其他本地 AI agent：

```text
https://github.com/juliaError/Econ-thesis-idea
```

然后对它说：

```text
请帮我安装这个 Codex skill。把仓库克隆到 ~/.codex/skills/thesis-idea；如果目录已存在，请先确认是更新还是覆盖。安装后提醒我重启或刷新 Codex，让 skill 列表重新加载。
```

如果你的 agent 没有本地文件系统或终端权限，请使用方法二手动安装。

### 方法二：手动安装

将这个仓库克隆到本地 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/juliaError/Econ-thesis-idea.git ~/.codex/skills/thesis-idea
```

安装后，重启或刷新 Codex，让 skill 列表重新加载。

## Install 🚀

### Method 1 (Recommended): Ask Your Agent To Install It

Send this project page to your Codex agent or another local AI agent:

```text
https://github.com/juliaError/Econ-thesis-idea
```

Then tell it:

```text
Please install this Codex skill for me. Clone the repository into ~/.codex/skills/thesis-idea. If the directory already exists, ask me whether to update or overwrite it first. After installation, remind me to restart or refresh Codex so the skill list is reloaded.
```

If your agent does not have local filesystem or terminal access, use Method 2.

### Method 2: Manual Install

Clone this repository into your local Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/juliaError/Econ-thesis-idea.git ~/.codex/skills/thesis-idea
```

After installation, restart or refresh Codex so the skill list is reloaded.

## 使用 🛠️

你不需要一开始就写完整 prompt。可以直接发一个研究直觉、初步 idea、导师方向、政策、变量、现象，甚至一句很模糊的话。

### 基础版

```text
用 thesis-idea 帮我打磨这个想法：
我想研究超级大型公司跟国家经济发展有什么关系。
```

```text
用 thesis-idea 帮我看看导师给的课题：
导师让我研究数字化与共同富裕的课题。
```

### 高级版

如果你已经知道自己想要更完整的诊断，可以用下面这种写法：

```text
用 thesis-idea 作为我的毕业论文 idea 打磨器。
我有一个关于[主题]的经济学毕业论文 idea。
请判断它是否可行，检查数据路径，压力测试识别思路，并把它整理成论文蓝图。

如果这个题目属于数字化、共同富裕、数字金融、绿色金融、ESG、
智慧城市、低碳城市、高质量发展等拥挤方向，
请先查中英文接近文献，判断是否已经做无可做；
如果空间不足，请直接建议我换题、暂缓或大幅转向。

如果原题太拥挤但我仍想保留部分兴趣，
请从原题的 X、Y、机制和反向因果出发，
按横向、纵向、逆向三个维度生发相邻方向，并筛选哪些值得继续验证。
```

## Use 🛠️

You do not need a full prompt at the beginning. You can send a rough intuition, early idea, advisor direction, policy, variable, phenomenon, or even a vague sentence.

### Basic Version

```text
Use thesis-idea to polish this idea:
I want to study how super-large firms relate to national economic development.
```

```text
Use thesis-idea to check this advisor-given topic:
My advisor asked me to study digitalization and common prosperity.
```

### Advanced Version

If you already want a fuller diagnosis, use a prompt like this:

```text
Use thesis-idea as my Thesis Idea Builder.
I have an economics thesis idea about [topic].
Please diagnose whether it is feasible, check the data path,
pressure-test identification, and turn it into a thesis blueprint.

If this is a crowded topic such as digitalization, common prosperity,
digital finance, green finance, ESG, smart cities, low-carbon cities,
or high-quality development, first inspect close Chinese and English literature
and tell me whether prior papers already exhaust the idea.
If the remaining space is too thin, recommend that I change, park,
or substantially pivot the topic.

If the exact topic is too crowded but I still want to preserve part of the interest,
branch from the original X, Y, mechanisms, and reverse causal direction
through horizontal, vertical, and reverse searches,
then screen which adjacent directions deserve validation.
```

## 数据可行性规则 🔎

对经验研究来说，题目有意思还不够。除非数据路径现实可行，否则这个 skill 不应把 idea 判定为可以推进。先过数据门槛，再谈识别和论文蓝图。

可接受的数据路径包括：相关既有论文、公开数据库、用户已有本地材料、导师组或课题组权限、学院或图书馆权限、论文复现材料、数据管理方、合规第三方数据服务，或其他授权渠道。

对中国相关题目，英文中国研究和中文经济学或管理学期刊文章是重要数据先例。小红书、微信公众号、Xiaohongshu、WeChat public accounts 等平台只能用于搜索或发帖求助数据来源线索。平台回复只是线索，不是已经验证的数据。使用任何由此发现的数据前，必须核查来源、授权、隐私风险、引用规则、可复现性，以及能否合法、合规、合伦理地用于毕业论文。

## Data Feasibility Rule 🔎

For empirical ideas, intellectual excitement is not enough. The skill should not mark an idea ready unless the data path is realistic. Data feasibility comes before identification claims and thesis blueprints.

Acceptable data paths include relevant prior papers, public databases, user-owned local materials, advisor or research-team access, school or library access, replication archives, data owners, compliant third-party services, or other authorized channels.

For China-related topics, English-language China papers and Chinese economics or management journal articles are important data precedents. 小红书, 微信公众号, Xiaohongshu, WeChat public accounts, and similar platforms may be used only to search or ask for data-source leads. Platform replies are leads, not validated data. Before using any discovered dataset, verify provenance, authorization, privacy risk, citation rules, reproducibility, and legal or ethical fit for a thesis.

## 默认输出 📦

对于单个 idea，默认输出包括：

- 更清楚的一句话研究问题；
- 论文类型和可行性判断；
- 五维评分和最需要补强的地方；
- 是否继续打磨，以及下一轮最该做什么；
- 文献拥挤度、近似文献和答辩风险；
- 可行的数据、测度、模型或理论路径；
- 如有需要，给出跨领域迁移路线及其风险；
- 识别、测度、理论或结构/量化方案及主要威胁；
- 现在不能声称的内容；
- 如果已经建议冻结或可以推进，再输出第一周验证计划、导师 memo、论文蓝图，以及升级、降级或转向建议。

## Output Contract 📦

For a single idea, the default output includes:

- a clearer one-sentence research question;
- paper type and feasibility judgment;
- five-dimensional scores and the weakest parts to improve;
- whether to keep polishing and what the next iteration should do;
- literature crowding, close papers, and defense risks;
- feasible data, measurement, model, or theory paths;
- when useful, cross-field transfer routes and their risks;
- identification, measurement, theory, or structural/quantitative options and major threats;
- claims the user should not make yet;
- if the idea is ready to freeze or proceed, first-week validation plan, advisor memo, thesis blueprint, and upgrade/downgrade/pivot suggestions.

## 边界 ⚠️

这个 skill 用于研究设计辅助。它不能替代导师判断、文献综述、来源核查、数据权限检查、实证执行，或学生自己的学术责任。它不得编造论文、引用、政策、数据、系数、制度事实、变量或结果。

## Boundaries ⚠️

This skill is for research design support. It does not replace advisor judgment, literature review, source verification, data access checks, empirical execution, or the student's own academic responsibility. It must not fabricate papers, citations, policies, data, coefficients, institutional facts, variables, or results.

## 致谢与引用 📚

本项目感谢 IRIS 论文带来的方法启发。IRIS 将研究 idea 的生成、评估和改进组织成可交互、可迭代、可比较的过程；这一思路启发了本项目在“毕业论文 idea 打磨器”中设计多维评分、连续 refinement 和小规模 MCTS/UCT 分支比较。

如果你在研究或开发中引用本项目中的 IRIS-style idea tree，请同时引用 IRIS 论文：Garikaparthi, Aniketh, Manasi Patwardhan, Lovekesh Vig, and Arman Cohan. 2025. “IRIS: Interactive Research Ideation System for Accelerating Scientific Discovery.” ACL 2025 System Demonstrations. DOI: `10.18653/v1/2025.acl-demo.57`。

为清楚说明引用边界：本项目是在经济学毕业论文选题与研究设计场景中的重新设计，没有复用 IRIS 的源码路径、源码映射、源码、prompt、UI、README 文案或运行说明，也不是 IRIS 的复刻版。

## Acknowledgements And Citation 📚

This project gratefully acknowledges the IRIS paper as an important source of methodological inspiration. IRIS shows how research ideation can be organized as an interactive, iterative, and comparable process; that helped shape this project's use of multi-dimensional scoring, iterative refinement, and small MCTS/UCT branch comparison for economics thesis topic design.

If you cite or build on the IRIS-style idea tree in this project, please also cite the IRIS paper: Garikaparthi, Aniketh, Manasi Patwardhan, Lovekesh Vig, and Arman Cohan. 2025. “IRIS: Interactive Research Ideation System for Accelerating Scientific Discovery.” ACL 2025 System Demonstrations. DOI: `10.18653/v1/2025.acl-demo.57`.

For clarity about citation boundaries: this repository is a redesign for economics thesis topic selection and research design. It does not reuse IRIS source paths, source mappings, source code, prompts, UI, README wording, or setup instructions, and it is not a reimplementation of IRIS.

## 许可 📄

本仓库原创内容采用 Creative Commons Attribution-NonCommercial 4.0 International（CC BY-NC 4.0）许可。商业使用需要取得仓库维护者的单独书面许可。详情见 `LICENSE`。

## License 📄

Original content in this repository is licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Commercial use requires separate written permission from the repository maintainer. See `LICENSE` for details.

## 给开发者看的内容 🧩

以下内容主要给想理解、维护或二次开发这个 skill 的开发者看。普通使用者可以跳过。

## For Developers 🧩

The following sections are mainly for people who want to understand, maintain, or extend this skill. Regular users can skip them.

### 仓库结构 🗂️

这个仓库只包含 `thesis-idea` standalone skill 和公开说明文件。

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── 00_master_router.md
    ├── 01_modes_and_inputs.md
    ├── 02_verdict_rules.md
    ├── 03_data_feasibility.md
    ├── 04_identification_diagnostics.md
    ├── 05_output_templates.md
    ├── 06_research_design_patterns.md
    ├── 07_literature_crowding_gate.md
    ├── 08_crowded_topic_pivot_lab.md
    ├── 09_selected_topic_refinement.md
    ├── 10_iris_ideation_loop.md
    ├── 11_paper_type_gates.md
    └── 12_cognitive_transfer_search.md
```

### Repository Structure 🗂️

This repository contains only the standalone `thesis-idea` skill and public-facing documentation.

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── 00_master_router.md
    ├── 01_modes_and_inputs.md
    ├── 02_verdict_rules.md
    ├── 03_data_feasibility.md
    ├── 04_identification_diagnostics.md
    ├── 05_output_templates.md
    ├── 06_research_design_patterns.md
    ├── 07_literature_crowding_gate.md
    ├── 08_crowded_topic_pivot_lab.md
    ├── 09_selected_topic_refinement.md
    ├── 10_iris_ideation_loop.md
    ├── 11_paper_type_gates.md
    └── 12_cognitive_transfer_search.md
```

### 工作流程 🧭

1. 先用总控路由记录当前阶段、活跃候选题、备选候选题、阻塞风险和下一步模块。
2. 接受用户的原始兴趣、导师方向、政策、变量、现象或口语化直觉，保留原话并生成临时 idea card。
3. 对每个 idea、候选分支和迭代版本做五维评分：novelty、clarity、feasibility、effectiveness、impact，并根据最弱项决定下一步。
4. 当存在多个可能方向时，运行小规模 IRIS-style MCTS/UCT 分支比较：生成 research brief，先评分每个方向，再执行 review/refine/refresh/retrieve 等动作；内部可记录 visits/value，但对外只总结为“小规模分支比较”和推荐路线。
5. 如果只有一个方向且明显红灯或明显可冻结，可以不跑 MCTS，但要说明原因，并询问是否调用三维生发模块寻找相邻新方向。
   认知迁移搜索是增强模块：当用户要求跨领域迁移，或新意、机制、理论、模型、测度路径卡住时，先把 idea 抽象成问题结构卡片，再比较其他学科的工具、结构或模型思路，并用结构、操作和经济学贡献 gate 过滤。
6. 判断用户阶段、截止时间、数据权限、方法水平、导师偏好和目标层级。
7. 对硕士生和拥挤题目先执行文献拥挤度 gate：查中英文接近文献，判断是否已有相同 X、Y、数据、方法和机制。
8. 若原题 `high/saturated` 但用户仍想保留部分兴趣，进入拥挤题目生发模块：横向拆 X/Y、纵向追机制链、逆向问“什么导致 X/Y”。生发阶段用“可读研究问题 + 关键对象”，不要过度压缩成难懂的一句话。
9. 对多个可行分支建立候选题池，让用户选择一个主线，同时保留其他方向作为备选。
10. 用户选中一个候选题后，冻结该分支，不再继续泛化生发。
11. 将选中候选题改写成一句可检验的经济学研究问题，并压成最小可行设计。
12. 按论文类型执行门槛：经验因果看数据与识别；测度/事实看概念、测量、覆盖与验证；理论看主体、约束、时序、均衡和命题；结构/量化看模型-数据映射、矩、估计/校准、拟合和反事实。
13. 对使用数据的 idea，区分 agent 证据核查和用户权限确认；先寻找可用变异、测度验证、理论机制或模型矩，再讨论 DID、IV、RDD、固定效应、结构估计、校准或仿真。
14. 同时输出可行性判定和行动决策：`green/yellow/red` 加 `proceed/pivot/park/kill/upgrade/downgrade`。
15. 立即用自然语言给出“是否继续打磨”，判断是否必须继续、可以冻结、可选继续升级，或应该暂停/更换路线。
16. 只有在建议冻结或可以推进时，才产出类型匹配的论文蓝图和第一周验证计划；若建议继续打磨，则停在下一轮选项。

### Core Workflow 🧭

1. Use the master router to track the current stage, active candidate, backup candidates, blocking risk, and next module.
2. Accept the user's raw interest, advisor direction, policy, variable, phenomenon, or colloquial intuition; preserve the wording and create a temporary idea card.
3. Score every idea, candidate branch, and iteration version on novelty, clarity, feasibility, effectiveness, and impact, then route by the weakest dimensions.
4. When several possible directions exist, run a small IRIS-style MCTS/UCT branch comparison: generate research briefs, score every branch before advancing it, and apply review/refine/refresh/retrieve actions. Visits/value may be tracked internally, but user-facing output should summarize this as a small branch comparison and recommendation.
5. If there is only one direction and it is clearly blocked or clearly ready to freeze, MCTS may be skipped, but the output must explain why and ask whether to call the three-dimensional branching module for adjacent alternatives.
   Cognitive Transfer Search is an enhancement module: when the user asks for cross-field transfer, or novelty, mechanism, theory, model, or measurement routes get stuck, abstract the idea into a problem structure card, compare tools, structures, or model ideas from other fields, and filter them through structure, operation, and economics-contribution gates.
6. Classify the user's stage, deadline, data access, method level, advisor preference, and ambition level.
7. For master's students and crowded topics, run a literature crowding gate first: inspect close Chinese and English papers and check whether the same X, Y, data, method, and mechanism already exist.
8. If the original idea is `high/saturated` but the user wants to preserve part of the interest, run the crowded topic pivot lab: horizontal X/Y splitting, vertical mechanism-chain search, and reverse-causality search. In this stage, use readable research questions plus key objects instead of over-compressed one-sentence questions.
9. Build a candidate bank for viable branches, ask the user to choose one primary branch, and keep other directions as backups.
10. After the user selects one candidate, freeze that branch instead of continuing broad ideation.
11. Rewrite the selected candidate into a testable economics question and compress it into a minimum viable design.
12. Apply type-specific gates: empirical causal ideas need data and identification; measurement/facts ideas need concept, measurement, coverage, and validation; theory ideas need agents, constraints, timing, equilibrium, and propositions; structural/quantitative ideas need model-data mapping, moments, estimation/calibration, fit, and counterfactuals.
13. For data-using ideas, separate agent-side evidence checks from user-side access confirmation; search for usable variation, measurement validation, theory mechanism, or model moments before naming DID, IV, RDD, fixed effects, structural estimation, calibration, or simulation.
14. Give both a feasibility verdict and an action decision: `green/yellow/red` plus `proceed/pivot/park/kill/upgrade/downgrade`.
15. Immediately give a natural-language stop-or-continue judgment: continue polishing, freeze the current version, proceed while optionally upgrading, or pause/change route.
16. Produce a type-matched thesis blueprint and first-week validation plan only when the idea is ready to freeze or proceed; if it still needs polishing, stop with next-iteration options.

### 开发说明 🤖

本项目由仓库维护者发起、设计和维护。Codex 参与了公开 skill 的结构化整理、规则拆分、README 与网页版 prompt 草拟、验证流程和本地同步。关键取舍、研究标准、公开边界和最终维护责任仍由项目维护者承担。这个说明只是透明记录 AI 辅助开发的作用，不表示把学术判断、数据核查或论文责任外包给 AI。

### Development Note 🤖

This project was initiated, designed, and maintained by the repository maintainer. Codex assisted with structuring the public skill, splitting rules into references, drafting the README and web AI prompt, validation workflow, and local synchronization. Key design choices, research standards, public boundaries, and final maintenance responsibility remain with the maintainer. This note records AI-assisted development transparently; it does not outsource academic judgment, data verification, or thesis responsibility to AI.
