# FT50 实证论文学术写作技能

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

面向 OpenCode / Claude Code / Codex 等AI编程智能体的FT50实证论文写作技能——覆盖从研究问题提出、理论构建、识别策略、实证结果、稳健性检验、机制分析到完整初稿的全流程。

覆盖金融时报50本顶级期刊（FT50），横跨六大领域：**会计学、金融学、管理学、市场营销学、运营与信息系统、经济学**。

## 技能功能

引导AI智能体完成FT50实证论文的**0到初稿五阶段流程**：

| 阶段 | 产出 | 关键交付物 |
|------|------|-----------|
| **阶段1**：研究问题与选题定位 | Gap table、期刊推荐、贡献陈述 | 投哪本期刊 + 创新点是什么 |
| **阶段2**：理论与假设 | 理论框架、概念模型、可检验假设 | §2 理论与假设初稿 |
| **阶段3**：识别策略与研究设计 | DID/RDD/IV/RCT/Synthetic Control、数据描述 | §3-4 研究设计初稿 |
| **阶段4**：结果与稳健性 | 主要结果、稳健性金字塔、Oster bounds、机制分析 | §5-6 结果与稳健性初稿 |
| **阶段5**：写作组装 | Introduction、文献综述、讨论、政策启示、摘要 | 完整初稿 |

该技能是**领域特化**的：内置了FT50实证研究特有的方法论规范——如识别策略设计、稳健性金字塔、Oster bounds处理不可观测选择性偏误、机制分析框架，以及六大管理学科各期刊的审稿人期望，这些是通用写作技能（如`scientific-writing`）不覆盖的。

### 核心功能

- **识别策略**：DID（交错处理、连续处理）、RDD（精确、模糊）、IV（2SLS、Bartik、shift-share）、RCT、Synthetic Control、事件研究法
- **稳健性金字塔**：系数稳定性图、Oster bounds、替代模型设定、证伪检验、样本限制
- **机制分析**：中介效应 vs. 调节效应、截面异质性分析、结构化估计
- **分学科指导**：针对会计学（TAR, JAE, JAR, CAR, RAST）、金融学（JF, JFE, RFS, JFQA, RF）、管理学（AMJ, AMR, ASQ, OS, SMJ, JOM, JMS, JIBS）、市场营销（MktSci, JMR, JM, JCR）、运营与信息系统（MS, OR, MSOM, ISR）、经济学（AER, ECMA, JPE, QJE, REStud）的差异化写作规范

