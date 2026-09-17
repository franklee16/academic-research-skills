---
name: glance
description: "Use this skill when the user uploads multiple papers, abstracts, or excerpts and wants a quick batch reading — not deep analysis, but a rapid, structured overview across all of them. Triggers include: 'glance at these papers', 'quick read', '粗略阅读', '快速浏览这几篇', '批量阅读', '这几篇文章讲了什么', 'skim these', 'give me an overview of these papers', or any request to summarize and compare multiple documents simultaneously. The output is a compact Chinese-language PDF compiled via WeasyPrint covering: (1) one-paragraph story per paper, (2) each paper's contribution, (3) collective inspiration for the user's own research. Designed for speed and brevity — not a substitute for readecon's deep analysis."
---

# Glance: Rapid Multi-Paper Overview Generator

## Overview

This skill produces a **brief, punchy reading overview** across multiple papers uploaded in a single session. Where `readecon` goes deep on one paper, `glance` goes wide across several. The output is a compact Chinese PDF — think of it as a reading group prep sheet, not a dissertation literature review.

**Golden rule: be short.** Every section has a strict length budget. If you find yourself writing more than the budget allows, cut — do not expand.

---

## Workflow

### Step 1: Inventory the Uploaded Papers

First, list all uploaded files. Read each one using the appropriate method:

- If the content is already visible in context (pasted abstract, visible PDF text): use it directly.
- If files are at `/mnt/user-data/uploads/`: run `pdftotext` on each, or use `pdfplumber` for structured extraction.
- For each paper, extract only: **title, authors, year/venue, abstract, introduction (first 2 paragraphs), conclusion (last 2 paragraphs)**. Do not read the full paper — this is a glance, not a deep read.

Number the papers in the order they were uploaded. This numbering persists throughout the document.

### Step 2: Analyze Each Paper on Three Dimensions

For each paper, produce exactly three things. Apply strict length limits:

#### 2A. 故事（Story）
**One paragraph, 80–120 Chinese characters.**
Answer: What question does this paper ask, and what does it find? Write as if explaining to a fellow doctoral student over coffee — clear, direct, no jargon inflation. No equations, no method names unless essential. Just the narrative arc: problem → approach → finding → so what.

#### 2B. 贡献（Contribution）
**3–5 bullet points, each one sentence (≤30 Chinese characters per bullet).**
What does this paper add to the literature? Focus on what is genuinely new: a new dataset, a new identification strategy, a new context, a new mechanism, a new theoretical prediction. Do not list things the paper does that are standard practice. Only what it contributes that others have not done.

#### 2C. 启发（Inspiration）
**2–3 bullet points, each one sentence.**
Not what the paper contributes to the field — but what it sparks for *the reader's own research*. Frame this from the perspective of someone working on Chinese urban economics, land policy, or fiscal federalism (adapt to user's context if known). Ask: does this methodology apply to my context? does this finding suggest a gap I could fill? does this paper's limitation point to something I could do?

### Step 3: Write the Cross-Paper Synthesis

After the per-paper sections, add one short synthesis block:

#### 综合启发（Synthesis）
**One paragraph, 100–150 Chinese characters.**
Across all the papers read in this session: what common thread emerges? What cumulative insight do they collectively offer? What shared gap or tension is visible across them? This is not a summary of summaries — it is a synthetic observation about what the batch of papers, taken together, implies for research direction.

### Step 4: Compile the PDF

Use **WeasyPrint** (HTML → PDF) — no LaTeX required. WeasyPrint handles Chinese text natively via Noto fonts and compiles in a single pass.

**Installation (if needed):**
```bash
pip install weasyprint --break-system-packages
# Verify fonts: fc-list :lang=zh family | grep -i noto
```

**Python generation pattern:**

