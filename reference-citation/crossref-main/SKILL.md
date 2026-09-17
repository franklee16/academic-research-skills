---
name: crossref
description: Match a pasted list of academic references against the Crossref REST API and produce a four-column markdown table (original, matched, confidence, flags) with canonical APA citations and DOIs. Use whenever the user pastes a bibliography or reference list and wants to verify, clean up, canonicalize, or find DOIs for those references — triggers include "verify bibliography", "match these references", "find DOIs for this reference list", "canonicalize my citations", "clean up the reference list against Crossref", "check these citations", or any pasted block of academic references accompanied by a request to normalize them.
---

# Crossref reference matcher

## Overview

Given a pasted bibliography, match every reference against Crossref (via a bundled script) and return one markdown table with columns `original`, `matched`, `confidence`, `flags`. The script only does the HTTP call; Claude does all parsing, matching judgement, APA formatting, and diff notes.

## Workflow

### 0. Bootstrap and smoke-test (first run only)

Before the first batch of queries in any new session, locate the script and confirm it works. The relative path `scripts/crossref_query.py` only resolves when the working directory is the skill root, which is not always true in managed sandboxes.

**(a) Resolve the script path.** 

**(b) Smoke-test with a known-good DOI.** A successful call returns one JSON object with `"doi": "10.1257/jep.31.3.89"`:

```bash
python scripts/crossref_query.py --doi "10.1257/jep.31.3.89" --extract
```

**(c) If the smoke test fails, identify the mode and stop.** Do not silently work around a broken install by copying files or patching paths; surface the problem to the user so they can fix it once.

| Symptom | Cause | What to tell the user |
| --- | --- | --- |
| `SyntaxError: '{' was never closed` or similar mid-file parse error | Stale sandbox view of the script, or a truncated install. The Read tool can confirm which: if Read shows the full file but bash doesn't, it's a sandbox snapshot issue; if Read also shows it truncated, the install is corrupt. | Ask them to restart the session (snapshot case) or re-install the skill from GitHub (corrupt case). |
| `HTTP 503` / `DNS cache overflow` on the first call | Cold container networking or missing allowed-domain entry. | Retry once. If it still fails, ask the user to add `api.crossref.org` under **Settings → Capabilities → Additional allowed domains** (Claude Desktop). |
| `ModuleNotFoundError` | Broken or partial install. | Ask them to re-install the skill from GitHub. |

### 1. Parse the pasted reference list

Split the pasted text into one reference (verbatim) per row by blank lines, numbered markers (`1.`, `[1]`), or bulleted markers. When a single reference wraps across lines, keep it as one row. Do not drop any entry.

**The skeleton table is the first visible output — not an optional step.** Render it before any queries, with the `original` column filled and the remaining cells empty. For pasted bibliographies of 30+ entries, the user should be given a chance to correct a bad split before you spend 30+ API calls on the wrong rows. Example:

```markdown
| # | original | matched | confidence | flags |
|---|----------|---------|------------|-------|
| 1 | Bebchuk, L. A., Cohen, A., & Hirst, S. (2017). The agency problems... | | | |
| 2 | ... | | | |
```

### 2. Query Crossref for each row in order

Loop through every row without stopping until all rows are checked. For each row:

- Detect a DOI with the regex `10\.\d{4,9}/[-._;()/:A-Z0-9]+` (case-insensitive).
- **Always pass `--extract`.** This emits a compact JSON array of normalized candidate records (one element in DOI mode, up to `--rows` in query mode) instead of the full Crossref payload. ASCII-safe output avoids Windows cp1252 encoding errors and keeps tool output small enough to batch many calls per message.
- **If a DOI is present:** run the script in DOI mode.
  ```bash
  python scripts/crossref_query.py --doi "<DOI>" --extract
  ```
- **If no DOI:** run the script in query mode with `rows=3`.
  ```bash
  python scripts/crossref_query.py --query "<reference text>" --rows 3 --extract
  ```

Each candidate record has these fields: `score, type, year, authors (list of [family, given]), title, subtitle, container, volume, issue, page, doi`.

If the script exits non-zero, note the error in the `flags` column for that row (e.g. `Crossref API error: HTTP 404`) and continue to the next row. Use the Bash tool and quote the query string. If you need the full raw response for debugging, drop `--extract`.

