# Paper-to-Presentation

A Claude Code skill that transforms a batch of academic papers into a structured slide deck through a four-stage pipeline: figure extraction → text curation → narrative architecture → slide generation.

## Why This Exists

The default AI-assisted presentation workflow has predictable failure modes: garish color palettes, vacuous section headers ("Introduction to Method X"), inconsistent citation formatting, and slides that give the speaker no timing guidance. You didn't notice until you were standing at the podium.

This skill decomposes the problem into four sequential agents, each producing structured, verifiable intermediate artifacts. When something goes wrong, you re-run one stage—not the entire pipeline.

## Pipeline

```
Papers (papers/)
    │
    ▼
┌─────────────────────────────────────────┐
│ agent1  Figure extraction   pdf skill   │
│         Output: assets/figures/ + index │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ agent2  Text curation       pdf skill   │
│         Output: claims DB + source map  │
│                 + data tables           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ agent3  Narrative design  ppt-creator   │
│         Output: per-slide spec (15-18)  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ agent4  Slide generation    pptx skill  │
│         Output: final_presentation.pptx │
└─────────────────────────────────────────┘
```

## Design Rationale

**Why four agents instead of one?** Each stage has an independent verification gate. Figure extraction missed a plot? Re-run agent1, nothing else. A single monolithic prompt produces lower-quality output and is harder to debug. Short, focused agent prompts outperform long ones.

**Why citations in speaker notes instead of on-slide?** The audience reads the slide; the speaker reads the notes. Provenance annotations belong in the latter. Clean slides, traceable claims.

**Why lock the color palette?** Giving an agent freedom to "pick a good color scheme" reliably produces blue-orange AI slop. Hardcoding Ocean Gradient removes this entire class of failure.

## Constraints

| Dimension | Rule |
|-----------|------|
| Content provenance | 100% sourced from papers. No fabrication, no extrapolation. |
| Color | `#065A82` / `#1C7293` / `#21295C` + white / light gray |
| Headlines | Full assertion sentences. No topic labels. |
| Citations | Speaker notes only: `[Paper X, Page N / Paragraph N]` |
| Typography | System UI fonts (Segoe UI / Helvetica) + Consolas for data |
| Animation | None. No transitions, no entrance effects, no gradients. |
| Text density | ≤ 70 words per slide (excluding annotations) |
| Speaker notes | 45–60 seconds of spoken material per slide |

## Installation

```bash
git clone https://github.com/elinglijiaoqiao/presentation-ppt-maker.git
ln -s "$(pwd)/presentation-ppt-maker" ~/.claude/skills/paper-to-presentation
```

Or copy `SKILL.md` directly into `~/.claude/skills/paper-to-presentation/`.

## Dependencies

| Skill | Role |
|-------|------|
| `pdf` | Figure extraction (agent1) + text extraction (agent2) |
| `ppt-creator` | Pyramid-principle narrative structure + assertion headlines (agent3) |
| `pptx` | pptxgenjs slide generation (agent4) |

All three ship with Claude Code. No additional installation required.

Optionally pair with a `paper-search` CLI for upstream literature retrieval (arXiv, Semantic Scholar, PubMed).

## Project Layout

```
your-presentation/
  papers/                    # Input: N PDF papers
  assets/
    figures/                 # agent1: extracted figures
    figures_index.md         # agent1: figure inventory
    core_text.md             # agent2: curated claims by chapter
    source_index.md          # agent2: full provenance table
    data_points.md           # agent2: key metrics quick-reference
  prd/
    slide_outline.md         # agent3: overall structure + timing
    slide_specs.md           # agent3: per-slide spec (10 fields)
    source_map.md            # agent3: slide-to-paper mapping
  final_presentation.pptx    # agent4: deliverable
  speaker_notes.md           # agent4: compiled speaker notes
```

## Use Cases

- Undergraduate / graduate course presentations (15–20 min)
- Group meeting paper reports
- Poster-to-oral conversion for conferences
- Review article visualization

## Not For

- Pitch decks or product launches (different narrative style)
- Non-academic content
- Single-paper lightning talks (the pipeline is overkill—use a lighter approach)

## License

MIT
