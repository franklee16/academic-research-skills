# DRIL Evidence Policy Template

## Source-Role Hierarchy

Define the priority ranking of source categories for your domain. Sources higher in the hierarchy override those lower when they conflict.

### Default Hierarchy (Institutional / Legal Research)

1. **Constitutional provisions** — National constitution, constitutional amendments, constitutional court rulings
2. **Statutes** — National legislation, organic laws, framework laws
3. **Regulations** — Decrees, ministerial resolutions, regulatory agency rules
4. **Official guidance** — Government circulars, official interpretations, administrative manuals
5. **International organization reports** — IMF Article IV reports, OECD reviews, World Bank diagnostics, UN reports
6. **Professional and legal commentaries** — Academic legal analyses, think-tank reports, professional association guidance
7. **Academic syntheses** — Peer-reviewed articles, edited volumes, literature reviews
8. **Specialized press and trade publications** — Domain-specific news outlets, industry reports

### Domain-Specific Adaptations

- For **fiscal data**: Official budget documents > IMF/World Bank reports > central bank publications > academic estimates
- For **regulatory indicators**: Regulatory agency filings > statutes > government reports > academic coding
- For **corporate data** (if applicable): SEC/company filings > analyst reports > press coverage

### Per-Variable Overrides

Some variables may require a different hierarchy. Document overrides in the research instrument under `per_variable_source_overrides`.

---

## Citation Contract

Every factual claim in the dataset must carry the following documentation:

1. **Verbatim excerpt**: The exact text from the source that supports the claim (minimum 100 characters for substantive claims; shorter allowed for simple factual statements like dates or numeric values)
2. **Source locator**:
   - For web sources: Working URL + access date (YYYY-MM-DD)
   - For document-based sources: Document name + page number
   - For legal texts: Article/section number, paragraph, or table reference (e.g., "Article 73, paragraph 2" or "Table 3.1, row for Argentina")
3. **Source metadata**: Author (if applicable), title, publishing institution, publication date

This contract ensures that every cell in the final dataset can be traced back to a specific passage in a specific source.

---

## Conflict Resolution Rules

When two or more sources provide contradictory information for the same variable and unit:

1. **Prefer the more authoritative source** according to the source-role hierarchy.
2. **If authority is equal**, prefer the more recent source.
3. **If recency is also equal**, report both values in the evidence record and flag the conflict for human review (set uncertainty status to `conflict_unresolved`).
4. **Do not average or synthesize conflicting values** without explicit authorization in the research instrument.

---

## Evidence Quality Standards

- **Primary over secondary**: Prefer primary sources (original legal texts, official reports) over secondary summaries.
- **Official over unofficial**: Prefer government or institutional publications over media reports or advocacy documents.
- **Dated sources**: Note the publication date. If the source is more than 5 years old for a time-sensitive variable, flag for review.
- **Language**: Prefer sources in the original language when possible, but English translations from official sources are acceptable. Note the language and whether the excerpt is a translation.
- **Accessibility**: Prioritize sources that are publicly accessible (open URL, open-access document). If a paywalled or restricted source is necessary, note the access limitation.

---

## Search Protocol Guidelines

The implementation agent should:

1. Start with the highest-priority source category in the hierarchy.
2. Search using official terminology (e.g., "tax expenditure report Ministry of Finance [Country] [Year]").
3. Consult at least two sources per variable when feasible, to surface potential conflicts.
4. Document every search query and the result (found / not found / irrelevant) in the search log.
5. If no qualifying source is found after exhaustive search, create a data gap record rather than leaving the cell blank.
