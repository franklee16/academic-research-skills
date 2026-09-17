---
name: revise-paper
description: >
  Autonomous paper revision from peer review reports. TRIGGER when: user has
  referee reports and wants to revise a paper, or says "revise my paper",
  "handle the reviews", "process referee reports", "address the referee
  comments". Works with both LaTeX (.tex) and Word (.docx) papers. Parses
  reports into a deduplicated JSON checklist, clusters issues, dispatches
  parallel editing agents, applies edits with git commits, compiles/validates
  after each batch with auto-fix, runs verification, and produces a
  response-to-reviewers letter. Halts on irreducible ambiguity.
argument-hint: "[paper.tex|paper.docx] [reports-folder/]"
allowed-tools: Agent, Read, Glob, Grep, Write, Edit, Bash, WebSearch
---

# Revise Paper — Autonomous Revision Workflow

Autonomous multi-agent pipeline that takes a paper (LaTeX `.tex` or Word `.docx`) and peer review reports, revises the paper, and produces a verified response-to-reviewers letter.

**Input:** `$ARGUMENTS` — path to paper file (`.tex` or `.docx`), then path to reports folder. Both optional (will infer from project if omitted).

---

## Pre-flight

1. Parse `$ARGUMENTS`:
   - First argument = paper file path (`.tex` or `.docx`). If omitted, search for `paper/main.tex`, `main.tex`, `paper.tex`, `main.docx`, `paper.docx`, or ask.
   - Second argument = reports folder path. If omitted, check `quality_reports/referee_reports/`, then ask.
2. Verify paper file exists and is readable. If not, HALT.
3. **Detect format**: set `PAPER_FORMAT = "latex"` for `.tex` files, `"word"` for `.docx` files. This variable controls branching throughout all phases.
4. Verify reports folder exists and contains files. If not, HALT.
5. Create working directories if missing: `quality_reports/edits/`, `quality_reports/plans/`.
6. Get today's date for file naming: `DATE = YYYY-MM-DD`.
7. Initialize revision progress log: `quality_reports/revision_progress.md`.

### Format-Specific Setup

**If `PAPER_FORMAT = "latex"`:**
- Verify `xelatex` is available (`xelatex --version`). If not, try `pdflatex`.
- Compilation uses: `xelatex → biber → xelatex → xelatex` (or `pdflatex` fallback).

**If `PAPER_FORMAT = "word"`:**
- Verify `python` is available.
- Check if `python-docx` is installed: `python -c "import docx"`. If not, install: `pip install python-docx`.
- Check if `markitdown` is installed: `python -c "import markitdown"`. If not, install: `pip install markitdown`.
- Create a helper script `quality_reports/word_edit_helper.py` for applying paragraph-level edits to `.docx` files (see Phase 4).

---

## Phase 1: Intake & Parsing

**Goal:** Extract every discrete comment from every report, classify, deduplicate, and save as a structured checklist.

### Step 1.1 — Read All Inputs
- Read the full paper file:
  - **If `PAPER_FORMAT = "latex"`**: Read the `.tex` file directly with the Read tool.
  - **If `PAPER_FORMAT = "word"`**: Convert `.docx` to markdown for processing:
    ```bash
    python -c "from markitdown import MarkItDown; md = MarkItDown(); result = md.convert('[paper.docx]'); print(result.text_content)" > quality_reports/paper_extracted.md
    ```
    Read the extracted markdown. Also note: the original `.docx` paragraph structure will be referenced when applying edits (paragraph index + first 80 chars as locator).
- Read every file in the reports folder (`.tex`, `.md`, `.txt`, `.pdf`, `.docx`).
- If a report file is PDF, read with the Read tool (use `pages` parameter for large PDFs).
- If a report file is `.docx`, convert with markitdown the same way as the paper.

### Step 1.2 — Extract Comments
- Parse each report into discrete comments. A "comment" is a single actionable criticism or request.
- Number sequentially across all reports: `R1-C1`, `R1-C2`, `R2-C1`, etc. (R = referee number).
- For each comment, extract:
  - `id`: unique identifier (e.g., `R1-C3`)
  - `referee`: which referee (1, 2, 3...)
  - `quote`: exact quote from the report (preserve original wording)
  - `location`: section/page/paragraph the comment targets (infer from context)
  - `classification`: one of `NEW_ANALYSIS`, `CLARIFICATION`, `REWRITE`, `DISAGREE`, `MINOR`
  - `severity`: one of `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`
  - `section`: which paper section is affected (e.g., `Introduction`, `Table 3`, `Appendix B`)

