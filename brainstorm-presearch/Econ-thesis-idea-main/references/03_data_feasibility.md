# Data Feasibility

## Data Gate

For empirical, measurement/facts, structural/quantitative, and data-backed policy projects, do not give `green/proceed` unless at least one credible data path exists:

- prior literature used closely related data;
- a public database contains the needed unit, years, and variables;
- local files or user materials show the data are available;
- an advisor group, library, research team, data owner, replication archive, compliant third-party service, or other authorized channel can provide access.

For China-related data, English-language China papers and Chinese economics or management journal articles are key evidence. 小红书, 微信公众号, Xiaohongshu, WeChat public accounts, and similar platforms can be used only to search or ask for data-source leads.

Informal platform replies are leads, not validated data. Before use, verify provenance, authorization, privacy risk, citation rules, reproducibility, and whether the data can be legally and ethically used in a thesis.

## Agent And Human Task Split

Separate evidence from access.

Agent-side evidence check can do:

- inspect closest papers, data sections, appendices, replication pages, public database pages, metadata, codebooks, and local files provided by the user;
- identify likely variables, units, periods, merge keys, and sample limits;
- check whether a small public sample, metadata file, or codebook can be viewed;
- mark evidence as public, literature precedent, local file, authorized lead, platform lead, or unverified.

Human-side access confirmation must do:

- confirm school, library, advisor-group, research-team, paid-database, data-owner, or third-party service access;
- verify actual download, file completeness, legal authorization, privacy constraints, citation rules, and thesis-use permission;
- confirm whether informal platform leads from 小红书, 微信公众号, Xiaohongshu, WeChat public accounts, or similar sources point to legal and reproducible data.

Do not say "data are available" if only the agent-side evidence check has found a precedent or a lead. Say "there is a plausible data evidence path; user-side access still needs confirmation."

## Data Path Must Specify

An acceptable data path should name:

- source or paper precedent;
- unit of observation;
- time period;
- core variables;
- merge keys if multiple sources are needed;
- access status;
- likely cleaning burden.

If these are unknown, mark data status as `unverified`, not `pass`.

Use access status labels in plain language:

- public and inspectable;
- used in prior papers but access not confirmed;
- requires school or advisor access;
- requires data-owner or third-party authorization;
- lead only, not verified;
- no realistic path found.

## Data And Variable Map

Use this structure in outputs:

| Component | Candidate variable | Data source | Agent-side evidence | User-side confirmation needed | Difficulty | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Outcome | measurable result | paper/database/source | | | low/medium/high | unit and period |
| Treatment/key variable | policy, exposure, shock, index, or measure | source | | | low/medium/high | variation source |
| Mechanism | channel proxy | source | | | low/medium/high | avoid outcome re-labeling |
| Controls | baseline covariates | source | | | low/medium/high | only useful controls |
| Unit | firm/county/person/etc. | source | | | low/medium/high | panel/cross-section |
| Time | year/month/day/etc. | source | | | low/medium/high | frequency match |

## Red Flags

- desired data are private, internal, expensive, confidential, or unavailable;
- outcome is conceptually attractive but not measurable;
- treatment exists only as a policy story without observable variation;
- merge requires identifiers that likely do not exist;
- data answer a different question from the user's idea;
- public data are too aggregated to support the proposed mechanism;
- cleaning burden exceeds the user's deadline or skill level.

## What Not To Claim

When data are weak, explicitly state what cannot be claimed:

- causal effects without credible variation;
- mechanism evidence without mechanism variables;
- micro behavior from aggregate data;
- policy evaluation without treated/control comparison or timing;
- novelty without literature checking;
- external validity beyond the sample.

## First Data Verification

The first data task should be concrete:

- agent: find the closest paper and inspect its data section;
- agent: open public database pages, metadata, codebooks, or replication materials when accessible;
- agent: check whether treatment, measure, outcome, moments, or facts vary over the needed dimension;
- user: confirm login, purchase, advisor/library access, authorization, and actual file availability;
- user: verify legal, privacy, citation, and thesis-use constraints;
- together: draft a data-source paragraph for advisor review.
