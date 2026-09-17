# Metadata Schema

Use this schema for every saved `metadata.json`.

## PaperRecord

```json
{
  "paper_id": "doi-10.1145_1234567.8901234",
  "title": "Example Paper Title",
  "abstract_en": "Original English abstract.",
  "abstract_zh": "对英文摘要原文的忠实直译。",
  "authors": [
    {
      "name": "Author Name",
      "affiliation": "Example University",
      "citation_count": 1234,
      "h_index": 22,
      "is_high_impact": false,
      "is_corresponding": false,
      "semantic_scholar_author_id": "123456",
      "evidence_source": "Semantic Scholar"
    }
  ],
  "first_author": {
    "name": "Author Name",
    "affiliation": "Example University",
    "citation_count": 1234,
    "h_index": 22,
    "evidence_source": "Semantic Scholar"
  },
  "last_author": {
    "name": "Senior Author",
    "affiliation": "Example Lab",
    "citation_count": 45678,
    "h_index": 81,
    "evidence_source": "Semantic Scholar"
  },
  "corresponding_authors": [
    {
      "name": "Corresponding Author",
      "affiliation": "Example Lab",
      "evidence_source": "paper front matter"
    }
  ],
  "corresponding_author_status": "未在可用来源中可靠识别，未猜测。",
  "author_influence_summary": [
    "Senior Author 的引用或 h-index 达到高影响力阈值，来源: Semantic Scholar。"
  ],
  "published_at": "2024-06-01",
  "venue": "CVPR 2024",
  "venue_type": "conference",
  "doi": "10.1145/1234567.8901234",
  "arxiv_id": "2401.01234",
  "citation_count": 42,
  "indexing_notes": [
    "Indexed by source metadata only"
  ],
  "pdf_path": "/abs/path/to/paper.pdf",
  "bundle_dir": "/abs/path/to/<save_root>/<paper_id>",
  "sources_dir": "/abs/path/to/<save_root>/<paper_id>/sources",
  "images_dir": "/abs/path/to/<save_root>/<paper_id>/images",
  "pdf_analysis_path": "/abs/path/to/pdf_analysis.json",
  "analysis_path": "/abs/path/to/analysis.json",
  "report_tex_path": "/abs/path/to/report.tex",
  "report_pdf_path": "/abs/path/to/report.pdf",
  "pdf_parse_status": {
    "state": "已解析",
    "parser": "docling",
    "page_count": 12,
    "notes": [
      "图和表优先由 Docling 直接解析为文档对象，再导出对应图像资产。",
      "当前未启用 Docling VLM、图片描述或远程模型服务。"
    ]
  },
  "figures": [
    {
      "label": "图 1",
      "label_original": "Figure 1",
      "caption": "Overview of the proposed architecture.",
      "caption_zh": "方法总体结构图。",
      "page": 3,
      "asset_path": "/abs/path/to/images/figure-1.png",
      "image_scale": 3.0,
      "crop_status": "已由 Docling 直接导出",
      "visual_type": "figure",
      "evidence_summary": "Shows the two-stage encoder-decoder pipeline.",
      "evidence_summary_zh": "展示了两阶段编码器-解码器流程。",
      "linked_sections": [
        "method_flow"
      ]
    }
  ],
  "tables": [
    {
      "label": "表 2",
      "label_original": "Table 2",
      "caption": "Main results on CIFAR-10.",
      "caption_zh": "CIFAR-10 主结果。",
      "page": 7,
      "asset_path": "/abs/path/to/images/table-2.png",
      "image_scale": 3.0,
      "crop_status": "已由 Docling 直接导出",
      "visual_type": "table",
      "evidence_summary": "Shows the proposed model outperforming the strongest baseline by 1.7 accuracy points.",
      "evidence_summary_zh": "显示该方法在 CIFAR-10 上比最强基线高 1.7 个点。",
      "linked_sections": [
        "results"
      ]
    }
  ],
  "equations": [
    {
      "label": "公式 1",
      "raw_expression": "L = sum_i ||W x_i - y_i||_2^2 + lambda ||W||_F^2",
      "latex_expression": "L = \\sum_i \\lVert W x_i - y_i \\rVert_2^2 + \\lambda \\lVert W \\rVert_F^2",
      "page": 4,
      "context": "训练目标",
      "symbol_explanations": {
        "W": "模型参数矩阵",
        "lambda": "正则化权重"
      },
      "method_role": "定义训练阶段优化的目标函数。",
      "derivation_summary": "将数据拟合项和 Frobenius 正则项结合起来。"
    }
  ],
  "theoretical_items": [
    {
      "label": "证明相关段落",
      "kind": "proof",
      "page": 5,
      "statement_summary": "检测到证明相关段落。",
      "assumptions": [
        "目标函数凸",
        "Hessian 正定"
      ],
      "proof_summary": "通过零梯度条件和凸性说明最优解唯一。",
      "importance": "用于支持优化稳定性相关论断。"
    }
  ],
  "document_text": "Full text exported by Docling, truncated if necessary.",
  "document_markdown": "Markdown exported by Docling, truncated if necessary.",
  "text_sections": [
    {
      "title": "3 SELF-CALIBRATION",
      "text": "Section-level text excerpt exported from the PDF."
    }
  ],
  "landing_page": "https://example.org/paper",
  "metadata_enrichment_status": {
    "sources_checked": [
      "openreview",
      "semantic_scholar",
      "crossref",
      "arxiv"
    ],
    "field_status": {
      "doi": "found",
      "arxiv_id": "found",
      "citation_count": "found",
      "authors": "found",
      "first_author": "found",
      "last_author": "found",
      "corresponding_authors": "not_found"
    },
    "missing_fields": [
      "corresponding_authors"
    ],
    "conflicts": []
  },
  "metadata_sources": [
    {
      "source_name": "arxiv",
      "source_type": "api",
      "source_url": "https://arxiv.org/abs/2401.01234",
      "access_method": "codex_web_or_mcp",
      "is_official": true,
      "retrieved_at": "2026-04-21T12:00:00Z",
      "fields": [
        "title",
        "abstract_en",
        "authors",
        "published_at"
      ]
    }
  ],
  "notes": [
    "Saved from topic search on test-time adaptation."
  ]
}
```