### Step 1.3 — Classification Rules
| Signal in Comment | Class | Severity |
|---|---|---|
| "run additional regression", "test for X", "control for Y", "robustness check", "alternative specification" | `NEW_ANALYSIS` | `HIGH` or `CRITICAL` |
| "unclear", "please explain", "elaborate on", "more discussion of" | `CLARIFICATION` | `MEDIUM` |
| "restructure", "rewrite", "reorganize", "major revision of section" | `REWRITE` | `HIGH` |
| "the authors claim X but Y", "I disagree with", "this argument is flawed" | `DISAGREE` | `HIGH` or `CRITICAL` |
| "typo", "formatting", "missing citation", "label", "notation" | `MINOR` | `LOW` |
| "add reference to", "discuss related work" | `CLARIFICATION` | `MEDIUM` |
| "the identification strategy is not convincing" | `DISAGREE` or `NEW_ANALYSIS` | `CRITICAL` |
| "table/figure should show X" | `NEW_ANALYSIS` if requires data, `CLARIFICATION` if just presentation | varies |

**Ambiguity rule:** If a comment could be two classes, pick the higher-effort one. If genuinely ambiguous, classify as `DISAGREE` and HALT for user judgment.

### Step 1.4 — Deduplication
- Compare all comments pairwise.
- If two comments from different referees target the same issue (e.g., both ask for robustness check X), merge into one entry with both quotes preserved.
- Mark merged entries with `duplicate_of: [original_id]`.
- Keep the more detailed quote as primary.

### Step 1.5 — Save Checklist
Write to `quality_reports/revision_checklist_[DATE].json`:
```json
{
  "paper": "path/to/paper.tex",
  "paper_format": "latex",
  "date": "YYYY-MM-DD",
  "referee_count": 2,
  "total_issues": 15,
  "classification_counts": {
    "NEW_ANALYSIS": 3,
    "CLARIFICATION": 5,
    "REWRITE": 2,
    "DISAGREE": 1,
    "MINOR": 4
  },
  "issues": [
    {
      "id": "R1-C1",
      "referee": 1,
      "quote": "exact text...",
      "location": "Section 3, paragraph 2",
      "classification": "CLARIFICATION",
      "severity": "MEDIUM",
      "section": "Data",
      "duplicate_of": null,
      "status": "PENDING"
    }
  ]
}
```

Append to progress log:
```
## [DATE] Phase 1 Complete
- Parsed N reports, extracted M comments
- Deduplicated to K unique issues
- Classification breakdown: [counts]
- Checklist saved to: quality_reports/revision_checklist_[DATE].json
```

---

## Phase 2: Clustering & Planning

**Goal:** Group related issues, determine execution order, identify items that need user input.

### Step 2.1 — Cluster Issues
Group issues by proximity and topic:
- **Section cluster**: all issues targeting the same paper section (e.g., "Introduction", "Results")
- **Table/Figure cluster**: all issues about the same table or figure
- **Concept cluster**: issues about the same concept across sections (e.g., "identification strategy" in both Intro and Empirical Strategy)

Each cluster gets:
- `cluster_id`: `C1`, `C2`, ...
- `issue_ids`: list of issue IDs in this cluster
- `target_sections`: which paper sections this cluster touches
- `files_affected`: which `.tex` files will be edited
- `dependencies`: list of cluster IDs that must complete first (empty if independent)

### Step 2.2 — Dependency Resolution
- Clusters editing the **same file** → sequential (order by severity: CRITICAL first)
- Clusters editing **different files** → can run in parallel
- Clusters with conceptual dependencies (e.g., one cluster defines a term another cluster uses) → sequential

### Step 2.3 — Flag Items Requiring User Input
- **ALL `NEW_ANALYSIS` items**: HALT. Present each to user:
  > "Referee [N] requests: [quote]. This requires new estimation/data work. Options:
  > (1) Approve new analysis → will dispatch coder agent
  > (2) Defer → will note as 'planned for revision' in response letter
  > (3) Dismiss → will draft diplomatic pushback"
