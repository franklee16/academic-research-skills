# Phase 0: Intake & Feedback Mapping

## Why This Phase Matters

Revision without a map is revision by wandering. Before touching any text, you need a clear picture of:
- What the manuscript currently contains
- What the feedback actually says (parsed, not paraphrased)
- Which sections need work
- Which skills should handle each section

This phase transforms vague "I got feedback" into actionable "here are 12 discrete items routed to 4 skills."

## Your Tasks

### Task 1: Read the Manuscript

Read the full manuscript (or all available sections). As you read, note:

1. **Section inventory**: What sections exist? (Intro, Theory/Lit Review, Methods, Case, Findings, Discussion, Conclusion)
2. **Section lengths**: Approximate word counts per section
3. **Section quality signals**: What seems strong? What seems weak even before feedback?
4. **Cross-references**: How do sections connect? Does intro set up what findings deliver?

Create a section inventory table:

```markdown
## Section Inventory

| Section | Present | ~Words | Notes |
|---------|---------|--------|-------|
| Abstract | Yes/No | | |
| Introduction | Yes/No | | |
| Theory/Literature | Yes/No | | |
| Case Justification | Yes/No | | |
| Methods | Yes/No | | |
| Findings | Yes/No | | |
| Discussion | Yes/No | | |
| Conclusion | Yes/No | | |
```

### Task 2: Read the Feedback Carefully

Read ALL feedback before parsing. Note:
- Who is giving the feedback? (Reviewer 1, Reviewer 2, editor, colleague)
- What's the overall tone? (Supportive with suggestions? Critical with demands?)
- What are the BIG issues vs. small issues?
- Is anything contradictory? (Reviewer 1 says expand X; Reviewer 2 says cut X)

### Task 3: Parse Feedback Into Discrete Items

Transform prose feedback into numbered, discrete items. Each item should be:
- **One issue** (not bundled)
- **Mapped to a section** (or "Cross-section" if it spans multiple)
- **Categorized by type** (Structural, Substantive, Methodological, Stylistic, Coherence)
- **Attributed to source** (R1, R2, Editor, Self)

**Parsing example**:

Original feedback:
> "The introduction is too long and the literature review feels repetitive—like you're introducing the topic twice. Also, the methods section needs more detail on how you coded the interviews, and I'd like to see scope conditions in the discussion."

Parsed:
```markdown
1. [Intro][Stylistic][R1] Introduction is too long
2. [Intro + Theory][Structural][R1] Two intros detected—lit review repeats intro framing
3. [Methods][Methodological][R1] More detail needed on interview coding process
4. [Discussion][Substantive][R1] Add scope conditions
```

### Task 4: Categorize Each Item

Use these categories:

| Category | What It Means | Typical Resolution |
|----------|---------------|-------------------|
| **Structural** | Organization, architecture, missing/extra sections | Skill architecture phases |
| **Substantive** | Argument strength, evidence, interpretation | Skill drafting phases |
| **Methodological** | Methods justification, credibility, transparency | methods-writer |
| **Stylistic** | Word count, clarity, repetition, prose quality | Skill calibration |
| **Coherence** | Cross-section alignment, promise-delivery | interview-bookends Phase 3 |

### Task 5: Route to Skills

For each section with feedback items, identify the primary skill:

| Section | Primary Skill | Backup Approach |
|---------|---------------|-----------------|
| Introduction | `interview-bookends` | Direct revision if minimal |
| Conclusion | `interview-bookends` | Direct revision if minimal |
| Theory/Literature | `lit-writeup` | Direct revision if < 3 items |
| Methods | `methods-writer` | Direct revision if < 3 items |
| Case Justification | `case-justification` | Direct revision if < 3 items |
| Findings | No dedicated skill | Direct revision with guidance |
| Discussion | `lit-writeup` techniques | Direct revision with guidance |

**Routing threshold**: If a section has 3+ substantive/structural items, route to the specialized skill. If it has only 1-2 stylistic items, may handle directly.

### Task 6: Identify Dependencies

Some feedback items depend on others:

- **Theory → Findings**: If theory framing changes, findings may need terminology updates
- **Intro → Conclusion**: If intro promises change, conclusion callbacks need adjustment
- **Methods → Findings**: If methods expand to include new credibility measures, findings may reference them
- **Case → Methods**: Case justification may overlap with site description in Methods

Note dependencies so you sequence revisions correctly.

### Task 7: Create the Revision Map

Create `revision-map.md` with this structure:

```markdown
# Revision Map

## Manuscript: [Title]
## Date: [Date]
## Feedback Sources: [R1, R2, Editor, etc.]

---

## Section Inventory

| Section | Present | ~Words | Skill | Items |
|---------|---------|--------|-------|-------|
| Introduction | Yes | 800 | interview-bookends | 2 |
| Theory | Yes | 1500 | lit-writeup | 3 |
| Methods | Yes | 900 | methods-writer | 2 |
| Findings | Yes | 4000 | Direct | 1 |
| Discussion | Yes | 1200 | Direct | 2 |
| Conclusion | Yes | 600 | interview-bookends | 1 |

---

## Parsed Feedback Items

### Introduction (2 items) → interview-bookends
| ID | Type | Source | Item | Status |
|----|------|--------|------|--------|
| I-1 | Stylistic | R1 | Too long | [ ] |
| I-2 | Structural | R1 | Two intros detected | [ ] |

### Theory (3 items) → lit-writeup
| ID | Type | Source | Item | Status |
|----|------|--------|------|--------|
| T-1 | Structural | R1 | Compress by 30% | [ ] |
| T-2 | Substantive | R2 | Strengthen turn | [ ] |
| T-3 | Stylistic | Editor | Define "organizational absorption" | [ ] |

[Continue for each section...]

---

## Dependencies

- I-2 depends on T-1 (if theory section changes, intro may need adjustment)
- Conclusion callbacks depend on intro (sequence: intro → conclusion)

---

## Revision Sequence (Proposed)

1. Theory section (T-1, T-2, T-3) — foundation changes
2. Introduction (I-1, I-2) — after theory settled
3. Methods (M-1, M-2) — independent
4. Findings (F-1) — may need terminology updates from theory
5. Discussion (D-1, D-2) — independent
6. Conclusion (C-1) — last, after intro finalized

---

## Questions for User

- [List any ambiguous items or decisions that need user input]
```

## Output Files

Create in `revision/` directory:
- `revision-map.md` — the master tracking document

## Guiding Principles

1. **Fidelity to feedback**: Parse what was said, not what you think was meant. If unclear, note it as a question.

2. **One item, one row**: Don't bundle. "Too long and repetitive" is two items.

3. **Everything gets tracked**: Even items you disagree with get logged (mark them for user discussion).

4. **Dependencies are critical**: Wrong sequencing wastes work. If theory changes, don't revise conclusions first.

5. **User owns decisions**: Flag contradictions and ambiguities rather than resolving them yourself.

## When You're Done

Summarize for the orchestrator:
- Total feedback items parsed
- Section-by-skill routing
- Proposed revision sequence
- Questions requiring user input

**Example summary**:
> Parsed 11 feedback items across 6 sections. Routing: Introduction/Conclusion → interview-bookends (3 items), Theory → lit-writeup (3 items), Methods → methods-writer (2 items), Findings/Discussion → direct (3 items). Proposed sequence: Theory → Intro → Methods → Findings → Discussion → Conclusion. One question for user: R1 says expand methods, R2 says paper is too long—how to reconcile?

Then pause for user confirmation before proceeding to Phase 1.
