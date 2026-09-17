# 营销科学学术写作技能

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

面向 OpenCode / Claude Code / Codex 等AI编程智能体的营销科学学术写作技能——覆盖从选题定位、消费者效用建模、识别策略设计、结构估计、反事实模拟到完整初稿的全流程。

覆盖8本营销科学旗舰期刊：UTD-24顶刊 **Marketing Science, JMR, JM, JCR**，以及次顶刊 **JAMS, IJRM, QME, Marketing Letters**。

## 技能功能

引导AI智能体完成营销科学论文的**0到初稿五阶段流程**：

| 阶段 | 产出 | 关键交付物 |
|------|------|-----------|
| **阶段1**：选题定位 | Gap table、期刊推荐、贡献陈述 | 投哪本期刊 + 创新点是什么 |
| **阶段2**：消费者效用模型 | 记法系统、效用设定、需求推导 | §3 模型章节初稿 |
| **阶段3**：识别与估计 | 识别策略（DID/RDD/IV）、估计方法、设定检验 | §4 方法章节初稿 |
| **阶段4**：反事实与实验 | 反事实设计、联合分析、田野/实验室实验 | §5-6 结果章节初稿 |
| **阶段5**：写作组装 | Introduction、文献综述、营销启示、摘要 | 完整初稿 |

该技能是**领域特化**的：内置了营销科学特有的方法论规范——包括消费者效用模型结构、识别策略论证（DID、RDD、IV、断点回归设计）、结构估计方法（BLP、GMM）、联合分析设计、反事实模拟工作流，以及各期刊审稿人期望等，这些是通用写作技能不覆盖的。

---

## 四大方法论支柱

### 1. 结构模型 (BLP)

消费者效用微观基础 → 随机系数Logit聚合需求 → 供给端定价博弈 → BLP/GMM估计。技能引导你完成效用函数设定（内生价格、外生产品特征、随机系数）、矩条件构造（需求侧矩、供给侧矩、微观矩），以及最优权重矩阵下的GMM目标函数。

### 2. 因果推断 (DID / RDD / IV)

自然实验、准实验设计和工具变量策略——用于识别营销中的因果效应。覆盖渐进采纳的DID、营销场景中的断点回归设计（如政策阈值、排名截断），以及IV构造方法（Hausman工具变量、BLP工具变量、成本转移变量）。

### 3. 田野实验

营销中的随机田野实验设计与分析——数字A/B测试、线下门店实验、定价实验。包括统计功效分析、随机化检验、异质性处理效应估计，以及与结构模型的衔接。

### 4. 反事实模拟

在结构模型估计后：预测反事实情景下的结果（并购模拟、价格歧视禁令、新产品引入、广告上限）。技能引导你在反事实世界中计算均衡，进行福利分析（消费者剩余、生产者利润、总福利），并将反事实结果与营销管理启示相衔接。