**Batching for lists > ~15 references.** Run queries in parallel: several `Bash` invocations in a single assistant message. `--extract` output is small enough that you can read the tool results directly; no temp files are needed. If you do write to disk, use absolute paths (background shells do not inherit `cd`).

**Respect Crossref rate limits.** The script supplies the `mailto:` identifier in its `User-Agent`, which admits it to the polite pool. Since 1 December 2025 the polite-pool limit is **10 req/s and 3 concurrent in-flight requests**, applied uniformly to all endpoints. The observed limit is echoed per-response in `X-Rate-Limit-Limit` / `X-Rate-Limit-Interval` / `X-Concurrency-Limit`.

Practical rule for batching:

- **Cap at 3 parallel calls per assistant message**, regardless of whether they are DOI-mode or query-mode.
- Let one batch finish before starting the next — Crossref's own guidance is "check that previous requests have completed before sending the next one."

The script retries once on `429 Too Many Requests` / `503 Service Unavailable` honouring `Retry-After`, but that is a safety net — do not rely on it by over-parallelizing. If `429`/`503` surfaces in any `flags` cell, drop concurrency further for the rest of the list. A `403 Forbidden` means Crossref has applied a manual block — stop and contact them via the `mailto:` address. See [references/crossref_api.md](references/crossref_api.md) for the full table, including the public (5 req/s, 1 concurrent) and Metadata Plus (150 req/s, unlimited concurrent) tiers.

**Stop rules — do not over-search.** The goal is a match table, not a bibliographic investigation. Budget at most **one retry per reference**, with a reworded query. After that, record `None` and move on. Do not: guess DOI ranges, brute-force publisher DOI sequences, or run 3+ reworded queries hunting for a better hit. If the first query returns top `score` < 30 and the correct author surname does not appear in any candidate, the reference is almost certainly miscited or not indexed — stop.

**Surface problems, don't paper over them.** Many pasted bibliographies — especially LLM-drafted ones — contain fabricated or garbled references. When matches fail, tell the user plainly in the `flags` column (`likely fabricated`, `author/title mismatch`, `no usable Crossref match`) and let them judge. Do **not** force a weak match just to fill the cell, and do **not** silently "correct" what looks like a citation error. If a large share of the list comes back as `None`, say so in a one-line note under the table so the user notices. The honest answer is more useful than a confidently wrong one.

### 3. Pick the best candidate

In DOI mode the `--extract` array has exactly one element — use it.

In query mode, inspect the returned array and apply two rules:

1. **Journal preference.** If the top two candidates are within ~10 Crossref score points AND one has `type: journal-article` while the other is `posted-content` / `report` (working paper / preprint), prefer the `journal-article`. The Bebchuk example illustrates this: the JEP version (score 72.9, `journal-article`) beats the SSRN version (score 67.8, `posted-content`) even though both are high-scoring.
2. **Otherwise pick the highest `score`.**

Declare no usable match when: the array is empty, top `score` < 20, or the top candidate clearly disagrees on author surname + year + title keyword with the original.

**Likely-miscited citations.** If the top candidate has the right title but different authors (or the right authors with a clearly different title), do NOT force a match. Record `None` and flag `likely fabricated or miscited — verify before use`. This pattern is common in LLM-drafted bibliographies, where plausible-sounding but nonexistent references slip in. A small number of `None` rows is an honest answer; fake matches are not.

### 4. Fill the `matched` column with an APA 7 citation

Build the citation from the chosen candidate record:

- **Authors:** `Family, G. I., Family, G. I., & Family, G. I.` — use initials from each `authors[i][1]` (given), surname from `authors[i][0]` (family). For >20 authors, follow APA: list the first 19, then `...`, then the last author.
- **Year:** `(YYYY).` — the `year` field.
- **Title:** sentence case, from `title` (plus `subtitle` if present, joined with `: `). Crossref often returns title case; convert to sentence case.
- **Container:** italicised journal/book name from `container`, title case.
- **Locators:** `volume(issue), page` — from `volume`, `issue`, `page` when non-null. Drop gracefully if absent (e.g. online-only articles).
- **DOI link:** trailing `https://doi.org/<doi>` rendered as a markdown link.

Example (from the Bebchuk test):

