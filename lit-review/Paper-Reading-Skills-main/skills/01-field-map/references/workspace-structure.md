# Field Map Workspace Structure

Create one workspace per research direction:

```text
{workspace-root}/field-maps/{field-slug}/
├── field_boundary.md
├── seed_papers/
├── search_strategy.md
├── all_papers/
├── research_clusters.md
├── research_opportunities.md
└── index.html
```

## Slug Rules

Use a concise lowercase slug derived from the confirmed Field Boundary.

```text
llm-agents-evaluation
retrieval-augmented-generation
multimodal-reasoning
```

Rules:

- lowercase
- words separated by hyphens
- no punctuation
- specific enough to distinguish this workspace from adjacent fields

## Paper File Naming

Use this format for paper markdown files:

```text
{year}-{short-title-slug}.md
```

Example:

```text
2023-retrieval-augmented-generation-for-knowledge-intensive-nlp.md
```

Rules:

- lowercase
- spaces become hyphens
- remove punctuation such as colons, question marks, and quotes
- keep the filename under 80 characters when practical
- if names collide, add the first author's surname or venue
- keep the full paper title inside the markdown file

Seed papers live in `seed_papers/`. Expansion papers live in `all_papers/`.

Do not duplicate seed paper files into `all_papers/`. When clusters or the HTML report need to reference seed papers, link directly to `seed_papers/{paper-file}.md`.
