# Method Inspiration Workspace Structure

A Method Inspiration Workspace is derived from exactly one field context and may start from either a Research Question Card or a Source Problem Brief. It lives at:

```text
{workspace-root}/method-inspirations/{field-slug}/
```

## Required Structure

```text
{workspace-root}/method-inspirations/{field-slug}/
|-- source_research_questions.md
|-- inspirations/
|   `-- {problem-slug}/
|       |-- source_problem.md
|       |-- method_need_decomposition.md
|       |-- targeted_method_search.md
|       |-- method_patterns.md
|       |-- transfer_mapping.md
|       |-- candidate_methods.md
|       `-- method_candidate_library.md
`-- method_candidate_libraries.md
```

## Artifact Roles

- `source_research_questions.md`: Records candidate source cards or source problem briefs and the selected source for method inspiration.
- `inspirations/{problem-slug}/source_problem.md`: Records the Method Inspiration Source Gate for exactly one source problem.
- `inspirations/{problem-slug}/method_need_decomposition.md`: Decomposes the source problem into Method Needs.
- `inspirations/{problem-slug}/targeted_method_search.md`: Records Same-Problem, Adjacent-Problem, and Far-Analogy search by Method Need.
- `inspirations/{problem-slug}/method_patterns.md`: Extracts reusable Method Patterns from searched papers.
- `inspirations/{problem-slug}/transfer_mapping.md`: Records Need-Pattern Fit, Assembly Roles, and Method Pattern Dispositions.
- `inspirations/{problem-slug}/candidate_methods.md`: Records 3-5 comparable Candidate Methods.
- `inspirations/{problem-slug}/method_candidate_library.md`: Stores the final Method Candidate Library for one source problem.
- `method_candidate_libraries.md`: Summarizes completed libraries and unresolved method-search gaps.

## Relationship To Later Workflows

This workspace does not contain a Committed Method Design.

Later experiment design or research-framing workflows should use a human-owned Committed Method Design as their main source. Baseline and metric selection are part of experiment design. Candidate Methods may inform that design, but they should not be treated as the paper's actual method.
