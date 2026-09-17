---
name: niulai
description: >-
  Master Academic Paper Polishing & Evidence-Preserving Rhetorical Guard Skill (牛来.skill).
  Synthesizes the empirical findings of AI peer-review research (120 papers, 4,200 variants, 42k reviews)
  with frontier LLM cognition insights. Applies Tier-1 rhetorical leverage (Evidence Framing & Confident Novelty Stance),
  enforces the strict GPT-5.6 Sol anti-AI syntax firewall (15-25 char sentences, zero nested "的", 50+ banned words purge,
  zero defensive self-sabotage), builds Claim-Evidence-Limit ledgers, and runs AST-level LaTeX structural guardrails.
  Use whenever polishing, refactoring, packaging, or auditing complete research manuscripts for top-tier conference/journal submissions.
---

# 牛来 (Niulai) — 顶会论文终稿高杠杆润色与证据守卫 Skill

`niulai` 是一款专为**学术论文终稿打磨（Camera-ready / Submission Polish）**设计的高杠杆润色与证据守卫智能体技能。深度融合了 42,000+ 次 AI 同行评审实证研究（《修辞如何对 AI 审稿人进行奖励黑客？》）所揭示的**审稿人高敏感修辞杠杆**与 `ko5.6sol` 的**反 AI 机械感硬核语法防火墙**。

---

## 1. 核心定位与五重能力架构 (Core Architecture)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   牛来 (Niulai.skill)                                   │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ 1. 六支柱数学/系统形式化 │ 2. 高杠杆审稿人修辞增强  │ 3. 5.6 SOL 反 AI 语法防火墙      │
│ - 问题数学空间与目标函数 │ - 证据呈现框架 (第一梯队)│ - 限制中文单句平均 15–25 字      │
│ - 四层解耦系统架构       │ - 创新姿态 (第一梯队)    │ - 彻底击碎多重“的”字缠绕句法     │
│ - 算法伪代码与执行流水线 │ - 论述范围 (第二梯队)    │ - 50+ 禁用过渡虚词与空洞热词熔断 │
│ - 受控变量与保真约束     │ - 显式量化指标差值 Δ     │ - 根除自黑与过度防御免责套话     │
├──────────────────────────┴──────────────────────────┴──────────────────────────────────┤
│ 4. 审稿证据台账与因果门控 (Claim-Evidence-Limit Ledger & Causal Gate)                  │
│ - 强制主张与实验证据 1:1 锚定；区分经验相关与因果结论；严禁无依据的 Overclaiming      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 5. 源码级自愈与 AST 自动化守卫 (Python latex_guard.py Tooling)                         │
│ - 100% 保护 LaTeX 语法、宏、公式、算法、交叉引用、图片路径与 .bib 数据源              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 标准执行流水线 (Execution Workflow)

当接收到论文终稿润色、方法论重构、LaTeX 源码修改或投审稿质量审核任务时，严格按以下 5 阶段执行：

### Stage 1: 科学实质与六支柱解构 (Formalize)
加载 [`references/methodology-six-pillars.md`](references/methodology-six-pillars.md)，将论文方法与贡献解构为：
1. **数学形式化**：输入空间 $\mathcal{X}$、变换算子 $\mathcal{T}$、目标函数 $\mathcal{L}$ 或成对估计量 $\widehat{\tau}$；
2. **系统分层架构**：数据准备层 $\to$ 核心处理层 $\to$ 校验自愈层 $\to$ 评估输出层；
3. **算法伪代码**：标准 LaTeX `algorithm` 流程与状态转移逻辑；
4. **控制变量与保真红线**：严禁篡改原始实验事实与数值排位；
5. **成对差分与统计检验**：提炼论文内成对差分与显著性验证设计。

### Stage 2: 注入第一梯队审稿人高杠杆修辞 (Amplify)
加载 [`references/rhetorical-power-matrix.md`](references/rhetorical-power-matrix.md)：
- **证据呈现框架 (Evidence Framing, 第一梯队)**：显式标明对比基线、量化增益差值 $\Delta$、核心指标提升与高信息密度图表 Caption；
- **自信创新姿态 (Novelty Stance, 第一梯队)**：事实优先，使用决断坚决的学术直叙，打破传统泛化偏见；
- **合理论述范围 (Scope Framing, 第二梯队)**：在实验充分支撑的区间内陈述最大普适性，拒绝狭隘自我封闭。

### Stage 3: 建立主张—证据台账与因果门控 (Audit)
加载 [`references/claim-evidence-ledger.md`](references/claim-evidence-ledger.md)：
- **建立 Claim–Evidence–Limit Ledger**：每个核心主张必须绑定明确的支撑图表/数据边界；
- **执行 Causal-Language Gate**：严禁把非正交全文干预吹嘘为单特征因果，使用精确限定词（如“在已评估流水线中观察到的成对差异”）。

### Stage 4: 启动 GPT-5.6 SOL 反 AI 语法防火墙 (Purge)
加载 [`references/anti-ai-syntax-firewall.md`](references/anti-ai-syntax-firewall.md)：
- **句长控制**：单句平均长度 15–25 字，主谓动作前置；
- **解绕定语**：单句禁止连续出现 3 个以上“的”；
- **清剿 50+ 禁用词**：熔断 `进一步`、`由此可见`、`基于此`、`与此同时`、`机制`、`支撑`、`稳健性` 等；
- **去自黑转化**：将自损免责重构为客观技术边界与未来演进路线。

### Stage 5: 代码保护与自动化脚本校验 (Shield)
- 运行 `python3 scripts/latex_guard.py` 对比基准快照，确保宏、标签、引用、公式、表格 100% 完好。

---

## 3. 核心质量验收清单 (Verification Checklist)

在输出润色结果前，必须逐条完成自检：

| 检查维度 | 合格标准 | 不合格典型表现（需立即重写） |
| :--- | :--- | :--- |
| **句长控制** | 中文 15–25 字/句，英文 12–18 词/句 | 出现单句超过 40 字的长难复合句 |
| **“的”字密度** | 单句 $\le 2$ 个“的”，无连续嵌套定语 | 出现“基于X的Y的Z的优化模型” |
| **AI 禁用词** | 50+ 禁用词列表 0 命中 | 出现“进一步”、“由此可见”、“机制”、“支撑” |
| **证据锚定** | 明确标出基线对比、指标提升与测试环境 | 仅泛泛而谈“取得了显著的性能提升” |
| **学术姿态** | 坚决自信，事实优先，无虚浮吹嘘与自黑 | 出现自我贬低免责或无根据的空泛自夸 |
| **因果门控** | 区分关联观察与因果，正确使用百分点 | 误将相关性写为绝对因果决定论 |
| **LaTeX 保护** | 宏、标签、引用、公式、表格 100% 完好 | 遗漏花括号、误改 label、破坏数学符号 |

---

## 4. 模块文件索引 (Module Index)

- 六支柱方法论形式化提取规范：[references/methodology-six-pillars.md](references/methodology-six-pillars.md)
- 审稿人高敏感修辞杠杆矩阵：[references/rhetorical-power-matrix.md](references/rhetorical-power-matrix.md)
- 主张—证据台账与因果语言门控：[references/claim-evidence-ledger.md](references/claim-evidence-ledger.md)
- GPT-5.6 SOL 反 AI 语法与词汇熔断防火墙：[references/anti-ai-syntax-firewall.md](references/anti-ai-syntax-firewall.md)
- 自动化 AST 结构守护脚本：[scripts/latex_guard.py](scripts/latex_guard.py)
- 端到端方法提取与重构案例：[examples/master-case-study.md](examples/master-case-study.md)
