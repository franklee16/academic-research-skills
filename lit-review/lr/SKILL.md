---
name: LR
description: "Use this skill whenever the user wants to write a literature review, conduct an academic survey, draft a systematic review section, or compile and synthesize scholarly sources on a research topic. Triggers include: 'literature review', 'write a LR', '文献综述', '写综述', '帮我综述', '综述这个领域', 'survey the literature', 'review the papers on', 'synthesize the literature', 'academic survey', or any request to collect, organize, and critically synthesize multiple academic sources. This skill coordinates with Deep Research mode and enforces two non-negotiable rules: (1) every cited paper must have a real, verified DOI — fabricated DOIs are strictly forbidden; (2) all references must follow APA 7th edition format. Use this skill even when the user's request is informal or partial, such as 'help me find papers on X and write something up' — the structured approach here improves output quality significantly."
---

# LR: Literature Review Writer with Verified DOIs

## Overview

This skill produces a structured academic literature review. It works best when **Deep Research mode is active** (Claude.ai's extended research capability), which allows thorough multi-source search before writing begins. The two non-negotiable output rules are:

> **Rule 1 — No fabricated DOIs.** Every reference must have a DOI that was verified via web search or CrossRef lookup during this session. If a DOI cannot be confirmed, the paper is either dropped or listed with an explicit `[DOI unverified]` flag.
>
> **Rule 2 — APA 7th edition throughout.** In-text citations and the reference list must strictly follow the 7th edition of the Publication Manual of the American Psychological Association (2020).

---

## Workflow

### Step 0: Clarify Scope (if needed)

Before searching, confirm with the user:
- **Topic and research question**: What is the review covering? Is there a guiding research question?
- **Disciplinary focus**: Economics, sociology, public policy, urban studies, etc.? (affects which databases and terminology to prioritize)
- **Time range**: Any cutoff (e.g., "post-2010 only")?
- **Language**: English only, or include Chinese-language literature?
- **Target length**: Short synthesis (~800–1,200 words) or full section (~2,000–4,000 words)?
- **Thematic structure vs. chronological**: How should the review be organized?

If the user has already provided these details, skip straight to Step 1.

---

### Step 1: Deep Research Phase — Search and Collect

**If Deep Research mode is active**: leverage it fully. Run multiple parallel searches across different angles of the topic before synthesizing. Aim for breadth first, then cull.

**If Deep Research mode is NOT active**: use `web_search` iteratively. Run at least 5–8 distinct searches covering different facets of the topic. Do not synthesize after just one or two searches.

#### Search strategy

Use varied query types to triangulate the literature:
- **Foundational/seminal works**: `"[topic]" seminal paper economics`, `"[topic]" foundational theory`
- **Recent empirical work**: `"[topic]" empirical evidence 2018 2024 journal`
- **Review papers**: `"[topic]" literature review OR survey OR meta-analysis`
- **Mechanism/channel searches**: `"[topic]" mechanism OR channel OR pathway`
- **China-specific** (when relevant): `"[topic]" China urban panel data`
- **CrossRef/DOI lookup**: `doi.org [author] [year] [title fragment]` or `crossref.org search`

Target collecting **15–30 candidate papers** before writing. Quality over quantity — prioritize papers published in peer-reviewed journals or reputable working paper series (NBER, CEPR, World Bank, SSRN with clear authorship).

#### DOI Verification Protocol (MANDATORY)

For every paper you intend to cite, perform DOI verification using ONE of these methods:

**Method A — Direct DOI resolution**:
```
web_fetch: https://doi.org/[DOI]
```
If the page resolves to the paper's landing page (journal website, publisher), the DOI is valid.

**Method B — CrossRef API lookup**:
```
web_fetch: https://api.crossref.org/works?query.title=[title]&query.author=[author]&rows=3
```
Parse the JSON response. If `DOI` field matches and `score` > 50, use that DOI.

**Method C — Google Scholar / publisher search**:
```
web_search: "[exact paper title]" "[first author surname]" doi site:doi.org
```
Confirm the DOI appears in the actual search result snippet alongside the correct title and author.

**If none of the three methods returns a confirmable DOI**: Do NOT invent one. Either drop the paper or include it with the flag `[DOI unverified — omit from final reference list if strict verification required]`.

Build a working reference table as you search:

| # | Author(s) | Year | Title (short) | Journal | DOI (verified?) | Notes |
|---|-----------|------|---------------|---------|-----------------|-------|
| 1 | ... | ... | ... | ... | ✓ 10.xxxx/... | key mechanism paper |
| 2 | ... | ... | ... | ... | ✗ unverified | drop or flag |

---

### Step 2: Read and Synthesize

After collecting and verifying sources, read the key papers carefully (use `web_fetch` on DOI-resolved URLs or abstract pages to get content beyond titles). For each paper, mentally note:

- Core argument / research question
- Key findings and effect sizes
- Methodology (theory, OLS, DID, RDD, IV, structural, etc.)
- Data source and geographic/temporal scope
- Limitations or debates it opens

Then **group papers thematically**. Common organizational logics for economics literature reviews:

1. **By mechanism**: theoretical foundations → empirical evidence for mechanism A → mechanism B → heterogeneity → policy implications
2. **By methodology**: descriptive evidence → reduced-form identification → structural approaches
3. **By geography/context**: international evidence → China-specific evidence
4. **Chronological with narrative arc**: early debates → resolution → frontier questions

Choose the structure that best fits the topic and research question. Do not use a structure just because it is common.

---

### Step 3: Write the Literature Review

#### Writing standards

- **Academic register**: Third-person, past tense for describing what papers found, present tense for stating what the literature shows as a consensus.
- **Synthesis over summary**: Do not describe papers one by one. Group ideas and use papers as evidence for claims. Example: "Several studies find a positive relationship between X and Y (Author A et al., 2018; Author B & Author C, 2020; Author D, 2022), though the magnitude varies substantially across urban and rural contexts."
- **Critical engagement**: Note methodological differences, conflicting findings, gaps. A good literature review identifies what is still unknown.
- **Concise citations**: Use author-date in-text citations throughout. For three or more authors, use the first author's surname followed by "et al." from the first citation.
- **No fabricated content**: Only cite papers you actually found and verified. Do not hallucinate titles, findings, or page numbers.

#### Structural template

```
[Opening paragraph]
Introduce the topic, explain why the literature exists, and state the organizing logic of the review.

[Thematic Section 1: e.g., Theoretical Foundations]
2–4 paragraphs synthesizing foundational theories and models.

[Thematic Section 2: e.g., Empirical Evidence — Main Effects]
3–5 paragraphs on empirical findings, with methodology and data variation noted.

[Thematic Section 3: e.g., Heterogeneity and Mechanisms]
2–3 paragraphs on what explains variation in findings.

[Thematic Section 4: e.g., China-Specific Evidence] (if relevant)
2–3 paragraphs on how findings apply or adapt in the Chinese institutional context.

[Closing paragraph — Gaps and Research Frontier]
What does the literature leave unresolved? Where does the current paper/dissertation fit?
```

Adapt this template to the topic. Not all sections will apply to every review.

---

### Step 4: Compile the Reference List

After the review body, output a complete reference list titled **References**.

#### APA 7th Edition Formatting Rules

**Journal article (standard)**:
```
Author, A. A., & Author, B. B. (Year). Title of article in sentence case. 
  Journal Name in Title Case, Volume(Issue), page–page. https://doi.org/xxxxx
```

**Journal article — 3 or more authors**:
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. 
  Journal Name, Volume(Issue), page–page. https://doi.org/xxxxx
```
(List ALL authors up to 20. For 21+, list first 19, then ..., then last author.)

**Working paper / NBER / CEPR**:
```
Author, A. A., & Author, B. B. (Year). Title of paper (Working Paper No. XXXX). 
  National Bureau of Economic Research. https://doi.org/xxxxx
```

**Book**:
```
Author, A. A. (Year). Title of book in sentence case. Publisher. https://doi.org/xxxxx
```

**Book chapter**:
```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), Title of book (pp. xx–xx). 
  Publisher. https://doi.org/xxxxx