---

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/liyuanbo1024/ft50-empirical-writing.git
```

### 2. 安装到AI智能体

| 智能体 | 安装命令 |
|--------|---------|
| **OpenCode** | `cp -r ft50-empirical-writing ~/.config/opencode/skills/` |
| **Claude Code** | `cp -r ft50-empirical-writing ~/.claude/skills/` |
| **Codex** | `cp -r ft50-empirical-writing ~/.agents/skills/` |
| **Cursor** | `cp -r ft50-empirical-writing ~/.cursor/skills/` |
| **Windsurf** | `cp -r ft50-empirical-writing ~/.windsurf/skills/` |

Windows PowerShell 用户将 `cp -r` 替换为 `Copy-Item -Recurse`，将 `~/` 替换为 `$env:USERPROFILE\`。

安装后通过自然语言触发，例如：

- "我要写一篇用DID分析最低工资就业效应的论文，帮我定位选题"
- "理论框架搭好了，帮我设计交错DID的识别策略并处理Bacon分解"
- "带我走一遍完整的FT50实证论文写作流程"

---

## 使用方式

### 管道模式

```
"带我走一遍完整的FT50实证写作流程。我的选题是……"
```

智能体会加载技能，评估当前阶段，从阶段1推进到阶段5，每个阶段完成后请求确认。

### 阶段跳转

| 触发语 | 跳转阶段 |
|--------|---------|
| "我有一个研究想法……" | 阶段1：选题定位 |
| "帮我构建理论框架" | 阶段2：理论与假设 |
| "帮我设计识别策略" | 阶段3：识别策略与研究设计 |
| "帮我分析结果/构建稳健性检验" | 阶段4：结果与稳健性 |
| "帮我写完整论文" | 阶段5：写作组装 |

### 参考模式

```
"JF对因果识别的审稿要求是什么？"
"如何实现Oster bounds来处理不可观测选择性偏误？"
"管理学顶刊的标准机制分析框架是什么？"
```

---

## 文件结构

```
ft50-empirical-writing/
├── SKILL.md                              主技能文件
├── references/
│   ├── journal-characteristics.md        50本FT50期刊详细特征（按学科）
│   ├── identification-strategies.md      DID/RDD/IV/RCT/Synthetic Control/事件研究
│   ├── theory-hypothesis-guide.md        理论框架、假设构建、概念模型
│   ├── robustness-oster-guide.md         稳健性金字塔、Oster bounds、证伪检验
│   ├── mechanism-analysis.md            中介、调节、异质性、结构化分析
│   ├── data-results-presentation.md      描述性统计、结果表格、可视化
│   ├── reviewer-expectations.md          各学科FT50审稿人期望
│   └── writing-patterns.md               已发表FT50论文的可复用写作模式
├── assets/
│   └── regression-table-template.md      标准回归表格规范
├── examples/
│   ├── manuscript_template.tex           期刊格式LaTeX模板
│   └── empirical_analysis.py             DID + Oster bounds分析模板
├── README.md                             英文说明
├── README.zh-CN.md                       中文说明（本文件）
├── README.ja.md                          日文说明
├── README.ko.md                          韩文说明
└── LICENSE                               MIT许可证
```

---

## 覆盖期刊

### 会计学

| 期刊 | 缩写 |
|------|------|
| The Accounting Review | TAR |
| Journal of Accounting and Economics | JAE |
| Journal of Accounting Research | JAR |
| Contemporary Accounting Research | CAR |
| Review of Accounting Studies | RAST |

### 金融学

| 期刊 | 缩写 |
|------|------|
| Journal of Finance | JF |
| Journal of Financial Economics | JFE |
| Review of Financial Studies | RFS |
| Journal of Financial and Quantitative Analysis | JFQA |
| Review of Finance | RF |

### 管理学

| 期刊 | 缩写 |
|------|------|
| Academy of Management Journal | AMJ |
| Academy of Management Review | AMR |
| Administrative Science Quarterly | ASQ |
| Organization Science | OS |
| Strategic Management Journal | SMJ |
| Journal of Management | JOM |
| Journal of Management Studies | JMS |
| Journal of International Business Studies | JIBS |

### 市场营销学

| 期刊 | 缩写 |
|------|------|
| Marketing Science | MktSci |
| Journal of Marketing Research | JMR |
| Journal of Marketing | JM |
| Journal of Consumer Research | JCR |

### 运营与信息系统

| 期刊 | 缩写 |
|------|------|
| Management Science | MS |
| Operations Research | OR |
| Manufacturing & Service Operations Management | MSOM |
| Information Systems Research | ISR |

### 经济学

| 期刊 | 缩写 |
|------|------|
| American Economic Review | AER |
| Econometrica | ECMA |
| Journal of Political Economy | JPE |
| Quarterly Journal of Economics | QJE |
| Review of Economic Studies | REStud |

---

## 定制化

### 添加新期刊

编辑 `references/journal-characteristics.md`，按模板格式新增期刊条目。

### 调整实证分析默认值

修改 `examples/empirical_analysis.py` 中的配置参数：

```python
@dataclass
class EmpiricalConfig:
    cluster_se: str = "state"   # 聚类标准误层级
    fe_absorb: str = "firm"     # 固定效应吸收变量
    oster_delta: float = 1.0    # Oster delta 参数
    # ...
```

### 创建新论文模板

1. 复制 `examples/manuscript_template.tex` 作为起点
2. 替换标题、作者和摘要
3. 填入理论、识别、结果与稳健性内容
4. 使用 `xelatex manuscript.tex` 编译（需编译两次）

---

## 示例

`examples/` 目录包含两个参考文件：

1. **`manuscript_template.tex`**：期刊格式LaTeX模板，含实证论文的标准占位章节（Introduction → Theory → Identification → Results → Robustness → Mechanism → Implications）。

2. **`empirical_analysis.py`**：可运行的Python实证分析模板，展示交错DID估计、事件研究图、Bacon分解、Oster bounds和稳健性检验的规范写法。使用合成数据集，可直接运行。

---

## 参与贡献

欢迎贡献。亟需帮助的方向：

- 尚未覆盖的期刊特征和审稿期望
- 从已发表FT50论文中提炼的额外写作模式
- 各期刊的官方LaTeX样式文件
- DID/RDD/IV/RCT/Synthetic Control的完整分析示例
- 更多语言的写作规范

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)。

---

## 致谢

基于 [agentskills.io](https://agentskills.io) 规范和 [OpenCode](https://github.com/anomalyco/opencode) 的技能创作方法论构建。FT50领域知识来源于金融时报50强期刊的编辑声明和实证管理研究社区的方法论指南。
