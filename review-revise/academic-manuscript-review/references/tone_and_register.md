# Tone and register calibration

This file calibrates *how* the review reads on the page. The analytical content is in SKILL.md; this file is about voice, prose register, and structural choices.

## The target register

The review should read like a careful, senior scholar's pre-submission diagnostic — direct, dense, organized, willing to say what's wrong without softening, but reasoning before verdict on every point.

Two real-world exemplars define the upper end of this register. The passages below are reconstructions written in each letter's register, not quotations; they preserve the rhetorical moves, not the words or the content.

**A real ASQ rejection letter** — direct, prose-driven, organized into numbered concerns with sub-points. Reconstructed passages in its register:

> "In several places, the reviewers and I were not persuaded that the measures capture the constructs the theory requires."

> "I struggled to understand how the generic act of entering a new export market necessarily represents a response to normative pressure."

> "This makes me wonder: Is the first hypothesis essential to the model at all?"

Note what these do: state a position directly, ground it in a specific problem, raise a constructive question. No hedging, no preamble.

**A real AMJ revise-and-resubmit letter** — substantially more verbose and warmer than the ASQ letter, but the structure is the same: numbered hierarchical concerns (1, 1.1, 1.2, 2, 2.1...) with quoted reviewer text and concrete suggestions. Reconstructed passages in its register:

> "I hope you will excuse the bluntness, but if this were published tomorrow, what would management scholars actually be learning from it?"

> "From a logical standpoint, an empirical gap can only motivate an empirical contribution: it does not by itself establish that a theoretical gap exists."

> "I would respectfully encourage you to consider rewriting the front end of the paper to reposition its contribution."

For the user's diagnostic-tool use case, **lean toward the ASQ letter's compactness, not the AMJ letter's warmth.** An editor writing an R&R is addressing authors they are trying not to demoralize; the user is the author and has explicitly asked for unsparing feedback. Drop the conversational warmth, the apologetic prefaces, and the chatty asides. Keep the structural rigor and the willingness to be direct.

## What good prose looks like in this skill's output

1. **Specific over general.** "The construct definition on p.7 conflates X with Y" beats "the constructs need work."
2. **Reasons before recommendations.** "X is a problem because Y; consider Z" beats "you should do Z."
3. **Quoted manuscript text where useful.** When critiquing a specific sentence, quote it (5–15 words) and react to what's actually there.
4. **Manuscript citations.** Use compact notation: "P5p2" for page 5 paragraph 2, "H3" for hypothesis 3, "Table 4 col 3," "intro ¶4." Reviewers do this; it makes feedback actionable.
5. **One issue, one home.** If the abstract problem is theoretical, it goes in Section 4. If it's a wording problem, it goes in Section 9 under "abstract." Never both.

## Anti-patterns: what to avoid

The AI-generated review used as this skill's negative exemplar is structurally competent but has telltale AI-output signatures. Do not produce these.

### Anti-pattern 1: Performative throat-clearing

Bad:
> "I want to be clear that I am not recommending rejection because the idea is uninteresting; I am recommending Reject & Resubmit because the current execution falls short of the bar in ways that require a substantial reconceptualization, not just revision."

Why it's bad: A real reviewer wouldn't bother with this clause. It's a hedge against being perceived as harsh — a social move, not an analytical one. The user has asked for unsparing feedback; this kind of preamble adds words without adding signal.

Good:
> "Reject & resubmit. The idea has genuine merit but the current execution requires reconceptualization, not revision."

### Anti-pattern 2: Saying the same thing in three places

The AI review flags the same measurement issue in Major Concern 2, again in Question 2, and again in the editor note. Each restatement adds length without information.

Rule: each issue gets one home. The "objections" section (Section 10 of SKILL.md) can echo the *framing* of an earlier issue (a real reviewer would phrase it differently than your diagnostic did) but should not duplicate the substance.

### Anti-pattern 3: Heavy formatting as substitute for argument

Bad: italicized phrases, bolded keywords, em-dashes for dramatic pauses, bold-italic combos for emphasis. The AI review uses ***bold-italic*** in numbered concern headers, which signals "this is important" without actually being important.

Good: prose that's emphatic because the *argument* is sharp, not because the formatting is loud. Headers can be bold. Sub-headers can be plain. Emphasis within prose is rare and earned.

### Anti-pattern 4: Theatrical hedge constructions

Phrases to never write:
- "It is worth noting that..."
- "Interestingly,..."
- "I want to be clear that..."
- "To be fair,..."
- "That said,..."
- "It bears mentioning..."
- "I would be remiss not to..."

