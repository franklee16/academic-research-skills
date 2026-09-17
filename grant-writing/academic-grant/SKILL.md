---
name: academic-grant
description: |
  Generate or fill in academic grant application forms (project statement, education plan,
  pathway to impact, references) using draft research material. MUST trigger when the user
  mentions: grant application, grant proposal, project statement, funding application,
  RGC/GRF/ECS/TRS proposal, filling in grant forms, academic grant, research grant, or any
  task involving converting research papers/drafts into grant application documents. Also
  trigger when the user provides sample grant forms and asks to fill them with project content,
  or says things like "write my grant", "help with the grant application", "fill in the
  application form". This skill uses a multi-agent approach: parallel section drafting,
  cross-section review with scored feedback, revision/assembly, citation verification, and
  supporting document generation.
version: 1.0.0
argument-hint: "[@blank_form.docx] [using @paper_draft.docx] [following sample @sample.docx]"
allowed-tools: [Read, Write, Edit, Bash, Agent]
---

# Academic Grant Writing Skill

## Overview

This skill produces complete grant application documents from research project material.
It handles the main project statement, education plan, pathway to impact, and references.
The workflow uses parallel agents for efficiency and a review-revision cycle for quality.

## What This Skill Does

1. Reads blank grant forms, sample documents, and project source material
2. Converts DOCX inputs to markdown for agent consumption
3. Dispatches parallel agents to draft each section of the form
4. Reviews all sections with scored feedback (0-100)
5. Revises based on review and assembles a unified document
6. Verifies citations against web sources and fixes metadata errors
7. Generates supporting documents (education plan, pathway to impact, references)
8. Produces final DOCX files with proper formatting

## What This Skill Does NOT Do

- Write the underlying research (it needs a paper draft or results as input)
- Invent empirical findings (all coefficients, p-values, and findings come from source material)
- Handle grant budgets or CVs (these require institution-specific templates)
- Replace human judgment on framing and contribution claims

## When to Use

Use this skill when the user has:
- A research paper draft, working paper, or preliminary results
- A blank grant application form (DOCX)
- Optionally: a sample completed form from a prior application

The skill works for economics, finance, accounting, and related social science grants
(RGC/GRF/ECS in Hong Kong, NSF/NIH in the US, ERC in Europe, etc.).

## Workflow

### Phase 1: Preparation

1. Identify files. Look for:
   - Blank grant form: typically named `Project_statement.docx`, `Application_form.docx`, etc.
   - Sample form: often named `*_sample.docx` or `*_example.docx`
   - Source material: paper drafts (`*.tex`, `*.docx`), result summaries, literature maps
2. Convert all DOCX files to markdown using `markitdown` or `python-docx` extraction.
3. Read the converted markdown to understand:
   - The form's section structure (e.g., 1. Research Context, 2. Research Questions, 3. Methodology)
   - The sample's paragraph structure, citation style, and level of detail
4. Create a task working directory: `agent_tasks/grant_YYYYMMDDHH/`
5. Write a brief execution plan to `agent_tasks/grant_YYYYMMDDHH/plan.md`:
   - List source files, sample files, target output files
   - Map each form section to its source material
   - Note any special requirements (word limits, specific formats)

### Phase 2: Draft Sections (Parallel)

Dispatch one agent per major section of the grant form. Agents run in parallel.

For each section, the agent receives:
- The section's source material (relevant parts of the paper draft)
- The corresponding section from the sample document (structural template)
- A specific output file path

**Agent prompt:** See `references/agent-prompts.md` → "Section Drafting Agent".

**Rules:**
- Each agent saves output to its own file immediately (do NOT return full text to main agent)
- The main agent only receives brief status summaries
- Maximum 8 parallel agents per phase
- If a form has more than 8 sections, group small sections together

### Phase 3: Review (1 Agent)

After all drafting agents complete, dispatch one review agent.

**Agent prompt:** See `references/agent-prompts.md` → "Review Agent".

**Key review checks:**
- Structure compliance: does each section match the form template?
- Completeness: are all required subsections present?
- Consistency: do citations introduced in later sections appear in the literature review?
- Accuracy: are coefficients, p-values, and sample sizes correct against source material?
- Cross-references: do section references point to sections that actually exist?
- Style: first-person plural, inline citations, academic tone

The review produces a scored document (`review_feedback.md`) with:
- Per-section scores (0-100)
- Issues by severity: Critical / Major / Minor
- A completeness checklist
- Verdict: PASS / REVISE / MAJOR REVISION

### Phase 4: Revise + Assemble (1 Agent)

Dispatch one agent to apply all review fixes and assemble the final document.

**Agent prompt:** See `references/agent-prompts.md` → "Revision + Assembly Agent".

