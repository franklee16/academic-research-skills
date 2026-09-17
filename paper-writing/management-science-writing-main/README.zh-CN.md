# 管理科学与工程学术写作技能

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

面向 OpenCode / Claude Code / Codex 等AI编程智能体的管理科学与工程学术写作技能——覆盖从选题定位、建模推导、数值实验到完整初稿的全流程。

覆盖13本MS&E旗舰期刊：UTD-24顶刊 **MS, OR, MSOM, POM**，以及次顶刊 **TS, TRB, DS, OMEGA, TRE, EJOR, IJPE, IJPR, C&IE**。

## 技能功能

引导AI智能体完成MS&E论文的**0到初稿五阶段流程**：

| 阶段 | 产出 | 关键交付物 |
|------|------|-----------|
| **阶段1**：选题定位 | Gap table、期刊推荐、贡献陈述 | 投哪本期刊 + 创新点是什么 |
| **阶段2**：模型构建 | 记法系统、假设框架、数学公式 | §3 模型章节初稿 |
| **阶段3**：推导分析 | Lemma→Theorem→Corollary证明链 | §4 分析章节初稿 |
| **阶段4**：数值实验 | 参数校准、敏感性分析、反事实 | §5-6 实验章节初稿 |
| **阶段5**：写作组装 | Introduction、文献综述、管理启示、摘要 | 完整初稿 |

该技能是**领域特化**的：内置了MS&E期刊特有的规范——如模型陈述结构、证明层级、管理启示SAR框架、各刊审稿人期望等，这些是通用写作技能（如`scientific-writing`）不覆盖的。

---

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/liyuanbo1024/management-science-writing.git
```

### 2. 安装到AI智能体

| 智能体 | 安装命令 |
|--------|---------|
| **OpenCode** | `cp -r management-science-writing ~/.config/opencode/skills/` |
| **Claude Code** | `cp -r management-science-writing ~/.claude/skills/` |
| **Codex** | `cp -r management-science-writing ~/.agents/skills/` |
| **Cursor** | `cp -r management-science-writing ~/.cursor/skills/` |
| **Windsurf** | `cp -r management-science-writing ~/.windsurf/skills/` |

Windows PowerShell 用户将 `cp -r` 替换为 `Copy-Item -Recurse`，将 `~/` 替换为 `$env:USERPROFILE\`。

安装后通过自然语言触发，例如：
- "我要写一篇动态定价的MSOM论文，帮我定位选题"
- "模型搭好了，帮我推导结构性质"
- "带我走一遍完整的管理科学论文写作流程"

---

## 使用方式

### 管道模式

```
"带我走一遍完整的MS&E写作流程。我的选题是……"
```

智能体会加载技能，评估当前阶段，从阶段1推进到阶段5，每个阶段完成后请求确认。

### 阶段跳转

| 触发语 | 跳转阶段 |
|--------|---------|
| "我有一个研究想法……" | 阶段1：选题定位 |
| "帮我设计数学模型" | 阶段2：模型构建 |
| "帮我推导/证明……" | 阶段3：推导分析 |
| "帮我设计数值实验" | 阶段4：数值实验 |
| "帮我写完整论文" | 阶段5：写作组装 |

### 参考模式

```
"MS对证明完备性的审稿要求是什么？"
"EJOR的管理启示应该怎么组织？"
```

---

## 文件结构

```
management-science-writing/
├── SKILL.md                              主技能文件
├── references/
│   ├── journal-characteristics.md        13本期刊详细特征
│   ├── modeling-conventions.md           记法·假设·模型类型
│   ├── proof-derivation-guide.md         证明层级·技法·期刊差异
│   ├── algorithm-solving-guide.md        伪代码·复杂度·近似比
│   ├── numerical-experiments.md          实验设计·参数校准
│   ├── managerial-insights.md            SAR框架·MI写作
│   ├── reviewer-expectations.md          审稿心理·Rebuttal策略
│   └── writing-patterns.md               6种可复用写作模式
├── assets/
│   └── theorem-structure-reference.md    通用定理结构参考
├── examples/
│   ├── manuscript_template.tex           INFORMS风格LaTeX模板
│   └── numerical_experiments.py          数值实验Python模板
├── README.md                             英文说明
├── README.zh-CN.md                       中文说明（本文件）
├── README.ja.md                          日文说明
├── README.ko.md                          韩文说明
└── LICENSE                               MIT许可证
```

---

## 覆盖期刊

### Tier 1 (UTD-24)

| 期刊 | 核心定位 |
|------|---------|
| **Management Science (MS)** | 广泛管理、高严谨度、重大贡献 |
| **Operations Research (OR)** | 方法论深度、优化聚焦 |
| **M&SOM (MSOM)** | 实证运营管理、行为运营 |
| **Production & Oper. Mgmt (POM)** | 数据驱动、广泛OM范围 |

### Tier 2（强领域期刊）

| 期刊 | 核心定位 |
|------|---------|
| Transportation Science (TS) | 交通系统、网络模型 |
| Transportation Research B (TRB) | 交通方法论 |
| Decision Sciences (DS) | 决策科学、MCDM |
| OMEGA | 简洁高影响力、管理导向 |
| Transportation Research E (TRE) | 物流与运输 |
| European J. Operational Research (EJOR) | 方法论包容、应用导向 |
| Int. J. Production Economics (IJPE) | 生产经济学、供应链 |
| Int. J. Production Research (IJPR) | 生产工程 |
| Computers & Industrial Eng. (C&IE) | 计算方法、工业工程 |

---

## 示例

`examples/` 目录包含两个参考文件：

1. **`manuscript_template.tex`**：INFORMS风格LaTeX模板，含MS&E论文的标准占位章节（模型→分析→实验→管理启示）。

2. **`numerical_experiments.py`**：可运行的Python数值实验模板，使用报童模型展示参数表、敏感性分析、基准对比的规范写法。

---

## 定制化

### 添加新期刊

编辑 `references/journal-characteristics.md`，按模板格式新增期刊条目。

### 调整参数默认值

修改 `examples/numerical_experiments.py` 中的 `Parameters` dataclass。

---

## 参与贡献

欢迎贡献。亟需帮助的方向：
- 尚未覆盖的期刊特征和审稿期望
- 从已发表论文中提炼的额外写作模式
- 各期刊的官方LaTeX样式文件
- 不同行业的校准数值实验

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)。

---

## 致谢

基于 [agentskills.io](https://agentskills.io) 规范和 [OpenCode](https://github.com/anomalyco/opencode) 的技能创作方法论构建。MS&E领域知识来源于INFORMS期刊编辑声明和运筹学社区的出版风格指南。
