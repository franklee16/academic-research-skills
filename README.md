# Academic Research Skills for Claude Code

A curated collection of Claude Code skills for academic research in economics, finance, and the broader social sciences — organized by the common **types of skills** a researcher needs across a project's lifecycle.

Each subfolder groups skills of one type (e.g., literature review, data analysis, paper writing). Inside each skill folder, a `SKILL.md` defines the skill's name, trigger conditions, and workflow. Skills with code may also include `references/`, `phases/`, `techniques/`, `src/`, or `requirements.txt`. A few entries are `.zip` archives of upstream skill collections — unzip to use.

## Common Types of Skills

The table below maps the **common skill types** to the folders in this repository. Detailed listings follow in the next section.

| Type | Folder | What it covers |
|------|--------|----------------|
| Ideation & brainstorming | `brainstorm-presearch/` | Research-question stress-testing, hypothesis generation, policy-doc analysis |
| Surveys & experiments | `running-surveys-experiments/` | 10 atomic skills from Bergman et al. (2020) on survey design, piloting, attrition audits |
| Literature search & reading | `lit-review/` | Paper discovery, deep research, paper summarization, reading notes |
| Humanities report suite | `humanities-report-writing-suite-main/` | Chinese humanities/social-science report writing (4 coordinated skills) |
| Data sourcing | `data-sourcing/` | External data access (FRED, SEC EDGAR, APIs) |
| Data analysis | `data-analysis/` | R, Stata, Python workflows, panel data, cleaning, EDA |
| Visualization | `visualization/` | Publication figures, matplotlib, TikZ, econ charts |
| Paper writing | `paper-writing/` | Drafting, econ/finance writing style, journal-specific guides, section-level writing |
| Humanizing & anti-AI prose | `humanizer/` | Strip AI tells and defensive writing from academic prose (9 skills) |
| Reference & citation | `reference-citation/` | BibTeX, CrossRef, reference checking |
| Review & revision | `review-revise/` | Peer review, referee simulation, R&R, fact-checking |
| Presentations | `presentations/` | Beamer, PPTX, scientific slides, deck compilation |
| Output tools | `output-tools/` | Posters, LaTeX tables/figures, diagrams, paper-to-web, econ tables/figures |
| Research promotion | `promote-skill/` | Turn papers into social media posts |
| Grant writing | `grant-writing/` | NSF, NIH, NSFC, and general proposal writing |
| Research workflow | `research-workflow/` | Pipelines, LLM-based measurement, validation, replication |
| Theory & modeling | `theory-skills/` | Theoretical toolbox, economic model building |
| Science databases | `science-skills/` | Bioinformatics databases (PubMed, AlphaFold, UniProt, etc.) |
| Nature journal suite | `nature-skills-main/` | Nature-style writing, citation, figures, response, paper-to-PPT |
| Journal skill packs (95 packs, 1600 skills) | `Awesome-Journal-Skills-main/` | Per-journal skill packs (AER, Econometrica, 经济研究, Cell, Nature, AAAI, AMJ ...) — see its own README |
| Tech transfer | `tech-transfer/` | Patent disclosure, software copyright (Chinese 软著), code-to-patent |

## Skills by Category

### Ideation & Brainstorming (`brainstorm-presearch/`)
- **research-brainstorm** — Senior-scholar dialogue that stress-tests research questions
- **hypothesis-generation** — Structured 8-step hypothesis formulation
- **scientific-brainstorming** — 5-phase research brainstorming
- **research-ideation** — Develop research ideas from seed questions
- **Econ-thesis-idea-main** — Economics thesis idea generation
- **economist-analyst** — Economist-style analysis and framing
- **good-question-main** — Sharpening research questions
- **econane** — Enrich economics arguments with anecdotal evidence (cases, media, disclosures) layered with academic findings
- **readpolicy** — Analyze policy documents (政策文本) into summary, keywords, and economics research directions (Word output)

