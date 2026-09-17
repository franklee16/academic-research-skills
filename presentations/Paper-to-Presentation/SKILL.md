---
name: paper-to-presentation
description: Use when creating course presentation slides from academic papers. Triggers on: "做 pre", "课程汇报", "论文 PPT", "presentation from papers", "把论文做成 PPT", or any request to turn research papers into slides for an academic talk.
---

# Paper-to-Presentation

A four-stage pipeline that transforms N academic papers into a course presentation deck. Each stage is an independent agent task whose output feeds the next. Must execute sequentially.

## Invariants (enforced across all stages)

### Content
- Every claim traces to a specific paper. No fabrication. No extrapolation.
- Numerical results cite exact source: `[Paper X, Page N / Paragraph N]`
- Source annotations go in Speaker Notes, never on the slide surface.
- Assumed audience: undergraduate STEM students who have taken the relevant introductory course. Skip basic terminology. Avoid derivations.

### Visual
- Color palette: Ocean Gradient only—`#065A82` (deep blue) / `#1C7293` (teal) / `#21295C` (midnight) + `#FFFFFF` (white) + `#F2F2F2` (light gray)
- Dark backgrounds reserved for: cover, closing slide, chapter dividers.
- No animations. No transitions. No gradients. No decorative elements.
- Typography: system UI fonts for body, monospace for data.
- Margins: ≥ 48px horizontal, ≥ 36px vertical.

### Narrative
- Every slide headline is a complete assertion (not a topic label). Example: "EDT achieves 5× frame rate gain with comparable image quality"—not "EDT Method Overview".
- 3–5 supporting points + 1 piece of evidence (figure / table / data) per slide.
- Speaker notes: 45–60 seconds of spoken material per slide. Structure: hook → core claim → evidence explanation → transition.
- ≤ 70 words per slide (excluding annotations).

## Directory Convention

```
project/
  papers/           # Input: N PDF papers
  assets/figures/   # agent1 output: extracted figures
  assets/           # agent2 output: text materials + provenance tables
  prd/              # agent3 output: per-slide specifications
  final_presentation.pptx  # agent4 deliverable
```

## Pipeline Stages

### agent1 — Figure Extraction
- **Tool**: `pdf` skill
- **Task**: Extract all embedded figures (diagrams, data plots, tables) from N papers. Discard decorative icons < 100px.
- **Output**:
  - `assets/figures/` — image files, naming convention `P<N>_<descriptor>.png`
  - `assets/figures_index.md` — inventory table: `| Figure | Paper N | Page | Suggested use |`
- **Constraints**: Preserve ≥ 150 dpi equivalent. No re-compression. No content alteration.

### agent2 — Text Curation
- **Tool**: `pdf` skill
- **Task**: Extract conclusive statements, quantitative results, and course-material connection points from N papers. Tag every item with precise provenance.
- **Output**:
  - `assets/core_text.md` — curated claims organized by chapter: `- [Paper X, Page N / §N] Original claim summary (retain English terminology)`
  - `assets/source_index.md` — full provenance table: `| ID | Paper | Page/§ | Summary | Suggested use |`
  - `assets/data_points.md` — key metrics quick-reference (performance numbers, comparison tables)
- **Constraints**: Every row must be traceable to a paper passage. Retain original English technical terms. Strip derivations and verbose experimental protocols.

### agent3 — PRD Per-Slide Specification
- **Tool**: `ppt-creator` skill
- **Task**: Using agent1+agent2 outputs, apply pyramid principle to produce a detailed per-slide spec.
- **Output**:
  - `prd/slide_outline.md` — overall structure + timing allocation (~15–18 slides)
  - `prd/slide_specs.md` — per-slide spec table, 10 fields per slide: page / chapter / assertion headline / core claim / supporting points (3–5) / figure reference / provenance / speaker notes outline / suggested layout
  - `prd/source_map.md` — slide-to-paper provenance mapping
- **Constraints**: ppt-creator must not fabricate data. No business-pitch tone. Fit within 20 minutes.

### agent4 — PPTX Generation
- **Tool**: `pptx` skill → `pptxgenjs`
- **Task**: Consume all outputs from agents 1–3. Generate slides page by page. Apply Ocean Gradient palette.
- **Output**: `final_presentation.pptx` + `speaker_notes.md`
- **Slide templates**: Cover (`#21295C` full-bleed) / TOC (white) / Standard content (top title bar + bottom page number) / Full-image / Closing (`#21295C` full-bleed)
- **Constraints**: Use relative paths for assets. Embed provenance in speaker notes on every slide. Use only fonts available on Windows.

## Getting Started

1. Create a project directory and place paper PDFs in `papers/`.
2. Optionally, use `paper-search` CLI to collect papers first.
3. Execute agent1 → agent2 → agent3 → agent4 in strict order.
4. Verify each agent's output before proceeding to the next.