## Required Fields

- `paper_id`
- `title`
- `authors`
- `metadata_sources`

## Strongly Recommended Fields

- `abstract_en`
- `published_at`
- `venue`
- `doi`
- `arxiv_id`
- `citation_count`
- `first_author`
- `last_author`
- `corresponding_authors`
- `author_influence_summary`
- `metadata_enrichment_status`
- `pdf_path`
- `report_tex_path`
- `report_pdf_path`
- `pdf_parse_status`
- `landing_page`
- `figures`
- `tables`
- `equations`
- `theoretical_items`

## Field Rules

- `paper_id`
  - computed by `doi > arXiv ID > title hash`
  - must be stable across re-runs
- `authors`
  - keep one object per author
  - use `null` for unknown numeric values
  - do not set `is_high_impact: true` without evidence
- `first_author`, `last_author`, and `corresponding_authors`
  - fill from source evidence when available
  - do not infer corresponding authors from author order alone
  - if corresponding authors are unavailable, set `corresponding_authors: []` and explain in `corresponding_author_status`
- `author_influence_summary`
  - summarize only source-backed author impact, affiliations, and notable coauthors
  - keep it concise and Chinese for direct report rendering
- `metadata_sources`
  - keep one record per evidence source
  - include `is_official`
  - include `access_method` when known, such as `codex_web`, `codex_mcp`, `codex_browser`, or `manual_inspection`
  - list the fields that came from that source when possible
- `metadata_enrichment_status`
  - record which sources were checked
  - mark important fields as `found` or `not_found`
  - preserve conflicts instead of silently overwriting values
- `indexing_notes`
  - store cautious notes, not unsupported claims
  - example: `Reported in publisher TOC`
- `pdf_path`
  - use an absolute path when the PDF exists locally
  - otherwise keep `null`
- `bundle_dir`
  - use the canonical bundle directory `<save_root>/<paper_id>`
  - do not point this field to a run directory or temporary directory
- `sources_dir`
  - use `<bundle_dir>/sources`
  - store Codex-collected external source payloads or normalized excerpts here
- `images_dir`
  - use `<bundle_dir>/images`
  - store extracted figure and table image assets here
- `pdf_analysis_path`
  - use `<bundle_dir>/pdf_analysis.json` when the PDF has been parsed
- `analysis_path`
  - use `<bundle_dir>/analysis.json` when a report has been authored
- `report_tex_path`
  - use `<bundle_dir>/report.tex` when `report.tex` exists locally
  - otherwise keep `null`
- `report_pdf_path`
  - use `<bundle_dir>/report.pdf` when `report.pdf` exists locally
  - otherwise keep `null`
- `pdf_parse_status`
  - use `state: parsed` only when a local parser completed successfully
  - include the parser name and page count when available
