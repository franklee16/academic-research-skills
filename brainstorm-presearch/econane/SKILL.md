---
name: econane
description: "Use this skill when the user wants to enrich an economics argument, paper section, dissertation chapter, or policy brief with anecdotal evidence — real-world cases, media reports, investigative journalism, government announcements, corporate disclosures, or on-the-ground narratives — and then integrate that anecdotal evidence with academic findings into a unified, layered evidentiary argument. Triggers include: 'add some anecdotes', 'find real-world cases', '找一些现实案例', '加一些佐证', '新闻报道', 'find media coverage', 'anecdotal evidence', '案例支撑', 'illustrate with examples', or any request to ground an abstract research finding in concrete reality. Also triggers when the user pastes a research argument or dissertation passage and asks Claude to 'make it more vivid', 'add texture', or 'support this with examples'. The output is a structured evidence memo that combines anecdotal and academic evidence into a coherent argumentative unit."
---

# EconAne: Anecdotal Evidence Enrichment for Economics Research

## Overview

Economics research is most persuasive when it combines formal statistical evidence with vivid, concrete reality. This skill finds, evaluates, and integrates anecdotal evidence — news reports, investigative journalism, policy documents, court records, local government announcements, firm-level disclosures, and narrative accounts — with the user's existing academic argument. The output is a structured **evidence memo** ready to be woven into a dissertation, policy brief, or research paper.

The anecdotal layer does not replace econometric evidence. It *contextualizes* it: showing that what the regressions detect actually happened in real places, to real actors, with real consequences.

---

## When to Use This Skill

- A regression shows an effect but the mechanism is hard to visualize — find cases where the mechanism played out explicitly.
- A theoretical claim about government incentives, firm behavior, or household decisions needs grounding — find documentary evidence of that behavior.
- A paper section reads as too abstract — anchor it with a representative case.
- Reviewers or supervisors ask "but did this actually happen?" — build the answer.
- Policy implications need real precedents — locate where similar policies were tried and what happened.

---

## Workflow

### Step 1: Understand the Research Context

Before searching, extract from the user's input:

1. **The core empirical claim or mechanism** — what is the research trying to show? (e.g., "local governments in China deliberately subdivide land parcels to maximize fiscal revenue and exclude public services")
2. **The unit of analysis** — firms, cities, parcels, households, officials?
3. **The institutional or geographic context** — China? specific provinces? a particular policy regime?
4. **The time period** — what years does the research cover?
5. **The causal chain** — what causes what? what are the intermediate steps?

If any of these are unclear, ask the user before searching.

---

### Step 2: Search for Anecdotal Evidence

Run **multiple targeted searches** across different source types. For each search, use the `web_search` tool. Aim for at least **4–6 distinct searches** covering different source types and angles. More is better — cast a wide net, then curate.

#### Source Type Hierarchy (search in this order of priority)

**Tier 1 — Highest evidentiary value:**
- Investigative journalism from established outlets (财新, 南方周末, 第一财经, Caixin English, Reuters, FT, Bloomberg, WSJ China)
- Government audit reports (审计署报告), inspection records (督察报告), court judgments (裁判文书网)
- Official policy documents, local government announcements, land bureau records
- Listed company disclosures (annual reports, exchange filings) mentioning the phenomenon

**Tier 2 — Good supporting evidence:**
- Academic case studies in Chinese journals (中国土地科学, 城市发展研究, 经济研究) that contain descriptive case evidence
- Think tank reports (国务院发展研究中心, 中国社科院, Brookings, NBER working papers with case chapters)
- Local government statistical yearbooks or land transaction databases with notable entries

**Tier 3 — Illustrative, use with care:**
- General news reports from mainstream outlets (人民日报, 新华社, 澎湃新闻, 界面新闻)
- Online platforms with traceable sources (知乎 high-voted answers citing primary sources, 微信公众号 from verified institutions)
- Documentary films, academic conference presentations with case material

