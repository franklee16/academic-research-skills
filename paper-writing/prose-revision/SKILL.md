---
name: prose-revision-simple 
description: Revise draft prose by diagnosing and improving idea flow before sentence-level polish. Use when the user asks for comments on a paragraph or sentence, says prose feels awkward, asks for better flow, wording alternatives, restructuring, rewriting, polishing, or general improvement of non-final prose. Default to this skill for paragraph-level writing questions unless the user explicitly asks for proofreading, typo checks, or final copyediting.
---

# Prose Revision

## Purpose

Revise draft prose by finding the best structure for the ideas the user already wants to express. The goal is clear logical movement supported by natural, elegant language: idea flow first, linguistic flow second.

Prose revision is different from proofreading. Prose revision takes a relatively unpolished draft and gets the prose into good shape. Proofreading takes a close-to-done draft and catches mistakes, typos, obvious phrasing problems, and final copyediting issues. Proofreading may flag passages that need prose revision, but prose revision logically comes first.

## Default Stance

Assume the user usually has the right set of ideas and wants help discovering the best structure for those ideas. Be willing to revise aggressively at the level of order, emphasis, sentence boundaries, transitions, and paragraph shape, while preserving the substantive claims.

Do not add or subtract ideas by default. The user's ideas are the raw material you are re-arranging, not a prompt for new content. Add a missing idea, remove an idea, or move an idea out of the paragraph only when it is clearly necessary for the paragraph to work - and when you do, name the intervention explicitly ("I added X because the contrast isn't legible without it" / "I dropped the aside about Y; it belongs in the next paragraph"). If you think an idea is missing but aren't sure, raise it as a suggestion rather than silently inserting it.

Treat awkward sentences as evidence of a possible idea-flow problem, not merely a bad-English problem. A sentence is often awkward because it is trying to do two jobs at once, because the previous sentence did not prepare it, or because the paragraph's logical order is not yet right. Polishing the sentence in place usually reproduces the original awkwardness in prettier words; restructuring the ideas around it actually fixes it.

## Workflow

1. Read the target prose and enough context to understand the local argument.
2. Identify the paragraph's intended job: the claim, contrast, mechanism, qualification, implication, or transition it needs to deliver.
3. Diagnose idea flow before wording. Look for ideas in the wrong order, overloaded sentences, missing connective tissue, premature qualifications, buried main claims, or a final sentence that belongs earlier.
4. If the idea structure prevents good flow, explain that structural problem first. Do not try to solve structural confusion with surface-level polish.
5. Rearrange and repack the existing ideas into a clearer logical sequence. Then make the language smoother, cleaner, and more elegant.
6. Offer revised versions that make different tradeoffs when useful: conservative, moderate, or more polished. Keep explanations concise and focused on why the structure works.
7. If the user asks to apply edits, edit the source file rather than generated outputs, and preserve notation, citations, labels, author notes, and technical claims unless the user explicitly asks to change them.

## What To Improve

Prioritize changes that improve the reader's path through the ideas:

- Put the main point where it can organize the rest of the paragraph - usually early, so the reader has a frame for what follows.
- Split sentences that are doing multiple logical jobs.
- Combine sentences when separation makes the logic choppy.
- Move qualifications after the claim they qualify, unless the qualification must come first for accuracy.
- Add transitions only after the underlying relation between ideas is clear. A transition word glued onto an unclear relation just disguises the problem.
- Replace vague connective language ("furthermore", "in addition", "moreover") with the actual logical relation: contrast, mechanism, implication, caveat, example, or consequence. If the relation is contrast, say how; if it is mechanism, the reader should see the mechanism.
- Prefer precise, economical wording once the idea structure is sound.

## Examples

The pattern below shows a diagnosis-first move: the sentence isn't bad English, it's doing two jobs and burying the main claim.

**Example 1 - overloaded sentence, buried claim**
Input: "Firms with high ESG scores, which have become increasingly popular among institutional investors in recent years, tend to exhibit lower return volatility, although the effect is concentrated in markets with strong regulation."
Diagnosis: One sentence carries a background trend, a main finding, and a qualification. The main claim is buried in a relative clause. Split into three beats: context, claim, scope.
Revision: "High-ESG firms have drawn growing institutional interest. They also tend to exhibit lower return volatility - though mainly in markets with strong regulation."

**Example 2 - vague transition hiding the real relation**
Input: "Investors overreact to salient news. Furthermore, the overreaction persists for several weeks."
Diagnosis: "Furthermore" signals addition, but the real relation is elaboration - the persistence is what makes the overreaction economically interesting, not a second separate fact.
Revision: "Investors overreact to salient news, and that overreaction persists for several weeks." (or, sharper: "Investors overreact to salient news - and the overreaction lingers for weeks, which is what makes it tradeable.")

**Example 3 - qualification arriving before the claim it qualifies**
Input: "The effect disappears in small samples. The treatment increases output by 12%."
Diagnosis: The qualification ("disappears in small samples") lands before the reader knows what effect is being qualified. Reverse the order so the claim arrives first.
Revision: "The treatment increases output by 12%. That effect disappears in small samples, however, so we treat the headline number cautiously."

These examples illustrate the stance, not a fixed template - the same diagnosis-first logic applies whatever the topic.

## Handling Longer Passages

For multi-paragraph sections, diagnose at the paragraph level before descending into sentences: does each paragraph have a single governing idea, and does the sequence of paragraphs advance a clear argument? If two paragraphs are doing one job, merge; if one paragraph is doing two, split. Only once the paragraph architecture is right does sentence-level revision pay off across the whole passage.

## LaTeX and Technical Prose

When the source is LaTeX, treat the markup as load-bearing structure, not noise. Preserve `\cite{}`, `\citep{}`, `\citet{}`, `\ref{}`, `\label{}`, `\cref{}`, math mode (`$...$`, `\[...\]`, `align`), `\thanks{}`, and `\textbf{}`/`\emph{}` for author-introduced emphasis. Revise the prose around them; do not rewrite a `\cite` into a paraphrase or flatten a displayed equation into inline math to "smooth the flow". If a citation or equation genuinely interrupts the logic, say so and propose moving it - don't silently relocate it.

## Output Style

For short interactive requests, usually provide:

1. A brief diagnosis of what is limiting the flow.
2. Two or three revised versions, if alternatives would help.
3. A short note on the tradeoff among versions.

For longer documents, provide a structured revision report unless the user asks for direct edits.

Keep line-level proofreading comments out of prose-revision responses unless they materially affect flow or clarity.
