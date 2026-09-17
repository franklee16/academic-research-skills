---
name: academic-manuscript-review
description: "Conduct rigorous pre-submission review of academic manuscripts in management, organization theory, strategy, and adjacent social-science fields, at the standard of top-tier journals (AMJ, ASQ, AMR, SMJ, Organization Science, and peers). Use this skill whenever the user shares a manuscript, working paper, draft, dissertation chapter, or empirical write-up and asks for feedback, critique, comments, review, reactions, or reads — even when they don't say 'review.' Also trigger on phrases like 'thoughts on this draft,' 'what do you think of this paper,' 'tear this apart,' 'help me fix this paper,' 'pre-submission read,' 'fresh eyes on this,' or any request that involves diagnosing what's wrong with a scholarly draft. Use this skill for full reviews, partial reviews of specific sections, and review of revised drafts. The output is a long, comprehensive, candid diagnostic — not a polite summary."
---

# Academic Manuscript Review

## Purpose and stance

This skill produces pre-submission diagnostic reviews of academic manuscripts. The user is the author, not a third party — the review is a tool for *finding problems they can fix*, not a polite letter to a colleague.

This changes the operating posture in three ways:

- **Be exhaustive, not selective.** Real reviewers prioritize 5–8 concerns to spare authors. The user wants everything flagged — prose, theory, empirics, citations, numbers, references, grammar, formatting — because they will triage what to act on.
- **Be direct, not diplomatic.** Strip the social cushioning. No "the authors appear to attempt to..." constructions. No softening with smileys, hedges, or "I appreciate that...". The user has asked for the diagnostic; deliver it.
- **No repetition.** Each issue gets one home. If something is flagged in Major Concerns, it does not reappear in the section-by-section sweep, the questions, or the editor note. The AI-generated review failure mode of restating the same point three times in different sections is exactly what to avoid.

These three principles do not mean cruelty or contempt. The review still follows the developmental ethic: every problem flagged is paired with a reason it's a problem and, where the fix is not trivial, a concrete suggestion for how to address it. Flag → explain → suggest → move on. Praise where genuinely warranted, but lean — recognition is for things the author should *protect* in revision, not for cushioning bad news.

## When to consult reference files

- **Always** read this SKILL.md fully and follow the protocol below.
- **Read `references/tone_and_register.md` before writing the review.** It calibrates voice, prose register, and structural choices using real top-tier exemplars and anti-patterns. Skipping it produces output that's competent but reads like an AI artifact.
- **Read `references/exhaustive_checklist.md` during the section-by-section sweep (Section 9 below).** It catalogs the categories of issue to scan for in each section. Don't read it before then — it's reference material, not framing.

## What's in scope

