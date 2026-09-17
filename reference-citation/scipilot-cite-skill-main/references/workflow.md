# 完整工作流程文档

本文详细说明 SciPilot-cite 8 个 Stage 的执行步骤、输入输出、用户交互点和边界情况处理。

---

## Stage 0：信息收集（主动逐项询问）

### 目的
在任何 API 调用前，与用户对齐全部参数。**禁止在缺参数情况下默默假设**。

### 询问顺序与字段

#### A. 输入模式（最先问）

| 字段 | 取值 | 说明 |
|---|---|---|
| `input_mode` | `A` 或 `B` | A = 论文文件插入引用；B = 给一段话/观点输出文献支撑列表 |

#### B. 基础参数（两种模式都必问）

| 字段 | 默认值 | 说明 |
|---|---|---|
| `target_object` | 无 | 模式 A: .tex/.docx 路径；模式 B: 用户粘贴的文字片段 |
| `target_count` | 用户答 | 5-30；模式 B 通常 5-15 |
| `style` | `ieee` | ieee / apa7 / nature / vancouver / gb-t-7714 / custom |

#### C. 检索范围（必问，告知默认）

| 字段 | 默认值 | 说明 |
|---|---|---|
| `year_range` | 近 5 年 | 基于当前日期动态计算 |
| `include_preprint` | `False` | 默认排除 arXiv / bioRxiv 等 |

#### D. 插入位置（仅模式 A 必问）

| 字段 | 默认值 | 说明 |
|---|---|---|
| `target_sections` | 自动判断 | 用户可指定列表如 `["Introduction", "Related Work"]` 或排除列表 |

#### E. 质量与偏好（主动询问，用户可逐项跳过）

| 字段 | 默认值 | 说明 |
|---|---|---|
| `must_cite_papers` | 空 | 必引论文（必须含 DOI 或完整元数据，禁止编造） |
| `preferred_venues` | 空 | 偏好期刊/会议列表 |
| `excluded_venues` | 空 | 排除的 venue |
| `journal_tier` | 不限 | `Q1` / `Q1Q2` / `cas1` / `cas12` / `none`；基于 LLM 软过滤，非权威 |
| `preferred_authors` | 空 | 偏好作者/课题组 |
| `excluded_authors` | 空 | 排除作者（如自引） |
| `preferred_affiliations` | 空 | 偏好机构（MIT/清华等） |
| `excluded_affiliations` | 空 | 排除机构 |
| `extra_keywords` | 空 | 自动抽取之外用户补充的关键词 |

### 复述确认
收齐后必须向用户口头复述所有参数并请求确认。例：

> 处理 **paper.tex**（模式 A），在 **Introduction + Related Work** 中插入
> **15 篇 IEEE 格式**文献，**2022-2026**，**不含预印本**，**JCR Q1**，
> 含 **MIT/清华** 机构。必引 **[DOI: 10.1038/s41586-024-07421-0]**。开始？

### 异常
- 用户输入模式不明 → 二选一确认
- 文件 / 片段未提供 → 等待
- 数量 >40 或 <3 → 提醒并请求确认
- 用户要求严格分区控制但未提供期刊白名单 → 告知"基于 LLM 软过滤、非权威"，请求是否继续

---

## Stage 1：论文分析

### 输入
`paper_path`、用户补充关键词。

### 步骤

**.tex 解析**（`scripts/insert_citations_latex.py::parse_latex`）：
1. 切分 preamble / body
2. 抽 `\section{}`、`\subsection{}` 段落
3. 提取 `\cite{...}` 已有引用
4. 识别 bibliography 类型：`thebibliography` / BibTeX / 无

**.docx 解析**（`scripts/insert_citations_docx.py::parse_docx`）：
1. 用 `python-docx` 读所有段落
2. 按 Heading 1/2/3 样式切分章节
3. 识别已有 References 章节

### 输出
```json
{
 "title": "...",
 "sections": ["Introduction", "Related Work", "Method", "Experiments"],
 "existing_citations": ["smith2023", "..."],
 "bibliography_type": "thebibliography",
 "keywords": ["llm", "alignment", "rlhf"]
}
```

### 异常
- 文件无 section → 视整篇为 body
- .docx 无 Heading → 在文末整体插入
- 文件解析失败 → 提示用户检查文件是否损坏

---

## Stage 2：文献检索

### 输入
`keywords`、`year_range`、`target_count`、`include_preprint`。

### 步骤
1. 构造主查询字符串（top-3 关键词组合）
2. 并行调用三个 API（`ThreadPoolExecutor(max_workers=3)`）
3. 每个 API 拉 `ceil(target_count * 3)` 篇
4. `merge_and_deduplicate`：DOI 主键去重 + 标题模糊去重
5. 按 `citation_count` 降序

