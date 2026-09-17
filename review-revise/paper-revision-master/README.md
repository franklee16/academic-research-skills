# paper-revision

A Claude Code skill for systematically handling journal Revise and Resubmit (R&R) decisions — from extracting referee comments to drafting the response letter.

Based on [Tanya Golash-Boza's proven R&R method](https://tanyagolashboza.com/the-professor-is-in-how-to-write-a-peer-journal-article-revision/).

## Quick Start

```bash
# 1. Parse referee reports into a structured tracker
python scripts/parse_referee_report.py referee1.pdf --output comments1.csv
python scripts/parse_referee_report.py referee2.txt --output comments2.csv

# 2. Classify comments and plan responses in the tracker

# 3. Generate a LaTeX response letter from the completed tracker
python scripts/generate_response_letter.py revision_tracker.csv \
  --output response_letter.tex \
  --title "Your Paper Title" \
  --author "Your Name"
```

## The 10-Step Workflow

| Step | Action | Output |
|------|--------|--------|
| 1 | Read the editor's letter — confirm R&R decision | Decision type |
| 2 | Create revision tracker | `revision_tracker.csv` |
| 3 | Extract all comments from each review | Raw comment list |
| 4 | Organize comments by section | Grouped tracker |
| 5 | Classify each comment (4 categories) | Classification column filled |
| 6 | Plan your response for each comment | Response Action column filled |
| 7 | Execute revisions (MINOR → CLARIFICATION → NEW ANALYSIS) | Revised manuscript |
| 8 | Write the response letter | `response_letter.tex` |
| 9 | Double-check completeness | Verification checklist |
| 10 | Final read and resubmit | Submission package |

## Comment Classification

Every referee comment falls into one of four categories, each with its own workflow:

| Classification | Meaning | Routing |
|---------------|---------|---------|
| **NEW ANALYSIS** | New estimation, robustness tests, data work | Coder → coder-critic → writer |
| **CLARIFICATION** | Text revision sufficient — no new code | Writer → writer-critic |
| **DISAGREE** | Pushback needed — misguided or infeasible request | **User approval required** |
| **MINOR** | Typos, formatting, small corrections | Writer (no critic) |

**Key rule:** Claude never autonomously disagrees with referees. All DISAGREE classifications require user approval before a diplomatic response is drafted.

### Decision Tree

```
Does this require new code/estimation?
  YES → NEW ANALYSIS
  NO → Does it require substantive text revision?
       YES → Can you do it as requested?
              YES → CLARIFICATION
              NO  → DISAGREE
       NO → MINOR
```

## File Structure

```
paper-revision/
├── SKILL.md                              # Main skill definition (10-step workflow)
├── README.md                             # This file
├── assets/
│   ├── revision_tracker_template.csv     # CSV template for tracking comments
│   └── response_letter_template.tex      # LaTeX response letter template
├── scripts/
│   ├── parse_referee_report.py           # Extract comments from PDF/text reports
│   └── generate_response_letter.py       # Generate LaTeX response letter from tracker
└── references/
    ├── comment_classification.md         # Detailed classification guide with examples
    ├── response_examples.md              # Model responses for each comment type
    └── revision_workflow_integration.md   # Integration with revision-protocol.md
```

## Scripts

### parse_referee_report.py

Extracts structured comments from referee reports (PDF or plain text). Identifies reviewer sections, extracts numbered/bulleted comments, and outputs JSON or CSV.

```bash
python scripts/parse_referee_report.py referee_report.pdf --output comments.json
python scripts/parse_referee_report.py referee_report.txt --output comments.csv --format csv
```

**Dependencies:** `pip install pdfplumber` (for PDF support; plain text works without it)

### generate_response_letter.py

Reads a completed revision tracker (Excel or CSV) and generates a formatted LaTeX response letter, grouping responses by reviewer.

```bash
python scripts/generate_response_letter.py revision_tracker.xlsx --output response_letter.tex
python scripts/generate_response_letter.py tracker.csv --output response.tex \
  --title "My Paper Title" \
  --id "MANUSCRIPT-123" \
  --author "Jane Doe" \
  --affiliation "University of Example" \
  --email "jane@example.edu"
```

**Dependencies:** `pip install pandas openpyxl`

## Revision Tracker Schema

The tracker CSV has these columns:

| Column | Description |
|--------|-------------|
| Reviewer | Source of the comment (Reviewer 1, Reviewer 2, Editor) |
| Comment ID | Sequential number |
| Original Comment | Exact text from the referee report |
| Paraphrased Suggestion | Your interpretation of what's being asked |
| Section | Paper section affected (Introduction, Methods, etc.) |
| Classification | NEW ANALYSIS / CLARIFICATION / DISAGREE / MINOR |
| Response Action | What you will do |
| Status | Pending / In Progress / Completed / Disagreed |
| Notes | Additional context |

## Integration with revision-protocol.md

This skill handles the **planning and organization** phase. For **execution with quality control**, it integrates with `revision-protocol.md`'s agent dispatch system:

1. Use this skill to extract and classify all comments (Steps 1–6)
2. Transition to revision-protocol.md to dispatch worker-critic pairs:
   - NEW ANALYSIS → coder + coder-critic
   - CLARIFICATION → writer + writer-critic
3. Return to this skill for response letter drafting (Step 8)

See [references/revision_workflow_integration.md](references/revision_workflow_integration.md) for the full decision matrix and workflow transitions.

## Installation

Copy or symlink the `paper-revision/` directory into your Claude Code skills folder:

```bash
# Option 1: Copy directly
cp -r paper-revision/ ~/.claude/skills/

# Option 2: Symlink (if managing skills from a central repo)
ln -s /path/to/paper-revision ~/.claude/skills/paper-revision
```

## Requirements

- **Claude Code** with skill support
- **Python 3.8+** for automation scripts
- Optional: `pdfplumber` (PDF parsing), `pandas` + `openpyxl` (response letter generation)
- A LaTeX distribution for compiling the response letter template

## License

MIT
