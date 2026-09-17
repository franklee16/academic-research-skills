# Research basis and limits

Primary source:

- Ming Li et al., “How Can Rhetoric Reward-Hack AI Reviewers? Dissecting Rhetorical Sensitivity in AI-Based Peer Review,” arXiv:2608.08975, 2026.
- Author repository: `MingLiiii/Dissecting_AI_Reviews` (MIT-licensed pipeline code).

## Findings used by this skill

The study created 4,200 rewritten manuscripts from 120 anonymized ICLR 2026 submissions and obtained more than 42,000 AI reviews. Within its tested AI-review configurations:

- quantitative evidence framing and novelty stance produced the largest, most consistent positive-versus-negative contrasts;
- scope framing formed a weaker second tier;
- contribution structure, technical register, and lexical complexity had smaller or less stable effects;
- low original AI scores tended to rise and high original scores tended to fall, so raw score movement partly reflected scale bounds or regression to the mean;
- joint, recursive, and reviewer-guided rewrites were model-dependent and showed diminishing or inconsistent gains;
- stricter review prompts lowered mean scores but did not consistently reduce rhetorical sensitivity;
- the rewrite model chiefly affected directional separation, while the reviewer model affected effect magnitude and sign.

These results motivate treating evidence framing and novelty as a co-primary tier, scope as a weaker second tier, using one coherent rewrite, strengthening preservation checks, and refusing to chase one evaluator's score.

## Limits that must remain visible

- The corpus was limited to recoverable ICLR 2026 submissions and public review metadata.
- The six rhetorical dimensions were not orthogonal.
- Most conditions used one AI review per manuscript.
- Some structured reviews were missing, potentially non-randomly.
- The study characterizes tested AI models and prompts. It does not prove the same effect sizes, directions, or score gains for human reviewers, other venues, or future models.

Accordingly, use the study as a prioritization signal. Never promise that a rewrite will raise a real review score, and never treat rhetoric as a substitute for missing evidence.