- **ALL `DISAGREE` items**: HALT. Present each to user:
  > "Referee [N] disagrees with: [quote]. What is your position?
  > (1) Concede fully → revise as requested
  > (2) Partial concession → describe what you accept
  > (3) Push back → describe your counter-argument, I'll draft diplomatic response"
- **Wait for user response** on all flagged items before proceeding.

### Step 2.4 — Save Plan
Write to `quality_reports/plans/[DATE]_revision-plan.md`:
```markdown
# Revision Plan — [DATE]

## Summary
- Total issues: N
- Auto-executable: N (CLARIFICATION, REWRITE, MINOR)
- Flagged (NEW_ANALYSIS): N — [user decisions]
- Flagged (DISAGREE): N — [user decisions]

## Execution Plan
### Batch 1 (parallel)
- Cluster C1: [description] — issues [R1-C1, R1-C3]
- Cluster C2: [description] — issues [R2-C1, R2-C4]

### Batch 2 (sequential after C1)
- Cluster C3: [description] — issues [R1-C2]

### Batch 3 (after user approval)
- Cluster C4: NEW_ANALYSIS — [coder task description]
```

Append to progress log:
```
## [DATE] Phase 2 Complete
- Created N clusters
- M clusters auto-executable, K clusters flagged
- Execution plan saved to: quality_reports/plans/[DATE]_revision-plan.md
- User decisions recorded for flagged items
```

---

## Phase 3: Parallel Dispatch

**Goal:** Spawn writer subagents to propose edits for each cluster. Context protection: subagents save to files, return only status summaries.

### Step 3.1 — Dispatch AUTO Clusters

For each batch of independent clusters, dispatch all in parallel using the Agent tool.

**If `PAPER_FORMAT = "latex"`:**

