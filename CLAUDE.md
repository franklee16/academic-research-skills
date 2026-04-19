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

**Reference-based skills** contain only a `SKILL.md` with embedded knowledge (e.g., `academic-writing`, `econ-write`, `peer-review`). These provide methodology guidance without code.

**Code-based skills** include supporting files:
- `references/` - Additional documentation and rules
- `phases/` - Multi-stage workflow definitions
- `techniques/` - Specific method implementations
- `src/` - Python source code (for skills with programmatic output)
- `requirements.txt` or `pyproject.toml` - Dependencies

### Skill Categories

| Category | Skills |
|----------|--------|
| Writing | `academic-writing`, `scientific-writing`, `econ-write` |
| Data Analysis | `r-analyst`, `stata-analyst`, `data-analysis`, `exploratory-data-analysis` |
| Literature | `lit-review`, `literature-review`, `academic-researcher` |
| Peer Review | `peer-review`, `referee2`, `scholarpeer-econ`, `paper-self-review` |
| Presentations | `beamer-presentation`, `scientific-slides`, `Aut_Sci_ppt-main` |
| Visualization | `matplotlib`, `scientific-visualization`, `econ-visualization` |

## Working with Skills

### Adding a New Skill

1. Create a folder with the skill name (use lowercase, hyphens for spaces)
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
├── SKILL.md files        # Main skill definitions (each folder is a skill)
├── references/           # Supporting documentation
├── phases/               # Workflow stage definitions
├── techniques/           # Specific method implementations
├── src/                  # Python code (code-based skills only)
└── requirements.txt      # Python dependencies
```

## Key Skill Examples

- `econ-write/` - Comprehensive economics writing guidance with embedded rules
- `peer-review/` - Systematic manuscript evaluation workflow
- `Aut_Sci_ppt-main/` - Full Python package for PDF-to-PPTX conversion
- `r-analyst/` - R analysis workflows with phases and techniques