- `figures` and `tables`
  - store caption-level evidence even if no image asset could be extracted
  - use absolute paths for `asset_path` when an extracted image exists locally
  - record `image_scale` when Docling image export used a non-default scale
  - prefer `caption_zh` and `evidence_summary_zh` for final report rendering
  - keep `crop_status` to distinguish Docling direct exports from caption-only cases without image assets
- `equations`
  - keep the raw expression text as extracted or lightly normalized
  - add `latex_expression` when possible so reports compile formulas as math
  - explain symbols only when you have evidence from the paper context
- `theoretical_items`
  - use for theorem, lemma, proposition, or proof related evidence
  - keep proof summaries concise and evidence-based
- `document_text`, `document_markdown`, and `text_sections`
  - use these Docling exports as the primary evidence source when writing the detailed Chinese analysis
  - do not rely only on figure/table captions or abstract-level metadata
  - keep generated reports concise by selecting relevant section snippets rather than dumping the full text
- `abstract_zh`
  - must be a faithful direct translation of `abstract_en`
  - do not use a free-form summary as the Chinese abstract

## AuthorProfile Shape

```json
{
  "name": "Author Name",
  "affiliation": "Example University",
  "citation_count": 1234,
  "h_index": 22,
  "semantic_scholar_author_id": "123456",
  "is_corresponding": false,
  "is_high_impact": false,
  "evidence_source": "Semantic Scholar"
}
```

## PaperSourceRecord Shape

```json
{
  "source_name": "semantic_scholar",
  "source_type": "api",
  "source_url": "https://api.semanticscholar.org/...",
  "access_method": "codex_web_or_mcp",
  "is_official": false,
  "retrieved_at": "2026-04-21T12:00:00Z",
  "fields": [
    "citation_count",
    "authors"
  ]
}
```

## Structured Analysis Input For `render_report.py`

The report renderer expects a second JSON file with Codex-authored analysis fields. `narrative_sections` is required for a real report; helper scripts should not infer the main story from legacy evidence fields.

```json
{
  "abstract_zh": "中文摘要",
  "summary_one_liner": "一句话概括",
  "author_analysis": [
    "一作来自 Example University，主要研究方向与本文主题一致。",
    "通讯作者未在可用来源中可靠识别，未猜测。"
  ],
  "narrative_plan": [
    {
      "reader_question_zh": "读者首先需要知道为什么这篇论文不能只用已有方法解决。",
      "answer_being_built_zh": "已有方法把候选生成和置信度判断割裂开，导致测试时扩展采样预算后仍然可能选错答案。",
      "evidence_ids": ["图 1", "公式 1"],
      "why_this_evidence_matters_zh": "图 1 解释流程上的断点，公式 1 解释作者如何把这个断点写成可优化的校准目标。"
    }
  ],
  "narrative_sections": [
    {
      "title_zh": "主线一：问题为什么存在",
      "reader_question_zh": "读者需要先理解论文里的核心矛盾是什么。",
      "blocks": [
        {
          "type": "paragraph",
          "text_zh": "先用完整自然段讲清楚论文要解决的具体矛盾，以及为什么已有方法在这里不够用。"
        },
        {
          "type": "evidence",
          "evidence_id": "图 1",
          "placement_hint_zh": "把总体结构图放在解释三段式决策链的位置。"
        },
        {
          "type": "paragraph",
          "text_zh": "图 1 里的输入先经过问题约束模块，再进入核心求解模块，最后由评估模块重新校准输出。这条路径把前面提出的矛盾压缩成三个连续决策：先限制搜索空间，再生成候选解，最后用校准信号决定保留哪一个。"
        },
        {
          "type": "paragraph",
          "text_zh": "沿着这条路径看，方法的关键不是多加一个模块，而是让每一步都消化上一步留下的不确定性；下一步需要说明的是，这种不确定性如何被写成可训练目标。"
        },
        {
          "type": "evidence",
          "evidence_id": "公式 1",
          "placement_hint_zh": "把目标函数放在三段式流程之后，用来解释训练信号。"
        },
        {
          "type": "paragraph",
          "text_zh": "公式 1 把这种不确定性写进训练目标：数据拟合项约束候选输出，正则项控制参数规模。因此优化过程同时回答两个问题：当前输出是否贴近目标，以及模型是否用过大的参数代价换取表面提升。"
        }
      ]
    }
  ],
  "evidence_blocks": [
    {
      "id": "method-overview",
      "type": "figure",
      "label": "图 1",
      "caption_zh": "方法总体结构图。",
      "asset_path": "/abs/path/to/images/figure-1.png",
      "evidence_summary_zh": "这张图展示方法的两阶段流程。"
    }
  ],
  "paper_goal": "这篇论文在做什么",
  "method_flow": [
    "核心步骤 1",
    "核心步骤 2"
  ],
  "method_evidence": [
    "图 1 展示了两阶段编码器-解码器流程。",
    "公式 1 定义了带正则项的训练目标。"
  ],
  "experiment_pipeline": [
    "实验步骤 1",
    "实验步骤 2"
  ],
  "key_experimental_points": [
    "最值得关注的点 1",
    "最值得关注的点 2"
  ],
  "result_evidence": [
    "表 2 显示该方法在 CIFAR-10 上比最强基线高 1.7 个点。"
  ],
  "key_figures": [
    {
      "label": "图 1",
      "caption": "Overview of the architecture.",
      "caption_zh": "方法总体结构图。",
      "page": 3,
      "asset_path": "/abs/path/to/images/figure-1.png",
      "crop_status": "已由 Docling 直接导出",
      "evidence_summary": "Shows the two-stage pipeline.",
      "evidence_summary_zh": "展示了两阶段流程。"
    }
  ],
  "key_tables": [
    {
      "label": "表 2",
      "caption": "Main results.",
      "caption_zh": "主要结果表。",
      "page": 7,
      "asset_path": "/abs/path/to/images/table-2.png",
      "crop_status": "已由 Docling 直接导出",
      "evidence_summary": "Shows the proposed model outperforming baselines.",
      "evidence_summary_zh": "显示该方法优于基线。"
    }
  ],
  "key_equations": [
    {
      "label": "公式 1",
      "raw_expression": "L = sum_i ||W x_i - y_i||_2^2 + lambda ||W||_F^2",
      "latex_expression": "L = \\sum_i \\lVert W x_i - y_i \\rVert_2^2 + \\lambda \\lVert W \\rVert_F^2",
      "symbol_explanations": {
        "W": "参数矩阵",
        "lambda": "正则化权重"
      },
      "method_role": "训练目标",
      "derivation_summary": "平衡数据拟合和正则化。"
    }
  ],
  "derivation_explanations": [
    "该损失在数据拟合项之外加入了 Frobenius 正则，以约束参数规模。"
  ],
  "proof_explanations": [
    "证明利用凸性和零梯度条件来说明最优解唯一。"
  ],
  "results": "实验结果总结",
  "value": "论文价值",
  "limitations": "局限",
  "improvements": "可以怎么优化",
  "collaboration_highlights": [
    "某合作作者引用很高"
  ]
}
```