### Surveys & Experiments (`running-surveys-experiments/`)

10 atomic skills distilled from Bergman, Chinco, Hartzmark, Sussman (2020), "Survey Curious?" — see the folder's `INDEX.md`:

- **survey-design-checklist** — Umbrella three-constraint check (ability × willingness × interpretation) on draft questions
- **clarity-concreteness**, **avoid-leading-questions**, **converging-evidence-design** — Question-design layer
- **pilot-protocol**, **quality-checks-diagnosis**, **selective-attrition-audit**, **relative-vs-absolute** — Operations and interpretation layer
- **platform-selection**, **fair-pay-and-reputation** — Platform fit and ethics layer

### Literature Search & Reading (`lit-review/`)
- **lit-review**, **lit-review-assistant**, **lit-review-summary** — Structured literature search and gap identification
- **literature-review**, **literature-review-master-main** — Comprehensive review toolkits
- **academic-researcher**, **academic-deep-research** — Academic literature discovery
- **deep-research**, **storm-deepresearch-skill**, **storm-research** — Multi-source research synthesis (Stanford STORM-style)
- **arxiv** — arXiv paper search and retrieval
- **cnki-skills-master** — CNKI (China National Knowledge Infrastructure) access
- **auto-paper-skill**, **yomitoki-main** — Automated paper reading
- **Paper-Reading-Skills-main**, **paper-summary-skills-main**, **paper-insight**, **paper-evidence-distiller** — Paper summarization and evidence extraction
- **real-literature-trace** — Verified literature tracing (anti-hallucination)
- **split-pdf** — PDF splitting for large papers
- **readecon** — Structured Chinese reading notes for economics papers
- **glance** — Rapid batch overview across multiple papers (compact Chinese PDF)
- **lr** (LR) — Literature review writer enforcing verified DOIs and APA 7th
- **paper-researcher** — Chinese paper explanation plus citation-landscape / field citation-tree exploration
- **research-defense-radar-main** — Monitor competitor landscape, novelty risk, and scooping risk for an ongoing project

### Data Sourcing (`data-sourcing/`)
- **fred-economic-data** — FRED API for 800,000+ economic time series
- **sec-edgar-parser** — SEC EDGAR corporate filings parser
- **api-data-fetcher** — General API data retrieval
- **polymarket-earnings** — Polymarket earnings calendar to CSV
- **find-data** — Data discovery and feasibility assessment
- **dril-dataset-construction** — Dataset construction workflow
- **universal-data-loader** — Universal data loading utilities

### Data Analysis (`data-analysis/`)
- **r-analyst**, **r-econometrics** — R statistical and econometric workflows
- **stata**, **stata-analyst**, **stata-regression**, **stata-data-cleaning**, **stata-skill-main**, **stata-accounting-research-master** — Stata analysis pipelines (cleaning to regression)
- **python-panel-data**, **vaex**, **tidy-data**, **universal-data-analyst-1.0.3** — Python analysis for panels and large data
- **exploratory-data-analysis**, **csv-data-summarizer** — EDA and quick summarization
- **StatsPAI_skill**, **statsmodels** — Statistical modeling
- **sociologist-analyst** — Sociological analysis
- **data-analysis**, **data-analysis-router-main** — End-to-end analysis dispatch
- **econometric-research-writing** — Writing up econometric results
- **data-storytelling** *(zip)* — Turning results into narratives
- **autonomous-qa-loop**, **explain-diff**, **neishengxing-main**, **visualization-expert** — QA, diff explanation, and inline visualization
- **lieflat-charts-main** — Template-driven single-file HTML charts and full-page reports (Mono-first palette)
- Zips: `csv-data-summarizer`, `data-analyst`, `huashu-excel-report`, `statistical-analysis`, `statsmodels`, `universal-data-loader`

