# JF Writing Style Guide — 使用说明

为金融学学术写作打造的 Journal of Finance 风格指南。从 144 篇 JF 论文（2022--2025）中提炼，涵盖句式模板、短语搭配、段落模式、润色工作流，适用于英文写作润色和中译英。

---

## 触发方式

在对话中输入以下任一关键词即可激活：

| 触发词 | 示例 |
|--------|------|
| `jf-skill` | `jf-skill 帮我润色这段引言` |
| `JF风格` | `JF风格，把这段结果翻译成英文` |
| `JF润色` | `JF润色 下面这段结论` |
| `JF写作` | `JF写作 帮我写一个摘要` |
| `JF翻译` | `JF翻译 这段中文引言` |
| `JF句型` / `JF句式` | `JF句型 这段结果怎么改` |
| `JF用语` | `JF用语 替换这段的口语化表达` |
| `JF polish` | `jf polish my introduction` |
| `JF translate` | `JF translate this abstract` |
| `JF style` | `apply JF style to my results section` |

**不会触发的情况：** 一般性的语法纠错、其他期刊风格咨询、纯内容/结构反馈（应走同行评审流程）。

---

## 使用场景

| 你说的话 | Skill 会做什么 | 加载的参考文件 |
|----------|---------------|----------------|
| "润色引言" / "polish introduction" | 匹配 JF 开头句式和段落结构 | `sentence-templates.md` §1-5 |
| "润色结果" / "polish results" | 应用 Claim-Evidence-Interpretation 段落模式 | `sentence-templates.md` §9-11 + `paragraph-patterns.md` §29-33 |
| "翻译摘要" / "translate abstract" | 中译英 + JF 短语替换 + hedging 校准 | `phrase-bank.md` |
| "检查全文写作风格" | 扫描全文 AI 指纹（三层防御）、过度 hedging、生僻搭配 | 全部 5 个 reference 文件 |
| "不知道怎么开头" | 提供 28 种 JF 开头风格选择 | `sentence-templates.md` §1 |
| "润色结论" / "polish conclusion" | 应用 JF 结论模板和 implication cascade | `sentence-templates.md` §15 |
| "改写段落" / "rewrite paragraph" | 匹配 33 种段落模式中合适的一种 | `paragraph-patterns.md` |

---

## 架构说明

Skill 采用模块化架构：主文件 `SKILL.md` 负责触发、路由和质量控制，例句、模板、短语库存放在 `references/` 子目录中，按需读取。

```
jf-skill-v3/
├── SKILL.md                          ← 主文件（触发条件、模式选择、质量标准）
└── references/
    ├── sentence-templates.md         ← 论文各部分句式（21 类，含完整例句和引用）
    ├── phrase-bank.md               ← 短语库（动词搭配、形容词对、hedging 分级、非学术→JF 替换表）
    ├── paragraph-patterns.md        ← 33 种段落模式（含变体和完整示例）
    ├── meta-discourse.md            ← 元话语模板（边界设定、解释控制、分层分析）
    └── usage-guide.md              ← 8 步润色工作流、附录模板、18 条关键警告（A-R，含三层 AI 检测防御体系）
```

---

## 工作流

每次激活后，Skill 按以下步骤工作：

1. **诊断** — 判断你的文本属于论文哪一部分（引言/结果/结论等）、需要润色还是翻译
2. **加载参考文件** — 多数任务只需 1-2 个 reference 文件，全文审查才需全部加载
3. **应用模式** — 匹配 JF 句型、替换短语、校准 hedging 强度
4. **润色** — 反复迭代，避免机械替换
5. **AI 指纹检查（三层防御）** — Tier 1: 12 项短语级扫描（"notably"、"potentially"、"Furthermore"、GPTZero 已学会的 hedging 短语等）；Tier 2: 5 项结构性自我审计（段落模板多样性、Introduction 四段式、平行 subsection 模板、不确定性表达、Conclusion 逐条重述）；Tier 3: 5 项量化验证（句长标准差、连接词密度、极端段落占比、不确定性表达式数、主导模板占比）

---

## 关键设计原则

**这是参考书，不是菜谱。** Skill 里的所有句型、搭配、段落模式都是描述性的（JF 作者实际怎么写），不是规定性的（你必须怎么写）。目标是帮你诊断文本缺什么、看看 JF 已发表论文怎么处理类似场景，而不是替代你自己的判断。

**一篇文章不需要全部模式。** 真正发表的 JF 论文只用其中一小部分模式。如果你一篇文章用了 5 个以上的特色搭配（"shed new light on"、"bridge different strands"、"demystify"等），读起来会像 AI 生成的。

**Hedging 要与证据强度匹配。** 模糊的 claim 用 speculative 措辞，扎实的发现用 confident 措辞。过度 hedging 和过度自信一样损害可信度。

**注意期刊差异。** ALL CAPS 开头、长枚举、"The remainder of the paper is organized as follows" 是 JF 惯例，投 JPE/QJE/Econometrica 时需要确认目标期刊规范。

**AI 检测的核心是结构对称性，不是用词。** 降低 AI 检测率的正确方法不是换词，而是打破结构对称性、注入不确定性、允许不完美的痕迹。详见 `usage-guide.md` Caveats M-R。

---

## 数据来源

从 144 篇 Journal of Finance 已发表论文（2022--2025）中逐句提取，涵盖资产定价、公司金融、银行、行为金融、家庭金融、国际金融、金融中介等子领域。所有例句均为 JF 原文的直接引用。

---

## 版本

v3.1.0（2026-06-05）— 三层 AI 指纹防御体系：Step 5 从 7 项扫描升级为 12 项短语扫描 + 5 项结构审计 + 5 项量化指标；反模式从 8 条扩展到 15 条（新增 7 条结构对称性相关反模式）；usage-guide.md 新增 Caveats M-R（对称问题、高触发模式及修复、量化审计指标、不完美写作作为防御、分章节风险表、2 分钟提交前检查）。原则吸收自 structure-randomizer 和 deep-humanize。

v3.0.0（2026-06-05）— 模块化重构：将 ~2000 行的单体 SKILL.md 拆分为 orchestrator + 5 个 reference 文件。

---

## 致谢

受 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) 的模块化架构启发。v3.1 AI 检测防御体系吸收自 structure-randomizer（结构方差作为检测对抗手段）和 deep-humanize（检测模型统计维度分析）。