**Tier 4 — Use only if nothing better exists:**
- Forum posts, social media, unverified secondary sources (must flag explicitly)

#### Search Strategy

Construct searches around:
- **The specific mechanism**: e.g., "地方政府 土地分割 财政收入" / "land parcel size manipulation fiscal revenue"
- **The outcome**: e.g., "工业用地 配套设施缺失" / "industrial land public services shortage"
- **Specific policy moments**: e.g., "限大令 执行 案例" / "land size restriction enforcement"
- **Named places or firms**: if the research has a geographic focus, search for that region specifically
- **News events that reflect the mechanism**: e.g., auctions with suspicious patterns, official investigations into land misallocation

Always search in **both Chinese and English** when the topic is China-related. Chinese sources often have richer case detail; English sources often have clearer narrative framing.

After each search, use `web_fetch` to retrieve the full text of the most promising results — snippets are rarely sufficient.

---

### Step 3: Evaluate and Curate

For each candidate piece of anecdotal evidence, apply this checklist:

| Criterion | Question |
|-----------|----------|
| **Relevance** | Does this case directly illustrate the mechanism the research identifies? |
| **Specificity** | Does it name real places, actors, dates, amounts? Vague cases are weak cases. |
| **Source credibility** | Is the source verifiable, established, and independent? |
| **Temporal fit** | Does the case fall within or near the study period? |
| **Causal clarity** | Does the case show the *cause → mechanism → outcome* chain, not just the outcome? |
| **Typicality vs. extremity** | Is this a representative case or an extreme outlier? (Both can be useful, but label them correctly.) |

Discard cases that are vague, unverifiable, or only tangentially related. **Quality over quantity.** Two sharp, specific cases beat ten fuzzy ones.

---

### Step 4: Assemble the Evidence Memo

Produce a structured memo with four components. Write in the language the user is working in (Chinese for Chinese dissertations; English for English papers; mixed if the user mixes).

---

#### Component A: 研究主张摘要 / Research Claim Summary

One short paragraph restating the core empirical claim or mechanism being illustrated. This anchors everything that follows.

> 例：本研究发现，地方政府在出让工业用地时倾向于将宗地面积压缩至较小规模，以降低单宗地价、扩大出让宗数，从而在土地财政压力下最大化短期财政收入。这一行为导致工业园区内公共服务配套严重不足。

---

#### Component B: 佐证案例库 / Anecdotal Evidence Repository

For each case found, present it in this format:

```
【案例 N】标题（地点 · 时间）
来源：出版物名称，报道日期，作者（如有），链接
核心事实：[2–4句话，陈述该案例中发生了什么，涉及哪些行为主体，结果如何]
机制对应：[1–2句话，说明该案例如何印证研究中识别的因果机制]
证据层级：Tier [1/2/3/4]
注意事项：[如有数据局限、来源偏差、时间不匹配等，在此注明]
```

Present cases in order of evidentiary strength (Tier 1 first).

---

#### Component C: 学术证据摘要 / Academic Evidence Summary

Summarize the key academic findings the user's research rests on (or that the user provides). Keep this tight — 3–6 bullet points, each citing a specific finding with source. This is the "formal evidence" side of the ledger.

If the user has not provided academic evidence, note what kinds of evidence the anecdotal cases most need to be paired with, and suggest search directions.

---

#### Component D: 综合证据论证 / Integrated Evidentiary Argument

This is the core deliverable. Write a **unified argumentative paragraph or passage** (300–600 words in the target language) that weaves together:

1. The theoretical mechanism (one sentence)
2. The statistical/econometric evidence (one or two sentences citing the academic findings)
3. The anecdotal cases (two to three cases, integrated as illustration, not list)
4. A synthesis sentence explaining why the combination of evidence types is mutually reinforcing