```
Bebchuk, L. A., Cohen, A., & Hirst, S. (2017). The agency problems of institutional investors. *Journal of Economic Perspectives*, 31(3), 89–112. https://doi.org/10.1257/jep.31.3.89
```

For non-`journal-article` matches, label the container appropriately (`*SSRN Electronic Journal*` for SSRN preprints, `NBER Working Paper No. XXXX` for reports, etc.) and still include the DOI.

**Crossref data quirks to expect.**

- **ALL-CAPS author surnames.** Older journal-article records (e.g. pre-2015 *Journal of Finance*, *Review of Financial Studies*) return `family` in uppercase — `BRADLEY`, `LOUGHRAN`, `REBELLO`. Title-case them before formatting.
- **Online-first vs. print year.** The `year` field often reflects online-first publication, sometimes one year before the cited print year. Treat a one-year offset a minor conflict; but still flag it.
- **Missing year on chapters.** Book chapters occasionally return `year: null`. Fall back to the year in the original citation.
- **SSRN preprints dominate working-paper searches.** DOI prefix `10.2139` is Crossref-indexed while the downstream journal version may not yet be. When you match to an SSRN preprint, flag that the user may want to check whether a published version now exists.

**Proper-noun preservation when converting title case to sentence case.** APA sentence case lowercases everything except the first word, the word after a colon/question-mark/period, and proper nouns. Keep capitalized: country and language names; common acronyms (`AI`, `ChatGPT`, `COVID`, `DiD`, `ESG`, `FD`, `FOMC`, `GAAP`, `GDP`, `IPO`, `IV`, `LLM`, `OLS`, `SEC`, `UK`, `US`, `TIAA-CREF`); and any all-caps token of length ≥ 2 that is clearly an acronym rather than stylized editorial formatting.

### 5. Fill the `confidence` column

Use the format `<score> (<Tier>)`. For DOI-mode matches there is no Crossref relevance score — use `DOI (<Tier>)` instead.

Tier rules (Crossref score when in query mode; field agreement when in DOI mode):

| Tier    | Criteria                                                                                     |
| ------- | -------------------------------------------------------------------------------------------- |
| High    | score ≥ 80 AND author surname + year + title keyword all agree; or DOI match with full field agreement |
| Medium  | score 40–80; or DOI match with minor title/journal/page mismatch                             |
| Low     | score 20–40; or clear mismatch on 1–2 fields                                                 |
| None    | no usable match (empty items, top score < 20, or severe author+year+title mismatch)          |

### 6. Fill the `flags` column

Comma-separated short notes in natural language describing anything different between the original and the matched entry, or anything the user should be aware of. Leave the cell empty if nothing is notable.

**Flag discipline — only flag what matters for downstream use.** Do NOT flag:

- missing issue numbers the user could simply add from the matched record (this is normal in finance/economics bibliographies, not a citation error)
- online-first vs. print year offsets of one year (treat as agreement — see Crossref quirks)
- ALL-CAPS surnames in Crossref (a data-source artifact, not a citation issue)
- punctuation differences the user did not introduce (e.g. en-dash vs. hyphen in page ranges)
- stray periods or whitespace in the original author names

Do flag: author typos, year disagreements > 1 year, title keyword mismatches, page-range digit differences, working-paper-vs-published-article mismatches, suspected fabrication, and anything the user needs to resolve before citing.

Example flags:

- `author surname typo (Bebchuck → Bebchuk)`
- `year off by one (2016 vs 2017)`
- `title differs slightly`
- `journal name abbreviated in original (JEP → Journal of Economic Perspectives)`
- `page range mismatch (89-112 vs 89-113)`
- `original had no DOI`
- `matched is a working paper, not the published journal article`
- `no usable Crossref match`
- `Crossref API error: HTTP 503`

### 7. Render the final table

Output one markdown table with `| # | original | matched | confidence | flags |` columns, one row per reference, in the original input order. Do not truncate rows. Do not add explanatory prose before or after — just the table.

**Exception:** if more than ~10% of rows are `None` or carry a `likely fabricated` / `author mismatch` flag, add a single-line note immediately under the table alerting the user (e.g. *"7 of 51 references had no usable match — several look fabricated or miscited; worth checking before you cite them."*). This is the only prose the skill should emit around the table.

## Reference

For Crossref endpoint details, response schema, work-type vocabulary, and rate-limit headers see `references/crossref_api.md`.