### Visualization (`visualization/`)
- **matplotlib** — Publication-quality matplotlib figures
- **scientific-visualization** — Journal-specific styles, colorblind-safe palettes
- **econ-visualization** — Economics-specific charts
- **paper-plot-skills-main** — Paper plotting utilities
- **publication-chart-skill** — Publication chart generation
- **tikz** — TikZ/pgfplots LaTeX figures
- **copyplot** — Reverse-engineer a scientific figure image into reproducible Matplotlib code
- **thu-digitizer-main** — Extract and validate numeric data from chart images and PDF figures

### Paper Writing (`paper-writing/`)
- **academic-writing**, **academic-paper-writer**, **scientific-writing** — Core drafting methodology
- **econ-write**, **econ-write-style** — Economics writing synthesizing 50+ guides
- **econ-writing-skills-main** — Section-level econ writing: titles, abstract, introduction, conclusion (4 sub-skills)
- **write-literature-review** — Write the literature-review section of an empirical paper as contribution positioning
- **paper-taste** — Research taste and writing quality for empirical finance/economics
- **ft50-empirical-writing-main** — Top-journal (FT50) empirical writing
- **jf-skill-1.0.0** — Journal of Finance writing conventions
- **cn-top-econ-writing** — Top Chinese economics-journal writing
- **management-science-writing-main**, **marketing-science-writing-main** *(zip)* — Field-specific writing
- **practitioner-finance-voice** — Rewrite for practitioner outlets (FAJ / JPM / JOI / JWM / JFI)
- **journal-adapt-skill** — Adapt drafts to journal styles
- **nature-story-main** — Turn engineering research ideas into general-interest story architectures
- **research-writing-skill-main** — 30 Chinese prompt templates covering the full paper-writing workflow
- **nan-paper-polish**, **niulai-paper-polish-main** — Manuscript polishing with evidence-calibrated workflows
- **humanizer-zh-academic**, **avoid-ai-writing-main** — De-AI-ify academic prose (Chinese and English)
- **prose-revision**, **prose-revision-skill** — Idea-flow revision before polish
- **ai-econ-finance-research**, **good-story-main**, **PaperSpine-main** — Research framing and storytelling

### Humanizing & Anti-AI Prose (`humanizer/`)

- **humanizer-zh-academic** — De-AI Chinese academic prose
- **avoid-ai-writing-main** — Strip English AI writing tells
- **academic-humanizer-main** — Clarity and voice for AI-assisted papers, theses, grant proposals
- **humanizer_academic-main** — Remove AI-writing signs from academic medical manuscripts
- **anti-defensive-writing**, **anti-defensive-writing-en** — Stop defensive (self-undermining) writing, Chinese and English
- **defensive-writing-checker**, **prevent-defensive-ai-writing** — Audit drafts for defensive, over-apologetic patterns
- **humanities-writing-zh-main** — Chinese humanities (文史) scholarly writing and revision

### Humanities Report Suite (`humanities-report-writing-suite-main/`)

Four coordinated skills for Chinese humanities/social-science reports (survey, interview, case, policy, archival material):

- **humanities-report-writer** — Orchestrate traceable, well-argued Chinese report drafting
- **source-grounded-research** — Web-grounded retrieval, fact-checking, and citation control
- **humanizer** — Remove AI-writing signs from report text
- **word-report-delivery** — Produce submission-ready formatted Word `.docx` output

### Reference & Citation (`reference-citation/`)
- **citation-management** — 5-phase citation workflow with Python scripts
- **academic-citation-manager** — Bibliography management
- **citation-check-skill-main**, **reference-checker** — Verify references and DOIs
- **crossref-main** — CrossRef API integration
- **chinese-reference-formatter-skill-main** — GB/T 7714 Chinese reference formatting
- **scipilot-cite-skill-main** — AI-assisted citation suggestion

