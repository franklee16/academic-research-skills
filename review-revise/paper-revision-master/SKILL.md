---
name: paper-revision
description: 'Comprehensive workflow for handling journal Revise and Resubmit (R&R) decisions. Use when you receive referee reports and need to systematically track, classify, and respond to reviewer comments. Triggers include R&R decisions, referee comments, response to reviewers, revision letter drafting, and handling referee reports. Provides structured 10-step workflow, revision tracking spreadsheet, LaTeX response letter template, and automated comment extraction.'
---

# Paper Revision: Handle R&R Decisions Systematically

A comprehensive skill for managing journal revise-and-resubmit workflows, from extracting referee comments to drafting the response letter.

## When to Use This Skill

Use this skill when:
- You receive an R&R decision from a journal
- You need to systematically track multiple referee comments
- You want structured guidance through the revision process
- You need to draft a professional response letter to the editor

## The 10-Step R&R Workflow

Based on Tanya Golash-Boza's proven method for successful revisions.

### Step 1: Read the Editor's Letter

Confirm you received an R&R decision. Other possible outcomes:
- **Reject** (no resubmission invited)
- **Conditional acceptance** (minor changes)
- **Outright acceptance** (rare)

If unsure, ask the editor or a senior colleague to review the letter.

### Step 2: Create Revision Tracker

Set up a systematic tracking system for all comments.

**Use the template:** [revision_tracker_template.csv](assets/revision_tracker_template.csv)

**Columns:**
- Reviewer (Reviewer 1, Reviewer 2, Editor)
- Comment ID (sequential numbering)
- Original Comment (exact text from referee)
- Paraphrased Suggestion (your interpretation)
- Section (Introduction, Methods, Results, etc.)
- Classification (NEW ANALYSIS, CLARIFICATION, DISAGREE, MINOR)
- Response Action (what you will do)
- Status (Pending, In Progress, Completed, Disagreed)
- Notes (additional context)

**Tip:** If you received referee reports as PDF or text files, use the automated parser:

```bash
python scripts/parse_referee_report.py referee_report.pdf --output revision_tracker.csv
```

This extracts comments and creates the initial tracker automatically. See [scripts/parse_referee_report.py](scripts/parse_referee_report.py) for details.

### Step 3: Extract All Comments

Read each review carefully and extract every suggestion.

**Key principle:** Paraphrase reviewer comments into actionable suggestions.

**Example:**
- **Original:** "One major problem with this article is that the research methods have insufficient evidence."
- **Paraphrased:** "Provide a more accurate and complete discussion of the data collection in the Methods section."

This lets you work from your paraphrased list without re-reading the reviews.

**Label each comment by source:** Reviewer 1, Reviewer 2, Editor, etc.

### Step 4: Organize Comments Logically

Group related comments together, even if from different reviewers.

**Common groupings:**
- Introduction / Motivation
- Literature Review
- Data / Methods
- Results
- Robustness
- Discussion / Conclusion

This makes it easier to revise systematically by section.

### Step 5: Classify Each Comment

Classify each comment to determine the appropriate response workflow.

**See detailed guide:** [references/comment_classification.md](references/comment_classification.md)

**Four classifications:**

| Classification | What It Means | Routing |
|----------------|---------------|---------|
| **NEW ANALYSIS** | Requires new empirical work (new regressions, robustness tests, data collection) | Coder → coder-critic → writer updates |
| **CLARIFICATION** | Text revision sufficient (add explanation, strengthen argument, improve clarity) | Writer → writer-critic |
| **DISAGREE** | Diplomatic pushback needed (request is misguided, infeasible, or beyond scope) | **USER APPROVAL REQUIRED** |
| **MINOR** | Typos, formatting, small corrections | Writer (no critic needed) |

**Critical:** Claude NEVER autonomously disagrees with referees. All DISAGREE classifications require user approval.

**Decision tree:**
```
Does this require new code/estimation?
  ├─ YES → NEW ANALYSIS
  └─ NO → Does it require substantive text revision?
           ├─ YES → Can you do it as requested?
           │        ├─ YES → CLARIFICATION
           │        └─ NO → DISAGREE
           └─ NO → MINOR
```

### Step 6: Plan Your Responses