---

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/liyuanbo1024/marketing-science-writing.git
```

### 2. 安装到AI智能体

| 智能体 | 安装命令 |
|--------|---------|
| **OpenCode** | `cp -r marketing-science-writing ~/.config/opencode/skills/` |
| **Claude Code** | `cp -r marketing-science-writing ~/.claude/skills/` |
| **Codex** | `cp -r marketing-science-writing ~/.agents/skills/` |
| **Cursor** | `cp -r marketing-science-writing ~/.cursor/skills/` |
| **Windsurf** | `cp -r marketing-science-writing ~/.windsurf/skills/` |

Windows PowerShell 用户将 `cp -r` 替换为 `Copy-Item -Recurse`，将 `~/` 替换为 `$env:USERPROFILE\`。

安装后通过自然语言触发，例如：
- "我要写一篇关于智能手机市场BLP需求估计的论文，帮我定位选题"
- "消费者效用模型搭好了，帮我设计工具变量的识别策略"
- "带我走一遍完整的营销科学论文写作流程"

---

## 使用方式

### 管道模式

```
"带我走一遍完整的营销科学写作流程。我的选题是……"
```

智能体会加载技能，评估当前阶段，从阶段1推进到阶段5，每个阶段完成后请求确认。

### 阶段跳转

| 触发语 | 跳转阶段 |
|--------|---------|
| "我有一个研究想法……" | 阶段1：选题定位 |
| "帮我设计消费者效用模型" | 阶段2：效用模型 |
| "帮我设计识别策略" | 阶段3：识别与估计 |
| "帮我设计反事实模拟" | 阶段4：反事实与实验 |
| "帮我写完整论文" | 阶段5：写作组装 |

### 参考模式

```
"Marketing Science对识别策略的审稿要求是什么？"
"JMR的联合分析应该怎么设计？"
"差异化产品市场的标准效用函数设定是什么样的？"
```

---

## 文件结构

```
marketing-science-writing/
├── SKILL.md                              主技能文件
├── references/
│   ├── journal-characteristics.md        8本期刊详细特征
│   ├── modeling-conventions.md           效用模型·需求系统·选择模型
│   ├── identification-guide.md           DID·RDD·IV·结构识别
│   ├── estimation-guide.md               BLP·GMM·MLE·贝叶斯估计
│   ├── counterfactual-guide.md           反事实模拟设计
│   ├── conjoint-analysis.md              联合分析·支付意愿估计
│   ├── field-experiments.md              田野实验设计与分析
│   ├── marketing-implications.md         营销启示写作框架
│   ├── reviewer-expectations.md          审稿心理·Rebuttal策略
│   └── writing-patterns.md               可复用写作模式
├── assets/
│   └── demand-model-reference.md         通用需求模型结构参考
├── examples/
│   ├── manuscript_template.tex           INFORMS风格LaTeX模板
│   └── blp_estimation_example.py         BLP估计Python模板
├── README.md / README.zh-CN.md / .ja.md / .ko.md
└── LICENSE                               MIT许可证
```

---

## 覆盖期刊

### Tier 1 (UTD-24)

| 期刊 | 核心定位 |
|------|---------|
| **Marketing Science** | 量化营销、结构模型、分析严谨性 |
| **Journal of Marketing Research (JMR)** | 实证营销、实验、行为研究 |
| **Journal of Marketing (JM)** | 广泛营销战略、实质性贡献 |
| **Journal of Consumer Research (JCR)** | 消费者行为、心理学基础 |

### Tier 2（强领域期刊）

| 期刊 | 核心定位 |
|------|---------|
| **JAMS** | 广泛营销科学、概念与实证 |
| **IJRM** | 欧洲营销研究、多元方法论 |
| **QME** | 结构计量、IO导向营销 |
| **Marketing Letters** | 简洁有力、实证与方法论前沿 |

---

## 常见拒稿原因

| 原因 | 频率 | 防范措施 |
|------|------|---------|
| 识别策略薄弱 | 极高 | 明确论证工具变量或自然实验的有效性 |
| 未处理内生性问题 | 极高 | 需求估计中必须处理价格内生性 |
| 文献贡献不足 | 高 | Introduction中列出明确Gap Table |
| 反事实情景缺乏政策相关性 | 高 | 将反事实锚定于真实营销决策 |
| 营销启示过于空泛 | 高 | 具体、编号、可追溯至结构估计结果 |
| 样本/数据不足以支撑方法 | 中 | 方法复杂度需与数据丰富度匹配 |

---

## 定制化

### 添加新期刊

编辑 `references/journal-characteristics.md`，按模板格式新增期刊条目。

### 调整BLP估计参数

修改 `examples/blp_estimation_example.py` 中的可配置参数。

---

## 参与贡献

欢迎贡献。亟需帮助的方向：
- 尚未覆盖的期刊特征和审稿期望
- 从已发表论文中提炼的额外写作模式
- 各期刊的官方LaTeX样式文件
- 经典营销论文的复现代码（BLP、Petrin等）

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)。

---

## 致谢

基于 [agentskills.io](https://agentskills.io) 规范和 [OpenCode](https://github.com/anomalyco/opencode) 的技能创作方法论构建。营销科学领域知识来源于INFORMS（Marketing Science）期刊编辑声明，以及量化营销社区的出版标准，包括 BLP (1995)、Petrin (2002) 及更广泛的结构IO-营销文献。
