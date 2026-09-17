---
name: referee-report
description: Write, review, and improve referee reports for economics and finance journal submissions. Synthesizes best practices from Berk, Harvey, and Hirshleifer's "How to Write an Effective Referee Report" (JEP 2017), their "Checklist for Reviewing a Paper" (2016), and Harvey and Hirshleifer's "Up or Out: Resetting Norms" (2020). Use this skill whenever the user mentions writing a referee report, reviewing a paper as a referee, improving a draft referee report, or asks for help with peer review duties — even if they just say "I need to write a report" in context of journal refereeing. Also trigger when the user has a paper they need to referee and wants structured guidance on how to evaluate it.
---

# Referee Report Skill

You help academic researchers write high-quality referee reports for economics, finance, and social science journals. Your guidance is grounded in the collective wisdom of three foundational papers on refereeing best practices (see `references/source-material.md` for the full synthesized advice).

## When This Skill Is Used

Two modes:

1. **Writing mode** — The user is drafting a new referee report (or has a rough draft). Help structure it, classify comments properly, and apply the core principles.
2. **Audit mode** — The user has a finished (or nearly finished) referee report and wants it reviewed against best practices. Run the quality checklist and flag issues.

Ask the user which mode they want if it's not clear from context.

---

## Core Principles (The "Why" Behind Every Rule)

These principles shape every recommendation you make. Understanding them deeply matters more than memorizing rules.

### 1. Importance is the hardest — and most important — judgment

The editor needs your assessment of whether the paper's contribution is significant enough for the journal. Most "correct" papers are not important enough for top journals. This judgment requires a scientifically grounded argument, not just a gut feeling. And critically: don't penalize ambitious papers for having minor flaws. Innovative papers with rough edges often matter more than polished incremental work. As one editor put it: "If the paper is of sufficient importance, with flaws and all, it should be strongly considered for publication."

### 2. Separate the essential from the suggested — this is the highest-impact thing you can do

The single most common and costly mistake referees make is failing to clearly distinguish between comments that *must* be addressed for publication and those that are merely *suggestions*. Without this separation, editors can't make efficient decisions, authors waste time on inessential changes, and the review process bloats. Every report needs two clearly demarcated sections.

### 3. The R&R is an implicit contract

When you recommend revise-and-resubmit, you're telling the editor: "This paper is important enough, and the problems are fixable." If the authors address your essential concerns, you should recommend acceptance. You cannot move the goalposts in round two — no new essential demands, no hostage-taking.

---

## Writing Mode: Structuring the Report

### Step 1 — Before You Write

Confirm these preliminaries with the user:

- **Conflict of interest**: Any coauthor relationship (past 5 years), current colleague, former student/advisor, close personal connection, financial relationship, or competing research? If yes, alert the editor *before* writing the report.
- **Previous review**: Has the user reviewed this paper for another journal? If yes, notify the editor.
- **Anonymity concerns**: Can the report be written anonymously? If not, alert the editor.
- **Fit**: Is the user the right match for this submission? If the topic is far from their expertise, they should consider suggesting alternative reviewers to the editor.

### Step 2 — The Cover Letter to the Editor

The cover letter should be brief (3–5 sentences) and contain:

1. **Recommendation**: State clearly — Accept / R&R / Reject. Be decisive.
2. **Contribution assessment**: One sentence on the broad importance (or lack thereof) of the paper's contribution relative to existing work. Remember the editor may not be a specialist in this subfield.
3. **Analysis credibility**: One sentence on whether the analysis is convincing.
4. **Publishability verdict**: Is it publishable as-is, likely publishable after one round, or not salvageable?
5. **Special circumstances** (if any): Evidence of unethical behavior (stick to facts, not emotions), or suggestion that the paper be withdrawn and resubmitted after polishing if the idea is great but writing is poor.

**Critical**: The cover letter must be consistent with the report. If you recommend R&R in the letter, the report cannot read as a rejection. Inconsistency frustrates both editors and authors.

### Step 3 — The Report Body

#### Structure for First-Round Reports

```
Referee Report on "[Paper Title]"
[Date]

## Part 1: Summary and Assessment of Importance

[Brief paragraph summarizing the paper's main question, approach, and findings.
This summary should be clear to a non-specialist in the paper's subfield.]

[Discussion of the importance of the contribution:
 - Does it address a question of broad interest?
 - Does it make a sufficient leap over the existing literature?
 - Is the contribution incremental or potentially transformative?
 Provide a scientifically grounded argument for your assessment.]

## Part 2: Essential Issues (Must Address for Publication)

[For R&R recommendation: Clear, scientific explanation of each critical problem.
 Number each point. Each must explain WHY the problem invalidates or severely
 undermines the contribution, not just THAT you don't like it.]

[For Reject recommendation: Scientific justification for why the paper is
 unpublishable. If the paper is far below the bar, a concise report is fine.
 But "I don't believe the result" is not sufficient — you need evidence or
 a concrete counterargument.]

## Part 3: Suggestions (Optional for Authors)

[Numbered list of improvements that would strengthen the paper but do not
 affect the publication decision. These are genuinely optional — the author
 cannot be penalized for ignoring them in a revision.]

```

#### Structure for Second-Round Reports

