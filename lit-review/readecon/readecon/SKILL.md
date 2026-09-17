---
name: readecon
description: "Use this skill whenever the user wants to read, analyze, or take structured notes on economics academic papers (journal articles, working papers, NBER/CEPR papers, dissertations). Triggers include: 'read this paper', 'analyze this article', 'literature reading notes', '文献阅读笔记', '读这篇论文', '分析这篇文章', or any request to systematically break down an economics paper's theory, empirical strategy, data, identification, limitations, or China-relevance. Also triggers when the user uploads a PDF of an economics paper and asks for analysis, summary, or structured notes. The final deliverable is a Chinese-language PDF reading note compiled via WeasyPrint. Use this skill even if the user only asks for part of the analysis (e.g., just the identification strategy) — the structured framework still helps organize the response."
---

# Readecon: Economics Literature Reading Note Generator

## Overview

This skill produces a structured, professional reading note for an economics paper. The note is written in Chinese, compiled via WeasyPrint (HTML → PDF, no LaTeX required), and output as a PDF. The analysis covers five dimensions that together give the reader a thorough understanding of the paper. **The first section is always 学理基础与研究贡献.**

## Workflow

### Step 1: Read the Paper

If the user uploads a PDF, read it using the pdf-reading skill's strategies:
1. Run `pdfinfo` and `pdftotext` to check structure.
2. Extract full text with `pdftotext` or `pdfplumber`.
3. If the paper has tables/figures that matter, rasterize key pages with `pypdfium2` for visual inspection.

If the paper's content is already in context (pasted text, or visible in the conversation), skip extraction and work directly with the content.

Read the paper carefully. Pay special attention to:
- Abstract, introduction, and conclusion (for the "story")
- Literature review and theoretical framework sections (for theoretical foundations)
- Data description and empirical strategy sections (for methods and identification)
- Robustness checks, limitations, and future research sections

### Step 2: Conduct the Six-Dimension Analysis

Analyze the paper along these six dimensions. Think like a doctoral seminar participant — be rigorous, specific, and critical.

#### Dimension 1: 学理基础与研究贡献 (Theoretical Foundations and Research Contributions)

This is the first section of the note. Cover two integrated aspects:

**学理基础 (Disciplinary/Theoretical Foundations):**
- Which economic theories or models does the paper build on? (e.g., Tiebout model, new economic geography, fiscal federalism, property rights theory, auction theory)
- What is the core theoretical mechanism or causal logic?
- Which seminal papers or intellectual traditions does it draw from?
- Is there a formal theoretical model? If so, what are its key assumptions and predictions?

**研究贡献 (Research Contributions):**
- What are the paper's main contributions to the literature? (empirical, theoretical, methodological, policy)
- How does it advance or challenge existing knowledge?
- What gap does it fill?

Be specific — name the theories, cite foundational works, and distinguish contributions clearly.

#### Dimension 2: 文章故事概括 (The Paper's Story in Plain Language)

Summarize in 3-5 sentences what the paper is about, as if explaining to an intelligent non-economist:
- What question does the paper ask?
- Why does this question matter (real-world motivation)?
- What does the paper find?
- What is the key insight or surprise?

Use plain, accessible Chinese. Avoid jargon. The goal is clarity, not sophistication.

#### Dimension 3: 数据、方法与因果识别 (Data, Methods, and Causal Identification)

Cover these sub-questions:
- **Data**: What datasets are used? What is the unit of observation? What is the time span? Is it cross-sectional, panel, or repeated cross-section? What is the sample size? Are there notable data limitations?
- **Methods**: What econometric tools are employed? (e.g., OLS, 2SLS/IV, DID, RDD, synthetic control, structural estimation, machine learning) Are there heterogeneity analyses or mechanism tests?
- **Model specification**: Write out the key regression equation(s) if possible.
- **Identification**: What is the identification strategy? What variation is being exploited? What are the key identifying assumptions (parallel trends, exclusion restriction, continuity, etc.)? How does the paper defend these assumptions? Are there threats to identification?

This is the most technical section — be precise.

#### Dimension 4: 不足之处与拓展空间 (Limitations and Extensions)

Critically evaluate:
- Internal validity concerns (endogeneity, measurement error, sample selection, SUTVA violations)
- External validity concerns (generalizability across contexts, time periods, populations)
- Data limitations the authors acknowledge or miss
- Methodological limitations
- What natural extensions could future research pursue?
- Are there alternative mechanisms the paper doesn't rule out?

Be constructive, not dismissive. Frame limitations as opportunities.

#### Dimension 5: 中国场景的迁移与思考 (Relevance and Adaptation to the Chinese Context)