```python
from weasyprint import HTML
import datetime

today = datetime.date.today().strftime("%Y年%m月%d日")
n_papers = 3  # actual count

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  /* ── BASE ── */
  body {{
    font-family: 'Noto Serif CJK SC', 'Noto Sans CJK SC', serif;
    font-size: 11pt; line-height: 1.85; color: #1a1a1a;
    word-break: normal; overflow-wrap: break-word;
    font-variant-east-asian: proportional-width;
  }}

  /* ── PAGE: 封面用独立 @page，正文页带页眉页脚 ── */
  @page {{
    size: A4; margin: 2.5cm 2.8cm 2.5cm 2.8cm;
    @top-left {{
      content: "文献速览";
      font-family: 'Noto Serif CJK SC', serif; font-size: 8.5pt; color: #bbb;
      border-bottom: 0.5pt solid #e2e8f0; padding-bottom: 3pt;
    }}
    @top-right {{
      content: "高呵呵";
      font-family: 'Noto Serif CJK SC', serif; font-size: 8.5pt; color: #bbb;
      border-bottom: 0.5pt solid #e2e8f0; padding-bottom: 3pt;
    }}
    @bottom-right {{
      content: counter(page);
      font-family: 'Noto Serif CJK SC', serif; font-size: 8.5pt; color: #aaa;
    }}
  }}
  @page cover-page {{ margin: 0; }}  /* 封面无页眉页脚 */
  .cover {{ page: cover-page; page-break-after: always; }}

  /* ── COVER ── */
  .cover {{
    min-height: 29.7cm; display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 4em; box-sizing: border-box;
    background: linear-gradient(160deg, #ebf4ff 0%, #f7f9ff 100%);
  }}
  .cover-inner {{ text-align: center; max-width: 32em; }}
  .cover h1 {{
    font-size: 24pt; font-weight: bold; color: #2c5282;
    letter-spacing: 0.1em; margin: 0 0 0.6em 0;
  }}
  .cover hr {{ width: 4em; border: none; border-top: 2.5px solid #2c5282; margin: 0.8em auto; }}
  .cover .subtitle {{ font-size: 11pt; color: #4a5568; margin: 0.3em 0; }}
  .cover .meta {{ font-size: 9.5pt; color: #718096; margin: 0.2em 0; }}

  /* ── 文献列表（封面后第一块） ── */
  .paper-list {{ margin-bottom: 1.8em; }}
  .paper-list ol {{ padding-left: 1.8em; }}
  .paper-list li {{ font-size: 10pt; margin: 0.35em 0; }}

  /* ── SECTION HEADINGS ── */
  h2 {{
    font-size: 13pt; font-weight: bold; color: #2c5282;
    letter-spacing: 0.04em;
    border-left: 4px solid #2c5282;
    padding: 0.15em 0 0.15em 0.7em;
    margin: 2em 0 0 0;
    break-after: avoid; page-break-after: avoid;
  }}
  h3 {{
    font-size: 10.5pt; font-weight: bold; color: #4a5568;
    letter-spacing: 0.02em;
    margin: 1em 0 0 0;
    break-after: avoid; page-break-after: avoid;
  }}

  /* ── H2-ANCHOR: 把 h2 和紧跟它的第一段内容绑定，防止孤立标题 ──
     用法：<div class="h2-anchor"><h2>…</h2>（第一段内容）</div>
     之后的 .subsection 放在 .h2-anchor 外面                        ── */
  .h2-anchor {{
    break-inside: avoid; page-break-inside: avoid;
  }}
  .h2-anchor h2 {{ margin-bottom: 0.5em; }}

  /* ── SUBSECTION: h3 + 其内容整体不跨页 ── */
  .subsection {{
    break-inside: avoid; page-break-inside: avoid;
    margin-top: 0.8em;
  }}
  .subsection h3 {{ margin-bottom: 0.3em; }}

  /* ── BODY TEXT ── */
  p {{
    margin: 0.45em 0; text-indent: 2em;
    text-align: justify; orphans: 3; widows: 3;
  }}

  /* ── LISTS ── */
  ul, ol {{ padding-left: 1.8em; margin: 0.25em 0; }}
  li {{
    margin: 0.25em 0; text-align: justify;
    break-inside: avoid; page-break-inside: avoid;
  }}

  /* ── SYNTHESIS ── */
  .synthesis {{
    background: #f0fff4; border-left: 4px solid #48bb78;
    border-radius: 0 4px 4px 0; padding: 0.9em 1.3em;
    margin: 2em 0 0 0;
    break-inside: avoid; page-break-inside: avoid;
  }}
  .synthesis-title {{
    font-size: 12pt; font-weight: bold; color: #276749;
    letter-spacing: 0.03em; margin: 0 0 0.4em 0;
  }}
  .synthesis p {{ text-indent: 2em; margin: 0; }}

  /* ── DIVIDERS ── */
  hr {{ border: none; border-top: 1px solid #e2e8f0; margin: 1.4em 0; }}
</style>
</head>
<body>

<!-- 封面：单独一页，无页眉页脚 -->
<div class="cover">
  <div class="cover-inner">
    <h1>文献速览</h1>
    <hr>
    <div class="subtitle">[来源，如 NBER Working Papers 周报]</div>
    <div class="meta">阅读日期：{today} &nbsp;·&nbsp; 文献数量：{n_papers}篇</div>
    <div class="meta">笔记作者：高呵呵</div>
  </div>
</div>

<!-- 文献列表 -->
<div class="paper-list">
  <h2 style="border-left:none;padding-left:0;margin-top:0;">本次阅读文献</h2>
  <ol>
    <li>作者（年份）. <em>标题</em>. 期刊/来源.</li>
    <!-- 重复 -->
  </ol>
</div>

<hr>

<!-- 每篇文章结构：
     .h2-anchor 包裹 h2 + 故事 subsection（绑定标题与第一内容块）
     贡献、启发各自是独立的 .subsection                          -->
<div class="h2-anchor">
<h2>【1】作者（年份）标题简称</h2>
<div class="subsection">
<h3>故事</h3>
<p>一段话，80–120字。</p>
</div>
</div>

<div class="subsection">
<h3>贡献</h3>
<ul>
  <li>贡献一</li>
  <li>贡献二</li>
  <li>贡献三</li>
</ul>
</div>

<div class="subsection">
<h3>启发</h3>
<ul>
  <li>启发一</li>
  <li>启发二</li>
</ul>
</div>

<!-- 重复以上结构 -->

<hr>

<div class="synthesis">
  <div class="synthesis-title">综合启发</div>
  <p>一段话，100–150字，跨篇综合观察。</p>
</div>

</body>
</html>"""

HTML(string=html).write_pdf('/home/claude/glance.pdf')
```

