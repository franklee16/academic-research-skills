# Research Defense Radar / 研究防御雷达

Research Defense Radar is an English–Chinese Agent Skill for researchers who need to protect and refine the contribution space of an active project—not merely collect papers around a topic. It turns a research question, proposal, draft, revision, or known comparison paper into a structured research fingerprint; searches for work that could overlap with the project's actual claims; grades the available evidence; and converts what it finds into concrete decisions about positioning, design, validation, and monitoring.

研究防御雷达是一个面向进行中研究项目的中英双语 Agent Skill。它的目标不是简单收集“主题相关”的论文，而是帮助研究者持续守住并改进项目的贡献空间。它可以从研究问题、proposal、论文草稿、修改稿或一篇已知对标论文出发，建立结构化的项目指纹，寻找真正可能与核心贡献重叠的研究，区分证据强弱，并把发现转化为关于定位、设计、验证和后续监控的具体行动。

> Project materials → research fingerprint → contribution-space search → evidence-graded competitors → novelty delta → recommended actions → persistent monitoring
>
> 项目材料 → 研究指纹 → 贡献空间检索 → 分级竞争证据 → novelty 变化 → 行动建议 → 持续监控

## Why it exists / 为什么需要它

A project's novelty is a moving target. New working papers appear, preprints become journal articles, abstracts understate important design details, and the project itself changes after each revision. A conventional literature search or weekly alert can surface relevant titles, but it usually does not answer the questions that matter most:

- Does this paper weaken one of our specific contribution claims?
- Is the apparent overlap based only on metadata, or is it confirmed in the full text?
- Is this a genuinely new competitor or another version of a paper already reviewed?
- Does a new method, dataset, or identification strategy strengthen the project even when the paper is not a direct competitor?
- What changed since the last scan, and what should the research team do next?

项目的 novelty 不是静态结论。新的 working paper 会持续出现，preprint 会演化为期刊版本，摘要常常省略关键设计细节，而项目自身也会在每轮修改后改变。普通文献检索或 weekly alert 能找到“相关标题”，却往往不能回答真正影响项目决策的问题：某篇论文是否削弱了具体贡献主张？这种重叠只是元数据层面的猜测，还是已由全文确认？它是新的竞争者，还是已审阅论文的另一个版本？非直接竞争论文中的方法、数据或识别策略能否反过来增强项目？与上次扫描相比究竟发生了什么变化，团队下一步应该做什么？

## Core capabilities / 核心功能

- **Build a research fingerprint / 建立研究指纹** — Extract the project's question, mechanism, setting, data, identification strategy, method, outcome, and claimed contributions instead of relying on a short keyword list.
- **Compare a known paper with the project / 对比已知论文与项目** — Separate genuine contribution overlap from superficial topical similarity, identify what remains differentiated, and propose bounded positioning language.
- **Create a baseline defense map / 建立基线防御地图** — Organize direct competitors, adjacent work, transferable methods, useful data, and unresolved uncertainties into an auditable starting state.
- **Refresh novelty after revisions / 修改后重评 novelty** — Recompute the project's fingerprint when its question, sample, mechanism, method, or contribution claims change; do not reuse a stale novelty assessment.
- **Discover transferable methods and data / 发现可迁移方法与数据** — Surface techniques, datasets, validation tests, or measurements that can improve the project even when the source is not a direct competitor.
- **Monitor meaningful deltas / 监控有意义的变化** — Report newly discovered or materially updated evidence, explain why it changes the threat or opportunity map, and recommend the next action instead of repeating a weekly bibliography.
- **Maintain durable research memory / 维护持久研究记忆** — Track DOI and version lineage, aliases, evidence grade, review status, query coverage, and unresolved follow-ups across runs.
- **Protect public-time priority / 保护公开时点 priority** — When the author's WP is already public, distinguish pre-disclosure prior work from later convergence so post-WP papers do not retroactively erase the project's novelty at disclosure.

## Design innovations / 设计创新

The innovation here is the workflow design and research memory—not a claim that no prior literature-search system has individual features of this kind.

这里所说的创新，指工作流与研究记忆的组合设计；它并不声称其他文献检索系统从未提供过其中某个单项功能。