This is where the reading note becomes most valuable for a Chinese economics researcher:
- Does the research question have a Chinese analogue? What institutional differences matter?
- Could the empirical strategy be replicated with Chinese data? What datasets would be needed? (e.g., 中国工业企业数据库, 土地交易数据, 城市统计年鉴, CFPS, CHIP, CHARLS)
- How do institutional differences (土地财政, 户籍制度, 央地关系, 国有企业, 经济特区) affect the theoretical predictions?
- What unique Chinese policy experiments (限大令, 营改增, 开发区设立, 撤县设区) could provide identification?
- What new research questions does this paper inspire in the Chinese context?

Be concrete — suggest specific research designs, data sources, and policy experiments.

#### Dimension 6: Output as PDF

Compile all five dimensions into a single, well-formatted PDF. See Step 3 below.

### Step 3: Compile the PDF

Use **WeasyPrint** (HTML → PDF) — no LaTeX required. WeasyPrint handles Chinese text natively via system Noto fonts and compiles in a single pass.

**Installation (if needed):**
```bash
pip install weasyprint --break-system-packages
# fonts-noto-cjk must be present (verify: fc-list :lang=zh family | grep -i noto)
```

**Python generation pattern:**

Write the full note as a styled HTML string, then compile:

```python
from weasyprint import HTML
import datetime

today = datetime.date.today().strftime("%Y年%m月%d日")

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
      content: "文献阅读笔记";
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
  @page cover-page {{ margin: 0; }}
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
  .cover .paper-title {{ font-size: 13pt; font-weight: bold; color: #2d3748; margin: 0.4em 0 0.2em; }}
  .cover .meta {{ font-size: 9.5pt; color: #718096; margin: 0.2em 0; }}

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
    font-size: 11pt; font-weight: bold; color: #4a5568;
    letter-spacing: 0.02em;
    margin: 1em 0 0 0;
    break-after: avoid; page-break-after: avoid;
  }}

  /* ── H2-ANCHOR: 把 h2 和紧跟它的第一段内容绑定，防止孤立标题 ──
     用法：<div class="h2-anchor"><h2>…</h2><p>第一段</p></div>    ── */
  .h2-anchor {{
    break-inside: avoid; page-break-inside: avoid;
  }}
  .h2-anchor h2 {{ margin-bottom: 0.5em; }}

  /* ── SUBSECTION: h3 + 其内容整体不跨页 ── */
  .subsection {{
    break-inside: avoid; page-break-inside: avoid;
    margin-top: 0.9em;
  }}
  .subsection h3 {{ margin-bottom: 0.3em; }}

  /* ── BODY TEXT ── */
  p {{
    margin: 0.45em 0; text-indent: 2em;
    text-align: justify; orphans: 3; widows: 3;
  }}

  /* ── LISTS ── */
  ul, ol {{ padding-left: 1.8em; margin: 0.3em 0; }}
  li {{
    margin: 0.28em 0; text-align: justify;
    break-inside: avoid; page-break-inside: avoid;
  }}

  /* ── EQUATION BLOCK ── */
  .eq-block {{
    background: #f7fafc; border-left: 3px solid #90cdf4;
    border-radius: 0 3px 3px 0; padding: 0.5em 1em; margin: 0.8em 0;
    font-family: 'Noto Sans Mono', 'Courier New', monospace; font-size: 10pt;
    break-inside: avoid; page-break-inside: avoid;
  }}

  /* ── TABLES ── */
  table {{
    border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 10pt;
    break-inside: avoid; page-break-inside: avoid;
  }}
  th {{ font-weight: bold; padding: 0.4em 0.8em; border: 1px solid #bee3f8; background: #ebf4ff; color: #2b6cb0; }}
  td {{ padding: 0.35em 0.8em; border: 1px solid #e2e8f0; }}

  /* ── DIVIDERS ── */
  hr {{ border: none; border-top: 1px solid #e2e8f0; margin: 1.5em 0; }}
</style>
</head>
<body>

<!-- 封面：单独一页，无页眉页脚 -->
<div class="cover">
  <div class="cover-inner">
    <h1>文献阅读笔记</h1>
    <hr>
    <div class="paper-title">[论文中文标题]</div>
    <div class="meta">原标题：[English Title]</div>
    <div class="meta">作者：[Authors] &nbsp;·&nbsp; 来源：[Journal, Year]</div>
    <div class="meta">笔记作者：高呵呵 &nbsp;·&nbsp; 阅读日期：{today}</div>
  </div>
</div>

<!-- 正文：每个 h2 用 .h2-anchor 包住标题+第一段；后续 .subsection 放在外面 -->

<div class="h2-anchor">
<h2>一、学理基础与研究贡献</h2>
<p>[内容第一段]</p>
</div>
<p>[后续段落，不受 break-inside 限制]</p>

<div class="h2-anchor">
<h2>二、文章核心故事</h2>
<p>[内容]</p>
</div>

<div class="h2-anchor">
<h2>三、数据、方法与因果识别</h2>
<div class="subsection">
<h3>3.1 数据来源与结构</h3>
<p>[内容]</p>
</div>
</div>
<div class="subsection">
<h3>3.2 计量方法与模型设定</h3>
<p>[内容]</p>
<div class="eq-block">Y_it = β·D_it + α·X_it + δ_i + ρ_t + ε_it</div>
</div>
<div class="subsection">
<h3>3.3 因果识别策略</h3>
<p>[内容]</p>
</div>

<div class="h2-anchor">
<h2>四、不足之处与拓展空间</h2>
<div class="subsection">
<h3>4.1 不足之处</h3>
<p>[内容]</p>
</div>
</div>
<div class="subsection">
<h3>4.2 可能的拓展方向</h3>
<p>[内容]</p>
</div>

<div class="h2-anchor">
<h2>五、中国场景的迁移与思考</h2>
<div class="subsection">
<h3>5.1 研究问题的中国对应</h3>
<p>[内容]</p>
</div>
</div>
<div class="subsection">
<h3>5.2 数据与识别策略的可行性</h3>
<p>[内容]</p>
</div>
<div class="subsection">
<h3>5.3 可能的研究设计</h3>
<p>[内容]</p>
</div>

</body>
</html>"""

HTML(string=html).write_pdf('/home/claude/reading_note.pdf')
```