```
Agent({
  description: "Revise cluster C1: [description]",
  subagent_type: "writer",
  prompt: [
    "You are revising a specific section of an academic paper based on peer review feedback.",
    "",
    "PAPER FILE: [path to .tex]",
    "SECTIONS TO REVISE: [section names]",
    "",
    "REVIEWER COMMENTS TO ADDRESS:",
    "- [R1-C1]: [quote]",
    "- [R1-C3]: [quote]",
    "",
    "FULL TEXT OF TARGET SECTIONS:",
    "[paste the full text of the relevant sections]",
    "",
    "CONSTRAINTS:",
    "- Make MINIMAL edits. Change only what is needed to address the specific comments.",
    "- Preserve existing notation, terminology, and style exactly.",
    "- Do not rewrite surrounding text that is not under review.",
    "- Do not change any \\label{}, \\ref{}, or \\cite{} commands unless the comment specifically asks.",
    "- Preserve all table structures (column counts, alignment).",
    "",
    "OUTPUT:",
    "Save your proposed edits to: quality_reports/edits/cluster_C1.md",
    "",
    "Format each edit as:",
    "### Issue [R1-C1]",
    "**File:** [file path]",
    "**Location:** [section/line context]",
    "**Old text:**",
    "```latex",
    "[exact text to replace]",
    "```",
    "**New text:**",
    "```latex",
    "[replacement text]",
    "```",
    "**Explanation:** [why this addresses the comment]",
    "",
    "After saving the file, report back ONLY a status summary:",
    "- Cluster ID",
    "- Number of edits proposed",
    "- Any concerns or ambiguities encountered"
  ].join("\n")
})
```

**If `PAPER_FORMAT = "word"`:**

```
Agent({
  description: "Revise cluster C1: [description]",
  subagent_type: "writer",
  prompt: [
    "You are revising a specific section of an academic Word document (.docx) based on peer review feedback.",
    "",
    "PAPER FILE: [path to .docx]",
    "EXTRACTED TEXT (from markitdown): quality_reports/paper_extracted.md",
    "SECTIONS TO REVISE: [section names]",
    "",
    "REVIEWER COMMENTS TO ADDRESS:",
    "- [R1-C1]: [quote]",
    "- [R1-C3]: [quote]",
    "",
    "FULL TEXT OF TARGET SECTIONS (from the extracted markdown):",
    "[paste the full text of the relevant sections]",
    "",
    "CONSTRAINTS:",
    "- Make MINIMAL edits. Change only what is needed to address the specific comments.",
    "- Preserve existing notation, terminology, and style exactly.",
    "- Do not rewrite surrounding text that is not under review.",
    "- Preserve all table structures.",
    "- This is a Word document, NOT LaTeX. Output plain text edits, not LaTeX commands.",
    "",
    "OUTPUT:",
    "Save your proposed edits to: quality_reports/edits/cluster_C1.md",
    "",
    "Format each edit as:",
    "### Issue [R1-C1]",
    "**Section:** [section heading or paragraph locator]",
    "**Old text:**",
    "```",
    "[exact paragraph or sentence(s) to replace — copy verbatim from the extracted text]",
    "```",
    "**New text:**",
    "```",
    "[replacement text — plain text, no LaTeX commands]",
    "```",
    "**Explanation:** [why this addresses the comment]",
    "",
    "After saving the file, report back ONLY a status summary:",
    "- Cluster ID",
    "- Number of edits proposed",
    "- Any concerns or ambiguities encountered"
  ].join("\n")
})
```

Dispatch all independent clusters in a **single message** (multiple Agent tool calls) so they run concurrently.

### Step 3.2 — Dispatch NEW_ANALYSIS Clusters (After User Approval)

For each NEW_ANALYSIS cluster approved by user, dispatch a `coder` subagent:
- Include: the specific analysis requested, existing scripts context, data paths from CLAUDE.md
- Output: new/modified script + results summary saved to `quality_reports/edits/cluster_CN_analysis.md`

### Step 3.3 — Handle DISAGREE Clusters

For each DISAGREE cluster, based on user's chosen stance:
- **Concede**: add to the nearest AUTO cluster (writer handles it)
- **Partial**: writer revises based on user's specified partial concession
- **Push back**: draft diplomatic response paragraph saved to `quality_reports/edits/disagree_CN.md`

### Step 3.4 — Read Subagent Outputs

After all subagents complete:
1. Read each `quality_reports/edits/cluster_*.md` file.
2. Validate:
   - **LaTeX**: does each edit have `Old text` and `New text` blocks with valid LaTeX?
   - **Word**: does each edit have `Old text` and `New text` blocks with plain text (no LaTeX commands)?
3. Flag any edits that seem to modify more than necessary.
4. Append status to progress log.

---

## Phase 4: Sequential Application & Validation

**Goal:** Apply proposed edits one cluster at a time, validate after each, commit.

### Step 4.1 — Pre-flight Check

**If `PAPER_FORMAT = "latex"`:**
- Compile the paper before any edits to establish a clean baseline.
- If it doesn't compile: HALT and fix pre-existing errors first.
- Record baseline compilation status.

**If `PAPER_FORMAT = "word"`:**
- Verify the `.docx` file can be opened by `python-docx`:
  ```bash
  python -c "from docx import Document; doc = Document('[paper.docx]'); print(f'OK: {len(doc.paragraphs)} paragraphs')"
  ```
- Create a backup copy: `cp [paper.docx] [paper]_backup_[DATE].docx`
- Record baseline paragraph count.

### Step 4.2 — Apply Cluster by Cluster

For each cluster (respecting dependency order):

#### 4.2.1 — Apply Edits (LaTeX)

**If `PAPER_FORMAT = "latex"`:**
- Read the cluster's edit proposal from `quality_reports/edits/cluster_CN.md`.
- For each edit in the cluster:
  1. Verify the `Old text` exists in the paper file (Read + Grep to confirm).
  2. If found: apply via Edit tool (old_string → new_string).
  3. If NOT found: log a warning, try fuzzy matching (whitespace-normalized), skip if still not found.

#### 4.2.1 — Apply Edits (Word)

**If `PAPER_FORMAT = "word"`:**
- Read the cluster's edit proposal from `quality_reports/edits/cluster_CN.md`.
- Apply edits via a Python helper script using `python-docx`. For each edit:
  1. Load the `.docx` with `Document(paper_path)`.
  2. Iterate paragraphs to find the one containing the `Old text` (substring match, case-sensitive).
  3. Replace the matching text within that paragraph's `runs` (to preserve formatting), or if formatting is complex, replace the full paragraph text.
  4. If `Old text` spans multiple paragraphs, find and replace across consecutive paragraphs.
  5. Save the modified `.docx`.
  6. If `Old text` not found: log a warning, try fuzzy matching (strip whitespace, normalize unicode), skip if still not found.

Use this pattern for each edit:
```python
from docx import Document
import copy, re