**Required actions:**
1. Address ALL Critical and Major issues from the review
2. Standardize header formatting (remove markdown #, use `**Section Title**`)
3. Convert LaTeX math to plain text (Word cannot render `$$...$$`)
4. Assemble sections in correct order
5. Save assembled markdown to `assembled_final.md`
6. Run the DOCX conversion script:
   ```
   python ~/.claude/skills/academic-grant/scripts/assemble_docx.py assembled_final.md Project_statement.docx
   ```

The script auto-installs `python-docx` if missing.

### Phase 5: Citation Verification (3 Parallel Agents)

After the project statement is assembled, verify all citations.

Dispatch 3 agents in parallel:
- **Agent A:** Extract in-text citations → `citations_extracted.txt`
- **Agent B:** Extract reference entries → `references_extracted.txt`
- **Agent C:** Verify metadata via web search → `citation_verification.txt`

**Agent prompts:** See `references/agent-prompts.md` → "Citation Extraction Agent A/B" and "Citation Verification Agent".

After agents complete, the main agent cross-checks:
1. Build Set A (cited in text) and Set B (in reference list)
2. Find: cited-but-not-referenced, referenced-but-not-cited, year mismatches
3. Read `citation_verification.txt` for metadata errors
4. Fix the references file and regenerate the DOCX

**Common issues to catch:**
- References listed as "forthcoming" that have since been published
- Wrong years (agent found paper published in 2026, listed as 2025)
- Author mismatches (cited as "Borghesi et al. 2019" but reference is 2015)

### Phase 6: Supporting Documents (2-3 Parallel Agents)

Generate supporting documents using the completed project statement as source.

Typical supporting documents:
- **Education Plan:** 3 paragraphs (teaching, RA training, classroom integration)
- **Pathway to Impact:** short/medium-long run impact + risks
- **References:** APA format, journal names in italics, alphabetical order

Each agent reads its sample + the completed project statement.

**Agent prompt:** See `references/agent-prompts.md` → "Supporting Document Agent".

Convert each to DOCX using the same script:
```
python ~/.claude/skills/academic-grant/scripts/assemble_docx.py education_plan.md Education_plan.docx
```

For the **References** DOCX, journal names must be in italics. If the assembled markdown uses `*Journal Name*` markers, the script handles this correctly.

## Quality Thresholds

| Gate | Score | Action |
|------|-------|--------|
| Section draft | ≥ 85/100 | Accept; < 85 requires revision |
| Review verdict | REVISE | Fix all Critical + Major issues |
| Citation check | 0 mismatches | All cited works must have references |
| Final DOCX | No formatting errors | No markdown artifacts, proper headings |

## Output Files

The skill produces these files in the task directory:

```
agent_tasks/grant_YYYYMMDDHH/
├── plan.md                    # Execution plan
├── section_*.md               # Individual drafted sections
├── review_feedback.md         # Scored review
├── assembled_final.md         # Revised, assembled project statement
├── citations_extracted.txt    # In-text citation list
├── references_extracted.txt   # Reference entry list
├── citation_verification.txt  # Metadata verification results
├── education_plan.md          # Education plan draft
├── pathway_to_impact.md       # Pathway to impact draft
└── references.md              # Reference list
```

And these DOCX files in the project directory:
- `Project_statement.docx`
- `Education_plan.docx`
- `Pathway2Impact.docx`
- `References.docx`

## Key Design Patterns

1. **Sample-driven drafting.** Every agent receives both source material AND a sample. The sample provides structure, tone, and citation style.
2. **Section-level parallelism.** Split the form into sections, one agent each. This maximizes parallelism while keeping sections coherent.
3. **Review produces scores + specific issues.** Not just prose feedback — numbered issues with severity ratings enable systematic revision.
4. **Revision addresses ALL major issues.** The revision agent is given a checklist of issues from the review and must address each one.
5. **Citation verification is standard.** After assembly, always verify citations against web sources. Catch year errors, "forthcoming" papers that published, and phantom references.
6. **DOCX formatting via script.** Use the bundled `assemble_docx.py` script for consistent formatting: Times New Roman 12pt, 1-inch margins, heading hierarchy, italics for journal names.

## Tips for Best Results

- Provide a **sample document** if available. The skill works without one, but output quality is higher with a structural template.
- Ensure **source material is readable**. Convert PDFs or LaTeX to markdown before starting. The skill can do this conversion but it takes time.
- Be specific about **word limits** if the grant form has them. Include this in the execution plan.
- For **complex forms** (e.g., NSF with 15 sections), group related sections into larger chunks (3-4 agents instead of 15).
- If the user says "shorten" or "trim," reduce the literature review to the most relevant studies and the results to the key findings only.

## Troubleshooting

**Agent outputs are inconsistent in tone:**
→ Ensure all agents receive the same sample document for tone reference.

**Review scores are low (< 80):**
→ The source material may be insufficient. Ask the user for additional content (e.g., a more complete paper draft).

**DOCX conversion fails:**
→ The script auto-installs `python-docx`. If this fails, the user may need to run `pip install python-docx` manually.

**Citation verification finds many errors:**
→ This is common with working papers and forthcoming articles. Focus on fixing year mismatches and removing phantom references.
