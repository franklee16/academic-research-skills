# Comment Classification Guide

## Overview

Each referee comment should be classified into one of four categories. This classification determines the routing and workflow for addressing the comment.

## Classification Categories

### NEW ANALYSIS

**Definition:** Requires new estimation, data work, or empirical analysis.

**Examples:**
- "The author should conduct additional robustness tests using alternative specifications."
- "I suggest adding a placebo test to rule out alternative mechanisms."
- "The sample should be restricted to [specific subgroup] to test the hypothesis."
- "Please estimate the model using [different estimation technique]."

**Routing:** Coder agent → coder-critic reviews → writer updates manuscript

**Workflow:**
1. Coder implements new analysis (R/Stata/Python scripts)
2. Coder-critic reviews code quality and reproducibility
3. Writer incorporates new results into manuscript
4. Writer-critic reviews the updated sections

**Response time:** 2-5 days depending on complexity

---

### CLARIFICATION

**Definition:** Text revision, explanation, or elaboration sufficient. No new empirical work needed.

**Examples:**
- "The author should more clearly explain the identification strategy."
- "Please add more detail about the data collection process."
- "The literature review is incomplete and should include [specific papers]."
- "The interpretation of the results on page 15 is unclear."
- "Please discuss the limitations of your approach more thoroughly."

**Routing:** Writer agent → writer-critic reviews

**Workflow:**
1. Writer revises the relevant sections
2. Writer-critic reviews for clarity, completeness, and style
3. Changes integrated into manuscript

**Response time:** Same day to 2 days

---

### DISAGREE

**Definition:** Diplomatic pushback needed. The comment is misguided, beyond scope, or technically infeasible.

**Examples:**
- "The reviewer requests a completely different research design that would require new data."
- "The suggestion contradicts established methodology in the field."
- "The requested analysis would take months and is not necessary for the paper's contribution."
- "The reviewer misunderstood the paper's main argument."

**Routing:** Flagged for USER review → diplomatic response drafted

**Workflow:**
1. Claude drafts a polite, professional explanation
2. User reviews and approves the response
3. Response letter explains why the suggestion was not implemented
4. Alternative solutions offered when appropriate

**CRITICAL:** Claude NEVER autonomously disagrees with referees. All DISAGREE classifications require user approval.

**Response time:** Requires user decision (variable)

**Response template:**
```
We appreciate the reviewer's suggestion to [X]. However, after careful consideration, 
we believe this would [reason]. Instead, we have [alternative if applicable].
```

---

### MINOR

**Definition:** Typos, formatting, small corrections, or minor clarifications.

**Examples:**
- "There is a typo on page 5."
- "Table 3 should include standard errors in parentheses."
- "Please format references according to journal style."
- "Add a footnote explaining the acronym."
- "Figure 2 is missing a title."

**Routing:** Writer (no critic review needed for truly minor items)

**Workflow:**
1. Make the requested change
2. Note the change in response letter
3. No separate critic review needed

**Response time:** Immediate to same day

---

## Classification Decision Tree

```
Does this comment require new data collection or estimation?
  ├─ YES → NEW ANALYSIS
  └─ NO → Does it require substantive text revision?
           ├─ YES → Can the revision be done as requested?
           │        ├─ YES → CLARIFICATION
           │        └─ NO → DISAGREE (requires user approval)
           └─ NO → MINOR
```

## Special Cases

### Borderline NEW ANALYSIS vs CLARIFICATION

**Rule of thumb:** If you need to write new code (R/Stata/Python), it's NEW ANALYSIS. If you only need to revise text, it's CLARIFICATION.

**Example:** "Please discuss robustness to alternative sample periods."
- If robustness tests already exist: CLARIFICATION (add discussion)
- If robustness tests don't exist: NEW ANALYSIS (run the tests first)

### Multiple Components in One Comment

**Rule:** Split into separate classifications.

**Example:** "The methods section is unclear and you should run additional robustness tests."
- Part 1: "Methods section is unclear" → CLARIFICATION
- Part 2: "Run additional robustness tests" → NEW ANALYSIS

### Editor vs Reviewer Comments

**Editor comments** should be classified the same way but may carry more weight. Always address editor comments first in the response letter.

---

## Tracking Classification

In the revision tracker spreadsheet, add a "Classification" column with one of:
- NEW ANALYSIS
- CLARIFICATION
- DISAGREE
- MINOR

This enables systematic routing and progress tracking.
