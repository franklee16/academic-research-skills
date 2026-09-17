# SciPilot-cite-skill

> SciPilot Skills family. Citation copilot for academic writing.
> SciPilot Skills 家族成员 — 学术写作的引用副驾驶。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)](#dependencies--依赖)
[![Status: v1.0.0](https://img.shields.io/badge/Status-v1.0.0-success.svg)](#)
[![Hallucination Audited: Gate 8](https://img.shields.io/badge/Hallucination%20Audited-Gate%208-c41e3a.svg)](#gate-8-physical-hallucination-audit--幻觉门控)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)](https://claude.com/claude-code)

A [Claude Code](https://claude.com/claude-code) / [Codex](https://github.com/openai/codex) / Cursor Skill that **discovers, verifies, and inserts academic references** into your LaTeX or Word manuscript. Backed by three independent scholarly APIs with an authenticity-first verification pipeline that **never fabricates a citation**.

> **Distinguishing feature — physical hallucination gate.** Every citation in the delivered bibliography must survive an end-to-end audit that re-verifies 100% of entries against live Crossref / Semantic Scholar / OpenAlex and reconciles them with a tamper-evident JSONL evidence log written during search and verification. No log entry, no live API hit, no citation — period. **"Never fabricates" is enforced by code, not by prompt.** See [Gate 8](#gate-8-physical-hallucination-audit--幻觉门控) below.

> [中文文档](#中文文档) | [English](#english)

---

## 中文文档

### 概览

`scipilot-cite-skill` 解决学术写作中最容易出错也最伤诚信的环节 —— **引用**。支持两种输入：

- **模式 A — 论文模式**：读取你的 `.tex` 或 `.docx` 论文，在正文对应章节插入引用 + 生成 References
- **模式 B — 片段模式**：你给一段话或一个观点，输出能支撑它的真实文献列表（不动文档）

两种模式都通过 **Semantic Scholar + OpenAlex + Crossref** 三源并行检索近年高引文献，对每篇候选执行 **DOI 解析 + 多源交叉验证**，把无法验证的全部丢弃，按你指定的格式（IEEE / APA 7 / Nature / Vancouver / GB/T 7714）输出。

**Stage 0 主动询问 12 项参数**：输入模式、文献数量、引用格式、年限、目标章节、必引论文、期刊偏好、**期刊分区**（Q1 / 中科院 1-2 区）、**作者偏好**、**作者单位偏好**、是否含预印本、额外关键词。不会默默用默认值。

**核心承诺：**
- 一篇都不编造 — 验证失败的文献直接丢弃，宁缺毋滥
- 引用编号严格按正文首次出现顺序，零跳跃零孤儿
- 原文一字不动 — 只追加引用标记和 References，不修改任何已有内容
- **物理幻觉门控** — 交付前 100% 重审计，任何无溯源凭证的引用都被自动拦截

### 为什么这个 Skill 不一样：Gate 8 幻觉门控

大多数 LLM 写引用的助手把"不编造"写在提示词里，然后祈祷模型遵守。这在长上下文、API 失败、用户施压等情境下经常崩溃——典型表现是**真期刊+假页码、真作者+假 DOI 的"高仿"引用**，连资深审稿人都很难一眼识破。

scipilot-cite-skill 把"不编造"从**口号**升级成**机器可证伪的契约**。具体做法：

```
search_papers.py  →  写 evidence_log.jsonl   （每篇 API 响应都落盘）
                                ↓
verify_paper.py   →  写 verification_log.jsonl（每条验证 verdict 落盘）
                                ↓
LLM 准备 final_papers.json （Stage 4 用户确认后的最终清单）
                                ↓
audit_no_hallucination.py 末端独立审计：
  · 100% 重新调 Crossref/S2/OpenAlex 实时复核
  · 与 verification_log.jsonl 逐条对账
  · 检测 verdict drift（日志说 VERIFIED 但实时说 UNVERIFIED）
  · 任何一条没溯源 / 日志缺失 / 漂移 → exit code 2 → 拒绝交付
```

**三种典型幻觉，全部物理拦截：**

| 幻觉模式 | 拦截机制 |
|---|---|
| LLM 凭印象添加论文 | 在 `verification_log.jsonl` 中**找不到** `paper_id` 条目 → FAIL |
| API 一时返错信息被采信 | 末端**实时复核** Crossref，若现在查不到 → FAIL |
| 真期刊 + 编造的 page/volume | DOI 解析返回真元数据，比对发现不一致 → MISMATCH → FAIL |

这就是 README 顶部那个红色 badge `Hallucination Audited: Gate 8` 的意义——它不只是装饰，对应的是工程上 `scripts/audit_no_hallucination.py` 里**真正会跑、真正会 exit 2、真正会阻止交付**的代码。

### Stage 0 主动询问机制（12 项参数）

很多 AI 引用工具默认填一组参数就开始干，结果出来的引用对不上用户预期。`scipilot-cite-skill` 把 Stage 0 设计成**强制对齐**阶段——不获得用户明确确认就不进入检索。具体询问：

| 类别 | 询问项 | 备注 |
|---|---|---|
| 输入模式 | 模式 A（论文）/ 模式 B（片段） | 最先问 |
| 基础参数 | 目标对象 / 文献数量 / 引用格式 | 必问 |
| 检索范围 | 年份 / 是否含预印本 | 告知默认 |
| 插入位置 | 目标章节（仅模式 A） | 默认自动判断 |
| 质量偏好 | 必引论文 / 期刊会议 / **期刊分区** / **作者偏好** / **作者单位** / 额外关键词 | 用户可逐项跳过 |

收齐后向用户**口头复述全部参数**，等待"开始"确认。

### 核心特性

| 维度 | 实现 |
|---|---|
| 数据源 | Semantic Scholar（200M+ 论文）、OpenAlex（250M+）、Crossref（150M+ DOI 权威） |
| 检索方式 | 三源 ThreadPool 并行，按引用量降序合并，DOI 主键去重 + 标题模糊去重 |
| 真实性验证 | **三档分级 + 末端再审计**：`VERIFIED` / `LIKELY_REAL` / `UNVERIFIED`，再过 Gate 8 100% 重审 |
| **幻觉门控** | **Stage 7 第 0 项：`audit_no_hallucination.py` 阻塞性运行；FAIL 即拒绝交付** |
| 证据账本 | `evidence_log.jsonl` + `verification_log.jsonl` 由脚本写，LLM 无写权限 |
| 引用格式 | IEEE / APA 7 / Nature / Vancouver / GB/T 7714-2015 + BibTeX 导出 |
| 文档格式 | LaTeX `.tex`（`\cite{}` + `thebibliography` 或 BibTeX）、Word `.docx`（保持原格式） |
| 工作流 | 8 个 Stage 严格顺序，每个 Stage 内置质量门 |
| 依赖 | `requests` + `python-docx` + `python-Levenshtein`，**全部 API 免费**，无需 key |

### 安装

#### 方式 A：让 Claude Code / Codex 自己装（推荐）

在终端启动 Claude Code 或 Codex，直接说：

```
请帮我安装这个 Skill：https://github.com/Haojae/scipilot-cite-skill.git
```

AI 会自动 `git clone` 到正确目录（`~/.claude/skills/` 或 `~/.codex/skills/`），并提示你装 Python 依赖。

#### 方式 B：手动 clone

```bash
git clone https://github.com/Haojae/scipilot-cite-skill.git ~/.claude/skills/scipilot-cite-skill
pip install -r ~/.claude/skills/scipilot-cite-skill/requirements.txt
```

Codex 用户把目标目录换成 `~/.codex/skills/`，Cursor 用户换成 `.cursor/skills/`。

#### 方式 C：下载 ZIP

1. 在 GitHub 仓库页面点 `Code` → `Download ZIP`
2. 解压到 `~/.claude/skills/scipilot-cite-skill/`
3. `pip install -r requirements.txt`

### 使用

#### 1. 自然语言触发

启动 Claude Code 后随便用一句中文或英文：

**模式 A — 论文插入**：

```
帮我的 paper.tex 加 15 篇参考文献，用 IEEE 格式，
只在 Introduction 和 Related Work 章节加。
```

```
读取 thesis.tex，补充 10 篇 GB/T 7714 格式引用，
只要中科院 1-2 区期刊，排除预印本。
```

**模式 B — 片段支撑**（新）：

```
我有这段话需要文献支撑：
"近年来基于扩散模型的图像生成方法在医学影像合成上
取得显著进展，能够缓解小样本数据稀缺问题。"
帮我找 8 篇 2022-2026 的近年高引文献，IEEE 格式，
偏好 MIT/Stanford/清华的工作。
```

```
这个观点有文献支撑吗：
"LLM 通过 RLHF 训练能显著降低有害输出。"
找 5 篇 Nature/Science/NeurIPS 顶刊文献。
```

Skill 会在 Stage 0 主动询问 12 项参数（见上节），全部确认后再开始检索 → 验证 → 输出。**关键决策点会等你拍板**。

#### 2. 命令行直接调脚本

不通过 Skill 也能独立使用每个脚本：

```bash
# 三源并行检索
python scripts/search_papers.py "diffusion model" --limit 10 --json > papers.json

# 验证一个 DOI
python scripts/verify_paper.py doi 10.1038/s41586-024-07421-0 \
       --title "Detecting hallucinations..." --year 2024

# 单条引用格式化
echo '{"title":"...","authors":["..."],"year":2024,"venue":"...","doi":"..."}' | \
  python scripts/format_citation.py --style ieee --number 1

# 端到端插入 LaTeX
python scripts/insert_citations_latex.py paper.tex papers.json --style ieee

# 端到端插入 Word
python scripts/insert_citations_docx.py paper.docx papers.json --style nature
```

### 工作流（8 个 Stage）

```
Stage 0  参数收集  (篇数 / 格式 / 年限 / 预印本 / 特殊要求)
   |
Stage 1  论文分析  (章节抽取 / 已有引用 / 关键词)
   |
Stage 2  文献检索  (S2 / OpenAlex / Crossref 并行 + DOI 去重)
                  └→ 写 evidence_log.jsonl
   |
Stage 3  真实性验证 (DOI / 跨源 → VERIFIED / LIKELY_REAL / UNVERIFIED)
                  └→ 写 verification_log.jsonl
   |
Stage 4  筛选排序  (相关性40% + 质量30% + 时效20% + 多样性10%)
   |
   *** 用户确认候选清单后才能继续 ***
   |
Stage 5  引用插入  (LaTeX \cite{} / docx [N] 标记)
   |
Stage 6  格式化输出 (IEEE / APA / Nature / Vancouver / GB/T 7714)
   |
Stage 7  ┌─ 第 0 项: Gate 8 幻觉门控 (audit_no_hallucination.py)
         │   · 100% 重审 vs verification_log.jsonl 对账
         │   · 任何 FAIL → exit 2，拒绝交付
         └─ 第 1-5 项: 结构自检 (编号连续性 / 孤儿 / 格式 / 原文 diff / 预印本占比)
```

### 真实性验证分级 + Gate 8 末端复核

| 等级 | 触发条件 | 处置 |
|---|---|---|
| `VERIFIED` | DOI 在 Crossref 命中，且标题相似度 ≥ 0.85、年份精确、首作者姓匹配 | 直接采用 |
| `LIKELY_REAL` | 无 DOI 或 DOI 不匹配，但 Semantic Scholar 与 OpenAlex 都搜到该标题（相似度 ≥ 0.85） | 采用，在最终报告中**显式标注** |
| `UNVERIFIED` | 上述都不通过 | **直接丢弃，不允许引用** |

Stage 3 完成只是初筛。**真正的最终防线是 Stage 7 第 0 项的 Gate 8**——
独立脚本 `audit_no_hallucination.py` 会对最终 bibliography 100% 重新验证（而不是抽样 20%），同时和 `verification_log.jsonl` 逐条对账。任何无溯源条目或 verdict 漂移立即触发 exit 2，整个交付流程中断。这是把"不编造"从提示词承诺升级成机器契约的关键一环。

### 支持的引用格式

| 格式 | 主用领域 | 正文标记 | 排列方式 |
|---|---|---|---|
| **IEEE** | 工程、计算机、通信 | `[1]` `[1, 2]` `[1-3]` | 首次出现顺序 |
| **APA 7th** | 心理学、教育学、社科 | `(Author, Year)` | 第一作者字母序 |
| **Nature** | 自然科学顶刊 | 上标 `¹` `¹⁻³` | 首次出现顺序 |
| **Vancouver** | 医学、生物医学 | `(1)` `(1-3)` | 首次出现顺序 |
| **GB/T 7714-2015** | 中文期刊、硕博论文 | `[1]` | 引用顺序或著者-出版年 |

完整格式规范、模板、真实示例见 [`references/citation-formats.md`](references/citation-formats.md)。

### SciPilot Skills 家族

| Skill | 状态 | 功能 |
|---|---|---|
| **scipilot-cite-skill** | v1.0.0 (本仓库) | 文献检索与引用插入 |
| scipilot-polish-skill | 规划中 | 学术论文润色 |
| scipilot-review-skill | 规划中 | AI 模拟审稿 |
| scipilot-figure-skill | [v2.0.0](https://github.com/Haojae/scipilot-figure-skill) | 科研数据可视化顾问 + 绘制 |
| scipilot-submit-skill | 规划中 | 投稿格式适配 |
| scipilot-read-skill | 规划中 | 论文阅读与翻译 |

家族成员共享四条设计原则：
1. **AI 是副驾驶**：关键决策点等用户拍板
2. **真实性第一**：不编造任何学术信息
3. **一手文献驱动**：规则来自真实期刊规范，不靠"一般感觉"
4. **格式即法律**：同一论文格式必须绝对一致

### 贡献

欢迎 Issue 报告 bug、Feature Request、新引用格式贡献。提 PR 前请：
1. 确保 `scripts/utils.py`、`scripts/format_citation.py` 的内嵌测试能跑通
2. 新增格式需同时更新 `assets/format_templates/<style>.json` 和 `references/citation-formats.md`
3. SKILL.md 改动控制在 500 行内，详细内容放 `references/`

### 许可证

[MIT](LICENSE) © 2026 Haojae

---

## English

### Overview

`scipilot-cite-skill` solves one of the most error-prone (and integrity-sensitive) parts of academic writing — **citations**. Two input modes:

- **Mode A — manuscript mode**: read a `.tex` or `.docx` paper and insert citations into the right sections, with a References list at the end
- **Mode B — snippet mode**: paste a paragraph or a viewpoint, get back a verified reference list that supports the claim (no document modification)

Both modes parallel-search recent high-citation papers across **Semantic Scholar + OpenAlex + Crossref**, run each candidate through **DOI resolution + multi-source cross-check**, drop everything that fails verification, and output in your chosen style (**IEEE / APA 7 / Nature / Vancouver / GB/T 7714**).

**Stage 0 actively asks 12 parameters**: input mode, count, citation style, year range, target sections, must-cite DOIs, venue preferences, **journal tier** (JCR Q1 / 中科院 1-2 区), **author preferences**, **author-affiliation preferences**, preprint policy, extra keywords. No silent defaults.

**Core guarantees:**
- Never fabricates a reference — failed candidates are discarded, not invented
- Reference numbers strictly follow first-occurrence order, no gaps, no orphans
- Your manuscript prose stays byte-identical except for the added markers and References
- **Physical hallucination gate** — every entry in the delivered bibliography is re-audited 100% before delivery; anything without a provenance trail is blocked

### Gate 8: Physical Hallucination Audit / 幻觉门控

Most LLM citation assistants write "do not fabricate" into the system prompt and pray. That breaks down under long contexts, partial API failures, or user pressure — the typical failure is the **real-journal-with-fake-page-numbers / real-author-with-fake-DOI hybrid** that fools even expert reviewers.

scipilot-cite-skill promotes "never fabricates" from a **slogan** to a **machine-checkable contract**:

```
search_papers.py  →  writes evidence_log.jsonl       (every API response logged)
                                    ↓
verify_paper.py   →  writes verification_log.jsonl    (every verdict logged)
                                    ↓
LLM prepares final_papers.json (after user sign-off in Stage 4)
                                    ↓
audit_no_hallucination.py — independent end-of-pipeline audit:
  · Re-queries 100% against live Crossref / S2 / OpenAlex
  · Reconciles every entry against verification_log.jsonl
  · Detects verdict drift (log says VERIFIED but live says UNVERIFIED)
  · Any orphan / log miss / drift → exit code 2 → delivery REFUSED
```

**Three concrete hallucination modes — all physically blocked:**

| Mode | How Gate 8 catches it |
|---|---|
| LLM adds a paper from memory without searching | No matching `paper_id` in `verification_log.jsonl` → FAIL |
| Stale or wrong API metadata accepted earlier | Live re-query at audit time returns 404 / mismatch → FAIL |
| Real journal name + fabricated page or volume | DOI resolution returns the true metadata; comparison flags inconsistency → MISMATCH → FAIL |

The red `Hallucination Audited: Gate 8` badge at the top of this README is not decoration — it points to `scripts/audit_no_hallucination.py`, which is the code that actually runs, actually exits with code 2, and actually refuses to deliver if any citation lacks provenance.

### Stage 0: active questioning (12 parameters)

Most AI citation tools fill in defaults and start searching, leaving the user surprised at what comes back. `scipilot-cite-skill` makes Stage 0 a hard alignment step — no parameter, no search.

| Category | Asked | Notes |
|---|---|---|
| Input mode | Mode A (paper) / Mode B (snippet) | Asked first |
| Basics | target file / count / citation style | Always asked |
| Search scope | year range / preprint policy | Defaults disclosed |
| Target sections | which sections to cite into (Mode A only) | Defaults to auto-detect |
| Quality / preferences | must-cite DOIs / venue preferences / **journal tier** / **author preferences** / **author affiliations** / extra keywords | User may skip per item |

Once collected, the Skill **repeats every parameter back** and waits for an explicit "go".

### Key Features

| Dimension | Implementation |
|---|---|
| Data sources | Semantic Scholar (200M+ papers), OpenAlex (250M+), Crossref (150M+ authoritative DOIs) |
| Retrieval | ThreadPool parallel across 3 APIs, sort by citation count, DOI-primary dedup + fuzzy title dedup |
| Authenticity tiers | `VERIFIED` (DOI hit) / `LIKELY_REAL` (cross-source) / `UNVERIFIED` (dropped) |
| **Hallucination gate** | **Stage 7 Step 0: `audit_no_hallucination.py` blocking run; FAIL refuses delivery** |
| Evidence ledger | `evidence_log.jsonl` + `verification_log.jsonl` written by scripts only; LLM has no write path |
| Citation styles | IEEE / APA 7 / Nature / Vancouver / GB/T 7714-2015 + BibTeX export |
| Document formats | LaTeX `.tex` (`\cite{}` + `thebibliography` or BibTeX), Word `.docx` (format-preserving) |
| Workflow | 8 sequential stages, each gated by quality checks |
| Dependencies | `requests` + `python-docx` + `python-Levenshtein`, **all APIs are free**, no key required |

### Installation

#### Option A: Let Claude Code / Codex install it (recommended)

Open Claude Code or Codex in your terminal and just type:

```
Please install this Skill for me: https://github.com/Haojae/scipilot-cite-skill.git
```

The agent will `git clone` into the right directory (`~/.claude/skills/` or `~/.codex/skills/`) and prompt you for the Python deps.

#### Option B: Manual clone

```bash
git clone https://github.com/Haojae/scipilot-cite-skill.git ~/.claude/skills/scipilot-cite-skill
pip install -r ~/.claude/skills/scipilot-cite-skill/requirements.txt
```

Codex users: target `~/.codex/skills/`. Cursor users: target `.cursor/skills/`.

#### Option C: Download ZIP

1. Click `Code` → `Download ZIP` on the GitHub page
2. Extract into `~/.claude/skills/scipilot-cite-skill/`
3. `pip install -r requirements.txt`

### Usage

#### 1. Natural language trigger

Inside Claude Code, plain prose in English or Chinese:

**Mode A — insert into a manuscript**:

```
Add 15 references to my paper.tex in IEEE format,
only into the Introduction and Related Work sections.
```

```
Read thesis.tex, add 10 citations in GB/T 7714 format,
prefer journals in JCR Q1, exclude preprints.
```

**Mode B — support a viewpoint (new)**:

```
I have this paragraph and want supporting references:
"Diffusion-based methods have made notable progress in medical
image synthesis, mitigating small-sample limitations."
Find 8 recent (2022-2026) high-citation papers in IEEE format,
prefer work from MIT / Stanford / Tsinghua.
```

```
Is this claim well-supported in the literature?
"RLHF significantly reduces harmful outputs of LLMs."
Find 5 citations from Nature / Science / NeurIPS.
```

The Skill confirms all 12 parameters in Stage 0 (see above) before running search → verify → output. **It waits for your sign-off at every decision point.**

#### 2. Standalone CLI

Each script also runs on its own:

```bash
# Parallel multi-source search
python scripts/search_papers.py "diffusion model" --limit 10 --json > papers.json

# Verify a real DOI
python scripts/verify_paper.py doi 10.1038/s41586-024-07421-0 \
       --title "Detecting hallucinations..." --year 2024

# Format one entry
echo '{"title":"...","authors":["..."],"year":2024,"venue":"...","doi":"..."}' | \
  python scripts/format_citation.py --style ieee --number 1

# End-to-end LaTeX insertion
python scripts/insert_citations_latex.py paper.tex papers.json --style ieee

# End-to-end Word insertion
python scripts/insert_citations_docx.py paper.docx papers.json --style nature
```

### Workflow (8 stages)

```
Stage 0  Parameter collection (count / style / years / preprint policy / extras)
   |
Stage 1  Manuscript analysis (sections / existing cites / keywords)
   |
Stage 2  Search (S2 / OpenAlex / Crossref in parallel, dedup by DOI)
                  └→ writes evidence_log.jsonl
   |
Stage 3  Verification (DOI / cross-check -> VERIFIED / LIKELY_REAL / UNVERIFIED)
                  └→ writes verification_log.jsonl
   |
Stage 4  Ranking (relevance 40 + quality 30 + recency 20 + diversity 10)
   |
   *** Wait for user confirmation of candidate list ***
   |
Stage 5  Insertion (LaTeX \cite{} / docx [N] markers)
   |
Stage 6  Format output (IEEE / APA / Nature / Vancouver / GB/T 7714)
   |
Stage 7  ┌─ Step 0: Gate 8 hallucination audit (audit_no_hallucination.py)
         │    · 100% live re-verify + reconcile vs verification_log.jsonl
         │    · ANY fail → exit 2, delivery REFUSED
         └─ Steps 1-5: structural checks (numbering / orphans / format / diff / preprint mix)
```

### Authenticity pipeline (3 tiers) + Gate 8 final audit

| Tier | Trigger | Handling |
|---|---|---|
| `VERIFIED` | DOI hits Crossref; title similarity ≥ 0.85, exact year, first-author surname match | Accepted silently |
| `LIKELY_REAL` | No DOI or DOI mismatch, but both Semantic Scholar and OpenAlex return the same title (similarity ≥ 0.85) | Accepted, **explicitly flagged** in the final report |
| `UNVERIFIED` | None of the above | **Discarded, not citable** |

Stage 3 is only an initial filter. **The real final defense is Gate 8 at Stage 7 Step 0** — the standalone `audit_no_hallucination.py` re-verifies 100% of the final bibliography (not a 20% sample) and reconciles every entry against `verification_log.jsonl`. Any orphaned entry or verdict drift triggers exit code 2, and the whole delivery pipeline stops. That is what turns "never fabricates" from a prompt-level promise into a machine-enforced contract.

### Supported citation styles

| Style | Discipline | In-text marker | Ordering |
|---|---|---|---|
| **IEEE** | Engineering, CS, communications | `[1]` `[1, 2]` `[1-3]` | First occurrence |
| **APA 7th** | Psychology, education, social sciences | `(Author, Year)` | Alphabetical by first author |
| **Nature** | Top natural-science journals | Superscript `¹` `¹⁻³` | First occurrence |
| **Vancouver** | Medicine, biomedicine | `(1)` `(1-3)` | First occurrence |
| **GB/T 7714-2015** | Chinese journals, theses | `[1]` | First occurrence or author-year |

Full specs, templates and real examples in [`references/citation-formats.md`](references/citation-formats.md).

### SciPilot Skills family

| Skill | Status | Purpose |
|---|---|---|
| **scipilot-cite-skill** | v1.0.0 (this repo) | Reference discovery and insertion |
| scipilot-polish-skill | Planned | Academic prose polishing |
| scipilot-review-skill | Planned | AI peer-review simulation |
| scipilot-figure-skill | [v2.0.0](https://github.com/Haojae/scipilot-figure-skill) | Visualization advisor + renderer |
| scipilot-submit-skill | Planned | Submission formatting |
| scipilot-read-skill | Planned | Paper reading and translation |

All members share four design principles:
1. **AI is a copilot** — wait for user sign-off at every decision point
2. **Authenticity first** — never fabricate academic information
3. **Primary-source driven** — rules come from real journal style guides
4. **Format is law** — one paper, one consistent style

### Contributing

Bug reports, feature requests, and new-style contributions are welcome. Before opening a PR:
1. Ensure the embedded smoke tests in `scripts/utils.py` and `scripts/format_citation.py` still pass
2. New styles must update both `assets/format_templates/<style>.json` and `references/citation-formats.md`
3. Keep SKILL.md under 500 lines; long-form content belongs in `references/`

### License

[MIT](LICENSE) © 2026 Haojae

### Dependencies

```
requests>=2.31.0
python-docx>=1.1.0
python-Levenshtein>=0.23.0
```

Python 3.9+ recommended.
