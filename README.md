# Academic Research Skills for Claude Code

A comprehensive collection of 79 Claude Code skills for academic research in economics, finance, and social sciences — organized by workflow stage.

## Repository Structure

```
academic-research-skills/
├── writing/              # 8 skills
├── literature-review/    # 9 skills
├── data-analysis/        # 14 skills
├── visualization/        # 6 skills
├── peer-review/          # 10 skills
├── presentations/        # 8 skills
├── citations/            # 2 skills
├── grants/               # 1 skill
├── brainstorming/        # 4 skills
├── data-sourcing/        # 3 skills
├── output-tools/         # 10 skills
├── project-management/   # 4 skills
├── CLAUDE.md
└── README.md
```

## Skill Categories

### writing/ — Academic Writing & Revision (8 skills)
- **academic-writing** — Academic writing methodology, IMRaD, FINER criteria
- **academic-writing-1.0.0** — Academic writing v1.0.0
- **academic-paper-write** — Academic paper writing support
- **academic-paper-writer** — Academic paper writer
- **econ-write** — Expert economics paper writing synthesizing 50+ guides
- **review-response** — Response letter drafting for R&R
- **revision-coordinator** — Orchestrate manuscript revisions
- **scientific-writing** — Core scientific writing

### literature-review/ — Literature Search & Discovery (9 skills)
- **lit-review** — Structured literature search and gap identification
- **lit-review-assistant** — Literature review assistant
- **literature-review** — Comprehensive literature review tools
- **academic-researcher** — Academic research and literature discovery
- **deep-research** — Multi-source research synthesis (5-step process)
- **deep-research-pro** — Professional deep research
- **academic-deep-research** — Academic deep research
- **Deep-Research-skills-master** — Deep research skills collection
- **conservative_retriever_skill-main** — Conservative retrieval for research

### data-analysis/ — Data Analysis & Statistics (14 skills)
- **data-analysis** — End-to-end R data analysis (5 phases)
- **exploratory-data-analysis** — EDA workflows
- **csv-data-summarizer** — CSV data summarization
- **r-analyst** — R statistical analysis with phases and techniques
- **r-econometrics** — R econometric analysis
- **python-panel-data** — Python panel data analysis
- **stata** — Stata programming support
- **stata-analyst** — Stata 6-phase analysis workflow
- **stata-regression** — Stata regression analysis
- **stata-data-cleaning** — Stata data cleaning utilities
- **stata-skill-main** — Stata skill
- **stata-accounting-research-master** — Stata for accounting research
- **StatsPAI_skill** — Statistical PAI
- **sociologist-analyst** — Sociological analysis

### visualization/ — Figures & Visualization (6 skills)
- **matplotlib** — Publication-quality matplotlib figures
- **scientific-visualization** — Journal-specific styles, colorblind-safe palettes
- **econ-visualization** — Economics-specific visualizations
- **paper-plot-skills-main** — Paper plotting utilities
- **galaxy-dawn-publication-chart-skill** — Publication chart generation
- **tikz** — TikZ/pgfplots LaTeX figures

### peer-review/ — Review & Quality Assurance (10 skills)
- **peer-review** — 7-stage systematic peer review toolkit
- **referee2** — Multi-agent peer review simulation
- **scholarpeer-econ** — Economics-focused peer review
- **paper-self-review** — Self-review before submission
- **review-paper** — Paper review assistance
- **scholar-evaluation** — Scholar evaluation tools
- **fletcher** — Defamiliarization audit (interpretation audit)
- **scientific-critical-thinking** — Evaluate scientific claims
- **consistency-checker** — 10-category pre-submission document audit
- **fact-checker** — Systematic fact verification with 6-level rating scale

### presentations/ — Slides & Presentations (8 skills)
- **beamer-presentation** — LaTeX Beamer with Metropolis theme
- **scientific-slides** — Scientific slide decks
- **academic-slides-main** — Academic presentation tools
- **academic-pptx-skill-main** — Academic PPTX creation
- **Aut_Sci_ppt-main** — PDF-to-PPTX Python package
- **Beamer_PPT_Skill** — Beamer PPT integration
- **beautiful_deck** — Beautiful presentation decks
- **compiledeck** — Compile Beamer decks

### citations/ — Citation Management (2 skills)
- **citation-management** — 5-phase citation workflow with Python scripts
- **crossref-main** — CrossRef API integration

### grants/ — Grant Proposals (1 skill)
- **research-grants** — NSF, NIH, DOE, DARPA, NSTC proposals (5 phases)

### brainstorming/ — Ideation & Hypothesis (4 skills)
- **hypothesis-generation** — 8-step structured hypothesis formulation
- **scientific-brainstorming** — 5-phase research brainstorming
- **research-ideation** — Research idea development
- **prompt-optimizer** — Prompt optimization for research

### data-sourcing/ — External Data Access (3 skills)
- **fred-economic-data** — FRED API for 800,000+ economic time series
- **sec-edgar-parser** — SEC EDGAR corporate filings parser
- **api-data-fetcher** — General API data retrieval

### output-tools/ — Specialized Output & Tools (10 skills)
- **market-research-reports** — 50+ page McKinsey/BCG-style reports
- **paper-2-web** — Convert academic papers to web format
- **latex-document-skill-main** — LaTeX document creation
- **latex-posters** — Academic poster creation
- **latex-tables** — Professional LaTeX tables
- **make-poster** — Poster generation
- **hbs-case-writer** — Harvard Business School case writing
- **interview-me** — Interview preparation
- **socrates-skill-main** — Socratic questioning for research
- **excalidraw-diagram-skill-main** — Excalidraw diagram creation

### project-management/ — Setup & Utilities (4 skills)
- **newproject** — Scaffold new research projects with standard structure
- **split-pdf** — PDF splitting and reading
- **strategic-analyst-skill-1.0.2** — Strategic project analysis
- **techdebt** — Technical debt management

## Installation

These skills are designed for use with Claude Code CLI. To install a skill:

1. Copy the skill folder from its category directory to your Claude Code skills directory
2. The skill will be available via `/skill-name` in Claude Code

## Requirements

Each skill may have specific requirements listed in its `SKILL.md` or `requirements.txt` file. Common dependencies include:
- Python 3.8+
- R with relevant packages
- Stata (for Stata-related skills)
- LaTeX distribution (for Beamer/LaTeX skills)

## Contributing

Contributions are welcome. Please place new skills in the appropriate category subdirectory.

## License

Individual skills may have their own licenses. Please check each skill's LICENSE file for details.


## Author

Weikai Li — Professor of Finance, City University of Hong Kong

## Repository

[https://github.com/franklee16/academic-research-skills](https://github.com/franklee16/academic-research-skills)