**排版关键规则（已内嵌于模板，勿删改）：**
- **封面独立一页**：`.cover { page: cover-page; page-break-after: always }` — 封面无页眉页脚
- **标题不孤立**：`.h2-anchor { break-inside: avoid }` 将 h2 与紧跟的第一内容绑定；`break-after: avoid` 双重保险
- **子节不跨页**：`.subsection { break-inside: avoid }` — h3 + 内容保持同页
- **孤行寡行控制**：`p { orphans: 3; widows: 3 }`
- **方程块不跨页**：`.eq-block { break-inside: avoid }`
- **中文字距优化**：`font-variant-east-asian: proportional-width`
- **页眉**：左侧"文献阅读笔记"、右侧"高呵呵"，带下划线分隔

**File output:**
```bash
cp /home/claude/reading_note.pdf /mnt/user-data/outputs/reading_note_[作者年份].pdf
```

Then use `present_files` to deliver.

### Step 4: Present the PDF

Copy the compiled PDF to `/mnt/user-data/outputs/` and present it to the user with `present_files`. Also briefly summarize the key takeaways in the chat — the user should be able to glance at the chat and know the paper's main contribution without opening the PDF.

## Quality Standards

- **Be specific, not generic.** Don't say "the paper uses panel data" — say "the paper uses a city-year panel of 285 prefecture-level cities from 2003 to 2017, sourced from the China City Statistical Yearbook."
- **Write equations when relevant.** If the paper has a key regression specification, reproduce it as plain text or Unicode math in an `<div class="eq-block">` HTML block (e.g., `Y_it = β·D_it + α·X_it + δ_i + ρ_t + ε_it`). No LaTeX math syntax needed.
- **Name names.** When discussing theoretical foundations, cite the actual seminal papers (e.g., "building on Tiebout (1956) and Oates (1972)").
- **Be honest about what you can't assess.** If the paper is too technical in a specific area, say so rather than making up a critique.
- **Use plain Chinese for the story section.** The rest can use standard academic Chinese, but the story section (Dimension 2) should be genuinely accessible.
- **Balance praise and critique.** The limitations section should be constructive and balanced — every paper has limitations, but good papers also have clear contributions.

## Edge Cases

- **If the paper is in Chinese**: Still produce the reading note in Chinese. Adapt Dimension 5 to focus on international comparisons or policy lessons from other countries that could inform Chinese research.
- **If the paper is theoretical (no empirical section)**: Dimension 3 focuses on the model setup, assumptions, equilibrium characterization, and comparative statics. Skip data discussion. In Dimension 5, discuss testable predictions and what Chinese data could validate the model.
- **If the paper is a review/survey**: Adapt the framework. Dimension 1 becomes "covered literature and organizing framework." Dimension 3 becomes "methodological trends and gaps identified." Focus Dimension 4 on what the survey misses.
- **If the user only wants specific dimensions**: Produce only what's requested, but maintain the same rigor and formatting standards.