For each comment, decide exactly what you will do.

**Format as clear instructions to yourself:**

**Example:**
- **Reviewer suggestion:** "More clearly explain how your study fits within existing literature."
- **Your planned action:** "Add one paragraph to introduction (page 3) clearly conveying the existing gap in literature that triggered this study."

**Important:** You must respond to ALL suggestions. If you disagree with a suggestion, explain why in your response letter.

**For DISAGREE comments:** Draft a polite, professional explanation. See [references/response_examples.md](references/response_examples.md) for templates.

### Step 7: Execute the Revision

Work through your plan systematically.

**Strategy:**
1. Start with MINOR comments (quick wins, builds momentum)
2. Then tackle CLARIFICATION comments
3. Finally, address NEW ANALYSIS comments (most time-consuming)

**For CLARIFICATION comments:** Revise the relevant sections of your LaTeX manuscript directly. Ensure changes are highlighted (e.g., bold or colored text) for easy identification.

**For NEW ANALYSIS comments:**
- Write the new code (R/Stata/Python)
- Generate new tables/figures
- Update the manuscript with new results
- Add discussion of new findings

**For DISAGREE comments:**
- Draft your diplomatic response
- Get user approval before finalizing
- Document your reasoning clearly

### Step 8: Write the Response Letter

Use your completed revision tracker to draft a comprehensive response letter.

**Template:** [assets/response_letter_template.tex](assets/response_letter_template.tex)

**Structure:**
1. Opening paragraph (thank editor, summarize revision)
2. Response to Reviewer 1 (all comments, numbered)
3. Response to Reviewer 2 (all comments, numbered)
4. Response to Editor comments
5. Closing paragraph

**For each comment:**
- Quote the original comment
- Explain your response
- Point to specific changes (page/line numbers)

**Automation:** Use the script to generate the initial draft:

```bash
python scripts/generate_response_letter.py revision_tracker.csv --output response_letter.tex --title "Your Paper Title"
```

See [scripts/generate_response_letter.py](scripts/generate_response_letter.py) for details.

**See example responses:** [references/response_examples.md](references/response_examples.md)

### Step 9: Double-Check Everything

Verify completeness before submission.

