# 牛来 (Niulai) — 顶会论文终稿高杠杆润色与证据守卫 Skill

<div align="center">

[![Skill](https://img.shields.io/badge/Codex%20%7C%20Claude%20Code%20%7C%20Antigravity-Skill-orange?style=flat-square)](https://github.com/handsomeZR-netizen/niulai-paper-polish)
[![Target](https://img.shields.io/badge/Target-Top--Tier%20Paper%20Polish-blue?style=flat-square)](https://github.com/handsomeZR-netizen/niulai-paper-polish)
[![Empirical Basis](https://img.shields.io/badge/Empirical%20Basis-120%20Papers%20%7C%2042K%20Reviews-green?style=flat-square)](https://github.com/handsomeZR-netizen/niulai-paper-polish)
[![Anti-AI Firewall](https://img.shields.io/badge/Anti--AI%20Firewall-KO%205.6%20Sol-red?style=flat-square)](https://github.com/handsomeZR-netizen/niulai-paper-polish)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

<p align="center">
  <b>让每一分真实的科学贡献，都能在审稿人眼中被清晰识别、正确定价与有力捍卫。</b>
</p>

</div>

---

## 故事与叙事：关于「牛来」的思考

在顶级学术会议（ICLR, NeurIPS, ICML, ACL）与顶刊的投稿闭环中，我们经常目睹这样一种令人扼腕的现实：一项扎实、硬核的研究工作，仅仅因为初稿写得过于客气保守、对比基线呈现不够锐利、或者被大模型润色后沾染了一身“AI 机械缠绕感”，便在审稿的第一轮初筛中被无情低估甚至拒稿。

**「牛来 (Niulai)」由此诞生。**

它不是一个泛泛的通用语法润色工具，而是一款**基于大规模同行评审实证数据与大模型底层认知偏置洞察**打造的“审稿人视角终稿高杠杆润色与证据守卫”智能体技能。

---

## 一、我们为什么要这么做？

### 1. 现实演进：AI 审稿人时代已经全面降临
当前，主流大语言模型（GPT-5.6 Sol、Claude Fable 5、Gemini 3.7 Flash、Qwen 4、GLM-5.3、DeepSeek-V4 Pro）已被深度嵌入学术初筛、辅助评审与元评审流程（LLM-as-a-Reviewer）。评审生态正在发生深刻重构。

### 2. 残酷的实证发现：审稿人对修辞存在系统性敏感度
我们在前沿实证研究《*How Can Rhetoric Reward-Hack AI Reviewers? Dissecting Rhetorical Sensitivity in AI-Based Peer Review*》（涵盖 120 篇 ICLR 真实匿名投稿原稿、4,200 篇受控变体、42,000+ 次盲审调用）中发现：
* **致命的“自卑惩罚”**：当作者采用谦逊、保守或过度推脱的语气（Negative Novelty Stance）时，AI 审稿人会误判其科学价值，导致总体评分（OA）暴跌 **-0.73 分**；
* **高杠杆的第一梯队**：在科学实质内容 100% 保持不变的前提下，仅仅通过优化**定量证据呈现 (Evidence Framing)** 与 **创新姿态 (Novelty Stance)**，就能使总体评分获得最高 **+0.93 分**的正向跃迁，弱录取概率提高 **13.0 个百分点**！

### 3. 大模型润色的致命悖论
当我们尝试用通用前沿模型（如 GPT-5.6 Sol）去润色论文时，大模型天然带有一套顽固的“AI 病态特征”：
* 连续嵌套多重“的”字定语从句（“*基于X的Y的Z的模型*”）；
* 滥用套路连接虚词（`进一步`、`由此可见`、`基于此`、`与此同时`）；
* 充斥空洞抽象热词（`机制`、`支撑`、`动态`、`稳健性`、`范式`）；
* 生成自我毁灭式的防御免责（“*本研究基于假数据/模型不可靠/不具备实际意义*”）。

这导致了一个恶性循环：**用带有 AI 机械感的大模型写出来的论文，在 AI 审稿人面前惨遭扣分**。「牛来」就是要打破这一死结。

---

## 二、这么做有什么好处？

### 1. 激活第一梯队高杠杆修辞收益
* **定量证据锐化**：将“取得了较好效果”转化为明确的对比基准、指标差值（$\Delta$）与高信息密度图表 Caption；
* **事实优先的自信姿态**：在实验支撑的边界内，采用坚决、确定的学术直叙，消除怯弱与多重假设从句；
* **清晰的四层分层架构**：将方法论形式化为输入空间、数学变换算子、执行流水线与成对统计验证。

### 2. 彻底洗净 AI 铅华，重塑顶刊力量感
* **严格短句控制**：中文单句平均长度压制在 **15–25 字**（英文 12–18 词），主干显性化，动作先行；
* **击碎多重修饰**：单句严禁连续出现 3 个及以上“的”字修饰；
* **50+ 禁用词库 100% 熔断**：彻底根除套路过渡词与空洞虚词。

### 3. 科学事实 100% 真实不可篡改
* 每一项结论都有证据台账严格核验，绝不凭空捏造实验数据与基准排位，确保学术诚信与保真红线。

---

## 三、为什么不选择其他的一些方法？

| 备选方案 | 为什么我们选择放弃？ | 「牛来」的更优解 |
| :--- | :--- | :--- |
| **通用提示词润色**<br>*(如：“请润色这段话使其更学术”)* | 会无脑堆砌 `robust`、`pivotal`、`moreover` 等虚词与冗长复合句。实证表明，表层语言复杂度对审稿得分收益几乎为 0，甚至因语句晦涩招致扣分。 | **聚焦第一梯队证据框架**：不搞辞藻堆砌，用极简有力的短句直接呈现对比增益。 |
| **多轮递归迭代润色**<br>*(Recursive Polish)* | 论文实证表明，递归多轮修改在第 2 轮之后收益迅速饱和；超过 3 轮会导致模型风格分化加剧、引入幻觉或被严格协议严厉惩罚。 | **单次协调性全文重构**：一次性完成高杠杆修辞注入与证据核验，避免过度修改导致风格失真。 |
| **隐蔽 Prompt 注入与对抗扰动**<br>*(Adversarial Laundering)* | 严重违反学术伦理，且在目前主流会议的多模态 PDF 解析与严格审稿协议下极易被过滤拦截。 | **阳谋式的合规修辞增强**：完全依靠事实与证据的高密度呈现赢得审稿人认可。 |

---

## 四、我们的一些精心小设计

在「牛来」的工程实现中，我们注入了多项细致入微的机制设计：

### 1. 六支柱数学/系统形式化引擎 (Six-Pillar Formalization)
无论输入的原始初稿多么口语化，「牛来」都能将其严谨解构为六大支柱：
1. **数学形式化与问题空间**（输入空间 $\mathcal{X}$、决策空间 $\mathcal{Y}$、映射算子 $\mathcal{T}$ 与目标函数 $\mathcal{L}$）；
2. **模块解耦与分层架构**（数据准备层 $\to$ 核心处理层 $\to$ 校验自愈层 $\to$ 盲审评估层）；
3. **算法伪代码与流程图**（标准 LaTeX `algorithm` 逻辑）；
4. **控制变量与保真约束**（基准排位与数值冻结）；
5. **评测基准与双协议设计**（标准协议 vs 严格协议）；
6. **成对差分与统计显著性检验**（成对差分 $\Delta\mathrm{OA}$ 与 5,000 次 Bootstrap 抽样）。

### 2. Claim–Evidence–Limit Ledger 证据台账
在重构全文时，系统会自动在文末或内部生成主张—证据台账，强制每一个核心论断都具备明确的图表支撑与边界定义，严禁无依据的 Overclaiming。

### 3. Causal-Language Gate 因果语言门控
严格区分“关联观察”与“因果结论”：
* 严禁将语篇级改写夸大为单特征因果（将“修辞决定了评分提升”纠正为“测试版本产生了可测量的成对评分差异”）；
* 严格区分百分比与百分点（区分 13% 与 13 个百分点）。

### 4. 去自黑转化机制 (Anti-Defensive Shield)
大模型在写 Discussion 和局限性时极易自毁免责（“*本研究基于假数据/模型不可靠*”）。「牛来」会将此类自黑套话无损转化为**客观严谨的适用边界界定**与**前瞻技术演进路线**（如多中心跨学科扩展），保持学术自信。

### 5. `latex_guard.py` 自动化 AST 结构守卫
内置独立的 Python 语法树保护脚本，在代码层面 100% 锁定 `\cite{}`、`\label{}`、`\ref{}`、数学公式环境（`align`, `equation`）与 `.bib` 数据库，彻底杜绝编译崩溃。

---

## 五、快速上手与安装

### 1. 在 OpenAI Codex / Codex CLI 中安装
将本仓库克隆至本地并在 `~/.codex/config.toml` 中启用：

```toml
[[skills.config]]
path = 'C:\Users\YourUsername\.codex\skills\niulai\SKILL.md'
enabled = true
```

### 2. 在 Antigravity 中使用
直接将目录放置于 `~/.gemini/config/skills/niulai/` 即可自动识别。

### 3. 典型调用指令

```markdown
请调用 $niulai 对当前论文的 main.tex / draft.md 进行终稿高杠杆润色与证据守卫：
1. 提取六支柱方法论结构；
2. 强化证据呈现框架与自信创新姿态；
3. 严格启动 GPT-5.6 Sol 反 AI 语法防火墙（15–25字短句、禁用词0命中、去自黑免责）；
4. 输出 Claim–Evidence 台账并确保 LaTeX 源码 100% 编译通过。
```

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。