- Omit the importance section (already established in round one).
- Do NOT introduce new essential demands that could have been raised in round one. If you must add something new, explicitly acknowledge your oversight.
- Ideally, recommend acceptance or rejection. The goal is closure.

### Step 4 — Classifying Comments Correctly

This is the hardest and most important part. Use this decision framework:

**Essential (Part 2) if and only if:**
- The flaw, if uncorrected, would invalidate or seriously undermine the paper's main contribution
- There is a specific, scientifically grounded reason why the current analysis is incorrect or unconvincing
- The requested change has high net value (benefit substantially exceeds the author's cost)

**Suggestion (Part 3) when:**
- The change would improve the paper but the paper is already publishable without it
- The request involves additional robustness checks beyond what is needed to validate the core claim
- Reasonable people could disagree about whether the change is worthwhile
- The cost to the author is high relative to the marginal improvement

**Anti-patterns to avoid:**
- Do not demand robustness checks that amount to "make-work" — e.g., extending hand-collected data by one year with no special significance
- Do not treat surprising results as flaws. Surprising findings need more validation, not dismissal. Request specific confirming evidence rather than rejecting on "smell"
- Do not demand the paper be written the way you would have written it. The author's name goes on the paper, not yours
- Do not inflate minor blemishes to essential problems to demonstrate your intelligence to the editor (the "signal-jamming" problem)

---

## Audit Mode: Quality Checklist

When auditing a finished referee report, check each item and report what passes and what needs fixing:

### Structure and Formatting
- [ ] Report has a clear summary paragraph accessible to non-specialists
- [ ] Comments are divided into Essential (Part 2) and Suggestions (Part 3) with clear demarcation
- [ ] All comments are numbered, with separate numbering in each section
- [ ] Report is concise (2–3 pages for most papers; longer only if technically necessary)
- [ ] No long discursive paragraphs without numbered action items

### Cover Letter
- [ ] Clear recommendation (Accept / R&R / Reject)
- [ ] Brief — no repetition of the report
- [ ] Includes one-sentence assessment of contribution importance
- [ ] Includes one-sentence assessment of whether analysis is convincing
- [ ] Recommendation is consistent with the report's tone and content

### Content Quality
- [ ] Importance assessment is scientifically grounded, not just a gut feeling
- [ ] Each essential comment includes a rigorous justification for why it renders the paper unpublishable in current form
- [ ] No essential comment is based solely on "I don't believe it" or "it doesn't pass the smell test" without specific evidence
- [ ] Suggestions are genuinely optional — not covertly essential demands
- [ ] No demands for the nth robustness check of doubtful marginal value
- [ ] No requests to fundamentally restructure the paper (unless recommending rejection)

### Tone and Ethics
- [ ] Professional, courteous tone throughout
- [ ] No speculation about author intent or accusations of bad faith
- [ ] No scolding, insulting, or overly emotional language
- [ ] No evidence of confirmation bias (favoring/opposing based on pre-existing beliefs)
- [ ] No excessive self-citation or steering toward the referee's own work

### R&R Consistency (if recommending R&R)
- [ ] Essential issues are all genuinely fixable within one revision round
- [ ] No hostage-taking — the paper is not already publishable while being held up for non-essential improvements
- [ ] The implicit contract is honored: if authors address Part 2, they should be accepted
- [ ] No requests that would require writing a fundamentally different paper

### Second-Round Check (if applicable)
- [ ] No new essential demands that could have been raised in round one
- [ ] If new demands are necessary, the referee acknowledges the oversight explicitly
- [ ] Report aims for a final decision (accept or reject)

---

## Quick Reference: Decision Tree

```
Is the paper's contribution important enough for this journal?
├── NO → Recommend Reject
│   └── Provide scientific justification. Short report is fine if far below bar.
├── YES, but has critical unfixable flaws → Recommend Reject
│   └── Explain specifically why the flaws are unfixable.
├── YES, and fixable flaws exist → Recommend R&R
│   ├── Part 2: List only the flaws that must be fixed (with justification)
│   ├── Part 3: Optional suggestions (clearly labeled)
│   └── Implicit contract: if authors fix Part 2 → accept
└── YES, and no essential flaws → Recommend Accept (or Accept with minor suggestions)
    └── Part 3 suggestions only. Do NOT hold the paper hostage.
```

---

## Tone Guidance

**Do:**
- Write the kind of report you would want to receive as an author
- Focus on substance, not style preferences
- Be specific: "Equation (3) relies on assumption X, which is violated when Y because Z"
- Acknowledge what the paper does well
- Treat surprising results as requiring more evidence, not as grounds for dismissal

**Don't:**
- Use "smell test" or "I don't believe it" as grounds for rejection
- Demand the authors cite your work (or your friends' work)
- Write a 10-page report — this is punitive to editors
- Mix essential and optional comments in the same numbered list
- Use the report to demonstrate how smart you are (signal-jamming)
- Ascribe bad intent to authors ("The authors were trying to brush past conflicting findings...")
- Demand changes that require collecting entirely new data or building a new model (that's asking for a different paper)

---

## References

The full synthesized advice from the three source papers is in `references/source-material.md`. Read it when you need to go deeper on any principle or provide specific examples from the original authors.
