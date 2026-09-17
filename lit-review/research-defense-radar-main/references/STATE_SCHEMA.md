# Durable State and Merge Protocol

Use this reference whenever a local/project-backed run reads or writes radar state. The state engine is deliberately conservative: it preserves identity history, distinguishes an attempted scan from a successful scan, and prevents incomplete coverage from producing a quiet result.

## Project files

Copy the bundled templates into user-controlled storage:

```text
research-radar/<project-slug>/
├── fingerprint.md
├── radar-state.json
├── observations.json
├── coverage.json
├── search-log.jsonl
└── alerts/
```

- `fingerprint.md` comes from `assets/RESEARCH_PROFILE_TEMPLATE.md`.
- `radar-state.json` comes from `assets/RADAR_STATE_TEMPLATE.json`.
- `observations.json` comes from `assets/OBSERVATION_TEMPLATE.json`.
- `coverage.json` comes from `assets/COVERAGE_TEMPLATE.json`.
- `search-log.jsonl` uses one object shaped like `assets/SEARCH_LOG_TEMPLATE.jsonl` per query attempt.

Do not store project files in the installed Skill directory.

## State clocks

- `last_attempted_scan_at` advances for completed, partial, and failed runs.
- `last_successful_scan_at` advances only when the run status is `completed` and every required coverage entry is `completed` or `not_applicable`, with at least one required source actually completed.
- `literature_cutoff_at` is the newest literature date the run intended to cover. It is not necessarily the same as a paper's publication, revision, or earliest-public date.

A later attempted date must never be used as the next incremental boundary when the corresponding run was partial or failed. Start the next search from the last successful cutoff and explicitly backfill the failed interval.

## Working-paper priority cutoff

When the user's own working paper is already public, record its earliest verifiable public date in `project.public_disclosure_date`. Use that date as the priority cutoff:

- work public before the cutoff can pre-empt or narrow the project's public-time novelty and needs a differentiation analysis;
- work public after the cutoff is `post_disclosure` and receives `priority_effect: no_preemption_post_disclosure`;
- same-day or unknown chronology remains uncertain until stronger date evidence is available.

Post-disclosure convergence may still deserve citation, monitoring, or method/data transfer, but it does not negate the project's novelty at its own public disclosure date and does not, by default, require the author to manufacture a new distinction.

A supplied WP manuscript is evidence about content, not public timing. If a stable repository, author page, conference programme, archive, or other public record does not establish the earliest public date, ask the user when it first became publicly accessible and record the answer as `user_stated`. Do not substitute the PDF creation date, file modification date, date printed inside a private draft, or date it was privately circulated.

## Observation identity and lineage

The merge engine keeps aliases from every observed version:

1. normalized DOI;
2. repository ID;
3. canonical and source URLs;
4. identifiers inside `versions`;
5. exact normalized title plus first author as a cautious fallback.

This lets a metadata-only working-paper record merge with a later DOI-bearing journal version while keeping the original stable paper ID. Conflicting non-empty DOIs or repository IDs block fallback title/author merging and require manual review.

## Evidence and scoring guardrail

Each new observation requires `category`, `evidence_level`, `verified_at`, and `confidence`. Metadata-only (`M`) observations cannot carry a numeric `overlap_score`. Use `null` for unknown or inapplicable dimension factors.

The JSON Schema files document portable shapes, while `scripts/update_radar_state.py` enforces the critical constraints using only the Python standard library.

## Change kinds

Use the narrowest applicable value:

- `identity_update` — DOI, repository, URL, author, or version identity changed;
- `metadata_update` — dates, publication status, or other non-substantive metadata changed;
- `evidence_upgrade` — stronger access changes M → A/F or A → F without itself changing the paper;
- `substantive_revision` — the paper changed its claims, mechanism, sample, data, design, or method;
- `novelty_impact_change` — the assessment of class, overlap, threat/help, affected claim, or recommended action changed.

Only `substantive_revision` and `novelty_impact_change` are material alerts by default. An evidence upgrade should still be reviewed because it may justify a later novelty-impact change.

## Merge command

Inspect help before use:

```bash
python scripts/update_radar_state.py --help
```

Validate without writing first:

```bash
python scripts/update_radar_state.py \
  --state research-radar/my-project/radar-state.json \
  --observations research-radar/my-project/observations.json \
  --coverage research-radar/my-project/coverage.json \
  --run-id 2026-08-24-weekly \
  --run-date 2026-08-24 \
  --literature-cutoff 2026-08-24 \
  --public-disclosure-date 2026-05-01 \
  --public-disclosure-url https://example.org/my-working-paper \
  --public-disclosure-provenance public_record \
  --dry-run
```

After review, repeat without `--dry-run`. Add `--backup` to preserve the previous output as `radar-state.json.bak`. Reusing the same run ID replaces that run record instead of creating a duplicate.

## Migration

Schema `1.0` state is migrated automatically during the next merge. The migration:

- preserves existing papers and stable IDs when present;
- coalesces compatible aliases;
- normalizes legacy coverage entries;
- converts `last_scan_at` into attempted/successful clocks conservatively; and
- writes schema `1.1` only after a successful command.

Keep a backup for important projects and inspect the first migrated result.