```

**Chinese-language journal article** (romanize per APA convention):
```
Author, A. [Chinese characters]. (Year). Title in pinyin or English translation [Chinese characters]. 
  Journal Name [Chinese characters], Volume(Issue), page–page. https://doi.org/xxxxx
```
Or follow the convention preferred by the user's institution.

#### Reference list rules
- Alphabetical by first author's surname.
- Hanging indent (second and subsequent lines indented 0.5 inches / 1.27 cm).
- Every entry **must** include the DOI as a hyperlink: `https://doi.org/...` — NOT `doi:...` or bare number.
- If a paper genuinely has no DOI (e.g., some older books), provide the URL of the publisher's catalog page instead.
- Papers flagged `[DOI unverified]` must either be removed from this list or explicitly flagged again here.

#### Example entry
```
Hsieh, C.-T., & Moretti, E. (2019). Housing constraints and spatial misallocation. 
  American Economic Journal: Macroeconomics, 11(2), 1–39. https://doi.org/10.1257/mac.20170388
```

> **Real-world verification note**: The DOI `10.1257/mac.20170388` above was confirmed via the AEA website and multiple independent sources during a live search. A plausible-sounding but incorrect DOI (`10.1257/mac.20180029`) exists in some training contexts — this is precisely why in-session web verification is mandatory. Never trust training memory alone for DOIs.