These are filler. Cut them. The sentence after the hedge is usually the actual point; just write that.

### Anti-pattern 5: Citing-into-existence

The negative exemplar gives a long list of "missing citations" with confident specifics: author trios, exact years, precise attributions of arguments to papers. This is a known LLM failure mode — fluent confabulation of plausible citations. Some are real, some aren't, and the model can't reliably tell which is which.

Rule: when flagging missing literature, **be epistemically honest about the model's limitations**. Acceptable framings:

> "The paper treats its focal actor category as homogeneous. There is a stream of work on heterogeneity within that category that the framing does not survive contact with; the user should identify the current citations and check whether the monolithic treatment holds."

> "Several streams seem underweighted: the platform-governance literature, behavioral work on responses to stakeholder pressure, and post-2020 work on the focal construct. The user should check what's appeared in AMJ/ASQ/SMJ/Organization Science in the last five years on these."

Don't fabricate specific titles, page numbers, or attributions. If a citation is genuinely canonical and verifiable from training (e.g., Williamson 1985, DiMaggio & Powell 1983), it can be named. When uncertain, point to *streams of literature* and let the user verify.

### Anti-pattern 6: Padding the strengths section

The "strongest assets" section in SKILL.md (Section 3) exists to tell the author what to protect. It's not a politeness device. If the paper has one strong move, name one. Don't invent two more for symmetry.

Bad:
> "**Strongest conceptual move:** The paper's recognition that the focal distinction is theoretically meaningful. **Strongest empirical support:** The estimation strategy and the within-unit decomposition. **Strongest section:** The methods section is well-organized."

When the methods section being "well-organized" is the third-best thing about the paper, you're padding. Just say: "The strongest move is X. The empirics are competent but not a comparative advantage; methods organization aside, nothing else stands out."

### Anti-pattern 7: Rhetorical questions used as evasion

> "Can you provide any evidence — direct or archival — that the actors in your setting actually perceive the two arrangements as differently attributable to the focal firm?"

This is not a question. It's a rebuke phrased as a question. Real reviewers use questions when they actually want an answer in the response letter; in a pre-submission diagnostic where there's no rebuttal cycle, "can you provide evidence" should just be "the paper provides no evidence for X; this is a major problem."

Reserve actual questions for genuine ambiguities — places where the user might be doing something you can't tell from the manuscript.

### Anti-pattern 8: Section names that sound like they're for show

The AI review has section headers like "**Manuscript Preparation Errors Must Be Corrected**" and "**The Failure of H2 Reveals a Theory Misspecification That Deserves More Than Acknowledgment**." These are too theatrical — the all-caps urgency, the dramatic phrasing.

Use plain section names: "Hypothesis 2 null result," "Manuscript preparation," "Construct validity of the main independent variable." The content does the work, not the label.

## Length calibration

The user does not mind length — they care about **density**. A 12-page review that says different things on each page is fine; a 12-page review that restates the same five concerns is not.

Approximate target lengths for full review of a typical 35-page empirical manuscript:
- Sections 1–3 (verdict, contribution, strengths): 1.5–2 pages combined
- Sections 4–8 (analytical core): 4–6 pages, weighted toward whichever sections matter most for this paper
- Section 9 (section-by-section): 2–3 pages — compact, can use bullet form
- Section 10 (objections): 1–1.5 pages
- Sections 11–12 (revision priorities, cut/rewrite/keep): 1.5–2 pages combined

If the manuscript has serious problems, weight toward the analytical core. If it's mostly clean and the issues are positioning/prose, weight toward Sections 9 and 11.

## Voice modulation

The default voice is direct-analytical. Adjust within bounds:

- **For drafts the user describes as "early" or "rough":** more developmental in tone, more emphasis on what to build toward, less on prose-level critique. The diagnosis is still candid.
- **For drafts described as "near-final" or "pre-submission":** sharper on prose, formatting, citation completeness, and the kinds of details a real reviewer would catch. Diagnostic is unchanged.
- **For revision drafts (without rebuttal review):** review as a standalone manuscript. Don't speculate about prior versions or reviewer cycles.
- **For drafts not by the user (rare — e.g., reviewing a colleague's work):** same diagnostic, but soften the absolute prohibition on hedging slightly. The user may want to share the review and shouldn't have to manually re-diplomacy it.

## A note on humor

Don't. The user is direct and analytical, not someone who appreciates wit in technical contexts. Reviewer 2 stereotypes (acerbic, occasionally sarcastic) are explicitly *not* what this skill produces.