**排版关键规则（已内嵌于模板，勿删改）：**
- **封面独立一页**：`.cover { page: cover-page; page-break-after: always }` + `@page cover-page { margin:0 }` — 封面无页眉页脚，正文从第二页开始
- **标题不孤立**：`.h2-anchor { break-inside: avoid }` 将 h2 与紧跟的第一内容块绑定；`h2/h3 { break-after: avoid }` 作为双重保险
- **子板块不跨页**：`.subsection { break-inside: avoid }` — h3 + 其内容整体保持同页（内容过长时 WeasyPrint 会自动放弃此约束，属正常行为）
- **孤行寡行控制**：`p { orphans: 3; widows: 3 }` — 段落至少保留3行在当前/下一页
- **列表项不截断**：`li { break-inside: avoid }`
- **中文字距优化**：`font-variant-east-asian: proportional-width` — CJK 字符等比例间距
- **页眉**：左侧"文献速览"、右侧"高呵呵"，带下划线分隔，比单一页码更专业

**File output:**
```bash
cp /home/claude/glance.pdf /mnt/user-data/outputs/glance_[日期].pdf
```

Then use `present_files` to deliver.

### Step 5: Present and Summarize

Copy the compiled PDF to `/mnt/user-data/outputs/` and use `present_files`. In the chat, add a **two-sentence** plain-language summary of the batch: what was the overall theme of the papers, and the single most actionable takeaway.

---

## Length Budget (Hard Limits)

| Section | Limit |
|--------|-------|
| 故事（per paper） | 80–120 Chinese characters |
| 贡献（per paper） | 3–5 bullets, ≤30 chars each |
| 启发（per paper） | 2–3 bullets, one sentence each |
| 综合启发 | 100–150 Chinese characters |
| Chat summary | 2 sentences |

If a paper is very short (abstract only), the story may be shorter. If a paper is unusually complex, the story may reach 150 characters at most — never more.

**Do not add sections.** Do not add a methodology subsection, a limitations subsection, or anything not listed above. The whole point of `glance` is constraint. Resist the urge to go deeper.

---

## Quality Standards

- **Concrete故事**: name the research question and the finding explicitly. "This paper studies land markets" is not a story. "This paper shows that industrial land parcel sizes in China shrink as city fiscal pressure rises, depressing public service provision in industrial zones" is a story.
- **Non-trivial贡献**: do not list "uses OLS regression" as a contribution. Contributions are things that push the frontier — new data, new identification, new context, new mechanism.
- **Researcher-facing启发**: the启发 bullets should feel like notes you'd write to yourself in the margin. They are about *your* research, not the paper's achievements.
- **Tight综合启发**: the synthesis should say something the individual paper sections do not already say. It is an emergent observation, not a concatenation.

---

## Edge Cases

- **If only one paper is uploaded**: complete the per-paper sections but skip the综合启发. Note in the chat that glance works best with 2+ papers and suggest readecon for single-paper deep analysis.
- **If abstracts only are provided (no full text)**: proceed, but flag clearly in each故事 section that it is based on abstract only, and keep贡献 to 2–3 bullets (do not infer contributions not stated in the abstract).
- **If papers are in English**: write all output in Chinese regardless. Translate titles and render author names in their original script.
- **If papers span very different topics**: the综合启发 may note the thematic heterogeneity rather than forcing a false synthesis. An honest "these papers share no common thread" is better than a manufactured one.
- **If there are more than 8 papers**: proceed normally — all three sections (故事、贡献、启发) are required for every paper regardless of batch size. The PDF will simply be longer; that is fine.