### 输出
`list[dict]` 候选清单，约 `target_count × 3` 篇。

### 异常
- API 5xx 持续失败 → 用其他两源补足；三源全失败 → 终止并报告
- 某主题搜索结果 <10 篇 → 提示用户放宽关键词或年份

---

## Stage 3：文献验证

### 输入
Stage 2 的候选清单。

### 步骤
对每篇候选并行调用 `verify_paper`：

1. **DOI 验证**（如果有 DOI）
 - 调 `https://api.crossref.org/works/{doi}`
 - 标题相似度 ≥0.85 ∧ 年份精确 ∧ 首作者姓匹配 → `VERIFIED`
2. **跨源验证**（如果无 DOI 或 DOI 不匹配）
 - 在 S2 + OpenAlex 各搜索同标题
 - 两源都命中（标题 ≥0.85 + 同年份 + 同首作者姓） → `LIKELY_REAL`
3. **丢弃** `UNVERIFIED`

### 输出
仅保留 `VERIFIED` + `LIKELY_REAL` 的文献，每篇带 `verification_details`。

### 异常
- 验证通过数 < 用户需求数 → 进入 Stage 4 前提示，必要时回退到 Stage 2 用补充关键词重检
- DOI URL 404 但跨源都命中 → `LIKELY_REAL`，向用户标注

---

## Stage 4：筛选与排序

### 评分公式

```
score = 0.4 * relevance + 0.3 * quality + 0.2 * recency + 0.1 * diversity
```

- **relevance**：摘要与论文章节关键词重叠度（0–1）
- **quality**：log(citation_count + 1) 归一化（0–1）
- **recency**：(year - year_min) / (year_max - year_min)（0–1）
- **diversity**：按首作者姓去掉同团队多次出现（penalty 累加）

### 输出
按分数排序的 top-`target_count`，每条带 `suggested_section`。

### 用户交互点 [WARN]
**必须向用户展示候选清单并等待确认**：

```
SciPilot 候选清单（已验证）：

[OK] [1] Vaswani et al. (2017) "Attention Is All You Need"
 Cited 100k+ | NeurIPS | 建议章节: Method
[OK] [2] LeCun et al. (2015) "Deep learning"
 Cited 80k+ | Nature | 建议章节: Introduction
[WARN] [3] Smith et al. (2024) "..."
 Cited 50 | LIKELY_REAL | 建议章节: Related Work

请确认或要求替换某些（输入编号 + 替换原因）。
```

如果用户替换 → 回到 Stage 2 用更精细的关键词重搜。

---

## Stage 5：引用插入

### LaTeX 路径
`scripts/insert_citations_latex.py::insert_citations_to_latex`：

1. 调 `find_insertion_points` 为每篇文献找最匹配句子末尾
2. 按 `assign_citation_numbers` 分配 `[1] [2] ...`
3. 按位置从后向前插入 `\cite{key}`（避免偏移）
4. 更新或新建 `thebibliography` / `.bib` 文件

### Word 路径
`scripts/insert_citations_docx.py::insert_citations_to_docx`：

1. 找最匹配的段落
2. 在段落最后一句句号前插入 `[N]` 文本
3. 在文末添加 References 章节并按编号顺序列出条目
4. **必须保存为新文件**（如 `paper_scipilot.docx`），不覆盖原文件

### 输出
修改后的论文文件路径 + 插入计划元数据。

### 异常
- 无合适插入点 → 终止并报告（论文太短或全部段落都是图表）
- 段落已含 `[N]` 标记 → 跳过并提醒（避免与既有手工引用冲突）

---

## Stage 6：格式化输出

调 `scripts/format_citation.py::format_citation(paper, style, number)` 生成每条 References 条目。

样式细节见 `references/citation-formats.md`。

---

## Stage 7：最终检查

### 第 0 项：阻塞性幻觉门控（Gate 8）

**先于所有其他自检执行；audit 不通过则立刻中断整个交付流程。**

把最终采用的文献列表序列化到 `final_papers.json`（结构为 `list[dict]` 或 `{"papers": [...]}`），然后运行：

```bash
python scripts/audit_no_hallucination.py final_papers.json \
       --log verification_log.jsonl \
       --report audit_report.json
```

audit 行为：
1. 加载 `verification_log.jsonl`，按 `paper_id` 建索引
2. 对 `final_papers.json` 中每篇文献：
   - 计算 `paper_id_hash`，到日志中查 verdict
   - **独立地**重新调用 `verify_paper()` 做实时验证（100% 抽样，不是 20%）
   - 三项必须同时满足：日志中存在 + 日志 verdict 是 VERIFIED/LIKELY_REAL + 实时 verdict 也是 VERIFIED/LIKELY_REAL
3. 检测 verdict drift（日志说 VERIFIED 但实时说 UNVERIFIED → 可能是 API 缓存污染或元数据漂移）

