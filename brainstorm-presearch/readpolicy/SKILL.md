---
name: readpolicy
description: "Use this skill whenever the user uploads or pastes a policy document (government policy, regulatory document, planning directive, ministerial notice, white paper, five-year plan excerpt, local government document, 政策文本, 政府文件, 规划, 通知, 意见, 办法, 条例, etc.) and asks for analysis, summary, keyword extraction, or research direction identification. Triggers include: '读这个政策', '分析政策文本', 'policy analysis', '政策解读', '关键词', '研究选题', '经济学研究方向', 'readpolicy', or any request to systematically break down a policy document. Also triggers when the user uploads any PDF/text that appears to be a government or regulatory document. The final deliverable is a clean, well-formatted Word (.docx) document containing: (1) overall summary, (2) key terms and phrases, (3) research directions for economics. Use this skill even if the user only wants part of the analysis."
---

# Readpolicy: Policy Document Analysis and Research Direction Generator

## Overview

This skill reads a policy document (Chinese or English) and produces a structured Word (.docx) document with three analytical layers:

1. **政策整体概括** — A concise overall summary of the document
2. **关键词与核心表述** — Key terms, phrases, and repeated rhetorical markers
3. **经济学研究新方向** — Specific wordings and concerns that signal new research opportunities

The output is a clean, professional Word document.

---

## Workflow

### Step 1: Read the Policy Document

If the user uploads a file, locate it in `/mnt/user-data/uploads/`. Read it using appropriate tools:

```bash
# For PDF
pdftotext /mnt/user-data/uploads/policy.pdf - 2>/dev/null

# For txt/docx content already in context
# Work directly from the text
```

If the full text is already visible in the conversation, skip file extraction.

Read carefully. Pay attention to:
- Document title, issuing authority, date, and document number (文号)
- Stated objectives and scope
- Specific numerical targets, timelines, or thresholds
- Lists of permitted/prohibited/encouraged actions
- New institutional arrangements or administrative mechanisms
- Repeated or emphasized phrases (especially those marked 重点, 重要, 明确, 严格, etc.)
- Appendices and schedules

---

### Step 2: Conduct the Three-Dimension Analysis

#### Dimension 1: 政策整体概括 (Overall Summary)

Write a clear, structured summary in 400–600 Chinese characters covering:

- **背景与目标**：What problem is this policy responding to? What are the stated goals?
- **主要内容**：What are the core measures, rules, or mechanisms introduced?
- **适用范围**：Who does this apply to? What sectors, regions, or actors?
- **实施要求**：Key timelines, enforcement mechanisms, accountability arrangements

Write in plain, direct academic Chinese. Avoid vague descriptors (如"深入贯彻"). Summarize substance, not slogans.

#### Dimension 2: 关键词与核心表述 (Key Terms and Phrases)

Extract and organize the following:

**A. 核心政策关键词** (core policy keywords):
Identify 10–20 specific terms that define this policy's conceptual frame. These may include:
- New administrative categories or classifications
- Names of specific programs, mechanisms, or funds
- Technical/legal terms defined or used in the document
- Sector-specific jargon

Format as a tagged list with a one-line gloss for each term.

**B. 频繁出现或强调的表述** (frequently appearing or emphasized phrases):
Identify 5–10 phrases that are repeated, bolded, or used in normative/directive contexts (e.g., 必须, 应当, 禁止, 鼓励). Note what behavior each phrase governs.

**C. 数量性指标与时间节点** (quantitative targets and deadlines):
List all numerical targets, ratios, thresholds, and deadlines explicitly mentioned. These are often the most actionable parts of a policy for empirical research.

#### Dimension 3: 经济学研究新方向 (New Directions for Economics Research)

This is the most valuable section for a research economist. Identify specific wordings, mechanisms, or policy concerns in the document that open new empirical or theoretical research questions.

For each direction, provide:
- **触发表述** (triggering phrase from the document): The exact phrase or passage that signals this direction
- **研究问题** (research question): The economic question this phrase raises
- **识别思路** (identification angle): How could an economist study this empirically? What variation does the policy create? What data might be needed?
- **文献关联** (literature connection): What existing literature does this connect to or extend?

Aim for 4–8 well-developed research directions. Prioritize directions that are:
- Empirically tractable (the policy creates variation that can be exploited)
- Connected to active debates in urban, public, labor, or development economics
- Specific to China's institutional context in ways that add genuine comparative value

Do NOT list generic directions like "we could study the effect of this policy." Be concrete: name the mechanism, the identification strategy, and the data.

---

### Step 3: Create the Word Document

Read the docx skill before generating the document:

**Required**: Before writing any code, verify `npm install -g docx` is available:
```bash
which docx-js 2>/dev/null || npm list -g docx 2>/dev/null | head -3
npm install -g docx 2>/dev/null || true
```

