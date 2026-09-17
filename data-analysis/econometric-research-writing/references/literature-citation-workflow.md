# Literature And Citation Workflow

Use this reference when finding papers, building a literature review, adding citations to a draft, verifying references, formatting a bibliography, citing data/code, or generating Word documents with author-year, footnote, or numeric superscript citations.

## Honesty Contract

- Do not invent papers, authors, titles, venues, years, DOIs, page ranges, URLs, datasets, or quotes.
- Do not cite a paper unless its identity has been verified from a reliable source.
- If no verified source is found, say `No verified source found for this claim/query` and either leave the claim uncited or mark it for manual follow-up.
- Distinguish "paper exists" from "paper supports this claim." A real DOI does not prove that the paper supports the sentence.
- Do not backfill missing fields from memory. Mark missing metadata as unknown until verified.
- Keep source provenance visible: database/tool used, URL/DOI, access date when relevant, and the exact claim the source supports.

## Search Strategy

Start from the user's topic, claim, or draft sentence and create a search plan:

1. Define the economic construct, empirical setting, method, and target claim.
2. Generate multiple query variants: theory term, empirical term, method term, synonyms, and key dataset/policy names.
3. Search broad academic indexes and field-specific sources when available: Google Scholar, Semantic Scholar, Crossref, OpenAlex, JSTOR, RePEc, NBER, SSRN, arXiv, journal pages, publisher pages, and official data/code repositories.
4. Use citation chasing for seminal work: backward references from key papers and forward citations to newer work.
5. Separate search results into seminal theory, empirical precedent, method precedent, data/source documentation, and contrary or mixed evidence.

When the agent has access to local skills or tools, prefer specialized search tools before ad hoc web browsing. Rather than hardcoding specific database clients into the writing skill, leverage the Model Context Protocol (MCP) and available environment tools as an abstract retrieval interface:

- **Literature Search Boundary**: Call available academic search MCP tools (e.g., Semantic Scholar search, Google Scholar wrappers, or local library query engines) to locate papers and compile raw bibliography records into a standard `references.json` file.
- **Verification Decoupling**: Once the raw JSON file is generated, execute `scripts/verify_references.py` to cross-validate, normalize metadata using the open Crossref endpoint, and generate an enriched reference database.
- **Zotero Integration**: If Zotero local-library integration is configured, query Zotero collections to populate the reference database instead of querying web databases.

## Screening Rules

For each candidate paper, record:

- Full title.
- Authors.
- Year.
- Venue or working-paper series.
- DOI, arXiv ID, SSRN/NBER/RePEc handle, or stable URL.
- Publication status: published article, accepted article, working paper, preprint, report, dataset documentation.
- Relevance: theory, empirical setting, identification method, measurement, data source, or robustness.
- Claim supported: one concise sentence.
- Evidence strength: direct support, indirect support, background only, contrary evidence, or not useful.

Reject or mark for manual review:

- Metadata mismatch across sources.
- Title-author-year combinations that do not agree.
- DOI resolves to a different title.
- Social-media/blog claims without a primary source.
- Citations found only in AI-generated text or unsourced lists.

## Claim-To-Source Ledger

Before adding citations to a paper, build a ledger:

| Claim in draft | Source | Support type | Exact location | Citation form | Verification |
|---|---|---|---|---|---|
| sentence-level claim | Author year | direct/indirect/background | page/table/section if available | `(Author Year)` | DOI/URL checked |

Use one citation for each substantive claim or cluster of closely related claims. Avoid citation padding.

## Citation Style Defaults

Default economics/finance style:

- Use Chicago-like author-year citations in text: `Author (2020)` or `(Author 2020)`.
- Use page numbers for specific facts, quotations, or narrow claims when available: `(Author 2020, 15)`.
- Alphabetize references by first author's last name.
- Ensure every in-text citation appears in the reference list and every reference-list item is cited in text.
- Cite data sources, code repositories, and official documentation when they materially support the analysis.

Management-style papers often follow APA-like author-year citation conventions. If the user names a target journal or style guide, follow that style over the default.

Numeric superscript citations are not the default for economics, but must be supported when the user, course, or target journal requires them.

## Word Citation Markers

When numeric citation markers, footnote markers, or endnote-style markers are required in Word:

- Use true Word superscript formatting for the marker, not plain正文 text such as `[1]` or `^1`.
- In generated `.docx`, create a run with `font.superscript = True` or equivalent OOXML `w:vertAlign w:val="superscript"`.
- Keep the citation marker immediately after the cited clause or sentence punctuation according to the target style.
- Do not convert superscript citation markers to Unicode superscript characters as the primary representation; Word styling is easier to inspect and revise.
- For true explanatory footnotes, use Word footnotes if the editing stack supports them. If it does not, disclose the limitation and do not pretend a plain superscript plus manual note is a native footnote.

`scripts/build_paper_docx.py` supports paragraph runs such as:

```json
{
  "type": "paragraph",
  "runs": [
    {"text": "This specification follows prior work"},
    {"text": "1", "superscript": true},
    {"text": " and estimates a fixed-effects model."}
  ]
}
```

Validate generated Word citation markers with `scripts/check_docx_integrity.py`; check that `superscript_run_count` is positive when superscript citations are expected.

## Reference Verification Output

Use `scripts/verify_references.py` to verify and enrich bibliography metadata:

```bash
python3 scripts/verify_references.py references.json --out-json verification.json --out-enriched-json references_clean.json
```

The enriched JSON includes normalized title, authors, year, venue/container title, DOI, URL, type, verification status, and match score for verified items. Unverified items retain the input metadata plus warning fields; do not treat them as confirmed sources.

## Reference List Entries

Prefer complete entries:

- Journal article: authors, year, title, journal, volume, issue, pages/article number, DOI.
- Working paper: authors, year, title, series/institution, working-paper number, URL.
- Dataset: author/agency, year/version, title, repository or agency, DOI/URL, access date when needed.
- Software/code: authors/organization, year/version, title, repository, DOI/URL.

Do not include references that were only searched but not cited.

## Literature Review Writing

Organize by argument, not by a flat annotated bibliography:

1. What the literature has established.
2. Where evidence or interpretation remains mixed.
3. Which identification/data/method gap the current paper addresses.
4. How the current design differs from the closest papers.

For econometric papers, separate:

- Substantive economics/management literature.
- Identification precedent.
- Measurement/data precedent.
- Methodological precedent.

## Citation QA

Before final delivery:

- Every citation has verified metadata.
- Every cited claim has a matching ledger entry or clear source note.
- Every reference-list item is cited in the text, table, figure, or appendix.
- No fabricated or partially fabricated reference remains.
- No citation marker appears as plain正文 when superscript styling is required.
- Tables and figures with source notes have corresponding reference entries.
- Any unverified source is explicitly flagged instead of silently included.
