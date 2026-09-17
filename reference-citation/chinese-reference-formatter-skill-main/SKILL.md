---
name: chinese-reference-formatter-skill
description: Use when a user needs通用中文参考文献、GB/T 7714-style bibliography entries, Chinese academic reference formatting, or BibTeX completion from Chinese or English literature titles, including 根据文献名补全参考文献、生成中文论文参考文献格式、format Chinese academic references.
license: MIT
compatibility: Requires internet access for public metadata verification. Bundled formatter uses Python 3 standard library only.
metadata:
  author: Zechang-Xiong
  version: "1.0.0"
  repository: https://github.com/Zechang-Xiong/chinese-reference-formatter-skill
  tags: chinese-references, bibliography, bibtex, gb-t-7714, academic-writing
---

# Chinese Reference Formatter

## Overview

Convert one or more Chinese or English reference titles into通用中文论文参考文献条目 and BibTeX. Always verify bibliographic metadata from public sources before formatting; do not invent missing references.

## Workflow

1. Read `references/chinese-reference-rules.md` before formatting.
2. For each input title, search public metadata sources and compare title, authors, year, venue, DOI/ISBN/URL.
3. Prefer DOI, publisher, university repository, official journal, official conference, official standards, or patent pages over aggregators.
4. If no DOI or official page exists, require a strong title match plus matching author/year/venue from at least one credible source.
5. If sources conflict and no source is clearly authoritative, return an ambiguity note instead of choosing.
6. If no clear match exists, output `未找到与“<title>”明确对应的公开文献。`
7. Normalize confirmed metadata to JSON and run `scripts/format_reference.py` to produce the reference entry plus BibTeX.

## Search Sources

Use sources appropriate to the document type:

- DOI and publisher metadata: Crossref, DataCite, official publisher pages.
- Broad scholarly metadata: OpenAlex, Semantic Scholar.
- Computer science papers: DBLP, arXiv, conference/open-review pages.
- Biomedical papers: PubMed/NCBI and official journal pages.
- Chinese references: DOI/publisher pages, university repositories, official journal pages; use CNKI/Wanfang metadata when reachable from web search.
- Standards, patents, books, theses: official standards bodies, patent offices, publishers, library catalogs, university repositories.

## Formatting

The formatter accepts a JSON object, a JSON list, or `{ "items": [...] }` through stdin or `--input`.

```bash
python scripts/format_reference.py --start 1 < metadata.json
```

Common normalized fields:

```json
{
  "type": "article",
  "title": "Paper title",
  "authors": ["Family, Given", "中文作者"],
  "journal": "Journal name",
  "booktitle": "Proceedings name",
  "year": 2026,
  "volume": "12",
  "issue": "3",
  "pages": "1-10",
  "doi": "10.xxxx/example",
  "url": "https://example.org",
  "access_date": "2026-05-07",
  "sources": ["https://source.example"]
}
```

Supported `type` values include `article`, `inproceedings`, `book`, `chapter`, `thesis`, `report`, `standard`, `patent`, `newspaper`, and `online`.

Default output for each resolved item:

````text
标准参考文献：[1] ...
BibTeX：
```bibtex
...
```
核验来源：...
````

Preserve the user's input order. Start numbering at `[1]` unless the user gives a different starting number. Do not append to a project `.bib` file unless the user explicitly asks.

## Conflict Rules

- DOI or official source metadata wins over aggregator metadata.
- Publisher version wins over preprint metadata when formatting the published version.
- Preprint metadata is valid only when the user asks for the preprint or no published version exists.
- If author order, year, venue, or page range conflicts, state the conflict and cite the competing sources.
- Use the actual current date for online access dates unless the source provides a citation access date or the user specifies one.

## Common Mistakes

- Do not format from title guesses alone.
- Do not silently translate titles or author names.
- Do not list more than three authors before `等` or `et al`.
- Do not force a school-specific thesis requirement unless the user explicitly provides that institution's rules.
- Do not count online resources or standards as ordinary journal/conference papers unless the user's style guide explicitly says to.