`narrative_sections[].blocks` rules:

- Use `paragraph` blocks for Codex-written Chinese explanation.
- Use `evidence` blocks to insert a figure, table, equation, or proof item exactly where the explanation needs it.
- Every evidence block should be immediately surrounded by paragraph blocks: one paragraph before it that makes the evidence necessary, and one paragraph after it that interprets the evidence and continues the argument.
- Use `placement_hint_zh` for non-rendered placement notes when useful. Legacy `lead_in_zh` and `takeaway_zh` are treated as non-rendered planning hints, not final report prose.
- `render_report.py` renders only the evidence asset for an evidence block. It does not print `placement_hint_zh`, `lead_in_zh`, or `takeaway_zh`.
- The paragraph immediately before an evidence block must not start with the evidence label, such as `表 1 把...`, `图 2 展示...`, or `公式 3 给出...`. It should first prepare the reader with definitions, compared methods, datasets, metrics, variables, assumptions, or proof goals.
- Do not put all evidence IDs at the end of a section unless the section is intentionally an appendix.
- Do not write meta placement language such as `应该放在这里`, `下面展示`, `正好对应`, `独立图表章节`, or `读这张图`.
- Do not write generic evidence prose such as `图 1 展示了方法流程`, `表 2 说明结果更好`, or `公式 1 定义目标函数`. Replace it with the specific modules, arrows, datasets, metrics, margins, variables, assumptions, or proof steps that the reader should understand.

`narrative_plan` rules:

- Use this as Codex's drafting scaffold before writing `narrative_sections`.
- Each plan item should answer one reader question and list the evidence IDs that will be used to answer it.
- Do not render the plan as a separate report section unless the user explicitly asks for a plan. Its purpose is to force reader-first ordering before prose is written.
- If experiments or theory are not central to the paper, say so in the relevant plan item and explain which evidence is still decisive.

Legacy fields such as `method_flow`, `key_figures`, `key_tables`, and `key_equations` are evidence pools. They are useful for drafting, but they are not a substitute for a Codex-written narrative.

Use UTF-8 for all files.
