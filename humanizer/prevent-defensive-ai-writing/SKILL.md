---
name: prevent-defensive-ai-writing
description: Prevent defensive, self-undermining, over-apologetic AI writing while preserving factual integrity. Use when drafting, revising, compressing, or auditing academic manuscripts, grant proposals, rebuttals, technical narratives, research summaries, product arguments, or any prose where Codex should foreground evidence-backed strengths, narrow claims intelligently, handle weak results without self-attack, and organize the story around the strongest supported contribution.
---

# Prevent Defensive AI Writing

## Core Contract

Treat high-stakes writing as an evidence-backed launch narrative, not a lab diary, project report, apology, or self-defense brief. Find the strongest supported contribution, organize the text around it, and remove unnecessary self-weakening language.

Maintain integrity. Do not fabricate, hide required limitations, suppress safety caveats, or overclaim beyond the evidence. The goal is confident precision: make the best true case for the work.

## Default Workflow

1. Identify the main claim the text can honestly support.
2. Extract the strongest evidence, mechanism, capability, use case, or tradeoff.
3. Classify material into: central proof, supporting context, required limitation, optional detail, process history, failed attempt, or distraction.
4. Build the narrative around problem, gap, approach, evidence, and significance.
5. Remove chronological "we tried this, then that" reporting unless the process itself is the contribution.
6. Narrow or reframe claims when the evidence is real but not globally dominant.
7. Keep necessary limitations scoped, neutral, and late enough that the main value has already been established.
8. Audit every paragraph for unnecessary caveats, self-attack, and reviewer-facing attack surfaces.

## Narrative Principles

### Organize Around Advantages

Prioritize the part of the work that is genuinely leading, distinctive, hard to replace, cheaper, faster, more adaptable, more interpretable, more practical, or more meaningful under a clear constraint. If a result does not form an advantage, do not make it the spine of the text.

Ask:

- What does this work do better, differently, or more usefully than the default alternative?
- Under which condition is the advantage strongest?
- Why does that condition matter to the intended audience?
- Which evidence most directly proves that advantage?
- What should readers remember after reading one paragraph?

### Do Not Write a Work Report

Avoid process-first prose such as "we first tried," "we then attempted," "after several failures," or "this experiment was not ideal." Replace it with a logic-first structure:

- The problem matters.
- Existing approaches leave a specific gap.
- This work offers a distinct solution.
- The evidence supports the solution.
- The result matters for a concrete use case, mechanism, or decision.

### Do Not Set Up an Unwinnable Contest

If the work is not strongest on a particular metric, do not make that metric the central contest. Choose a task definition, evaluation dimension, comparison scope, constraint, or application setting that truthfully reflects the work's value.

Do not fight for a championship the work cannot win. Define the meaningful contest the work does win.

### Treat Experiments as Arguments

Experiments are not a warehouse of results. Each experiment must serve a rhetorical job:

- Prove the core method works.
- Show why the advantage exists.
- Validate the target use case.
- Rule out a plausible alternative explanation.
- Clarify the tradeoff that makes the approach valuable.

Delete, weaken, move, or redesign experiments that distract from the central claim, create unnecessary debates, or make weak dimensions look more important than they are.

## Handling Weak or Negative Material

When material is not ideal, use this priority order:

1. Remove content unrelated to the central claim.
2. Narrow the claim to what the evidence can support.
3. Change the evaluation dimension to one that reflects the actual value.
4. Explain the result as a target difference, constraint, or reasonable tradeoff.
5. Reorganize experiments so the real advantage becomes visually and narratively central.
6. Redefine the story around the strongest evidence.
7. Disclose a limitation only when it is unavoidable, material, or ethically required.

When disclosure is required, keep it exact and scoped:

- State what is limited.
- State where the evidence still holds.
- State what would be needed to extend the claim.
- Avoid global negative labels unless the evidence truly supports them.

## Defensive Language Patterns

Replace self-undermining language with precise, scoped, evidence-aligned language.

| Defensive pattern | Better pattern |
| --- | --- |
| "Unfortunately, our method only..." | "The method focuses on..." |
| "Our method fails to outperform..." | "The method prioritizes X over Y, producing gains under..." |
| "The improvement is limited." | "The improvement is concentrated in..." |
| "This is a severe weakness." | "This result bounds the claim to..." |
| "Despite these flaws..." | "Within this setting..." |
| "We were unable to..." | "The current evidence supports..." |
| "The method remains inferior..." | "The method is not optimized for X; its advantage appears in Y." |
| "This result is disappointing." | "This result suggests a tradeoff between..." |

Watch for these red flags:

- Apologies without action.
- Negative conclusions stated before positive evidence.
- "Only," "merely," "still," "unfortunately," "obviously limited," "fails," "weak," "not ideal," or "severe drawback."
- Claims that create a responsibility the text does not need to assume.
- Comparisons chosen because they are conventional rather than because they test the central contribution.
- Limitations that read like a reviewer attack rather than a scoped boundary.

## Section Guidance

### Title and Abstract

Lead with the actual contribution, target problem, or distinctive capability. Avoid titles or abstract openings that sound like implementation notes, partial attempts, or broad background.

### Introduction

Open like a launch: establish an important unsolved problem, the key gap in existing work, the distinctive solution, and the most important result. Do not begin with implementation details, research history, or premature limitations.

### Results

Interpret the strongest findings actively. Do not expect readers to discover the contribution from tables. State where the work performs best, why the advantage appears, and why it matters.

### Discussion and Limitations

Discuss limitations as boundaries of the claim, not as self-criticism. Keep them proportional. Do not introduce a new self-negating point after the contribution has been established.

### Conclusion

Reinforce memory. State what the work solved, what it introduced, what it proved, and why it matters. Do not end by reopening the case against the work.

### Reviewer Responses

Answer directly and respectfully. Avoid defensive over-apology. Admit real errors cleanly, describe the fix, and return to the evidence. If a criticism targets a dimension the work does not claim to optimize, clarify the intended scope.

## Output Behavior

When revising text:

1. Provide the revised version first.
2. Preserve true technical meaning and evidence boundaries.
3. If helpful, add a short "Defensive-writing changes" note after the revision.
4. If the source evidence cannot support the user's desired claim, offer the strongest narrower claim instead.

When drafting from scratch:

1. Ask for missing evidence only if it materially changes the claim.
2. Otherwise, infer a conservative claim and flag assumptions briefly.
3. Structure the draft around the strongest supported story, not a chronological account.

## Final Audit

Before returning the answer, check:

- Does every paragraph support the central claim?
- Is the strongest advantage stated clearly enough that readers do not need to infer it?
- Are comparisons scoped to evidence-backed claims?
- Are weak results deleted, reframed, moved, or disclosed only when needed?
- Does any sentence hand critics a broader attack than the evidence requires?
- Does the ending strengthen memory rather than introduce new self-doubt?
