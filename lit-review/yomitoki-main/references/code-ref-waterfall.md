# Code Reference Guide

Code refs are not a quota. They are implementation handles for claims in the note.

Use a side-panel code ref when the reader would naturally ask:

- "Where is this algorithm implemented?"
- "What lines correspond to this paper formula?"
- "How did they measure this result?"
- "Is there a smaller runnable version I can inspect?"

If a ref does not answer one of those questions, leave it out.

## Target Shape

Most papers land at 4-8 refs. More is fine for code-heavy systems papers; fewer is fine for theoretical papers. Prefer a few strong claim-linked refs over many loose bookmarks.

Valid `section` IDs:

`tldr`, `overview`, `timeline`, `context`, `method`, `experiments`, `comparison`, `related`, `limits`, `qa`, `quiz`

## Ref Object

```json
{
  "section": "method",
  "source": "author_repo",
  "title": "Scaled dot-product attention forward pass",
  "repo": "harvardnlp/annotated-transformer",
  "path": "the_annotated_transformer.py",
  "url": "https://github.com/harvardnlp/annotated-transformer/blob/master/the_annotated_transformer.py#L330-L347",
  "anchor_phrase": "scores every query against every key",
  "snippet": "# shape preview; see linked lines for exact implementation\nattention(query, key, value):\n    scores = query @ key.transpose(-2, -1) / sqrt(d_k)\n    weights = softmax(scores)\n    return weights @ value",
  "note": "Line range for the attention operation matching the paper's formula."
}
```

Fields:

- `section`: renderer block where the card appears.
- `source`: `author_repo`, `web`, `github_search`, or `llm_generated`.
- `title`: concept implemented by the ref, not just the filename.
- `url`: prefer exact line ranges for repo code.
- `anchor_phrase`: 4-10 words copied from prose in the target section.
- `snippet`: short preview. For external code, keep it compact.
- `note`: why this ref matters, and any caveat.

`stars` is optional and not rendered.

## Anchor Rule

For method refs, use `anchor_phrase` when possible. It makes the side-panel card clickable from the prose.

Pick a phrase from the sentence where the reader would want code. Good anchors are ordinary prose:

- `scores every query against every key`
- `adds the residual path before normalization`

Avoid:

- code identifiers: `forward()`, `cub::BlockReduce`
- headings: `Algorithm 2`
- bare nouns: `score matrix`
- math snippets: `\(QK^\top\)`
- phrases not present verbatim in the body

Fix missing, dead, or code-like anchors when they make the code panel hard to use.

## Source Waterfall

### 1. Author Repo

Use first for the paper's own contribution when available.

Find the repo from page 1, footnotes, implementation details, experiments, acknowledgments, or arXiv metadata. Prefer links near words like "code", "official", or "reproduce".

Map claims to files by reading the repo tree:

```bash
curl -fsSL "https://api.github.com/repos/$OWNER/$REPO/git/trees/main?recursive=1" \
  | jq -r '.tree[] | select(.type == "blob") | .path'
```

Pin the smallest useful line range:

- Kernel/function body for the algorithm.
- Helper/operator for the recurrence or math.
- Dispatch/evaluation block for benchmark claims.
- Training/data/model code for ML pipeline papers.

Verify line numbers with `nl -ba <file>` or GitHub's line UI. A repo-root card is allowed once as an overview, but it does not count as the implementation ref for a method claim.

### 2. Web

Use for annotated tutorials, readable explanations with code, official docs, or posts that teach the implementation better than the raw repo.

Search the title or method plus `annotated`, `from scratch`, `implementation`, `explained`, or `tutorial`. Prefer respected authors, official docs, and high-quality technical blogs. Skip SEO content.

### 3. GitHub Search

Use when there is no usable author repo, or when a community implementation is materially clearer than the official code.

Accept a repo only if it is credible and contains files matching the paper's method. Mark it as `source: github_search` and note that it is a community implementation.

### 4. Synthesized Snippet

Use only when justified:

1. No real implementation exists.
2. The snippet explains a prerequisite or baseline the paper assumes.
3. A small Python toy clarifies dense official C++, Rust, or framework code, alongside the real ref.

Do not let synthesized snippets replace official implementation refs for the paper's central contribution. If an author repo exists, use it for the main method when possible.

Synthesized snippets should be runnable, minimal, and visibly labeled with `source: llm_generated`.

If an official or author-linked repo exists but you still use a synthesized snippet, say why in the ref note: no matching implementation found, official code is only infrastructure, the real code is too large for a sidebar preview, or the snippet is only a toy baseline. Do not use synthesized code just because it is faster to write.

## Snippet Previews

For real external code:

- Use a short exact excerpt only when appropriate.
- Otherwise write a structural preview, clearly labeled:

```text
# shape preview; see linked lines for exact implementation
attention(query, key, value):
    compute scaled dot-product scores
    apply softmax over keys
    mix values with the attention weights
```

Never leave all author-repo snippets empty. 

## What Not To Link

Skip refs that are:

- Generic library entry points unrelated to the paragraph.
- Whole files when only 20 lines matter.
- Repeated links to the same code path without a new concept.
- Synthesized snippets that duplicate inline body code.
- Cards added only to hit a target count.

## Saving

Save as:

```json
{"refs": [ ... ]}
```

Path:

`/tmp/yomitoki/<paper-slug>/coderefs.json`
