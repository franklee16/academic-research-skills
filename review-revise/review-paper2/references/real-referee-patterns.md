# Real Referee Report Patterns — /review-paper Reference

*Distilled from actual referee reports and editor letters at top economics journals (REStat). Use these patterns to calibrate tone, depth, and focus when generating reviews.*

---

## 1. How Real Referees Structure Reports

### Positive referee (recommends R&R)
```
Summary paragraph (restate paper's question, method, findings in 3-4 sentences)
→ Strengths paragraph (specific: "well-executed evaluation," "comprehensive indicators," "high follow-up")
→ Numbered substantive comments (5-8), each 1-2 paragraphs
→ Each comment includes a concrete suggestion or question
```

### Skeptical referee (recommends reject/major revision)
```
Summary paragraph
→ Brief acknowledgment of execution quality
→ Main Comments section (numbered, with sub-numbers like 1.1, 1.2 for related points)
→ Minor Comments section (bulleted, shorter)
→ Each main comment explains WHY it matters, not just WHAT the issue is
```

### Editor letter
```
Characterizes referee positions ("one is positive... the other is negative")
→ States own view and where it departs from referees
→ Numbered comments (often 10-16), mixing substantive and presentational
→ Gives explicit framing guidance
→ May push back on BOTH author AND referee positions
```

---

## 2. What Real Referees Prioritize (Beyond Standard Checklists)

### A. Mechanism Testing — Positive Evidence, Not Just Ruling Out
Real referees don't accept mechanism claims based solely on ruling out alternatives. They want:
- **Specific heterogeneity analyses that discriminate between theories.** E.g., if signaling is the claimed mechanism, effects should be larger where employers have less information (tighter labor markets, disadvantaged groups, no prior work experience).
- **Benchmarking.** "Benchmark the treatment effect with an estimate of the returns to education."
- **Direct evidence.** "Could you check whether those with more previous work experience are less likely to benefit?"

*Pattern: Suggest 2-3 heterogeneity cuts that are consistent with the claimed mechanism but inconsistent with alternatives.*

### B. Implementation Fidelity ↔ Interpretation
For program evaluations, referees care deeply about whether the program was delivered as designed:
- Payment delays, mistargeting, short spells — what do these mean for interpreting the results?
- "It is hard to know what would have happened had the program adequately addressed the underlying hypothesized constraints"
- Implementation challenges are not just limitations — they shape what the paper can and cannot claim.

*Pattern: Ask whether the paper evaluates the program-as-designed or the program-as-implemented, and whether the distinction matters for the contribution.*

### C. Cost-Benefit / Return on Investment
Referees want more than just "is the effect significant?" — they want to know if the program is worth it:
- "Complement your discussion of the program benefits with a discussion of the costs"
- "Give the reader a better sense of the return on investment for this specific program"
- Even when cost data is imperfect, back-of-envelope calculations are valuable.

*Pattern: If the paper evaluates a program, ask about costs per participant, cost per unit of outcome change, and comparison to alternative interventions.*

### D. Displacement / General Equilibrium Effects
For labor market interventions, this is nearly always raised:
- "Given that the mechanism is signaling, we have to be concerned with displacement effects"
- Should be discussed early in the paper, not buried in the conclusion
- Can sometimes be tested using variation in treatment saturation across localities

*Pattern: Flag if displacement is acknowledged only in the conclusion. Suggest it be discussed alongside the main results. Propose any available empirical tests.*

### E. Sample Representativeness & External Validity
Real referees push on this in specific, testable ways — not just "is it generalizable?":
- How do study sites compare to non-study sites? (Can be tested with admin/census data)
- How does the study sample compare to the average program participant?
- Are implementation challenges (short duration, menial tasks) common in similar programs elsewhere?
- Editors may push back on excessive defensiveness: "If this was a large-scale U.S. program, we would not be having this discussion."

*Pattern: Don't just flag external validity as a limitation. Suggest a constructive test (compare participating vs. non-participating sites) and push the author toward a confident-but-honest framing.*

### F. Framing — Broader Is Usually Better
Both referees and editors often push authors to broaden their framing:
- "Summer jobs for youth" → "alleviating job experience constraints" (brings in internships, apprenticeships, etc.)
- Narrow framing undersells the contribution: "This actually makes your paper seem more of a small question than it actually is"
- Avoid "first paper to..." claims — they're debatable and they shrink the scope

*Pattern: If the paper is positioned in a narrow literature, suggest a broader frame that captures the same results but connects to a larger question. This is almost always a gift to the author.*

### G. Null Results — Don't Just Say "Not Significant"
- Report p-values even when results are not significant
- Report minimum detectable effect sizes (MDEs) — what can you rule out?
- "It would be good to see what kind of effect sizes you can rule out if the treatment effect is not significant for main outcomes"
- For outcomes with high baseline rates (e.g., 95% enrollment), acknowledge the ceiling explicitly

*Pattern: For every null result, ask: (1) p-value? (2) what is the MDE? (3) is the null informative or just underpowered?*

---

## 3. Table & Presentation Comments Real Referees Make

These are the kinds of specific, actionable table comments that distinguish a useful review:

- **Balance tables**: Show treatment and control means separately, not just the difference. Include randomization inference and joint test.
- **Admin vs. self-reported data**: If both exist, show both. Flag discrepancies as a data quality signal.
- **ITT vs. IV/LATE**: Pick one for the main tables, put the other in the appendix. "They are basically saying the same thing."
- **Combine related tables**: If tables can be merged without loss, suggest it for parsimony.
- **Label self-reported outcomes**: Table titles should flag when outcomes are self-reported.
- **Show results without controls**: If main results include controls, show an appendix table without (except for stratification fixed effects).
- **Variable definitions**: List what's in composite indices. Readers can't evaluate what they can't see.
- **Table notes**: Should make each table self-contained (sample, specification, outcome definition).

---

## 4. Tone Calibration

### What good referees do:
- Acknowledge difficulty and execution: "Successful evaluations of government programs are very challenging. Kudos to the authors."
- Be honest about their own uncertainty: "I don't know if this data exists, but I was wondering..."
- Offer choices, not mandates: "I would leave it to you to decide what you would like to do."
- Distinguish what's necessary from what would be nice: Main Comments vs. Minor Comments separation

### What good referees avoid:
- Vague complaints without suggestions
- Listing every possible concern without prioritizing
- Demanding analyses that would require entirely new data or experiments
- Being more negative than their own evidence warrants

---

## 5. Patterns for the Skill to Emulate

When generating a review, check these patterns against the current skill output:

1. **Does the summary restate the paper's contribution fairly before any criticism?** (Both real referees do this.)
2. **Does each major concern include a concrete suggestion?** (Not just "this is a problem" — "here is how to fix it.")
3. **Are mechanism claims tested with specific heterogeneity suggestions?** (Not just "the mechanism claim is weak.")
4. **Are null results evaluated with MDEs, not just dismissed?**
5. **Is external validity addressed constructively** (suggest comparisons) **rather than as a generic limitation?**
6. **Are table comments specific enough to be actionable?** (Which table, what to add/remove, what format.)
7. **Is the framing advice generous?** (Help the author see the bigger question their paper answers.)
8. **Are displacement/GE effects discussed for labor market papers?**
9. **Is implementation fidelity × interpretation addressed for program evaluations?**
10. **Is cost-benefit analysis requested when reviewing an intervention?**