The document must follow this structure and design:

#### Document Design Spec

- **Page**: A4, margins 2.5cm all sides
- **Font**: 宋体 (SimSun) for body, 黑体 (SimHei) for headings — fall back to Arial if unavailable
- **Body size**: 11pt, 1.5x line spacing
- **Color palette**:
  - Header bar color: `2C5F8A` (policy blue)
  - Section heading color: `1A4971`
  - Accent/highlight: `E8F0F7`
  - Keyword tag background: `D4E8F5`
- **Structure**:
  1. Cover block (title, document issuer, date, "分析报告" label)
  2. Section 1: 政策整体概括
  3. Section 2: 关键词与核心表述 (three sub-tables: A, B, C)
  4. Section 3: 经济学研究新方向 (numbered cards/blocks)
  5. Footer with page numbers

#### JavaScript Template

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
        LevelFormat, VerticalAlign, PageNumber, Footer } = require('docx');
const fs = require('fs');

// ---- HELPER: section heading paragraph ----
function sectionHeading(text) {
  return new Paragraph({
    children: [
      new TextRun({
        text,
        bold: true,
        size: 28,       // 14pt
        color: "1A4971",
        font: "Arial"
      })
    ],
    spacing: { before: 360, after: 160 },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 6, color: "2C5F8A", space: 1 }
    }
  });
}

// ---- HELPER: body paragraph ----
function bodyPara(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, size: 22, font: "Arial", ...opts })],
    spacing: { after: 120 },
    indent: { firstLine: 440 }
  });
}

// ---- HELPER: keyword table row ----
function kwRow(term, gloss, colWidths) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new TableRow({
    children: [
      new TableCell({
        borders,
        width: { size: colWidths[0], type: WidthType.DXA },
        shading: { fill: "D4E8F5", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: term, bold: true, size: 20, font: "Arial" })] })]
      }),
      new TableCell({
        borders,
        width: { size: colWidths[1], type: WidthType.DXA },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: gloss, size: 20, font: "Arial" })] })]
      })
    ]
  });
}

// ---- HELPER: research direction block ----
function researchBlock(index, trigger, question, identification, literature) {
  const border = { style: BorderStyle.SINGLE, size: 4, color: "2C5F8A" };
  const blockBorders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [9026],
    rows: [
      new TableRow({ children: [new TableCell({
        borders: blockBorders,
        shading: { fill: "E8F0F7", type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 200, right: 200 },
        children: [
          new Paragraph({ children: [new TextRun({ text: `方向 ${index}`, bold: true, size: 24, color: "2C5F8A", font: "Arial" })] }),
          new Paragraph({ children: [new TextRun({ text: `触发表述：${trigger}`, size: 20, italics: true, font: "Arial" })], spacing: { before: 80 } }),
          new Paragraph({ children: [new TextRun({ text: `研究问题：${question}`, size: 20, font: "Arial" })], spacing: { before: 80 } }),
          new Paragraph({ children: [new TextRun({ text: `识别思路：${identification}`, size: 20, font: "Arial" })], spacing: { before: 80 } }),
          new Paragraph({ children: [new TextRun({ text: `文献关联：${literature}`, size: 20, font: "Arial" })], spacing: { before: 80 } }),
        ]
      })] })
    ]
  });
}

// ---- DOCUMENT ASSEMBLY ----
// Replace placeholder arrays below with actual analysis content

const POLICY_TITLE = "【政策文件标题】";
const POLICY_ISSUER = "【发文机关】";
const POLICY_DATE = "【发文日期】";
const SUMMARY_TEXT = "【政策整体概括正文，400–600字，分段落】";

const KEYWORDS_A = [
  // { term: "关键词", gloss: "含义说明" },
];
const KEYWORDS_B = [
  // { term: "表述", gloss: "规范对象与行为" },
];
const KEYWORDS_C = [
  // { term: "指标/节点", gloss: "具体数值或时间" },
];

const RESEARCH_DIRECTIONS = [
  // { trigger: "...", question: "...", identification: "...", literature: "..." },
];

const TABLE_WIDTH = 9026;
const COL_WIDTHS = [3000, 6026];

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

