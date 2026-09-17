# Phase 4: Verification & Response

## Why This Phase Matters

Before declaring revision complete, you need to verify that all feedback has actually been addressed. This phase creates accountability—a clear record of what was changed, how each feedback item was handled, and any remaining gaps.

If the revision is for a journal R&R, this phase also produces the response memo.

## Verification Tasks

### Task 1: Feedback Item Audit

Go through EVERY feedback item from Phase 0 and verify its status:

```markdown
## Feedback Item Audit

### Introduction Items
| ID | Feedback | Status | How Addressed | Location |
|----|----------|--------|---------------|----------|
| I-1 | Too long | [x] | Cut 200 words, removed redundant para | Intro para 2 removed |
| I-2 | Two intros | [x] | Merged into single intro | N/A |

### Theory Items
| ID | Feedback | Status | How Addressed | Location |
|----|----------|--------|---------------|----------|
| T-1 | Compress 30% | [x] | Cut 450 words | Throughout |
| T-2 | Strengthen turn | [x] | Sharpened gap→contribution pivot | Theory, final para |
| T-3 | Define "absorption" | [x] | Added definition | Theory para 2 |

### Methods Items
| ID | Feedback | Status | How Addressed | Location |
|----|----------|--------|---------------|----------|
| M-1 | Coding detail | [x] | Expanded coding process description | Methods para 4-5 |
| M-2 | Reliability | [x] | Added structured recoding statement | Methods para 5 |

### [Continue for all sections...]
```

**Status codes**:
- `[x]` — Fully addressed
- `[~]` — Partially addressed (explain what remains)
- `[!]` — Requires user decision (explain options)
- `[-]` — Declined to address (explain why)

### Task 2: Change Summary

Create a section-by-section summary of what changed:

```markdown
## Revision Summary

### Introduction
**Word count**: 850 → 650 (-200 words)
**Structural changes**: Merged two introductions into one; removed redundant "Background" section
**Key improvements**: Opening now directly poses the puzzle; roadmap is clearer

### Theory/Literature Review
**Word count**: 1800 → 1350 (-450 words)
**Structural changes**: None (same 3 subsections)
**Key improvements**: Turn (gap → contribution) is now explicit and positioned at section end; "organizational absorption" defined with observable indicators

### Methods
**Word count**: 900 → 1400 (+500 words)
**Structural changes**: Changed from Efficient to Detailed pathway
**Key improvements**: Added coding process (para 4-5), structured recoding (para 5), saturation statement (para 6)

### Findings
**Word count**: 4000 → 3850 (-150 words)
**Structural changes**: None
**Key improvements**: Aligned terminology with revised theory section; tightened some evidence-interpretation sequences

### Discussion
**Word count**: 1200 → 1400 (+200 words)
**Structural changes**: Added scope conditions subsection
**Key improvements**: Explicit scope conditions; stronger connection to literatures

### Conclusion
**Word count**: 600 → 550 (-50 words)
**Structural changes**: None
**Key improvements**: Added callbacks to intro language ("dispersal" framing)
```

### Task 3: Unaddressed Items Documentation

For any items marked `[~]`, `[!]`, or `[-]`, provide detailed explanation:

```markdown
## Unaddressed or Partially Addressed Items

### [!] D-1: Scope conditions
**Feedback**: "Add scope conditions"
**Status**: Requires user decision
**Options**:
1. Limit to high-intensity movements only (narrower, safer)
2. Propose generalization to any identity-absorbing organization (broader, riskier)
3. Add both as explicit contrasting scope conditions

**Recommendation**: Option 3 (present both, let readers judge)

### [~] F-1: More quantitative data
**Feedback**: "Consider adding more quantitative data"
**Status**: Partially addressed
**What was done**: Added counts for each exit pathway type (Table 2)
**What remains**: Did not add multivariate analysis (beyond scope of qualitative approach)
**Rationale**: Qualitative methodology doesn't support statistical inference; counts are descriptive

### [-] R2-3: Compare to other movements
**Feedback**: "Would be strengthened by comparison to other movements"
**Status**: Declined to address
**Rationale**:
- Would require additional data collection beyond revision scope
- Comparative claims are already hedged as future research direction
- Single-case depth is methodological strength, not weakness
```

### Task 4: Word Count Reconciliation

If word limits are a constraint, verify compliance:

```markdown
## Word Count Summary

| Section | Original | Revised | Change |
|---------|----------|---------|--------|
| Abstract | 150 | 148 | -2 |
| Introduction | 850 | 650 | -200 |
| Theory | 1800 | 1350 | -450 |
| Methods | 900 | 1400 | +500 |
| Findings | 4000 | 3850 | -150 |
| Discussion | 1200 | 1400 | +200 |
| Conclusion | 600 | 550 | -50 |
| **Total** | **9500** | **9348** | **-152** |

**Target**: 10,000 words
**Status**: ✓ Within limit
```

### Task 5: Response Memo (for R&R)

If this is a journal revision, draft a response memo:

```markdown
# Response to Reviewers

## Editor
Thank you for the opportunity to revise this manuscript. We have carefully considered all feedback and made substantial revisions as detailed below.

## Reviewer 1

### Comment 1.1
> "The introduction is too long and repetitive—you have two intros."

**Response**: We agree and have restructured the opening. The original manuscript had both an Introduction and a "Background" section that covered similar ground. We have merged these into a single, streamlined Introduction (now 650 words, down from 850). The Introduction now opens directly with the empirical puzzle, presents the gap, previews our contribution, and provides a roadmap—without the repetition the reviewer correctly identified.

**Changes**: See revised Introduction, pp. 1-2.

### Comment 1.2
> "Methods need more detail on coding."

**Response**: We have substantially expanded the Methods section (now 1400 words, up from 900) to address this concern. Specifically, we added:
- A detailed description of our three-stage coding process (para 4)
- Explanation of how we distinguished key constructs (pace exhaustion vs. grief accumulation vs. fit failure) (para 5)
- Statement on structured recoding after refining definitions (para 5)

**Changes**: See revised Methods, pp. X-Y, paragraphs 4-5.

### [Continue for all feedback items...]

## Reviewer 2

[Same format...]

## Summary of Major Changes

1. **Structural**: Merged two introductions; added scope conditions to Discussion
2. **Methodological**: Expanded coding detail; clarified construct distinctions
3. **Conceptual**: Sharpened the turn (gap → contribution); defined "organizational absorption" with observable indicators
4. **Presentational**: Compressed theory section by 25%; added Table 2 (exit pathway counts)

We believe these revisions address the reviewers' concerns while preserving the manuscript's core contributions. Thank you again for the constructive feedback.
```

## Verification Checklist

Before declaring revision complete, confirm:

- [ ] All feedback items have a status (`[x]`, `[~]`, `[!]`, or `[-]`)
- [ ] All `[~]` items have explanation of what remains
- [ ] All `[!]` items have options presented to user
- [ ] All `[-]` items have rationale for declining
- [ ] Change summary covers every section
- [ ] Word count is within limits (if applicable)
- [ ] Response memo drafted (if R&R)
- [ ] Revised manuscript assembled in correct order

## Output Files

Create in `revision/` directory:
- `revision-summary.md` — Complete accounting of changes
- `response-memo.md` — Reviewer response (if R&R)
- `revised-draft.md` — Complete revised manuscript

## Final Assembly

Assemble the revised manuscript in correct order:

1. Title page (if required)
2. Abstract
3. Introduction
4. Theory/Literature Review
5. Case Justification (if Policy-Driven cluster: before Theory)
6. Methods
7. Findings
8. Discussion
9. Conclusion
10. References
11. Tables and Figures
12. Appendices

## When You're Done

Summarize for user:
- Total feedback items: X
- Fully addressed: Y
- Partially addressed: Z (with reasons)
- Requires decision: W (with options)
- Declined: V (with rationale)
- Word count change: ±N words
- Response memo: Ready/Not needed

**Example final summary**:
> Revision complete.
>
> **Feedback accountability**:
> - 11 feedback items total
> - 9 fully addressed [x]
> - 1 partially addressed [~] (quantitative data — added counts, declined multivariate)
> - 1 requires decision [!] (scope conditions — three options presented)
> - 0 declined
>
> **Word count**: 9500 → 9348 (-152 words), within 10K limit
>
> **Deliverables**:
> - `revised-draft.md` — Complete revised manuscript
> - `revision-summary.md` — Full change documentation
> - `response-memo.md` — Reviewer response ready for review
>
> **Action needed**: Please confirm scope conditions choice (D-1) before finalizing.

Revision coordination complete.
