# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a collection of Claude Code skills for academic research in economics, finance, and social sciences. Each skill is a self-contained module that provides specialized capabilities for different stages of the research workflow.

## Skill Architecture

Each skill folder contains a `SKILL.md` file with YAML frontmatter defining:
- `name`: Skill identifier (used to invoke via `/skill-name`)
- `description`: When and how to use the skill
- `allowed-tools`: Tools the skill can use (optional)
- `argument-hint`: Expected arguments (optional)
- `user-invocable`: Whether users can directly invoke (optional)

### Common Skill Patterns

**Reference-based skills** contain only a `SKILL.md` with embedded knowledge (e.g., `writing/academic-writing`, `writing/econ-write`, `peer-review/peer-review`). These provide methodology guidance without code.

**Code-based skills** include supporting files:
- `references/` - Additional documentation and rules
- `phases/` - Multi-stage workflow definitions
- `techniques/` - Specific method implementations
- `src/` - Python source code (for skills with programmatic output)
- `requirements.txt` or `pyproject.toml` - Dependencies

### Skill Categories

Skills are organized into 12 category subdirectories following the academic research workflow:

| Category | Count | Description |
|----------|-------|-------------|
| `writing/` | 8 | Academic writing, drafting, revision, response letters |
| `literature-review/` | 9 | Literature search, deep research, paper discovery |
| `data-analysis/` | 14 | R, Stata, Python analysis, panel data, cleaning |
| `visualization/` | 6 | Publication figures, matplotlib, TikZ, econ charts |
| `peer-review/` | 10 | Review, referee, quality checks, fact-checking |
| `presentations/` | 8 | Beamer, PPT, scientific slides, slide decks |
| `citations/` | 2 | Reference management, CrossRef, BibTeX |
| `grants/` | 1 | Grant proposals (NSF, NIH, NSTC) |
| `brainstorming/` | 4 | Hypothesis generation, ideation, prompt optimization |
| `data-sourcing/` | 3 | FRED, SEC EDGAR, API data fetching |
| `output-tools/` | 10 | Posters, web, LaTeX tools, case writing, diagrams |
| `project-management/` | 4 | Project scaffolding, PDF tools, strategic analysis |

## Working with Skills

### Adding a New Skill

1. Create a folder inside the appropriate category (e.g., `writing/my-new-skill/`)
2. Add `SKILL.md` with required frontmatter
3. Add supporting files as needed (`references/`, `phases/`, `techniques/`)
4. If the skill has Python code, include `requirements.txt` or `pyproject.toml`

### Modifying Existing Skills

Edit the `SKILL.md` file directly. For skills with code:
- Python packages are in `src/` following standard package structure
- Entry points are defined in `pyproject.toml` under `[project.scripts]`

### Testing Python-based Skills

For skills with `pyproject.toml`:
```bash
cd <skill-folder>
pip install -e .
```

For skills with `requirements.txt`:
```bash
cd <skill-folder>
pip install -r requirements.txt
```

## Repository Structure

```
academic-research-skills/
├── writing/              # 8 skills — academic writing, econ-write, revision
├── literature-review/    # 9 skills — lit search, deep research, discovery
├── data-analysis/        # 14 skills — R, Stata, Python, panel data, cleaning
├── visualization/        # 6 skills — matplotlib, TikZ, econ charts
├── peer-review/          # 10 skills — review, referee, fact-checking, consistency
├── presentations/        # 8 skills — Beamer, PPT, scientific slides
├── citations/            # 2 skills — reference management, CrossRef
├── grants/               # 1 skill — NSF/NIH/NSTC grant proposals
├── brainstorming/        # 4 skills — hypothesis generation, ideation
├── data-sourcing/        # 3 skills — FRED, SEC EDGAR, API fetching
├── output-tools/         # 10 skills — posters, web, LaTeX tools, diagrams
├── project-management/   # 4 skills — scaffolding, PDF tools, strategic analysis
├── CLAUDE.md
└── README.md
```

Each skill folder contains a `SKILL.md` file with YAML frontmatter. Code-based skills may also include `src/`, `references/`, `phases/`, or `techniques/` subdirectories.

## Key Skill Examples

- `writing/econ-write/` - Comprehensive economics writing guidance with embedded rules
- `peer-review/peer-review/` - Systematic manuscript evaluation workflow (note: skill inside category dir)
- `presentations/Aut_Sci_ppt-main/` - Full Python package for PDF-to-PPTX conversion
- `data-analysis/r-analyst/` - R analysis workflows with phases and techniques
- `literature-review/deep-research/` - Multi-source research synthesis
- `visualization/scientific-visualization/` - Publication-ready figure generation