def apply_word_edit(doc_path, old_text, new_text, output_path):
    doc = Document(doc_path)
    # Try exact match in a single paragraph first
    for para in doc.paragraphs:
        if old_text in para.text:
            # Replace within runs to preserve formatting
            for run in para.runs:
                if old_text in run.text:
                    run.text = run.text.replace(old_text, new_text)
                    doc.save(output_path)
                    return True
            # Fallback: replace full paragraph text (loses run-level formatting)
            if old_text in para.text:
                para.text = para.text.replace(old_text, new_text)
                doc.save(output_path)
                return True
    return False  # not found
```

#### 4.2.2 — Validate

**If `PAPER_FORMAT = "latex"`** — Compile:
```bash
xelatex -interaction=nonstopmode [paper].tex
biber [paper]
xelatex -interaction=nonstopmode [paper].tex
xelatex -interaction=nonstopmode [paper].tex
```

Parse compilation output:
- `!` lines = errors (must fix)
- `Overfull \hbox` > 10pt = minor warning
- `Undefined control sequence`, `Missing` = errors
- `Label multiply defined` = warning
- `Citation .* undefined` = warning (may resolve after biber)

**If `PAPER_FORMAT = "word"`** — Validate:
```bash
python -c "from docx import Document; doc = Document('[paper.docx]'); print(f'OK: {len(doc.paragraphs)} paragraphs')"
```
- Verify the file opens without error.
- Verify paragraph count is consistent (should be similar or slightly different; a dramatic drop indicates corruption).
- Re-extract to markdown and verify key section headings still exist:
  ```bash
  python -c "from markitdown import MarkItDown; md = MarkItDown(); r = md.convert('[paper.docx]'); print(r.text_content[:500])"
  ```

#### 4.2.3 — Auto-fix Common Errors (LaTeX only, up to 2 attempts per cluster)

| Error Pattern | Auto-fix |
|---|---|
| `Extra alignment tab` | Read the table, count columns, fix `\begin{tabular}` spec |
| `Missing \end{tabular}` | Find unclosed table, add `\end{tabular}` |
| `Missing \end{table}` | Find unclosed table float, add `\end{table}` |
| `Undefined control sequence \XXX` | Check if package is missing, or command is typo |
| `Citation .* undefined` | Run biber again |
| `Aux file corrupted` | Delete all `.aux`, `.bbl`, `.bcf`, `.run.xml` files, recompile full cycle |
| `Missing \item` | Check enumerate/itemize environment |

After auto-fix: recompile and check again.

**For Word files:** common issues are text-not-found (already handled with fuzzy matching above) or formatting corruption (if detected, restore from backup and retry with a simpler replacement strategy).

#### 4.2.4 — Commit
```bash
git add [files modified by this cluster]
git commit -m "revise: [cluster description] (refs: R1-C1, R1-C3)"
```

#### 4.2.5 — If Validation Fails After 2 Fixes

**LaTeX:** HALT. Report to user:
> "Cluster C3 applied but compilation fails. Error: [error message].
> Options: (1) Let me try another fix, (2) Revert this cluster, (3) You fix manually."

**Word:** HALT. Report to user:
> "Cluster C3 applied but the Word file appears corrupted or validation failed.
> Options: (1) Restore from backup and retry, (2) Revert this cluster, (3) You fix manually."

### Step 4.3 — Post-application Verification
- **LaTeX**: compile once more (full cycle). Save final compilation log to `quality_reports/compilation_log.txt`.
- **Word**: re-extract full text with markitdown and verify all section headings are present. Save validation log to `quality_reports/compilation_log.txt`.
- If clean: proceed to Phase 5.
- If errors: report and HALT.

Append to progress log:
```
## [DATE] Phase 4 Complete
- Applied N clusters
- M edits total
- Validation: [CLEAN / WARNINGS / ERRORS]
- Commits: [list of commit hashes]
```

---

## Phase 5: Verification

**Goal:** Verify every checklist item is actually addressed in the revised paper.

### Step 5.1 — Dispatch Verification Agent
Spawn a `writer-critic` subagent:

**If `PAPER_FORMAT = "latex"`:**

```
Agent({
  description: "Verify revision checklist coverage",
  subagent_type: "writer-critic",
  prompt: [
    "You are verifying that a paper revision has addressed all peer review comments.",
    "",
    "CHECKLIST: quality_reports/revision_checklist_[DATE].json",
    "REVISED PAPER: [path to .tex]",
    "",
    "For each issue in the checklist:",
    "1. Read the relevant section of the revised paper.",
    "2. Compare against the original reviewer quote.",
    "3. Determine if the comment has been addressed.",
    "",
    "Classify each as:",
    "- RESOLVED: The revision directly addresses the comment.",
    "- PARTIALLY: The revision addresses some but not all aspects.",
    "- UNRESOLVED: The revision does not address the comment.",
    "",
    "Save your verification report to: quality_reports/revision_verification_[DATE].md",
    "",
    "Report format:",
    "## Issue [ID]: [classification] — [severity]",
    "**Quote:** [referee quote]",
    "**Verdict:** RESOLVED / PARTIALLY / UNRESOLVED",
    "**Evidence:** [what changed in the paper, with line references]",
    "**Remaining concerns:** [if PARTIALLY or UNRESOLVED, what is still missing]",
    "",
    "At the end, produce a summary table:",
    "| Issue | Classification | Severity | Verdict | Notes |",
    "",
    "IMPORTANT: You are a READ-ONLY reviewer. Do not edit any files except your verification report."
  ].join("\n")
})
```

**If `PAPER_FORMAT = "word"`:**

```
Agent({
  description: "Verify revision checklist coverage (Word)",
  subagent_type: "writer-critic",
  prompt: [
    "You are verifying that a Word document revision has addressed all peer review comments.",
    "",
    "CHECKLIST: quality_reports/revision_checklist_[DATE].json",
    "REVISED PAPER (extracted text): quality_reports/paper_extracted.md",
    "ORIGINAL PAPER BACKUP: [paper]_backup_[DATE].docx",
    "",
    "For each issue in the checklist:",
    "1. Search the extracted text for the relevant section.",
    "2. Compare against the original reviewer quote and the old/new text from the edit proposals.",
    "3. Determine if the comment has been addressed.",
    "",
    "Classify each as:",
    "- RESOLVED: The revision directly addresses the comment.",
    "- PARTIALLY: The revision addresses some but not all aspects.",
    "- UNRESOLVED: The revision does not address the comment.",
    "",
    "Save your verification report to: quality_reports/revision_verification_[DATE].md",
    "",
    "Report format:",
    "## Issue [ID]: [classification] — [severity]",
    "**Quote:** [referee quote]",
    "**Verdict:** RESOLVED / PARTIALLY / UNRESOLVED",
    "**Evidence:** [what changed, with paragraph/section references from extracted text]",
    "**Remaining concerns:** [if PARTIALLY or UNRESOLVED, what is still missing]",
    "",
    "At the end, produce a summary table:",
    "| Issue | Classification | Severity | Verdict | Notes |",
    "",
    "IMPORTANT: You are a READ-ONLY reviewer. Do not edit any files except your verification report."
  ].join("\n")
})
```

### Step 5.2 — Process Verification Results
1. Read `quality_reports/revision_verification_[DATE].md`.
2. Count: RESOLVED / PARTIALLY / UNRESOLVED (by severity).
3. **If any CRITICAL or HIGH items are UNRESOLVED:**
   - Loop back to Phase 3 for those specific items (max 1 retry).
   - After retry, if still UNRESOLVED → HALT and report to user.
4. **If only MEDIUM/LOW items are PARTIALLY or UNRESOLVED:**
   - Note them in the response letter as "partially addressed" or "deferred to future work."
   - Proceed to Phase 6.

Append to progress log:
```
## [DATE] Phase 5 Complete
- Verification: X RESOLVED, Y PARTIALLY, Z UNRESOLVED
- UNRESOLVED critical/high items: [list or 'none']
- Verification report: quality_reports/revision_verification_[DATE].md
```

---

## Phase 6: Response-to-Reviewers Letter

**Goal:** Produce a response letter mapping each comment to the specific change made.

### Step 6.1 — Generate Response Letter (LaTeX)

**If `PAPER_FORMAT = "latex"`:**

Write `quality_reports/response_to_reviewers_[DATE].tex` using the working paper preamble standard.

```latex
\documentclass[12pt]{article}
\usepackage[left=1.0in,right=1.0in,top=1.0in,bottom=1.0in]{geometry}
\usepackage{setspace}
\doublespacing
\usepackage{xcolor}
\usepackage{enumitem}