---

### Step 5: Self-Check Before Delivering

Run through this checklist mentally before finalizing output:

- [ ] Every in-text citation has a matching entry in the reference list
- [ ] Every reference list entry has a verified DOI (or is explicitly flagged)
- [ ] No author names, titles, or findings were invented — all come from papers actually found via search
- [ ] APA 7th format is consistent throughout (sentence case titles, `&` not "and" in references, correct DOI URL format)
- [ ] The review is synthetic (papers grouped by theme/argument) not a sequential series of summaries
- [ ] The closing paragraph identifies at least one gap or frontier question

---

## Quality Standards

- **Never invent a DOI.** A plausible-looking DOI (`10.1257/something`) that was not verified is worse than no DOI — it misleads readers and corrupts the reference list. When in doubt, flag and drop.
- **Verify DOIs proactively.** Even for famous papers you know well (e.g., classic AER or JPE articles), verify via CrossRef or doi.org within this session. Training knowledge about DOIs is unreliable.
- **Depth over breadth in writing.** It is better to synthesize 12 papers well than to mention 30 papers superficially.
- **Preserve author intent.** When summarizing a paper's findings, do not overstate effect sizes or generalize beyond what the paper actually claims.
- **Match the user's disciplinary voice.** Economics literature reviews are typically more terse and mechanism-focused than those in sociology or education. Adjust tone accordingly.

---

## Edge Cases

- **User provides their own paper list**: Skip Step 1 collection; go straight to DOI verification for each paper they provided, then synthesize.
- **Topic has very limited DOI-able literature** (e.g., very new policy, grey literature): Note this explicitly. Use DOI-free sources only if you flag them clearly and provide alternative stable URLs.
- **Chinese literature heavy**: Apply the Chinese-language APA format convention. Note that CNKI papers sometimes lack DOIs — use CNKI stable URLs instead and flag.
- **User wants output in Chinese**: Write the review body in Chinese, but keep reference entries in their original language (English papers cited in English, Chinese papers in Chinese). APA format applies regardless of language.
- **User requests a specific citation count**: Treat this as a minimum floor, not a ceiling. If verification fails for some papers, explain transparently rather than padding with unverified sources to hit the number.
- **Conflict between sources**: When papers directly contradict each other, note the conflict explicitly and, if possible, attribute it to methodological differences (OLS vs. IV, different time periods, different country contexts).
