---
name: auto-paper-skill
description: Find, deduplicate, save, index, and analyze research papers through Codex conversation. Use this skill when the user asks for papers by research direction, conference or journal year, DOI, arXiv ID, or title; compare against a local paper library; save canonical paper bundles; enrich metadata; parse PDFs; and generate Chinese paper reports.
---

# AutoPaperSkill

Use this skill for paper discovery, venue collection, direct paper lookup, local-library deduplication, durable paper storage, metadata enrichment, PDF parsing, and Chinese paper reports.

The user-facing workflow is conversational. Scripts are only for deterministic local work: scanning, matching, storage, metadata merging, PDF parsing, LaTeX rendering, PDF compilation, and `papers.html` index generation. Codex must perform external lookup, read the evidence, decide the narrative, and write the analysis.

## References

Load only what the current task needs:

- `references/source-policy.md`: paper sources, venue fallback, ranking, duplicate heuristics.
- `references/metadata-schema.md`: `metadata.json`, `pdf_analysis.json`, `analysis.json` fields.
- `references/report-template.md`: report section order, narrative style, evidence integration rules.

## Modes

- Research direction: find new relevant papers, deduplicate against the local library, prefer reasonable citation signals for age, and show a shortlist before saving unless direct save was requested.
- Conference or journal: use official venue/proceedings/publisher pages first; support explicit years; record fallback sources when official pages are unavailable.
- Specific papers: resolve DOI and arXiv IDs first, title-only inputs second; ask before saving if a title has multiple plausible matches.

## Required State

Before saving, deduplication, parsing, or report generation, determine:

- local paper directory when deduplication is requested
- durable library root for saved papers
- whether the user wants discovery only, save, or save plus report

Resolve the library root in this order:

1. explicit path from the request or earlier conversation
2. `AUTOPAPER_LIBRARY_DIR`
3. `~/.config/autopaper-skill/config.json` field `library_dir`

Do not silently use `/tmp`, a run directory, or the current working directory as the durable library root.

## Workflow

1. Scan or inspect the local library when available.
   - Use `python3 scripts/paper_store.py scan --library-dir <dir> --json` when useful.
2. Search or resolve papers.
   - External lookup is Codex's responsibility. Use conversation-available web/search/MCP/browser tools.
   - Do not use helper scripts to contact OpenReview, Semantic Scholar, Crossref, arXiv, publishers, or venue APIs.
3. Retrieve the PDF for any deep analysis or report.
   - Discovery-only workflows may stop before PDF download.
   - If OpenReview exposes a PDF or attachment, use that PDF source and troubleshoot failures instead of silently switching to arXiv.
4. Continue metadata enrichment after PDF retrieval.
   - OpenReview can be the PDF source, but still query or inspect DOI/arXiv/citation/author-impact sources when fields are missing.
   - Do not use scripts for external metadata fetching.
   - Save source payloads or normalized excerpts under `sources/`; scripts may merge local payloads but must not fetch them.
   - Record unavailable fields in `metadata_enrichment_status`.
5. Normalize metadata and deduplicate.
   - Use `references/metadata-schema.md`.
   - Compute `paper_id` by `doi > arXiv ID > title hash`.
   - Use `python3 scripts/paper_store.py match --library-dir <dir> --metadata-file <file> --json` when a deterministic duplicate decision is useful.
6. Save accepted papers as canonical bundles.
   - Treat the user path as a library root, not a per-paper directory.
   - Use `python3 scripts/paper_store.py upsert --library-dir <root> --metadata-file <metadata> --json`.
   - Final files belong under `<library_root>/<paper_id>/`, not ad hoc run directories.
7. Parse the saved PDF.
   - Use `python3 scripts/pdf_analyzer.py --pdf <paper_pdf> --output-json <pdf_analysis_json> --images-dir <images_dir>`.
   - Docling is the required parser. If it fails, report the failure instead of falling back silently.
   - Default image export scale is `3`; increase with `--image-scale 4` or higher when assets are blurry.
8. Codex writes `analysis.json`.
   - Read PDF text/Markdown, sections, captions, extracted images, formulas, proof items, metadata, and author evidence.
   - Inspect important extracted images; do not rely only on captions.
   - Write `narrative_plan` first, then Codex-authored `narrative_sections`.
   - Legacy fields such as `method_flow`, `key_figures`, `key_tables`, and `key_equations` are evidence pools, not a report.
9. Render and compile.
   - Use `python3 scripts/render_report.py --metadata-file <metadata_json> --analysis-file <analysis_json> --output <report_tex> --pdf-output <report_pdf>`.
   - `render_report.py` refreshes `<library_root>/papers.html` when metadata is inside a canonical bundle.
   - Use `python3 scripts/paper_store.py refresh-index --library-dir <root> --json` after manual edits.

## Report Contract

The final report is Chinese except `英文摘要原文` and raw math. `中文摘要` must be a faithful translation of the English abstract, not a new summary.

Required report content:

- paper snapshot and metadata source status
- author and influence analysis, including first author, corresponding author if reliably identified, and high-impact collaborators only with evidence
- English abstract, Chinese abstract, and one-line summary
- reader-first narrative covering problem, method, experiments, results, theory when relevant, value, limitations, and possible improvements
- key figures, tables, formulas, and proof items integrated into the narrative where they matter

Evidence integration is strict:

- Decide the reader's next question before inserting evidence.
- Prepare the reader before evidence: define concepts, compared methods, datasets, metrics, variables, assumptions, or proof goals.
- The paragraph before evidence must not start with the evidence label, such as `表 1 把...`, `图 2 展示...`, or `公式 3 给出...`.
- Use `placement_hint_zh`, `lead_in_zh`, and `takeaway_zh` only as planning notes. They are not rendered.
- Final prose must be `paragraph -> evidence asset -> paragraph`, with fresh context-aware paragraphs around the evidence.
- Do not create isolated `关键图/关键表/关键公式` sections by default.
- Do not write generic claims like `方法有效` or `实验充分` without concrete evidence.

`render_report.py` rejects missing `narrative_sections`, meta placement language, non-Chinese analysis prose, evidence without surrounding paragraphs, abrupt evidence-label openings, unsafe math, and obvious raw-formula rendering mistakes.

## Storage Contract

Each saved paper bundle lives under:

`<library_root>/<paper_id>/`

Canonical files:

- `paper.pdf`
- `metadata.json`
- `pdf_analysis.json`
- `analysis.json`
- `images/`
- `sources/`
- `report.tex`
- `report.pdf`

The library root also contains generated `papers.html`, with venue grouping and right-side PDF/report preview.

## Script Index

- `scripts/paper_store.py`: `config get-library`, `config set-library`, `scan`, `match`, `layout`, `upsert`, `validate-layout`, `refresh-index`.
- `scripts/pdf_analyzer.py`: mandatory Docling PDF parser; exports text, sections, figures, tables, equations, proofs, and images.
- `scripts/metadata_enricher.py`: merges local source payloads only; never fetches external services.
- `scripts/render_report.py`: renders Codex-authored `analysis.json` into `report.tex` and optionally `report.pdf`; refreshes `papers.html`.
- `scripts/render_report_pdf.py`: compiles existing `report.tex` to `report.pdf` with XeLaTeX.

Use `tc` conda environment for this repo when the user has requested it or when running the existing test suite.
