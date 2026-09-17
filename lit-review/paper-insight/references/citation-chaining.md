# Citation Chaining

Use this reference when the user asks to expand related work, understand a paper's predecessors, find later work that builds on it, locate same-task alternatives, check SOTA on the same benchmark, or find critiques and failed reproductions.

Default output is Markdown. Prefer 5-12 high-value papers with clear relationship labels over long unfiltered lists.

## Strategy Selection

| User intent | Primary strategy | Secondary strategy |
|---|---|---|
| "这篇论文之前有哪些工作？" | Backward chaining | Lateral search |
| "后续有哪些工作基于它？" | Forward chaining | Benchmark search |
| "同任务还有哪些不同方法？" | Lateral search | Benchmark search |
| "现在这个数据集/benchmark 的 SOTA 是什么？" | Benchmark search | Forward chaining |
| "有没有反例、复现失败、批评？" | Negative/critique search | Forward chaining |
| "帮我写 related work" | Backward + lateral + forward | Benchmark search |
| "基于这篇论文还能做什么？" | Forward + negative/critique | Benchmark + lateral |

## Backward Chaining

Purpose: identify the intellectual roots of the target paper and the closest prior work it builds on.

Procedure:

1. Read the target paper's related work, introduction, method motivation, and references.
2. Extract papers cited as task definitions, datasets, baselines, direct predecessors, or theoretical/method foundations.
3. Prioritize citations that the target paper explicitly contrasts against, improves upon, or uses as baselines.
4. Mark whether each relationship is paper-stated or inferred.

Search patterns:

```text
"<cited paper title>"
"<target method>" "baseline"
"<target paper title>" references
"<task>" "<dataset>" earliest paper
```

Output columns:

| Paper | Year | Role | Why it is a source/predecessor | Evidence from target paper |
|---|---:|---|---|---|

## Forward Chaining

Purpose: find later work that cites, extends, applies, criticizes, or replaces the target paper. Use this when the user cares about "后续发展" or "基于当前论文基础做的工作".

Procedure:

1. Search by exact title, DOI, arXiv ID, or author/method name in Semantic Scholar, Google Scholar snippets via web search, OpenReview, ACL Anthology, arXiv, publisher pages, and Papers with Code.
2. Prefer papers that cite the target and also share task, dataset, method component, or problem motivation.
3. Separate true extensions from shallow citations.
4. Record publication/preprint date for fast-moving areas.
5. If the target paper is recent and has few citations, search method keywords and benchmark names to find parallel or follow-up work.

Search patterns:

```text
"<target paper title>" cited by
"<target paper title>" "cites"
"<target method name>" "<task>"
"<target arXiv id>"
"<target paper title>" site:openreview.net OR site:arxiv.org OR site:aclanthology.org
```

Output columns:

| Later paper | Year | Relationship | What it changed or reused | Is it truly based on target? | Evidence |
|---|---:|---|---|---|---|

Relationship labels:

- Extends: directly improves a module, objective, dataset, or setting.
- Applies: uses the idea in a new domain/task.
- Compares: uses the target as a baseline.
- Replaces: proposes an alternative that addresses the same weakness.
- Critiques: challenges assumptions or results.
- Shallow cite: cites without substantive dependence.

## Lateral Search

Purpose: find same-task or same-problem papers that do not necessarily cite the target paper.

Procedure:

1. Extract task, dataset, metric, and core problem from the target paper.
2. Search the same task with alternative method families.
3. Include papers that change the user's interpretation of available approaches.
4. Avoid adding papers that are only topically adjacent.

Search dimensions:

- Same task + different architecture: RNN, Transformer, GNN, retrieval, diffusion, causal, contrastive, probabilistic, symbolic, etc.
- Same task + different modality: text-only, audio-only, visual-only, multimodal, missing-modality, noisy-modality.
- Same problem + different assumption: supervised, semi-supervised, few-shot, zero-shot, domain adaptation, robustness, fairness.

Search patterns:

```text
"<task>" "<dataset>" transformer
"<task>" "<dataset>" graph neural network
"<task>" "<metric>" survey
"<task>" "<limitation keyword>" paper
```

Output columns:

| Paper | Method family | Same problem? | Key difference | Why it matters |
|---|---|---|---|---|

## Benchmark Search

Purpose: find work competing on the same datasets, metrics, or leaderboards, including newer SOTA.

Procedure:

1. Identify exact dataset names, splits, metrics, and evaluation protocol.
2. Search dataset + metric + task, plus Papers with Code or official benchmark pages when available.
3. Check whether results are comparable: same split, same modalities, same preprocessing, same label set, same metric.
4. Separate peer-reviewed SOTA from preprint or leaderboard-only claims.

Search patterns:

```text
"<dataset>" "<task>" "state of the art"
"<dataset>" "<metric>" "<task>"
site:paperswithcode.com "<dataset>" "<task>"
"<dataset>" "<target paper baseline name>"
```

Output columns:

| Paper/System | Year | Dataset/metric | Reported result | Comparable? | Caveat |
|---|---:|---|---|---|---|

Comparison caveats:

- Different train/test split.
- Different modalities or missing-modality setting.
- Different label mapping.
- Uses external data or pretrained model not used by target.
- Reports macro-F1 vs weighted-F1 or accuracy.
- Uses private test set or leaderboard-only result.

## Negative/Critique Search

Purpose: find reasons not to overtrust the target paper: failed reproductions, critiques, contradictory findings, weak baselines, leakage, dataset bias, or limitations later work exposed.

Procedure:

1. Search target title/method with "reproduce", "replication", "limitations", "critique", "failure", "negative result", and "issue".
2. Check official repo issues, Papers with Code discussions, OpenReview reviews, workshop critiques, and later papers' limitation sections.
3. Distinguish evidence-backed critique from unsupported opinion.
4. Report absence of critique as "not found in searched sources", not as proof that none exists.

Search patterns:

```text
"<target paper title>" reproducibility
"<target method>" replication
"<target method>" limitation
"<target dataset>" bias
"<target method>" GitHub issues
"<target paper title>" OpenReview
```

Output columns:

| Source | Critique or negative evidence | Strength | Implication |
|---|---|---|---|

Strength labels:

- Strong: reproduction, ablation, formal analysis, or controlled experiment.
- Medium: later paper limitation analysis or credible benchmark mismatch.
- Weak: anecdotal issue, informal comment, or unsupported claim.

## Integrated Expansion Output

When the user asks for a complete expansion, output:

```text
Expansion scope:
Search paths used:
Inclusion criteria:
Key finding:
```

Then use this table:

| Paper | Year | Search path | Relationship | Key idea | Why it changes the map |
|---|---:|---|---|---|---|

End with:

```text
What came before:
What came after:
Parallel alternatives:
Benchmark/SOTA context:
Critiques or weak evidence:
Recommended next papers to read:
Search limitations:
```

## Stopping Rules

Stop when:

- Each selected search path has at least 1-3 high-value papers or no credible hits after reasonable search.
- New papers repeat already-covered relationships.
- Candidate papers do not change the user's decision, literature map, or research direction.
- The user requested a bounded number, date range, venue range, or domain.