**Writing principles for Component D:**
- Anecdotal cases should *follow* statistical evidence, not precede it. The pattern comes first; the case confirms it.
- Do not quote more than 15 words verbatim from any source. Paraphrase and attribute.
- Each case should be introduced with a transitional phrase that makes its role explicit: "这一机制在X案例中得到了具体体现……" / "This dynamic is visible in the case of X, where…"
- The passage should read as academic prose, not a list of examples.
- If cases come from different regions or time periods, briefly note this to support generalizability.

---

### Step 5: Flag Limitations

Always end the memo with a short **证据局限说明 / Evidence Limitations Note** (3–5 bullet points):

- Which source tiers dominate the anecdotal evidence (and what that implies for credibility)
- Whether the cases are geographically or temporally concentrated
- Any selection bias in media coverage (journalists report problems, not successful cases)
- Whether the cases show correlation vs. the mechanism itself
- What additional evidence would most strengthen the argument

---

## Output Format

The memo is delivered **in the chat** as formatted text with clear section headers. The user can copy Component D directly into their draft.

**After delivering the memo in chat, always proceed to Step 6 to generate a PDF version.** The PDF is a polished, standalone deliverable the user can share, archive, or attach to their research notes.

---

### Step 6: Generate the PDF

Use **WeasyPrint** (HTML → PDF) for Chinese-compatible PDF generation. This avoids LaTeX entirely and produces clean, professional output.

#### Installation (if needed)
```bash
pip install weasyprint --break-system-packages
# Fonts: Noto Serif/Sans CJK SC must be available (check with fc-list :lang=zh)
```

#### Python generation script

Write the full memo content as a styled HTML string, then compile with WeasyPrint:

