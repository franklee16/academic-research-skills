# Crossref REST API — quick reference

Distilled from <https://github.com/CrossRef/rest-api-doc> and
<https://api.crossref.org/swagger-ui/>. Only the bits this skill uses.

## Base URL

`https://api.crossref.org`

## Endpoints used

### 1. `GET /works?query=...` — full-text metadata search

Query parameters this skill cares about:

| Param                  | Purpose                                                     |
| ---------------------- | ----------------------------------------------------------- |
| `query`                | free-text, searches all bibliographic fields                |
| `query.bibliographic`  | free-text over title + container-title + year + pages       |
| `query.author`         | author-name-only filter                                     |
| `query.title`          | title-only filter                                           |
| `rows`                 | how many items to return (default 20, cap 1000)             |
| `select`               | comma-separated fields to include (shrinks payload)         |
| `filter`               | `type:journal-article`, `from-pub-date:YYYY`, etc.          |
| `mailto`               | polite-pool identifier (the skill sets this in User-Agent)  |

Example (matches the one in the skill trigger):
```
https://api.crossref.org/works?query=Bebchuk+Cohen+Hirst+agency+problems+institutional+investors&rows=3
```

### 2. `GET /works/{doi}` — exact DOI lookup

Returns a single record. Use this when the original reference already has a DOI.
Example: `https://api.crossref.org/works/10.1257/jep.31.3.89`.

## Response envelope

Both endpoints return:

```json
{
  "status": "ok",
  "message-type": "work" | "work-list",
  "message-version": "1.0.0",
  "message": { ... }
}
```

- `/works/{doi}` → `message` is a single work object.
- `/works?query=...` → `message.items[]` is an array of work objects; `message.total-results` gives the global hit count.

## Fields used for matching (per item)

| Field                       | Notes                                                       |
| --------------------------- | ----------------------------------------------------------- |
| `DOI`                       | canonical identifier (lowercase)                            |
| `score`                     | Crossref's relevance score (only on search; higher = better) |
| `type`                      | work type — see vocabulary below                            |
| `title`                     | array of strings (usually length 1)                         |
| `subtitle`                  | array of strings (optional)                                 |
| `container-title`           | array of strings — journal / book / proceedings name        |
| `short-container-title`     | abbreviated journal name, optional                          |
| `author[]`                  | objects with `given`, `family`, `sequence`, optional `ORCID`|
| `issued.date-parts`         | `[[YYYY, MM, DD]]` — earliest known date; MM/DD may be missing |
| `published-print.date-parts`| print publication date                                      |
| `published-online.date-parts`| online publication date                                    |
| `volume`, `issue`, `page`   | journal locators                                            |
| `publisher`                 | publisher name                                              |
| `URL`                       | canonical DOI resolver URL                                  |

Missing fields simply do not appear in the JSON — expect absence, not nulls.

## `type` vocabulary (common values)

| type ID                | meaning                          |
| ---------------------- | -------------------------------- |
| `journal-article`      | peer-reviewed journal article    |
| `posted-content`       | preprint (SSRN, arXiv, bioRxiv)  |
| `report`               | working paper / technical report |
| `book-chapter`         | edited-volume chapter            |
| `book`                 | monograph                        |
| `proceedings-article`  | conference paper                 |
| `dissertation`         | PhD/Masters thesis               |
| `dataset`              | deposited dataset                |
| `reference-entry`      | encyclopedia/handbook entry      |

The full authoritative list is `GET /types`. The journal-vs-working-paper
preference rule keys on `journal-article` being preferred over
`posted-content` / `report` when scores are close.

## Polite-pool etiquette

Two equivalent ways to identify yourself — this skill uses the User-Agent form:

```
User-Agent: crossref-skill/0.1 (mailto:your@email.com)
```

Polite-pool traffic goes to a separately provisioned cluster; public-pool
traffic does not. Crossref staff use the mailto to contact misbehaving
clients before IP-blocking.

## Rate limits

**Effective 1 December 2025.** Three access pools, each with a fixed rate and
concurrency cap that applies uniformly across endpoints (`/works/{doi}`,
`/works?query=...`, etc.):

| Pool          | How to authenticate                                   | Req/s | Concurrent |
| ------------- | ----------------------------------------------------- | ----- | ---------- |
| Public        | none — anonymous access                               | 5     | 1          |
| Polite        | `mailto:` in `User-Agent` or `mailto` query parameter | 10    | 3          |
| Metadata Plus | `Crossref-Plus-API-Token: Bearer <API key>` header    | 150   | unlimited  |

This skill supplies `mailto:` via the `User-Agent` header, so it runs in the
polite pool (10 req/s, 3 concurrent). Metadata Plus is Crossref's paid tier.

Limits advertised per response:

- `X-Rate-Limit-Limit` — max requests per window
- `X-Rate-Limit-Interval` — window length (e.g. `1s`)
- `X-Concurrency-Limit` — max simultaneous in-flight requests
- `X-Api-Pool` — `public`, `polite`, or `plus`

Breach behaviour:

- **`429 Too Many Requests`** — rate or concurrency limit hit. Back off, retry
  at a lower rate or with fewer simultaneous requests. Often includes
  `Retry-After` (seconds). The script honours it once, capped at 10s.
- **`503 Service Unavailable`** — transient server error. Same retry logic.
- **`403 Forbidden`** — manual block. Crossref attempts to contact the
  `mailto:` address first; `mailto:` is therefore recommended for everything,
  not only for the polite-pool rate uplift.

**Practical implication for batching.** Concurrency (3 in polite, 1 in public)
is the binding constraint — stay at **≤ 3 parallel calls** in any one
assistant message. Crossref's own guidance: "check that previous requests have
completed before sending the next one."

Sources: [Access and
authentication](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/)
(Crossref, authoritative); [Announcing changes to REST API rate
limits](https://www.crossref.org/blog/announcing-changes-to-rest-api-rate-limits/)
(2025 announcement).

## Error modes the script handles

- DNS / connection failure (`URLError`)
- HTTP 4xx / 5xx (`HTTPError`) — body is surfaced in stderr
- Malformed JSON body (`json.JSONDecodeError`)
- `429` / `503` — one retry honouring `Retry-After`
- Request timeout (20s default)

## Useful additional endpoints (not used by this skill, for reference)

- `GET /works/{doi}/agency` — which registration agency owns the DOI
- `GET /journals/{issn}/works` — scope a search to one journal by ISSN
- `GET /types` — canonical work-type vocabulary
- `GET /members/{id}` — publisher info