\definecolor{refcolor}{RGB}{0,0,180}
\definecolor{changecolor}{RGB}{0,128,0}
\definecolor{deferredcolor}{RGB}{128,128,128}
\definecolor{disagreecolor}{RGB}{180,0,0}

\newcommand{\refquote}[1]{\textcolor{refcolor}{\textit{``#1''}}}
\newcommand{\changed}[1]{\textcolor{changecolor}{#1}}
\newcommand{\deferred}[1]{\textcolor{deferredcolor}{#1}}
\newcommand{\disagree}[1]{\textcolor{disagreecolor}{#1}}

\title{Response to Referee Reports}
\author{[Author Names]}
\date{\today}

\begin{document}
\maketitle
\thispagestyle{empty}
\newpage
\setcounter{page}{1}

\noindent Dear Editor,

\noindent We thank the editor and referees for their constructive comments...
[summary paragraph of major changes]

\section{Response to Referee 1}

[For each issue:]

\subsection*{Comment [R1-C1]: [short title]}
\refquote{[exact referee quote]}

\changed{Response: [description of change made]. See Section X, page Y.}

[Repeat for all issues, all referees]

\end{document}
```

### Step 6.2 — Response Formatting Rules (shared by both formats)
- **RESOLVED items** → "We have revised... See Section X."
- **PARTIALLY items** → "We have partially addressed this by... [remaining aspect] is deferred because..."
- **UNRESOLVED items** → "We acknowledge this concern and plan to address it in..."
- **DISAGREE items** → "We appreciate the referee's perspective. However, [diplomatic pushback with evidence]..."
- **NEW_ANALYSIS items** → "We have conducted additional analysis as suggested. [Summary of results]. See Table/Figure X."

### Step 6.3 — Generate Response Letter (Word)

**If `PAPER_FORMAT = "word"`:**

Generate the response letter as a `.docx` file using `python-docx`:

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Title
title = doc.add_heading('Response to Referee Reports', level=0)

# Opening
doc.add_paragraph('Dear Editor,')
doc.add_paragraph('We thank the editor and referees for their constructive comments...')
doc.add_paragraph('')  # blank line

# For each referee:
for referee_num in [1, 2, ...]:
    doc.add_heading(f'Response to Referee {referee_num}', level=1)

    for issue in referee_issues:
        doc.add_heading(f'Comment {issue.id}: {issue.short_title}', level=2)

        # Referee quote in blue italic
        quote_para = doc.add_paragraph()
        quote_run = quote_para.add_run(f'"{issue.quote}"')
        quote_run.italic = True
        quote_run.font.color.rgb = RGBColor(0, 0, 180)

        # Response in green (or red for disagreements, gray for deferred)
        response_para = doc.add_paragraph()
        response_run = response_para.add_run(f'Response: {issue.response_text}')
        if issue.classification == 'DISAGREE':
            response_run.font.color.rgb = RGBColor(180, 0, 0)
        elif issue.status == 'UNRESOLVED':
            response_run.font.color.rgb = RGBColor(128, 128, 128)
        else:
            response_run.font.color.rgb = RGBColor(0, 128, 0)

doc.save('quality_reports/response_to_reviewers_[DATE].docx')
```

Write and run this script via Bash.

### Step 6.4 — Compile/Finalize Response Letter

**If `PAPER_FORMAT = "latex"`:**
```bash
xelatex -interaction=nonstopmode quality_reports/response_to_reviewers_[DATE].tex
```

**If `PAPER_FORMAT = "word"`:**
Verify the `.docx` response letter was created and can be opened:
```bash
python -c "from docx import Document; doc = Document('quality_reports/response_to_reviewers_[DATE].docx'); print(f'OK: {len(doc.paragraphs)} paragraphs')"
```

Append to progress log:
```
## [DATE] Phase 6 Complete
- Response letter generated: quality_reports/response_to_reviewers_[DATE].tex
- Compiled: [CLEAN / WARNINGS]
- Final status: X/N issues addressed
```

---

## Final Summary

After all phases complete, present to user:

```
## Revision Complete

**Paper:** [path]
**Checklist:** quality_reports/revision_checklist_[DATE].json

**Results:**
- Total issues: N
- Resolved: X (X%)
- Partially resolved: Y
- Unresolved: Z
- Deferred: W

**Files modified:**
- [list of files changed — .tex or .docx]

**Commits:**
- [hash] revise: [cluster 1 description]
- [hash] revise: [cluster 2 description]
- ...

**Outputs:**
- Checklist: quality_reports/revision_checklist_[DATE].json
- Plan: quality_reports/plans/[DATE]_revision-plan.md
- Edits: quality_reports/edits/cluster_*.md
- Verification: quality_reports/revision_verification_[DATE].md
- Response letter: quality_reports/response_to_reviewers_[DATE].[tex|docx]
- Validation log: quality_reports/compilation_log.txt
- Progress log: quality_reports/revision_progress.md
- Word backup (if applicable): [paper]_backup_[DATE].docx

**Action needed:** [list any UNRESOLVED or deferred items requiring manual attention]
```

---

## Error Handling Summary

| Condition | Phase | Action |
|---|---|---|
| Paper file not found | Pre-flight | HALT: ask user for correct path |
| Reports folder empty | Pre-flight | HALT: ask user for correct path |
| `python-docx` not installed (Word) | Pre-flight | Auto-install via `pip install python-docx` |
| `markitdown` not installed (Word) | Pre-flight | Auto-install via `pip install markitdown` |
| Paper won't compile initially (LaTeX) | Phase 4 | HALT: fix pre-existing errors first |
| Paper won't open in python-docx (Word) | Phase 4 | HALT: file may be corrupted or password-protected |
| `NEW_ANALYSIS` classified | Phase 2 | HALT: ask user for approval/deferral/dismissal |
| `DISAGREE` classified | Phase 2 | HALT: ask user for stance (concede/partial/push back) |
| Ambiguous classification | Phase 1 | Classify as `DISAGREE`, HALT for user judgment |
| Compilation fails ×2 (LaTeX) | Phase 4 | HALT: show errors, offer revert/manual-fix options |
| Validation fails ×2 (Word) | Phase 4 | HALT: restore from backup, offer revert/manual-fix options |
| Verification finds CRITICAL unresolved | Phase 5 | Retry once, then HALT |
| Subagent crashes | Phase 3 | Retry once, then skip cluster and flag |
| Edit's `Old text` not found (LaTeX) | Phase 4 | Log warning, attempt fuzzy match, skip if unresolvable |
| Edit's `Old text` not found (Word) | Phase 4 | Log warning, attempt fuzzy match (strip whitespace, normalize unicode), skip if unresolvable |
| Word file corrupted after edit | Phase 4 | Restore from backup `[paper]_backup_[DATE].docx`, retry with simpler replacement |

---

## Core Principles

1. **Minimal diffs.** Each edit changes only what is necessary to address the specific comment. No drive-by improvements.
2. **Context protection.** Subagents save results to local files. Main agent receives status summaries only.
3. **Halt on ambiguity.** Never guess the user's stance on a disagreement or the scope of a new analysis request.
4. **Validate after every change.** For LaTeX: compile after every batch. For Word: verify file integrity and section structure after every batch. Catch errors early, when the cause is obvious.
5. **Traceability.** Every edit maps to a checklist item. Every checklist item maps to a reviewer quote. Every commit references issue IDs.
6. **Never fabricate.** Do not invent results, statistics, or citations. Mark unknown items as TBD.
7. **The response letter is the user's voice.** Match their professional tone. Never condescending toward referees.
