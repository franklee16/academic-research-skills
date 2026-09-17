# Search Playbook

## Objective

Find literature that changes a research decision. Shared vocabulary is neither necessary nor sufficient for contribution overlap.

## Query families

Run the families relevant to the selected mode and record each one in the search log.

1. **Question** — exposure/trait × outcome × unit/setting.
2. **Mechanism** — mechanism without the original setting or dataset.
3. **Data/institution** — dataset, platform, registry, policy, country, industry, or institution × adjacent outcomes.
4. **Identification** — experiment, shock, threshold, instrument, reform, or design × substantive domain.
5. **Measurement** — latent construct, proxy, text/image/behavioral measure, validation, and measurement error.
6. **Method lift** — estimator, linkage, imputation, causal ML, LLM validation, structural method, simulation, or engineering step independent of topic.
7. **Threat combinations** — two- and three-way combinations among question, mechanism, data, measurement, identification, and claim.
8. **Known-paper neighborhood** — newer citing work, shared antecedents, author pages, working-paper series, conference versions, and revisions.
9. **Counterevidence** — alternative signs, null effects, failed mechanisms, boundary conditions, and falsification evidence.

For a known-paper comparison, begin with the supplied paper, its lineage, and the fingerprint fields it touches. Broaden only when necessary.

## Public chronology and priority

If the user's project has a public WP, verify or ask for its earliest public date before making a priority claim. A supplied manuscript does not establish when it became public. Prefer a stable repository record, author page, conference programme, archive, or other public timestamp; otherwise record the user's answer as user-stated provenance.

Search broadly enough to understand the current landscape, but use only pre-disclosure work to judge whether the project's public-time novelty was already occupied. Label later work `post-disclosure convergence`; do not use it to downgrade public-time novelty or require differentiation by default. Treat same-day chronology as uncertain unless finer-grained evidence resolves priority.

## Source families

Adapt to the field and report what was actually checked.

- Publisher and journal pages; DOI/Crossref/OpenAlex-style metadata; author and department pages.
- Economics/finance/management: NBER, CEPR, IZA, RePEc/IDEAS, SSRN when discoverable, major conference programmes, job-market pages, and journal forthcoming/online-first pages.
- Computer science/statistics: arXiv, proceedings, accepted-paper lists, OpenReview, lab/project pages, and code repositories for implementation evidence.
- Biomedical/life sciences: PubMed, publisher pages, bioRxiv/medRxiv, trial or preregistration databases, and relevant data repositories.
- Other social sciences/humanities: SocArXiv, OSF, field repositories, working-paper series, conference programmes, and online-first pages.

Discovery indexes can surface candidates but may not establish current status or substantive claims. Verify priority items on a publisher, repository, author manuscript, or other primary record whenever possible.

## Evidence and access

- Metadata-only evidence can verify identity, DOI, dates, and status but not a contribution claim.
- An abstract supports a provisional comparison at the level the abstract actually reports.
- Use full text or a detailed manuscript for identification, mechanism, measurement, robustness, and fine-grained contribution comparisons.
- When sources disagree, show the conflict and prefer the paper's current primary record for status and the earliest verifiable public version for chronology.
- Do not use a PDF creation date, file timestamp, private-circulation date, or date printed in an inaccessible/private draft as proof of public availability.
- Do not invent details to fill an inaccessible paper. Lower confidence or classify it as a watch item.

## Freshness for monitoring

Each incremental run combines:

1. a fresh search, normally covering the last 7–14 days plus revision/online-first dates; and
2. a small evergreen backfill without a narrow date filter.

Also revisit known high-threat papers. A revision to an existing paper may matter more than a new title.

## Deduplication and lineage

Preferred keys:

1. normalized DOI;
2. repository identifier;
3. canonical URL;
4. normalized title plus first-author overlap;
5. high title similarity plus multiple-author overlap, reviewed manually.

Retain the earliest public date and the newest substantive version. Record version URLs and changed claims rather than creating duplicate paper rows.

## Coverage log

For every required source family, record:

- source name and URL;
- query family;
- checked-at timestamp;
- status: `completed`, `partial`, `inaccessible`, or `not_applicable`;
- evidence level reached;
- notes on index lag, blocked pages, missing abstracts, or other blind spots.

Do not interpret an inaccessible source as a zero-result source.

## Privacy

Create a private-to-public mapping before searching confidential projects. Generalize proprietary identifiers and unpublished hypotheses while preserving question, mechanism, and design. If the generalized query becomes too revealing or too vague, ask the user to approve the query surface.

## Stopping rules

For a normal baseline, stop broadening only after:

- the relevant query families were attempted;
- at least two independent source families were checked when available;
- the top competitor neighborhood is stable across additional queries; and
- new searches return mostly background or duplicates.

An exhaustive request expands citation neighborhoods, conference programmes, author pages, and field repositories, but the visible report remains ranked and states that exhaustive web coverage cannot be guaranteed.
