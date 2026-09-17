# Report Template

Use this reference before writing `analysis.json` and rendering `report.tex`. The report should read like a coherent Chinese explanation, not a dump of metadata, figures, tables, and formulas.

Codex writes the intellectual content. Helper scripts only render LaTeX, compile PDF, insert evidence assets, and enforce guardrails.

## Section Order

1. `论文概览与元数据`
2. `作者与影响力`
3. `英文摘要原文`
4. `中文摘要`
5. `一句话概括`
6. Multiple narrative sections chosen by Codex
7. `价值、局限与可优化方向`

Keep every section. Use `暂无信息。` only when the evidence is genuinely missing.

## Narrative Contract

- First read the full evidence bundle: metadata, source payloads, PDF text/Markdown, section snippets, captions, extracted images, formulas, and proof items.
- Draft `narrative_plan` before `narrative_sections`: reader question, answer being built, evidence IDs, and why the evidence matters.
- The narrative spine should answer the reader's next natural question, usually moving through problem tension, key idea, method construction, math mechanism, experiment design, result interpretation, value, and limits.
- Prefer paragraphs over bullets in narrative sections.
- Keep final narration in Chinese, except the original English abstract and raw mathematical expressions.
- `中文摘要` must be a faithful translation of `英文摘要原文`, not a free summary.
- Preserve source conflicts in metadata and summarize only the relevant conflict in the report.

## Evidence Integration

Use `paragraph -> evidence asset -> paragraph`.

- The paragraph before evidence must prepare the reader: define concepts, compared methods, datasets, metrics, variables, assumptions, or proof goals.
- The paragraph before evidence must not start with `表 1 把...`, `图 2 展示...`, `公式 3 给出...`, or similar evidence-label openings.
- The paragraph after evidence must explain how the visible structure, number, formula term, or proof step changes the argument.
- `placement_hint_zh`, `lead_in_zh`, and `takeaway_zh` are planning notes only. `render_report.py` does not render them.
- Do not create isolated `关键图/关键表/关键公式` sections by default.
- Do not use generic claims such as `方法有效`, `实验充分`, `表说明效果好`, or `公式定义目标函数` without concrete details.
- Embed extracted images when `asset_path` exists. Images are scaled by pixel width and capped at the text width.
- Render formulas with `latex_expression` in math mode when possible.

## Examples

Bad:

`表 1 把 GSM8K 与 SVAMP 上的校准误差放在一起比较，核心信号是 SSC 的 ECE 低于原始 P(True) 和普通 self-consistency。`

Better:

`这里有三个置信度来源需要先区分：P(True) 是模型对单条回答的真假自评，Self-Consistency 看多个采样答案是否集中，SSC 则把同一最终答案下多条响应的置信度合成答案组分数。作者在 GSM8K 和 SVAMP 上比较它们的 ECE，是为了检验哪一种信号更适合决定 repeated sampling 何时停止、哪个答案组更可信。`

Bad:

`图 2 正好对应这条训练闭环，因此应该放在解释 Self-Calibration 的位置。`

Better:

`图 2 中，多响应采样产生的候选答案先经过置信度打分，再按最终答案聚合成软监督信号；这解释了为什么 Self-Calibration 不是简单相信单条自评，而是把多响应之间的一致性变成训练目标。`

Bad:

`公式 2 定义了训练目标。`

Better:

`公式 2 把答案一致性项和置信度项绑在同一个目标里：前者要求同一最终答案的响应聚合到一起，后者惩罚模型对低质量响应给出过高自信。这个目标解释了为什么后面的推理阶段可以用软自一致性分数排序答案组。`