```python
from weasyprint import HTML
import datetime

today = datetime.date.today().strftime("%Y年%m月%d日")

html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  /* ── BASE ── */
  body {
    font-family: 'Noto Serif CJK SC', 'Noto Sans CJK SC', serif;
    font-size: 11pt; line-height: 1.85; color: #1a1a1a;
    word-break: normal; overflow-wrap: break-word;
    font-variant-east-asian: proportional-width;
  }

  /* ── PAGE: 封面用独立 @page，正文页带页眉页脚 ── */
  @page {
    size: A4; margin: 2.5cm 2.8cm 2.5cm 2.8cm;
    @top-left {
      content: "文献佐证备忘录";
      font-family: 'Noto Serif CJK SC', serif; font-size: 8.5pt; color: #bbb;
      border-bottom: 0.5pt solid #e2e8f0; padding-bottom: 3pt;
    }
    @top-right {
      content: "高呵呵";
      font-family: 'Noto Serif CJK SC', serif; font-size: 8.5pt; color: #bbb;
      border-bottom: 0.5pt solid #e2e8f0; padding-bottom: 3pt;
    }
    @bottom-right {
      content: counter(page);
      font-family: 'Noto Serif CJK SC', serif; font-size: 8.5pt; color: #aaa;
    }
  }
  @page cover-page { margin: 0; }
  .cover { page: cover-page; page-break-after: always; }

  /* ── COVER ── */
  .cover {
    min-height: 29.7cm; display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 4em; box-sizing: border-box;
    background: linear-gradient(160deg, #f3f0ff 0%, #faf5ff 100%);
  }
  .cover-inner { text-align: center; max-width: 32em; }
  .cover h1 {
    font-size: 24pt; font-weight: bold; color: #553c9a;
    letter-spacing: 0.1em; margin: 0 0 0.6em 0;
  }
  .cover hr { width: 4em; border: none; border-top: 2.5px solid #553c9a; margin: 0.8em auto; }
  .cover .subtitle { font-size: 11pt; color: #4a5568; margin: 0.3em 0; }
  .cover .meta { font-size: 9.5pt; color: #718096; margin: 0.2em 0; }

  /* ── SECTION HEADINGS ── */
  h2 {
    font-size: 13pt; font-weight: bold; color: #553c9a;
    letter-spacing: 0.04em;
    border-left: 4px solid #553c9a;
    padding: 0.15em 0 0.15em 0.7em;
    margin: 2em 0 0 0;
    break-after: avoid; page-break-after: avoid;
  }
  h3 {
    font-size: 11pt; font-weight: bold; color: #4a5568;
    letter-spacing: 0.02em;
    margin: 1em 0 0 0;
    break-after: avoid; page-break-after: avoid;
  }

  /* ── H2-ANCHOR ── */
  .h2-anchor { break-inside: avoid; page-break-inside: avoid; }
  .h2-anchor h2 { margin-bottom: 0.5em; }

  /* ── BODY TEXT ── */
  p { margin: 0.45em 0; text-align: justify; orphans: 3; widows: 3; }
  .section-body > p { text-indent: 2em; }

  /* ── LISTS ── */
  ul, ol { padding-left: 1.8em; margin: 0.3em 0; }
  li {
    margin: 0.28em 0; text-align: justify;
    break-inside: avoid; page-break-inside: avoid;
  }

  /* ── CASE CARDS ── */
  .case-card {
    background: #f7fafc; border: 1px solid #e2e8f0;
    border-left: 4px solid #4299e1; border-radius: 0 4px 4px 0;
    padding: 0.9em 1.2em; margin: 1.2em 0;
    break-inside: avoid; page-break-inside: avoid;
  }
  .case-title { font-weight: bold; font-size: 10.5pt; color: #2b6cb0; margin-bottom: 0.35em; }
  .case-meta { font-size: 8.5pt; color: #718096; margin-bottom: 0.55em; font-style: italic; }
  .tier-badge {
    display: inline; background: #ebf8ff; color: #2b6cb0;
    border: 1px solid #bee3f8; border-radius: 3px;
    font-size: 7.5pt; padding: 1px 5px; margin-left: 0.5em; font-style: normal;
  }
  .case-card p { margin: 0.35em 0; text-indent: 0; }
  .label { font-weight: bold; color: #4a5568; }

  /* ── ACADEMIC EVIDENCE BLOCK ── */
  .acad-bullets {
    background: #fffff0; border: 1px solid #faf089;
    border-left: 4px solid #d69e2e; border-radius: 0 4px 4px 0;
    padding: 0.8em 1.2em; margin: 1em 0;
    break-inside: avoid; page-break-inside: avoid;
  }

  /* ── INTEGRATED ARGUMENT ── */
  .integrated {
    background: #faf5ff; border: 1px solid #d6bcfa;
    border-left: 4px solid #805ad5; border-radius: 0 4px 4px 0;
    padding: 1em 1.4em; margin: 1em 0;
    break-inside: avoid; page-break-inside: avoid;
  }
  .integrated p { margin: 0.5em 0; text-indent: 2em; orphans: 3; widows: 3; }

  /* ── LIMITATIONS ── */
  .limitations {
    background: #fff5f5; border: 1px solid #fed7d7;
    border-left: 4px solid #fc8181; border-radius: 0 4px 4px 0;
    padding: 0.8em 1.2em; margin: 1em 0; font-size: 10pt;
    break-inside: avoid; page-break-inside: avoid;
  }

  /* ── DIVIDERS ── */
  hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.5em 0; }
</style>
</head>
<body>

<!-- 封面：单独一页，无页眉页脚 -->
<div class="cover">
  <div class="cover-inner">
    <h1>文献佐证备忘录</h1>
    <hr>
    <div class="subtitle">论文：[论文标题]</div>
    <div class="meta">研究者：高呵呵 &nbsp;·&nbsp; 生成日期：[日期]</div>
  </div>
</div>

<!-- Component A -->
<div class="h2-anchor">
<h2>一、研究主张摘要</h2>
<div class="section-body"><p>[核心机制描述段落]</p></div>
</div>

<!-- Component B -->
<div class="h2-anchor">
<h2>二、佐证案例库</h2>
<div class="case-card">
  <div class="case-title">【案例1】标题（地点·时间）<span class="tier-badge">Tier 1</span></div>
  <div class="case-meta">来源：出版物名称，日期，链接</div>
  <p><span class="label">核心事实：</span>…</p>
  <p><span class="label">机制对应：</span>…</p>
  <p><span class="label">注意事项：</span>…</p>
</div>
</div>
<!-- 重复案例卡片：放在 .h2-anchor 外面，break 不受约束 -->

<!-- Component C -->
<div class="h2-anchor">
<h2>三、学术证据摘要</h2>
<div class="acad-bullets"><ul><li>…</li></ul></div>
</div>

<!-- Component D -->
<div class="h2-anchor">
<h2>四、综合证据论证</h2>
<div class="integrated"><p>…</p></div>
</div>

<!-- Limitations -->
<div class="h2-anchor">
<h2>五、证据局限说明</h2>
<div class="limitations"><ul><li>…</li></ul></div>
</div>

</body>
</html>
"""

HTML(string=html_content).write_pdf('/home/claude/econane_memo.pdf')
```