function tableHeader(labels, colWidths) {
  return new TableRow({
    tableHeader: true,
    children: labels.map((label, i) =>
      new TableCell({
        borders,
        width: { size: colWidths[i], type: WidthType.DXA },
        shading: { fill: "2C5F8A", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: label, bold: true, size: 20, color: "FFFFFF", font: "Arial" })] })]
      })
    )
  });
}

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ children: [PageNumber.CURRENT], size: 18, font: "Arial" }),
            new TextRun({ text: " / ", size: 18, font: "Arial" }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, font: "Arial" })
          ]
        })]
      })
    },
    children: [

      // ---- COVER BLOCK ----
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 480, after: 240 },
        children: [new TextRun({ text: "政策文本分析报告", bold: true, size: 52, color: "2C5F8A", font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 },
        children: [new TextRun({ text: POLICY_TITLE, bold: true, size: 28, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({ text: `发文机关：${POLICY_ISSUER}　　发文日期：${POLICY_DATE}`, size: 22, color: "666666", font: "Arial" })]
      }),
      new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "2C5F8A", space: 4 } },
        spacing: { after: 480 },
        children: []
      }),

      // ---- SECTION 1: SUMMARY ----
      sectionHeading("一、政策整体概括"),
      bodyPara(SUMMARY_TEXT),

      // ---- SECTION 2: KEYWORDS ----
      sectionHeading("二、关键词与核心表述"),

      new Paragraph({ children: [new TextRun({ text: "A. 核心政策关键词", bold: true, size: 22, font: "Arial" })], spacing: { before: 240, after: 120 } }),
      new Table({
        width: { size: TABLE_WIDTH, type: WidthType.DXA },
        columnWidths: COL_WIDTHS,
        rows: [
          tableHeader(["关键词", "含义与说明"], COL_WIDTHS),
          ...KEYWORDS_A.map(k => kwRow(k.term, k.gloss, COL_WIDTHS))
        ]
      }),

      new Paragraph({ children: [new TextRun({ text: "B. 频繁出现或强调的表述", bold: true, size: 22, font: "Arial" })], spacing: { before: 320, after: 120 } }),
      new Table({
        width: { size: TABLE_WIDTH, type: WidthType.DXA },
        columnWidths: COL_WIDTHS,
        rows: [
          tableHeader(["表述", "规范对象与行为"], COL_WIDTHS),
          ...KEYWORDS_B.map(k => kwRow(k.term, k.gloss, COL_WIDTHS))
        ]
      }),

      new Paragraph({ children: [new TextRun({ text: "C. 数量性指标与时间节点", bold: true, size: 22, font: "Arial" })], spacing: { before: 320, after: 120 } }),
      new Table({
        width: { size: TABLE_WIDTH, type: WidthType.DXA },
        columnWidths: COL_WIDTHS,
        rows: [
          tableHeader(["指标 / 节点", "具体内容"], COL_WIDTHS),
          ...KEYWORDS_C.map(k => kwRow(k.term, k.gloss, COL_WIDTHS))
        ]
      }),

      // ---- SECTION 3: RESEARCH DIRECTIONS ----
      sectionHeading("三、经济学研究新方向"),
      new Paragraph({ children: [new TextRun({ text: "以下方向源自政策文本中的具体措辞或制度安排，具备较强的经济学研究可行性。", size: 20, color: "444444", font: "Arial" })], spacing: { after: 200 } }),

      ...RESEARCH_DIRECTIONS.flatMap((d, i) => [
        researchBlock(i + 1, d.trigger, d.question, d.identification, d.literature),
        new Paragraph({ spacing: { after: 160 }, children: [] })
      ])

    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/claude/policy_analysis.docx", buf);
  console.log("Done");
});
```

**After generating**, validate and copy:
```bash
node policy_doc.js
python scripts/office/validate.py /home/claude/policy_analysis.docx || true
cp /home/claude/policy_analysis.docx /mnt/user-data/outputs/policy_analysis.docx
```

---

### Step 4: Present the Document

Copy the file to `/mnt/user-data/outputs/` and call `present_files`. Also provide a brief inline summary in the chat — the three most important research directions, in one sentence each — so the user doesn't need to open the document to get started.

---

## Quality Standards

- **具体，不笼统**：Summary must name actual mechanisms, not just say "加强监管". Every keyword entry must have a substantive gloss.
- **研究方向必须可操作**：Each research direction must name a specific identification strategy (DID, IV, RDD, etc.) or data source. "Can study X" is not enough.
- **尊重政策语言**：When quoting triggering phrases in Section 3, use the document's exact wording, not paraphrases.
- **数量指标务必完整**：All numerical targets and deadlines must appear in the C-table; these are the most empirically actionable elements.
- **英文政策文件同等适用**：If the policy is in English, conduct the analysis in Chinese but quote English source phrases directly in the "触发表述" field.

## Edge Cases

- **If the document is very long (>10,000 characters)**: Focus on the main body text; note in the summary that appendices or implementation rules were treated as secondary.
- **If the document contains multiple sub-policies or annexed regulations**: Note each sub-document in the cover block. Analyze them as a unified policy package.
- **If no quantitative targets are present**: Note "本文件未包含明确数量指标" in the C-table and add a row explaining the qualitative scope instead.
- **If the user only wants one section**: Produce only that section's content in the Word doc, but maintain the same formatting quality.
- **If the policy domain is highly technical (e.g., financial regulation, environmental standards)**: Briefly flag technical terms that require domain expertise and note where the analysis may be limited.