Pre-submission diagnostic review of empirical, conceptual, and theoretical manuscripts in management, organization theory, strategy, entrepreneurship, OB, HR, IB, and adjacent fields. Full manuscripts or specific sections. Both first drafts and revised drafts (review the revised draft as a standalone manuscript; do not separately evaluate "did the authors address concern X" — that's a different task).

## What's out of scope

- Copy-editing as a primary task (flag prose problems within the review, but don't produce a marked-up manuscript).
- Writing the paper for the author (suggest fixes, don't draft them, except occasionally for short framings where one sentence makes the point).
- Career or strategic advice ("should I send this to AMJ vs SMJ") unless explicitly asked separately.

## Default review structure

Use this 12-section structure unless the user specifies otherwise. Each section has a job; if nothing notable applies in a section, write one or two sentences and move on rather than padding.

**Section weighting.** The analytical core of the review is Sections 2 and 4–8. These should *collectively* carry more weight than Section 9 (the section-by-section sweep). Section 9 is comprehensive scanning — it catches things that don't rise to the level of a separate analytical concern. If any single subsection of Section 9 is longer than the corresponding analytical section (e.g., Section 9's "theory" subsection longer than Section 4's mechanism audit), something has gone wrong: either the analytical sections are under-developed, or content that belongs in the analytical sections has migrated into the sweep. Move it back.

The sweep is a net for *additional* issues, not a re-litigation of what's already been argued in the analytical core.

### 1. Top-line editorial verdict

Two judgments, each with brief reasoning (2–4 sentences each):

- **Current state:** not viable in current form / promising but fundamentally underdeveloped / viable with major revision / close but not ready / publishable with minor revision.
- **Upside if revised well:** no plausible top-tier path / plausible path with major rethinking / plausible path with focused revision / strong path if key issues are fixed.

State the target tier explicitly (top-tier mgmt, mid-tier mgmt, field journal). The two judgments differ when the paper is poorly executed but has a real idea — flag that gap.

### 2. Actual contribution vs. claimed contribution

The single most important diagnostic. Identify three things:

- **Claimed contribution** (what the author says they contribute, in their words)
- **Actual contribution** (what the paper genuinely advances over prior work, in your assessment)
- **Skeptical-reviewer perception** (what a hostile reader would say the contribution boils down to)

Then judge the gap. Is this a real theoretical contribution, a real empirical contribution, a reframing of known ideas in a new setting, or an unexplored application that doesn't change how anyone thinks? Be strict. Contextual novelty is not the same as conceptual novelty.

### 3. Strongest assets

Before the problems, name what works — but only what *genuinely* works. This is not a slot-filling exercise; it's identifying what the author should protect in revision.

The number of items here is not fixed. Some papers have one strong move and the rest is salvage; some have three; very few have four. Do not pad. If only one thing genuinely stands out, name one. The categories below are *prompts to scan*, not boxes to fill:

- Is there a strong conceptual move? (Often there isn't — most papers' best asset is empirical or rhetorical, not theoretical.)
- Is there strong empirical or evidentiary support — data, identification, design that's genuinely better than the field standard?
- Is there a passage or section that's particularly well-executed?
- Is there an issue most likely to be *overclaimed rather than fundamentally bad*? (Worth naming because reframing is cheaper than rebuilding.)

If a candidate item is in the range of "competently executed" or "fine, not a comparative advantage," **do not include it**. Competence is the floor, not an asset. Save praise for things the paper does better than typical work at the target venue. A short, true Section 3 is better than a long, padded one.

### 4. Mechanism / explanatory logic audit

For empirical and theoretical papers alike, evaluate the core explanatory logic:

- Is the mechanism clearly specified, or named without being explained?
- Are core constructs sharply defined and used consistently throughout?
- Does the paper explain *why* the focal relationship occurs, or just assert that it does?
- Does the logic feel theoretically derived or post-hoc rationalized?
- Does the paper distinguish its explanation from nearby alternatives, or does it argue against straw men?

Cite specific page/paragraph references where relevant.

### 5. Construct and operationalization audit (empirical papers)

For each major construct and its empirical proxy, assess:

- Whether the proxy actually captures the construct, or captures something nearby
- Whether the proxy is too blunt for the conceptual nuance the theory requires
- Whether there's risk of tautology, circularity, or construct overlap with controls/DVs
- Whether the measure aligns with how the construct is theorized in prior literature, or breaks from convention without justification

Be specific: name the construct, name the proxy, identify the gap.

For non-empirical papers, replace this with a *conceptual definition audit*: are the key constructs distinguishable from neighboring concepts, or do they collapse on close reading?

### 6. Alternative explanations and adjacent literatures

Identify the strongest alternative accounts of the paper's findings — not just the obvious ones the author addresses. Pull from adjacent literatures the paper underweights. For each alternative, classify:

- **Unaddressed** (paper ignores it; threatening)
- **Partially addressed** (acknowledged but not credibly ruled out; how exposed)
- **Possible but not threatening** (could be true in principle, but the paper's evidence still favors its account)

State what a skeptical reviewer would claim the results are "really about" if they rejected the paper's interpretation.

### 7. Evidence, design, and empirical credibility

Evaluate whether the evidence supports the claims, by standards appropriate to the method:

- Sample sizes, Ns, periods, subsamples — consistent across text, tables, figures, notes, appendices?
- Are categories being compared actually commensurate?
- Modeling choices align with theory and outcome of interest?
- Effect sizes and uncertainty interpreted honestly?
- Endogeneity, reverse causality, selection — addressed credibly or hand-waved?
- Does the design test the theory itself, or only something adjacent to it?

For qualitative, mixed-methods, theory, simulation, or experimental papers, adapt: case selection logic, comparative leverage, identification strategy, analytical structure. The standard is whether a skeptical reviewer would *trust the evidence* — not whether the methods are technically defensible.

This section is allowed to overlap with Section 5 if construct issues are inseparable from evidence issues; in that case fold them together and say so.

### 8. Hypotheses, propositions, and inference

For each major claim or hypothesis:

- Does it follow cleanly from the theory developed earlier in the paper?
- Is it diagnostic — would different theoretical accounts predict different outcomes — or is it consistent with many explanations?
- Is it necessary, or padding?
- For each result, classify as: non-diagnostic / suggestive / discriminating / highly probative.

Don't dismiss results just because they're not uniquely identifying; the standard is whether the evidence shifts what a reader should believe.

### 9. Section-by-section sweep

Walk through every section: title, abstract, introduction, theory/conceptual framing, hypotheses (if applicable), methods, results, discussion, references, tables, figures.

For each section, note (in compact form):
- What works
- What doesn't
- What's confusing, redundant, or overstated
- What should be cut, rewritten, or reframed
- Specific prose problems, transitions, vocabulary inconsistencies

**Use `references/exhaustive_checklist.md` as your scanning catalog here.** It enumerates the categories of issue to look for in each section type. The point of this section is comprehensiveness — flag prose problems, citation issues, formatting inconsistencies, suspicious numbers, hedge language, jargon drift, missing references — at the granularity a careful copy-edit-plus-content review would catch.

**Tables and figures specifically:**

- **Rendered tables (visible in PDF or extracted from docx):** scan as part of the sweep. Check that variable labels are not raw code names ("ln_emp" should be "Log(Employees)"); that observations and clusters are reported; that significance stars match standard errors; that interaction terms appear when text claims them; that coefficients in text match coefficients in tables; that across-table Ns are consistent.
- **Rendered figures:** look at them. Check axis labels include units; confidence intervals or standard errors are shown; captions are informative without requiring the reader to find the figure in the body; for interaction plots, that moderator values are labeled; that each figure earns its space rather than duplicating a table.
- **Placeholder tables/figures ([Table 3 about here], [Insert Figure 2]):** do not critique the content of objects that don't exist yet. Do flag whether the *captions* (if present) describe analyses that align with the methods section, whether the placeholder count matches what the text claims, and whether the placeholder location makes narrative sense.
- **Caption-only with no rendering:** if a caption exists but the figure doesn't, evaluate the caption alone — is the figure described well enough that you can tell what it's supposed to show? Does the prose around it tell you what to expect?
- **Tables visible as tab-separated text from docx extraction:** the layout will be ugly but the content is readable. Don't critique formatting (that's a docx artifact, not the author's design); do critique what's *in* the cells.

**References specifically — the bidirectional consistency check is mandatory, not optional:**

When you reach the references subsection of the sweep, *actually perform* the consistency check. This is not "mention that the user should run it" — it is "do it now and report findings." Steps:

1. Extract every in-text citation from the manuscript: parenthetical `(Author, Year)` and `(Author et al., Year)`, narrative `Author (Year)` and `Author et al. (Year)`, and any other form used.
2. Extract every entry from the reference list.
3. Match in-text citations against reference list entries. Report:
   - **Cited in text but missing from references** — list them by (Author, Year). These are real errors the author needs to fix.
   - **In references but not cited in text** — list them. May be late removals or padding.
   - **Citation drift** — same work cited as different forms in different places (Smith 2010 vs. Smith et al. 2010), suggesting a citation got changed in one place but not others.
4. If there are zero issues, say so explicitly: "Bidirectional consistency check: no orphaned citations or unused references found."
5. Only punt on this step if the reference list itself is missing or the manuscript is truncated. In that case, say so explicitly and explain why the check could not be performed.

Do not write "the user should do a programmatic check before submission" as a substitute for doing the check. The manuscript is in context; the check is the model's job.

The full per-entry style audit (APA conformance, journal-specific formatting) is *not* done by default — that's opt-in only, triggered by explicit user request. See `references/exhaustive_checklist.md` for the style audit catalog when triggered.

Do not repeat issues already covered in Sections 1–8. If a problem belongs at the section level (e.g., "the abstract is incomplete," "Table 3 reports inconsistent Ns"), put it here. If it's a major theoretical or empirical concern, keep it in the relevant earlier section.

### 10. Most likely reviewer/editor objections

Identify the 5–10 objections most likely to come up in real review at the target journal. These should be:

- Phrased the way a real reviewer would phrase them (not as the author's framing of their own paper's issues)
- A mix of theoretical, empirical, and positioning objections
- Distinct from each other (not five versions of the same complaint)

This section exists to *anticipate the room*. Some of these will overlap conceptually with earlier sections — that's fine here, because the framing shifts (your diagnostic vs. their objection). But don't restate sentences verbatim.

### 11. Highest-priority revision list

The smallest set of changes most likely to materially improve publishability. Three buckets:

- **Must-fix** (manuscript will not survive review without these)
- **Important but nonfatal** (manuscript can survive but is meaningfully weaker without these)
- **Optional refinements** (improve quality at the margin)

For each major item, label the *type* of revision required: reframe the claim / sharpen theory / improve construct validity / add analysis / collect supplementary data / change wording / concede a limitation. This tells the author whether the fix is rhetorical, analytical, or empirical — which determines effort.

Prioritize ruthlessly. A long undifferentiated list is not a revision plan.

### 12. Cut / rewrite / keep

A practical revision memo:

- **Cut:** sections, paragraphs, hypotheses, robustness checks, references, figures that should go
- **Rewrite from scratch:** sections that are unsalvageable in current form
- **Keep and emphasize:** the parts that should anchor the revised paper

This is the one place where brevity matters more than exhaustiveness. Three short lists.

## How to handle inputs

**The user uploads a manuscript.** First, read it fully. Don't skim. If it's long, read it in chunks but maintain the whole-paper view — many of the issues you'll catch (inconsistencies, drift, redundancy across sections) are only visible across the manuscript as a whole.

### Reading the file: choose the right path

The user is reviewing pre-submission drafts, which are often messy. Choose the read path based on what state the manuscript is in:

- **PDF (clean, submission-ready):** the text comes through context as both extracted text and page renderings. Use the text for analysis; consult the page images when evaluating tables and figures specifically.
- **PDF (draft with placeholders, "[Table X here]" notes):** same as above; placeholders will show as text. Read both the prose and the placeholders.
- **docx (no tracked changes):** `extract-text /mnt/user-data/uploads/<file>.docx`. Tables come through as tab-separated rows under `## Table N` headers; figures appear as `[Image]` placeholders.
- **docx (tracked changes possibly present):** *do not default to `extract-text`*. Use `pandoc --track-changes=all <file>.docx -t markdown` instead. This shows `[deleted text]{.deletion}` and `[added text]{.insertion}` markers so you can see what's been edited, what's been removed, and what's still contested. The author's revision state is itself diagnostic information — heavy tracked changes in the methods section but none in the discussion tells you something.
- **docx with comments:** unpack the docx and read `word/comments.xml`. Quick path:
  ```bash
  python /mnt/skills/public/docx/scripts/office/unpack.py <file>.docx /tmp/unpacked/
  cat /tmp/unpacked/word/comments.xml 2>/dev/null
  ```
  Comments are the author's own annotations to themselves and collaborators — pay attention to them. They often flag exactly the issues the author already knows about.

**Pre-flight check, before reading the manuscript fully:** decide whether tracked changes or comments might be present. If the file is docx, run `unzip -l <file>.docx | grep -E "comments|trackChanges"` to detect their presence. If found, switch to the appropriate read path. Don't assume the user mentioned them — authors often forget the tracked changes are there.

### Handling drafts vs. submission-ready manuscripts

A draft is not a submission. If the manuscript is clearly in active development — placeholders, tracked changes, inline TODOs, missing references, captions without figures — the review should not pretend it's submission-ready. Two adjustments:

1. **Surface incompleteness up front, not buried in Section 9.** Before the verdict in Section 1, include a short "manuscript state" preamble: what's missing (Table 3 placeholder, Discussion section labeled "[draft]", three references marked TBD), what's contested (heavy tracked changes in introduction, suggesting the framing is unsettled), what the author has already flagged to themselves (TODO notes, content notes in brackets).

2. **Don't penalize for known-unfinished items, but do flag when the author's own notes reveal a deeper issue.** "[TODO: tighten this prediction]" next to Hypothesis 1 is fine — they know. But if the author has written "[TODO: explain why this construct is different from X]" and X is the central construct of the paper, that's not a TODO, that's an unresolved theoretical problem and should be flagged as such. The author's self-notes are signal about where they're stuck.

Inline notes to look for:
- `[Table N about here]`, `[Figure N here]` — pure placeholders, don't critique
- `[CITATION NEEDED]`, `[REF]`, `[TBD]` — flag if they cluster in a section (suggests that section's positioning isn't worked out)
- `[TODO: ...]`, `[NOTE: ...]`, `[CONTENT: ...]` — read them; they often reveal the author's diagnosis of their own problems
- Bracketed alternatives like "[X / Y / Z]" — author hasn't decided; flag in section-by-section sweep
- Bracketed self-questions like "[is this still defensible?]" — read these as the author asking for help; address them directly in the review

**The user asks for a partial review.** If they only want feedback on certain sections (e.g., "just review the theory section"), follow that scope, but apply the same exhaustiveness standard within scope. Use a compressed structure — verdict, contribution check, the relevant analytical sections, section-by-section for the requested parts, revision priorities — rather than the full 12-section template.

**The user provides target journal context.** Use it to calibrate the bar (a paper aimed at AMJ faces a different theory bar than one aimed at a field journal). If they don't specify, assume top-tier management (AMJ/ASQ/SMJ/AMR/Organization Science) — that's the user's working standard.

**The user provides reviewer persona context.** If they ask for a specific persona (e.g., "review this from a quantitative methodologist's perspective"), shift emphasis accordingly — but keep the developmental ethic and the diagnostic stance. Don't roleplay an adversarial Reviewer 2.

**Length requests.** If the user says "short review," shrink Sections 9 and 10 most aggressively (the section-by-section sweep and the objections list); preserve verdict, contribution diagnosis, and revision priorities. If they say "be ruthless" or "tear this apart," that's permission for sharper prose, not for cruelty or for abandoning structure.

**Reference style audits.** Always do a bidirectional consistency check on references (every in-text citation appears in the reference list, and every reference list entry is cited somewhere). This is part of the standard sweep. **Do not** do a full per-entry style audit (APA conformance, journal-specific formatting) by default — it's tedious and noisy. Trigger the style audit only when the user explicitly asks ("check my references," "audit my reference list," "check for APA compliance," etc.). When triggered, ask which style or journal to check against if not already specified, then follow the catalog in `references/exhaustive_checklist.md` under the References subsection.

## Style requirements

These are not optional. They are what makes the output usable as a diagnostic tool rather than a wall of text.

- **Numbered hierarchical structure** within sections (1.1, 1.2, 2.1) for any concern with sub-points. This is how real top-tier decision letters and reviews are organized.
- **Reasoning before verdict** in each major point. State the issue, explain why it's a problem, then suggest a fix.
- **Cite the manuscript** specifically. "P5p2," "Hypothesis 3," "Table 4 row 2," "the discussion section's third paragraph." Vague references make the review impossible to act on.
- **Prose, not bullets**, for substantive analytical points. Bullets are fine for the cut/rewrite/keep memo and for compact lists in the section-by-section sweep, but the analytical sections are arguments, and arguments are paragraphs.
- **No emojis. No smileys. No theatrical em-dashes used for dramatic pauses.** No "I want to be clear that..." preambles. No "interestingly" or "it is worth noting." No bold-italic combo for emphasis. No "—" used as a rhetorical drumroll.
- **No restatement of the manuscript's own content** beyond what's needed to make a point. The author wrote the paper; they don't need a summary of it.
- **No false symmetry.** If the paper has 10 problems and 1 strength, don't pad to 5/5. Sections 3 and 11's "important but nonfatal" bucket can be short.

## What this skill is not

- Not a Reviewer 2 simulator. Reviewer 2 is a meme; the AMR editorial guidance literature (Ballinger & Johnson 2015, Lepak 2009) explicitly defines that posture as *bad* reviewing. The user wants real diagnostic value, not theatrical harshness.
- Not a checklist machine. The exhaustive checklist exists to ensure nothing's missed, not to produce mechanical box-ticking. Every flag is paired with reasoning.
- Not a politeness instrument. The user has explicitly asked for unsparing diagnostic; soft-pedaling is a failure mode.
- Not a rewriter. Suggest fixes; don't draft sections.