exit code 含义：
- `0` PASS：每篇都通过对账+实时复核，**才能**继续 Stage 7 后续 5 项自检
- `2` FAIL：至少一篇可疑。读 `audit_report.json` 的 `per_paper` 字段，向用户报告每条 `pass=false` 的：标题、DOI、`log_verdict`、`live_verdict`、`reasons`。然后请用户决定：
  - 丢弃这些条目（推荐——最安全，保留通过 audit 的条目继续交付）
  - 用替代关键词重检（回 Stage 2）
  - 放弃整次操作
- `3` 运行性错误（输入文件不存在/JSON 损坏）→ 修复后重跑

### 第 1-5 项（第 0 项 PASS 后才执行）

1. **编号连续性**：`{1, 2, ..., N}` 完整无跳跃
2. **正文→列表存在性**：每个 `[N]` 都有对应条目
3. **列表→正文存在性**：每个条目都被正文引用（无孤儿）
4. **格式一致性**：所有条目使用同一 style
5. **原文完整性**：diff 比对，确认原文段落无意外修改

第 1-5 项是结构性检查，已被前序流程基本保证。第 0 项是核心防御。

### 输出报告

```markdown
# SciPilot 引用报告

- 论文：paper.tex
- 添加文献：15 篇
- 引用格式：IEEE
- 验证：VERIFIED 13 篇 / LIKELY_REAL 2 篇 / UNVERIFIED 0

## Gate 8 审计
- audit_report.json: PASS
- 重验证: 15/15 实时通过 Crossref/S2/OpenAlex
- 日志对账: 15/15 在 verification_log.jsonl 中有对应条目
- 漂移检测: 0 篇 verdict drift

## 章节分布
- Introduction: 3
- Related Work: 6
- Method: 4
- Experiments: 2

## 数据源分布
- semantic_scholar: 12
- openalex: 14
- crossref: 15（DOI 验证全部通过）

## LIKELY_REAL 警告
- [7] Smith et al. (2024) — DOI 缺失，但 S2+OpenAlex 跨源验证通过

## 结构自检
1-5 项全部通过
```

---

## 边界情况处理

### 1. 用户论文已有部分引用
- Stage 1 提取 `existing_citations`
- Stage 5 默认从最大编号 +1 开始；询问用户是否重排
- 重排时：保留原始 BibTeX keys，仅重新映射数字编号

### 2. 论文是中英混合
- 关键词抽取支持中文
- 编号格式自动适配（GB/T 7714 用全角空格和书名号）

### 3. 某 API 完全不可用（持续 5xx）
- 自动剔除该源，用其他两源补足
- 在 Stage 7 报告中明确标注

### 4. 用户提供的"必引论文"在 API 中找不到
- 尝试 DOI 直查
- 仍找不到则要求用户提供 DOI 或完整元数据，不得编造

### 5. 找不到足够数量的合格文献
- Stage 3 后提示实际找到 K 篇 < 目标 N 篇
- 询问用户选项：(a) 放宽年限 (b) 放宽预印本 (c) 接受 K 篇 (d) 换关键词

### 6. 论文格式异常（损坏的 .docx 或语法错误的 .tex）
- 解析失败时立即终止
- 输出具体错误位置和修复建议

### 7. Gate 8 审计 FAIL（疑似幻觉条目被拦截）
- 这是新增的物理门控触发场景，几种典型情况：
  - **缺日志条目**：某篇文献在 `final_papers.json` 里但 `verification_log.jsonl` 找不到对应 `paper_id` → 说明该文献从未经过 Stage 3，可能是 LLM 凭印象添加的，必须丢弃
  - **verdict drift**：日志记录 VERIFIED 但实时复核 UNVERIFIED → 可能 Crossref 元数据更新、API 缓存污染、或日志被篡改；保守处理是丢弃该条
  - **DOI 解析失效**：日志中曾 VERIFIED，现 Crossref 返回 404 → 文献可能下架；建议保留但在报告中标注
- 处置原则：**永不"放过"FAIL 条目**。即使用户施压，也必须从 bibliography 中移除或重新跑 Stage 2 找替代论文
- 用户可选：(a) 丢弃 FAIL 条目继续交付剩余 PASS 条目 (b) 回 Stage 2 用补充关键词重检 (c) 用户提供精确 DOI 强制重新验证 (d) 终止整次操作

---

## 与 SciPilot 家族其他成员的协作

| 触发条件 | 推荐 |
|---|---|
| 插入引用后想润色新增句子 | `scipilot-polish` |
| 想让 AI 模拟评审看完整论文 | `scipilot-review` |
| 想根据新引用调整图表 | `scipilot-figure` |
| 准备投稿目标期刊格式 | `scipilot-submit` |
| 想阅读理解新引用论文 | `scipilot-read` |
