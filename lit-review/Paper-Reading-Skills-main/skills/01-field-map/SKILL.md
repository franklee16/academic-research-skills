---
name: paper-reading-field-map
description: Use when the user is new to a research direction and wants to scan papers to understand branches, representative works, common methods, benchmarks, metrics, saturated areas, and unclear areas.
---

# Field Map

Use this skill to run a complete Field Map Workflow: define the field boundary, collect seed papers, expand the literature set, extract paper position records, cluster the field, identify research opportunity candidates, and produce a static HTML report.

The goal is not to fully summarize every paper. The goal is to build a durable map of the field: what problems exist, what method routes exist, which assumptions they rely on, how they are evaluated, where papers agree or conflict, and what gaps remain.

## Output Root

Set `{workspace-root}` before creating, scanning, or updating artifacts:

- Default `{workspace-root}` to `workspace` (the repo-local `workspace/` directory).
- If the user specifies a workspace root, use that path exactly and do not add another `workspace/` layer.
- If the user provides an existing artifact or workflow path, infer `{workspace-root}` from that path and keep related artifacts under the same root.
- Do not create new generated workflow directories directly at the repository root. If the user points to an existing root-level legacy workspace, inspect or update only that existing path.

## Core Workflow

1. Draft a Proposed Field Boundary from the user's initial direction.
2. Revise the boundary with the user until they explicitly confirm it.
3. Create a Field Map Workspace at `{workspace-root}/field-maps/{field-slug}/`.
4. Write `field_boundary.md`.
5. Discover an 8-12 paper Seed Set and ask the user to confirm it.
6. After confirmation, create one Paper Position Record per seed paper in `seed_papers/`.
7. Use the seed papers to draft `search_strategy.md`, including candidate discovery directions and selection criteria.
8. Ask the user to confirm the search strategy.
9. Build a Candidate Pool, select roughly 25-35 expansion papers, and create Paper Position Records in `all_papers/`.
10. Cluster all read papers into no more than 10 Research Clusters and write `research_clusters.md`.
11. Derive evidence-backed Research Opportunity Candidates and write `research_opportunities.md`.
12. Create a zero-build static `index.html` report that links to the markdown artifacts.

## Hard Confirmation Gates

Do not skip these gates:

1. **Field Boundary confirmed**: do not discover seed papers until the user confirms the field boundary.
2. **Seed Set confirmed**: do not create seed paper records until the user confirms the proposed Seed Set.
3. **Search Strategy confirmed**: do not expand to the full paper set until the user confirms the search strategy.

If the user gives corrections at any gate, revise the artifact or proposal and ask for confirmation again.

## Field Boundary Rules

Start by drafting a Proposed Field Boundary instead of asking the user to fill out a blank questionnaire. The proposed boundary must include:

1. Research Target
2. In Scope
3. Out of Scope
4. Time / Venue Boundary
5. User Goal
6. Stop Condition

Ask the user what is inaccurate, missing, or too broad. Continue revising until they confirm. Then write the confirmed boundary to `field_boundary.md` using `references/field-boundary-template.md`.

## Paper Discovery Rules

If the user directly uploads or links papers, prioritize those User-Provided Papers.

If the user does not directly provide papers, use Network Discovery by default. Search online sources such as survey bibliographies, citation trails, benchmark pages, conference proceedings, leaderboards, and academic search engines.

For every paper, record:

- Resource
- Source Verified
- Discovery Source

If network access is unavailable, do not pretend discovery is complete. Tell the user what could not be searched and ask for paper links or permission to continue when network access is available.

## Seed Set Rules

The Seed Set should contain roughly 8-12 papers. Prefer coverage over exact count:

- 1-2 survey, tutorial, or overview papers
- 2-3 classic or foundational papers
- 2-3 recent high-impact papers
- 1-2 benchmark, dataset, or evaluation papers
- 1-2 system or application papers

If a category is absent in the field, record that absence in `search_strategy.md`; it may indicate an Evaluation Gap or System Gap.

Before reading seed papers, present the proposed Seed Set with a short reason for each paper and wait for confirmation.

## Reading Depth

Use Position-Oriented Reading. Read only deeply enough to complete the Paper Position Record and place the paper in the field.

Default reading order:

1. Title / Abstract / Introduction
2. Related Work
3. Method overview
4. Experiment setup and main results
5. Limitations / Discussion
6. Conclusion

Read methods, formulas, appendices, or experiments more deeply only when the paper is foundational, defines a benchmark, or determines a cluster boundary.

## Expansion Rules

After seed paper records are complete, draft `search_strategy.md` before reading expansion papers. The strategy must include:

- Search Directions
- Selection Criteria
- Exclusion Criteria
- Citation Chasing Sources
- Keyword Queries
- Why These Papers
- Known Blind Spots

Use a Candidate Pool first, then select roughly 25-35 papers as the Selected Expansion Set. Create one Paper Position Record per selected paper in `all_papers/`.

## Clustering Rules

Cluster all read papers into no more than 10 Research Clusters.

Each paper must have exactly one Primary Research Cluster and may have zero or more Secondary Research Clusters. If more than 10 clusters appear necessary, merge them into higher-level clusters and record the boundary tradeoff.

## Research Opportunity Rules

Do not list unsupported speculation as a Research Opportunity Candidate. Each opportunity must be backed by links to specific paper records and must be phrased so it can become a possible research question.

Use these gap types:

- Conceptual gap
- Method gap
- Evaluation gap
- System gap
- Theoretical gap

## HTML Report Rules

Create a zero-build static `index.html` inside the Field Map Workspace. It should be readable by opening the file directly and should link to the markdown artifacts.

Do not introduce a frontend framework, build step, or external runtime for the report.

## Required Templates

Use the reference templates in this directory:

- `references/workspace-structure.md`
- `references/field-boundary-template.md`
- `references/paper-position-record-template.md`
- `references/search-strategy-template.md`
- `references/research-clusters-template.md`
- `references/research-opportunities-template.md`
- `references/html-report-template.md`

## Stop Condition

Stop when the user can explain:

- the confirmed field boundary,
- the main research clusters,
- representative papers for each cluster,
- the assumptions and evaluation patterns across the field,
- saturated areas,
- unclear areas,
- and evidence-backed research opportunity candidates.