#### 排版关键规则（已内嵌于模板，勿删改）：
- **封面独立一页**：`.cover { page: cover-page; page-break-after: always }` — 封面无页眉页脚，紫色渐变背景
- **标题不孤立**：`.h2-anchor { break-inside: avoid }` 将 h2 与紧跟的第一个内容块（案例卡片/色块）绑定
- **卡片/色块不跨页**：`.case-card / .acad-bullets / .integrated / .limitations { break-inside: avoid }`
- **列表项不截断**：`li { break-inside: avoid }`
- **论证段落孤行控制**：`.integrated p { orphans: 3; widows: 3 }`
- **中文字距优化**：`font-variant-east-asian: proportional-width`
- **页眉**：左侧"文献佐证备忘录"、右侧"高呵呵"，带下划线分隔
- **三个 skill 主题色区分**：readecon=蓝色 `#2c5282`，econane=紫色 `#553c9a`，glance=蓝色 `#2c5282`（synthesis 绿色 `#48bb78`）

#### File output:
```bash
cp /home/claude/econane_memo.pdf /mnt/user-data/outputs/econane_memo.pdf
```

Then use `present_files` to deliver it to the user.

---

## Quality Standards

- **Every case must have a traceable source.** No case without an outlet name, date, and ideally a URL.
- **Specificity is non-negotiable.** "A city in Jiangsu" is weak. "苏州工业园区，2017年，据财新报道" is strong.
- **The integrated argument (Component D) must be prose, not bullets.** It should be ready to paste into a dissertation with minimal editing.
- **Maintain the academic register of the user's research.** If the user writes in formal academic Chinese, Component D must match that register.
- **Be honest about what you could not find.** If Tier 1 sources on a specific mechanism do not exist, say so and explain why (the phenomenon may be deliberately obscured, or the topic may be underreported).

---

## Edge Cases

- **If the user provides a specific passage to enrich**: analyze the passage first, identify all the implicit claims that could benefit from anecdotal grounding, then search and report back.
- **If the topic is sensitive (e.g., official malfeasance, corruption)**: prioritize court records, audit reports, and official investigation results over news reports. Do not speculate beyond what sources state.
- **If no good anecdotal evidence exists**: report this honestly, suggest why (topic underreported, phenomenon recently emerged, geographic specificity too narrow), and propose the closest available cases with explicit caveats.
- **If the user is writing in English but the cases are in Chinese**: provide the case summary in English with the Chinese source cited. Do not fabricate English-language sources for Chinese-language phenomena.
- **If the user wants cases from outside China**: apply the same framework but substitute China-specific source recommendations with equivalents (ProPublica, NYT investigative, FT, country-specific audit institutions).
