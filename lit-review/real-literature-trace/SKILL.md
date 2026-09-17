---
id: real-literature-trace
name: Real Literature Trace
version: 0.2.0
description: Use this skill whenever the user wants to search, verify, screen, compare, or organize real academic papers and return traceable paper addresses or links, especially for literature reviews, core-paper lists, recent papers, high-quality paper screening, CNKI traceability, DOI/publisher pages, Google Scholar discovery, top conference/journal screening, or when the user explicitly asks for “真实文献”, “文献地址”, “可追溯链接”, “核心文献”, “筛选优秀文献”, “国外优秀文献”, or “顶会顶刊”. If the topic is broad or underspecified, use this skill to narrow the scope first before searching.
stages: [research, review, writing]
tools: [bash]
---

# Real Literature Trace

Use this skill to turn a vague literature request into a traceable paper set with clear selection reasons and real source links.

## What this skill is for

Use it when the user wants any of the following:

- find real academic papers instead of invented references
- return paper addresses that can be checked by the user
- screen out weak, duplicate, or off-topic papers
- build a core-paper list for a literature review
- collect recent papers with publication traces
- mix Chinese and English literature and keep the provenance clear
- return CNKI links when possible, and otherwise give DOI, publisher, or other canonical pages
- find strong international papers from Google Scholar, top journals, and top conferences

## International source strategy

When the user wants foreign literature or a mixed Chinese-international set, treat the workflow as two linked passes:

1. Discovery pass
   - use Google Scholar-style discovery or equivalent search results to surface candidate papers
   - cast a wider net across journals, conferences, and preprints if needed
2. Verification pass
   - verify each selected paper on the publisher page, DOI page, or official proceedings page
   - prefer a canonical landing page over a search-result page whenever possible

When ranking international papers, prioritize these sources first:

- top journals in the domain
- top conferences in the domain
- publisher pages with DOI or proceedings metadata
- stable institutional repository pages only when the publisher page is unavailable

Do not treat a paper as strong just because it appears in Google Scholar. Use Scholar for discovery, then verify with an official source.

## Default assumptions

If the user does not specify these details, use sensible defaults and state them briefly before searching:

- focus on the last 5 years unless the topic is classical or the user asks for a longer range
- aim for 12-18 papers for a normal literature set
- prefer traceable sources over a larger but weaker set
- prefer CNKI-reachable papers when the topic is Chinese or the user wants Chinese references
- prefer top journals and top conferences when the user wants foreign or mixed literature
- keep the final response in Chinese unless the user asks for another language

## Scope narrowing

Do not jump straight into broad search if the topic is vague.

If the user says things like:

- `帮我找文献`
- `搜一些论文`
- `做文献综述`
- `筛选优秀文献`
- `给我真实文献地址`
- a broad topic without task, scenario, or time window

then narrow the request first.

Ask only the highest-value missing details:

- exact subtopic or application direction
- Chinese, English, or mixed literature
- recent papers only or classic + recent
- how many papers they want
- whether CNKI traceability is mandatory

If the user still stays vague after one round, choose one reasonable interpretation, say it explicitly, and proceed.

## Search workflow

Follow this order.

### 1. Restate the working scope

Before searching, restate the agreed scope in 2-5 lines:

- topic boundary
- time window
- source preference
- target paper count
- output format

### 2. Build a retrieval plan

Prepare a small bilingual keyword set:

- 3-6 Chinese keyword groups
- 3-6 English keyword groups
- a few combinations that reflect task, method, dataset, or scenario

Split broad topics into subthemes so the results are diverse rather than repetitive.

If the user wants foreign literature, include venue-aware retrieval terms such as:

- conference names
- journal family names
- method keywords
- task keywords

Examples:

- `spacecraft pursuit evasion game IEEE TAC`
- `orbital pursuit evasion game AIAA`
- `differential game spacecraft Automatica`

### 3. Search with traceability in mind

Prefer sources that can be verified later:

- Crossref, DOI pages, publisher pages, or official proceedings pages for international papers
- CNKI or CNKI-reachable records for Chinese papers
- Google Scholar or scholar-style fallback only when needed for discovery, not for final quality decisions

For international screening, treat venue quality as part of the retrieval plan:

- prefer papers from top journals or top conferences in the field
- separate journal papers from conference papers in the notes
- flag preprints as provisional unless a final published version is available

Do not promote a paper to the final set unless you can explain where it came from and how to check it.

### 4. Screen the candidate set

Keep papers that best satisfy most of these conditions:

- strongly relevant to the narrowed topic
- published in the target time window
- methodologically representative or influential
- from a credible venue
- for foreign literature, from a recognized journal or conference with a stable official page
- useful for a literature review, comparison table, or related-work section
- traceable to a real page or record

Reject papers that are:

- duplicates or near-duplicates
- too generic to support the target topic
- missing enough metadata to verify
- low quality or clearly tangential

### 5. Verify links

For each selected paper, return the best available address in this order:

1. canonical publisher or DOI page
2. CNKI record or CNKI landing page when available
3. other stable official page
4. Google Scholar only as a discovery reference if no official page can be confirmed

If a link cannot be confirmed, say `待核验` instead of guessing.

### 6. Produce the final set

Return the final papers with:

- title
- authors
- year
- venue
- why it was selected
- paper status, such as `strong`, `selected`, or `backup`
- canonical link
- CNKI link if available
- DOI if available
- notes about any uncertainty

## Screening rubric

Use a practical ranking approach:

- `A` for core papers that are highly relevant and easy to verify
- `B` for good supporting papers
- `C` for backup papers that may still be useful
- `S` for standout international papers from top journals or top conferences that are both highly relevant and strongly influential

When deciding between similar papers, prefer the one with:

- better topical fit
- clearer method or contribution
- stronger venue or more stable source
- easier link verification
- for foreign papers, stronger venue reputation and better official traceability

Do not overvalue citation counts alone. A newer but more exact paper can be better than a famous but generic one.

## Output format

When the user asks for a paper list, use a table by default.

Recommended columns:

- 序号
- 文献题目
- 作者
- 年份
- 期刊/会议
- 选择理由
- 质量等级
- 真实地址
- CNKI地址
- DOI
- 谷歌学术/Scholar
- 备注

If the user wants a literature review or related-work section, summarize the final set into:

- research theme
- major methods
- gaps or limitations
- recommended citation order

## Quality rules

- Never fabricate paper titles, DOIs, CNKI links, or publisher pages.
- Never hide uncertainty. Mark unverified links as unverified.
- Prefer fewer papers with real traceability over many papers with weak provenance.
- If the topic is broad, explain the narrowing choice before searching.
- If the user wants Chinese literature, make CNKI traceability part of the selection logic.
- If the user wants foreign literature, make venue quality and official provenance part of the selection logic.

## Good response pattern

1. Confirm the scope.
2. Search with broad-to-narrow queries.
3. Screen by relevance and credibility.
4. Verify links.
5. Return the final paper set with selection reasons and traceable addresses.