### Review & Revision (`review-revise/`)
- **peer-review**, **review-paper**, **review-paper2** — Manuscript evaluation toolkits
- **academic-manuscript-review** — Candid pre-submission diagnostic for management/org-science manuscripts
- **Top-journal-manuscript-review-main** — Audit and restructure manuscripts for Nature/Science/Cell/PNAS-tier journals
- **mhe-identification** — Angrist-Pischke (MHE, modernized) evaluation of identification strategies; draft endogeneity sections
- **referee2**, **scholarpeer-econ** *(zip)* — Multi-agent referee simulation for economics
- **publication-coach** — Pre-submission diagnostic (Edmans' 1,000-rejections framework)
- **paper-self-review** — Author self-review before submission
- **paper-revision-master**, **revise-paper**, **review-response**, **revision-coordinator**, **comment-synthesis** — R&R workflow and response letters
- **referee-report-improve** — Improve referee reports you write
- **consistency-checker** — 10-category pre-submission document audit
- **fact-checker** — 6-level fact verification
- **fletcher** — Defamiliarization/interpretation audit
- **scientific-critical-thinking** — Evaluate scientific claims
- **scholar-evaluation**, **paper-analysis** — Paper and scholar evaluation
- **paper-workshop-main** *(zip)*, **paperjury-main** *(zip)* — Workshop and jury-style reviews

### Presentations (`presentations/`)
- **beamer-presentation**, **Beamer_PPT** — LaTeX Beamer (Metropolis and PPT bridges)
- **compiledeck**, **beautiful_deck** — Deck compilation and styling
- **paper-slides** — Beamer decks from research papers per Weikai Li's slide style guide
- **scientific-slides**, **academic-slides** — Scientific and academic decks
- **academic-pptx-skil**, **aut_sci_ppt**, **proslide-main** — PPTX generation and PDF-to-PPTX
- **html-ppt-skill-main**, **marp-slides-creator** — HTML/Marp slide formats
- **Paper-to-Presentation**, **paper-motivator**, **paper-2-web** — Convert papers to talks and web
- **latex-posters** — LaTeX academic posters

### Output Tools (`output-tools/`)
- **latex-document-skill-main** — Universal LaTeX document creation
- **latex-tables**, **latex-posters** — Professional tables and posters
- **econtable** — Journal-ready economics tables from estimation results
- **econfigure** — Publication-ready economics figures and plotting code
- **code-to-notation-table** — Word notation dictionary mapping code variables to paper symbols
- **make-poster** — HTML conference poster (printable to PDF)
- **excalidraw-diagram-skill-main**, **diagram-generator-1.1.1** — Diagram creation
- **lieflat-charts-main** — Template-driven HTML charts and full-page reports
- **extract-figures**, **extract-tables** — Pull figures and tables from PDFs
- **academic-figure-prompt** — Prompt templates for figure generation
- **market-research-reports** — 50+ page McKinsey/BCG-style reports
- **paper-2-web** — Convert papers to web format
- **llm-replication-disclosure** — LLM-use disclosure for replication packages

### Research Promotion (`promote-skill/`)

- **paper-to-social** — Turn a paper into LinkedIn posts, X threads, 小红书 posts, and Substack essays

### Grant Writing (`grant-writing/`)
- **research-grants** — NSF, NIH, DOE, DARPA, Taiwan NSTC proposals
- **academic-grant**, **write-grant-proposal-main** — General proposal writing
- **Chinese-Grant-Writer-Skills-main**, **NSFC-skills-main** — Chinese NSFC (国家自然科学基金) grant writing
- **nsfc-agent-skills-master** — NSFC agent suite: `nsfc-write` (撰写指南), `nsfc-literature` (OpenAlex 文献检索引用), `nsfc-figure` (概念图/技术路线图), `nsfc-policy` (2026 申报政策速查)

### Research Workflow (`research-workflow/`)
- **llm-research-workflow** — LLM-based data pipelines and measures in empirical research (Ferrara 2026)
- **codex-paper-skills-main**, **monthly-workflow-main**, **sci-ssci-polishing** — Workflow templates
- Zips: `empirical-paper-main`, `llm-corpus-pipeline`, `llm-measurement-error`, `llm-prompt-design`, `llm-validation-protocol`, `research-pipeline`, `verify-regression-output`, `verify-slide-deck`

### Theory & Modeling (`theory-skills/`)
- **theorist-toolbox-master** — Theorist's toolbox for economic model building
- **pAI-Econ-claude-main** — Economic theory with AI assistance
- **general-equilibrium-model-builder** — Build and solve Walrasian GE models with theory derivations and Julia computation

### Science Databases (`science-skills/`)
Bioinformatics and natural-science data access. Each subfolder targets one database or task: **pubmed_database**, **clinical_trials_database**, **alphafold_database_fetch_and_analyze**, **alphagenome_single_variant_analysis**, **uniprot_database**, **pdb_database**, **gnomad_database**, **clinvar_database**, **chembl_database**, **pubchem_database**, **dbsnp_database**, **gtex_database**, **human_protein_atlas_database**, **encode_ccres_database**, **ensembl_database**, **interpro_database**, **jaspar_database**, **opentargets_database**, **openfda_database**, **quickgo_database**, **reactome_database**, **string_database**, **unibind_database**, **ucsc_conservation_and_tfbs**, **embl_ebi_ols**.
Literature helpers: **literature_search_arxiv**, **literature_search_biorxiv**, **literature_search_europepmc**, **literature_search_openalex**.
Sequence/structure tools: **ncbi_sequence_fetch**, **protein_sequence_msa**, **protein_sequence_similarity_search**, **foldseek_structural_search**, **pymol**.
Shared utilities: **science_skills_common** (HTTP client with rate limiting), **workflow_skill_creator**, **uv**.

### Nature Journal Suite (`nature-skills-main/`)
End-to-end skills tuned to *Nature*-style publication:

- **nature-polishing** — Polish, restructure, or translate prose into Nature-leaning English
- **nature-citation** — Nature-style citation formatting
- **nature-figure** — Nature-style figure preparation
- **nature-data** — Nature-style data and reporting
- **nature-response** — Response-to-reviewers for Nature submissions
- **nature-paper2ppt** — Convert Nature papers to presentation slides

### Awesome Journal Skills (`Awesome-Journal-Skills-main/`)

A 95-pack, 1600-skill index of per-journal skill packs maintained by CoPaper.AI (Stanford REAP) — AER/Econometrica/AEJ, 经济研究/金融研究 and other Chinese journals, Cell/Nature/Science families, AAAI/NeurIPS conference packs, AMJ/AMR/ASQ management journals, and more. Browsable by journal cover in its own `README.md`; each pack holds writing, review, and submission skills for that venue.

### Tech Transfer (`tech-transfer/`)

- **software-copyright-materials** — Chinese 软件著作权 application materials (source extraction, manuals, forms)
- **code2patent** — Extract technical evidence from a code repo and draft Chinese invention-patent materials (交底书 → 权利要求布局卡 → 专利初稿)
- **patent-disclosure-skill-main** *(zip)* — Patent disclosure drafting

## Installation

These skills target Claude Code. To install one:

1. Copy the skill folder into your Claude Code skills directory (e.g., `~/.claude/skills/`).
2. For zipped archives, unzip first.
3. Skills with `pyproject.toml` or `requirements.txt` need dependencies installed: `pip install -e .` or `pip install -r requirements.txt`.
4. Invoke via `/skill-name` inside Claude Code.

## Requirements

Common dependencies across skills: Python 3.8+, R with relevant packages, Stata (for Stata skills), a LaTeX distribution (for Beamer/LaTeX skills), and a Firecrawl/Tavily API key for web-based literature skills.

## Author

Weikai Li — Associate Professor of Finance, City University of Hong Kong

## Repository

<https://github.com/franklee16/academic-research-skills>