1. **Project-centric rather than query-centric / 以项目而非关键词为中心.** The unit of analysis is a versioned research project with explicit contribution claims. Queries are generated from multiple dimensions of that project and are regenerated when the project changes.
2. **Contribution-space reasoning / 面向贡献空间推理.** Results are compared on question, mechanism, setting, data, identification, method, outcome, and claim—not ranked only by title, abstract, or semantic similarity.
3. **Evidence-calibrated judgments / 证据校准判断.** Every material assessment records whether it rests on metadata, an abstract, or full text, along with confidence and uncertainty. An unsuccessful search is never treated as proof that prior work does not exist.
4. **Version and lineage awareness / 版本与 lineage 感知.** Working papers, conference versions, preprints, and journal articles can be linked as one evolving research object, reducing duplicate alarms while preserving substantive changes.
5. **Delta-first monitoring / 变化优先的监控.** Recurring runs emphasize what is new, what changed, why it matters, and what action follows. This makes the radar different from a generic weekly paper digest.
6. **Threat and opportunity in one map / 同时识别威胁与机会.** The same scan searches for direct novelty threats and for methods, data, measurements, robustness tests, and framing that can strengthen the project.
7. **Privacy-aware search abstraction / 隐私友好的检索抽象.** When necessary, the workflow can generalize sensitive project details into searchable concepts while retaining the dimensions needed to detect contribution overlap.
8. **Bilingual and cross-domain adaptation / 中英双语与跨领域适配.** The canonical workflow is usable in English or Chinese and includes an explicit adaptation layer for field-specific databases, working-paper ecosystems, terminology, and evidence norms.
9. **Public-disclosure-aware novelty / 公开时点感知的 novelty.** A full draft is not treated as proof of publication timing. The workflow verifies or asks for the earliest public WP date, evaluates differentiation against earlier work, and separates later convergence from true pre-emption.

## Intended users and outputs / 适用对象与输出

The Skill is designed for PhD students, job-market candidates, principal investigators, coauthor teams, research assistants, and research organizations working on a live project. It can produce a known-paper comparison, baseline competitor map, novelty-risk register, method/data opportunity list, revision-aware refresh, recurring delta report, search-coverage audit, and a durable machine-readable radar state.

本 Skill 适合博士生、求职论文作者、PI、合作者团队、研究助理和研究机构，用于仍在推进或修改中的具体项目。它可输出已知论文对比、基线竞争地图、novelty 风险清单、方法／数据机会、修改后重评、周期性变化报告、搜索覆盖审计，以及可持续更新的机器可读 radar state。

It is not a substitute for expert judgment, a formal systematic review, or a guarantee of novelty. Its value is a reproducible and cautious decision process: trace the evidence, state uncertainty, preserve history, and make each research-defense recommendation inspectable.

它不能替代领域专家判断、正式系统综述，也不能保证项目具有 novelty。它提供的是一套可复现且审慎的决策过程：保留证据来源，明确不确定性，记录历史变化，并让每一条“研究防御”建议都可以被检查。

## Build an uploadable ZIP / 生成可上传 ZIP

[Download the ready-to-upload ZIP / 下载可直接上传的 ZIP](https://github.com/SuperJayLiu/research-defense-radar/raw/main/packages/research-defense-radar.zip)

From the repository root / 在仓库根目录运行：

```bash
python scripts/package_skill.py
```

Upload `dist/research-defense-radar.zip` through the ChatGPT or Claude Skills interface, subject to product/workspace availability.

根据产品和工作区是否开放自定义 Skills，通过 ChatGPT 或 Claude 的 Skills 界面上传 `dist/research-defense-radar.zip`。

## Local installation / 本地安装

- Codex: copy this directory to `~/.agents/skills/research-defense-radar/`, then invoke `$research-defense-radar`.
- Claude Code: copy it to `~/.claude/skills/research-defense-radar/`, then invoke `/research-defense-radar`.

完整安装、定时任务和云端状态说明见 [`references/INSTALL.md`](references/INSTALL.md) 与 [`references/AUTOMATION.md`](references/AUTOMATION.md)。

## Test / 校验

```bash
python scripts/update_radar_state.py --self-test
python scripts/test_update_radar_state.py
python scripts/package_skill.py --self-test
python scripts/check_distribution.py
```

Runtime scripts use only the Python standard library. / 运行脚本仅依赖 Python 标准库。