**Checklist:**
- [ ] Every comment from every reviewer is addressed
- [ ] Each response explains what you did (or why you didn't)
- [ ] Page/line numbers are accurate
- [ ] All referenced tables/figures exist
- [ ] Response letter is professional and polite
- [ ] No typos in response letter
- [ ] Manuscript changes are clearly highlighted

**Tip:** Read the response letter aloud to catch awkward phrasing.

### Step 10: Final Read and Resubmit

**Read the manuscript as a new reader:**
- Someone who hasn't seen the original version
- Someone who doesn't know the referee comments

Ensure the paper maintains coherence and flow despite the revisions.

**Resubmit:**
- Revised manuscript (with changes highlighted)
- Response letter to editor
- Any supplementary materials requested

---

## Workflow Integration

### With revision-protocol.md

This skill provides the comprehensive R&R workflow. For targeted agent dispatch with quality control, transition to revision-protocol.md after planning.

**See:** [references/revision_workflow_integration.md](references/revision_workflow_integration.md)

**When to use each:**
- **This skill:** Planning, organization, tracking, response letter drafting
- **revision-protocol.md:** Targeted execution with worker-critic pairs and quality gates

**Example workflow:**
1. Use this skill to extract and classify all comments (Steps 1-6)
2. Transition to revision-protocol.md to dispatch:
   - NEW ANALYSIS → coder + coder-critic
   - CLARIFICATION → writer + writer-critic
3. Return to this skill for response letter drafting (Step 8)

### With LaTeX Workflow

This skill integrates with your LaTeX manuscript editing:

- Read and revise .tex files directly
- Use writer agent for section revisions
- Track all changes in revision tracker
- Ensure changes are highlighted for reviewers

---

## Resources Overview

### Assets (Templates)

**[revision_tracker_template.csv](assets/revision_tracker_template.csv)**
- CSV template for systematic comment tracking
- Pre-formatted with example entries
- Import into Excel for easier editing

**[response_letter_template.tex](assets/response_letter_template.tex)**
- LaTeX template for professional response letter
- Structured sections for each reviewer
- Professional academic formatting

### Scripts (Automation)

**[scripts/parse_referee_report.py](scripts/parse_referee_report.py)**
- Extracts comments from PDF/text referee reports
- Identifies reviewer sections
- Outputs JSON or CSV for import into tracker

**Usage:**
```bash
# Basic usage
python scripts/parse_referee_report.py referee_report.pdf --output comments.json

# CSV output
python scripts/parse_referee_report.py referee_report.txt --output comments.csv

# With format specification
python scripts/parse_referee_report.py report.pdf --format csv --output comments.csv
```

**Requirements:** `pip install pdfplumber` (for PDF support)

**[scripts/generate_response_letter.py](scripts/generate_response_letter.py)**
- Reads completed revision tracker
- Generates formatted LaTeX response letter
- Groups responses by reviewer

**Usage:**
```bash
# Basic usage
python scripts/generate_response_letter.py revision_tracker.xlsx --output response_letter.tex

# With metadata
python scripts/generate_response_letter.py tracker.csv --output response.tex \
  --title "My Paper Title" \
  --author "Your Name" \
  --affiliation "Your University"
```

**Requirements:** `pip install pandas openpyxl`

### References (Detailed Guidance)

**[references/comment_classification.md](references/comment_classification.md)**
- Detailed classification system with examples
- Decision tree for borderline cases
- Routing logic for each classification

**[references/response_examples.md](references/response_examples.md)**
- Model responses for each comment type
- Polite disagreement templates
- Common phrases and best practices

**[references/revision_workflow_integration.md](references/revision_workflow_integration.md)**
- How this skill integrates with revision-protocol.md
- When to use each system
- Example workflow transitions

---

## Quick Start

**Scenario:** You just received an R&R decision with 2 referee reports.

**Minimal workflow:**

1. **Parse the reports:**
   ```bash
   python scripts/parse_referee_report.py referee1.pdf --output comments1.csv
   python scripts/parse_referee_report.py referee2.pdf --output comments2.csv
   ```

2. **Combine into master tracker:**
   - Open both CSV files
   - Copy into [revision_tracker_template.csv](assets/revision_tracker_template.csv)
   - Fill in Classification, Response Action, and Status columns

3. **Execute revisions:**
   - Work through tracker systematically
   - Update Status as you complete each comment

4. **Generate response letter:**
   ```bash
   python scripts/generate_response_letter.py revision_tracker.csv \
     --output response_letter.tex \
     --title "Your Paper Title"
   ```

5. **Finalize:**
   - Edit response_letter.tex to polish language
   - Add specific page/line references
   - Double-check all comments addressed

---

## Key Principles

1. **Respond to EVERY comment** - No comment is too minor to address
2. **Be grateful, not defensive** - Reviewers are (usually) trying to help
3. **Be specific** - Cite exact page numbers, line numbers, table numbers
4. **Start easy** - Tackle MINOR comments first to build momentum
5. **Track everything** - The revision tracker is your single source of truth
6. **Classify before executing** - Different classifications need different workflows
7. **Never disagree autonomously** - DISAGREE comments require user approval

---

## Troubleshooting

**Problem:** Parse script doesn't extract comments correctly.

**Solution:** Manually review and adjust. The script is designed to help with initial extraction, but complex formatting may require manual cleanup.

**Problem:** Too many NEW ANALYSIS comments, feeling overwhelmed.

**Solution:**
- Prioritize by importance
- Group similar requests (e.g., all robustness tests together)
- Consider which are essential vs. nice-to-have
- Discuss with co-authors about scope

**Problem:** Referee asks for something that would take months.

**Solution:**
- Classify as DISAGREE
- Explain the time/resource constraint politely
- Offer an alternative when possible
- Note it as a limitation in the revised manuscript

**Problem:** Two reviewers give contradictory suggestions.

**Solution:**
- Acknowledge both perspectives in your response
- Explain which you followed and why
- If truly contradictory, seek editor guidance

---

## Final Notes

Receiving an R&R is good news—the editor sees potential in your work. The key is systematic, thorough revision. This skill provides the structure; your expertise provides the content.

**Remember:** The goal is not just to address each comment, but to produce a stronger, more convincing paper.
