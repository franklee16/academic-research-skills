---
name: paper-evidence-distiller
description: |
  把任意学术论文的 .md 或 .pdf 文件蒸馏成一份"最小但完整"的证据卡（.distilled.md），不是摘要；PDF 先抽取成中间 Markdown 再蒸馏。

  Use this skill when the user supplies one or more academic paper .md or .pdf files and wants a
  compact, evidence-grounded record of each paper that:
  - keeps everything needed to interpret, trust, and reuse the paper's conclusions
    (sample, time range, measures, key analyses, model specification, effect direction, etc.);
  - drops repetition, generic background, irrelevant metadata, decorative content;
  - binds every important claim to a source location (section name, page anchor, table/figure
    number) so a reader can jump back to the original.

  Trigger this skill whenever the user asks for paper notes / evidence cards / a distillation
  of a research paper .md or .pdf, even if they don't say "paper-evidence-distiller". Do NOT use this
  skill for non-academic documents, for full literature reviews, or for tasks that need the
  author to keep reading beyond the supplied source file.
---

# paper-evidence-distiller

A Codex skill that turns a single academic paper `.md` or `.pdf` into one same-named
`.distilled.md` evidence card. The card is **evidence-first, not a summary**:
information completeness beats terseness, but no claim is added without a source anchor.

The skill never modifies the input source file. For PDFs, first create an intermediate
Markdown file with `scripts/pdf_to_markdown.py`, then distill that Markdown. Each output goes into a user-chosen
output directory (default: `distilled/`), with one file per paper.

---

## 1. When to use this skill

- User gives you the path to one or more paper `.md` or `.pdf` files and wants structured notes.
- User wants a record they can later grep when writing a literature review, theoretical
  framework, methods section, or discussion.
- User explicitly says "distill this paper", "make an evidence card", "做蒸馏卡",
  "把这篇论文压成卡片", or similar.

Do **not** use this skill for:

- Tasks that need content the supplied source file doesn't contain (then it's "not in the
  supplied text" — write "未确认", don't invent).
- Full lit-review writing, gap-finding across many papers, or topic modeling.
- Non-academic documents (blog posts, news, contracts).

---

## 2. Operating principles (read these before writing)

1. **No pre-classification of the paper.** Don't decide "this is an empirical paper using
   DCE" up front and template the card. Let the paper's own structure (abstract → intro →
   methods → results → discussion → conclusion → tables/figures) tell you what to keep.
   Different papers (theoretical, simulation, qualitative, mixed methods, systematic review)
   get different evidence cards. The six output sections are the only constant.
2. **Abstract alone is not evidence.** The abstract is a starting point, not a citation.
   Every key claim must be re-located in the body before it enters the card.
3. **Direct finding vs. author interpretation vs. author claim vs. inspiration for current
   research** are four different things. Keep them in four different places and label them
   (see §5).
4. **Preserve the original wording** for technical terms, variable names, hypothesis IDs
   (H1, H2a, …), model names, and any sentence the reader will want to quote verbatim.
   Chinese is the narration language; English original words stay in English.
5. **Bind every important number, sample, time range, effect direction, and conclusion
   to a source location.** A claim without a section/table/figure anchor is not admissible
   in §3, §4, §5. If you can't find an anchor, write "未确认" and move on.
6. **If the Markdown or PDF extraction omitted a table / formula / figure / page number**,
   do not reconstruct or paraphrase it. Use only text, numbers, captions, and anchors that
   are actually present in the accessible source.
7. **If a paper has multiple studies, datasets, or waves**, list them separately. Don't
   collapse them into one result.
8. **Hedge honestly.** "相关 / 关联 / 暗示 / 作者推测" must never be upgraded to
   "导致 / 证明 / 确定". If the authors themselves hedge, the card must hedge.
9. **No padding.** Don't repeat the same finding in two sections. Don't restate the
   abstract as if it were a result. Don't write generic lines like "this paper is
   important" without a specific reason.
10. **Output is for a later human reader** (you, the user, or a research assistant) who
    will write a review or a paper. Optimize for searchability: stable section names,
    exact anchors, copy-pasteable strings.
11. **压缩 ≠ 删除**：信息压缩到"关键主张 3–5 条"时，系数、模型细节、稳健性结果和控制变量必须移入"复核记录"，不得删节、不得合并掉无法合并的差异（详见 §9）。
12. **不得擅自补全**：未在原文出现的发表年份、投稿时间、数据收集时间、样本来源、统计结论，一律写"原文未报告"或"未确认"（详见 §9）。

---

## 3. Input contract

A single input is a path to a `.md` or `.pdf` file. Examples:

```text
papers/Zero-price-effect-on-hotel-demand--Evidence-from-a-discre_2023_Tourism-Manag.md
papers/Zero-price-effect-on-hotel-demand--Evidence-from-a-discre_2023_Tourism-Manag.pdf
```

If the user provides a directory, run this skill once per `.md` or `.pdf` in the directory,
stopping to report after each one if the user asked for a trial run.

If the user does not specify an output directory, use
`distilled/` relative to the project root and create it if
missing. Filename: `<original-stem>.distilled.md`.

Before you write anything, **read the whole paper**. The procedure is in §4.

---

## 4. Procedure

```
0. If the input is a PDF, extract it to Markdown first:
   `python scripts/pdf_to_markdown.py <paper.pdf> -o <stem>.extracted.md`.
   The script auto-installs missing Python packages (`pypdf`, `pdfplumber`) unless
   `PAPER_EVIDENCE_DISTILLER_NO_INSTALL=1` is set.
   Use the generated `.extracted.md` as the source for every later step. Do not record
   missing tables, formulas, or images as special issues; simply do not use inaccessible
   content as evidence.

1. Open the source Markdown and skim its top-level structure.
   - Note: title, authors, year, journal, DOI if visible.
   - Locate: abstract, introduction, theory/conceptual framework, methods, results,
     discussion, conclusion, limitations, references, tables, figures.

2. Read the paper end-to-end in this order:
   a) Abstract (skim — never cite as evidence).
   b) Introduction (to learn the research question, hypotheses, claimed gap).
   c) Theory / conceptual framework / literature (note mechanism claims and cited
      antecedents; the card only keeps the ones the authors actually rely on).
   d) Methods (sample, time range, data source, measurement, model, identification
      strategy, robustness checks).
   e) Results (every reported effect, table, figure, coefficient, p-value, CI,
      sample size per cell).
   f) Discussion (authors' interpretation of results; mechanisms they propose;
      boundary conditions they flag).
   g) Conclusion + limitations + future research.
   h) Tables and figures that the text refers to (read the captions and the numbers
      in the cells, not the decorative labels).

3. For each candidate evidence item, write down BOTH:
   - the claim,
   - the source anchor (section name + page anchor like "Section 4.1, Table 3" or
     "p. 6, Table 2" if the paper has page anchors; if not, "Section 4.1, table
     captioned 'Estimation results of simple EC model'").

4. Draft the card in the structure from §5. Apply the compression rules in §9:
   - §3 (关键主张与证据) holds at most **3–5** numbered items. Merge findings that
     share one table, one model, or one argument chain. Move the supporting numbers
     (coefficients, p-values, CIs, sample sizes, robustness estimates, control-variable
     results) into the "复核记录" appendix in §5, not into §3.
   - §4 (证据如何产生) keeps the high-level design and identification strategy. Move
     detailed model specification, all control-variable results, full robustness
     tables, and code/tooling details to the "复核记录" appendix.
   - §5 (边界与未解决问题) keeps the three sub-buckets from §5; sub-points that need
     exact numbers (e.g. the subsample where a sign flips) live in "复核记录".

5. Self-audit before writing the file. Use the checklist in §6 plus the precision and
   compression rules in §9.

6. Write the file. Do not modify the input source file. Report the output path and, for
   PDFs, the intermediate Markdown path.
```

---

## 5. Output structure (the only constant across paper types)

Output is a Markdown file with the six sections below, in this order, with the exact
H1 headings. Omit no section — if a section is empty in the source, write "无可记录内容"
or "未在原文中提及" inside it, do not delete the heading.

```markdown
# 论文要回答什么

<one or two sentences: the real question, gap, or theoretical dispute the authors
are addressing. State the research question, not the answer.>

# 作者的核心回答

<one or two short paragraphs: the authors' final answer, contribution, or stance.
List the key claims at a high level. Do not restate the abstract verbatim.>

# 关键主张与证据

<numbered list, **3–5 items maximum**. Each item must contain all four sub-bullets.>

1. **<claim, in Chinese, with English key term preserved>**
   - 支撑证据 / 论证：<one-sentence pointer to the evidence — a quote, a figure
     description, or a reference like "see 复核记录 R3 for the coefficients". Do NOT
     list all coefficients in §3; numbers live in the appendix unless they ARE the
     claim>.
   - 原文位置：<section name + page anchor, table number, figure number, or equation
     number>. 例: "Section 4.1, Table 3, p. 6".
   - 适用条件 / 限定 / 不确定性：<context (sample, country, time range), the
     authors' hedging, or "未确认" if the paper did not say>.

2. …

<every claim you put here must be either (a) a direct empirical finding the authors
report, (b) a hypothesis the authors state with an ID, (c) a defined construct /
model / variable whose definition matters for re-use, or (d) a key argumentative
step in the paper's reasoning. Do NOT list "we review the literature on X" as a
claim.

If two candidate claims share the same table / model / argument chain, merge them.
If a result is significant only when you keep certain control variables or when you
read the coefficient off a different table, do not promote it to §3; record it in
复核记录.>

# 证据如何产生

<free-form prose, but must cover, when applicable, each of these:>

- 材料 / 数据来源：<where the data come from, who collected them, units of
  observation>. **Time range of data collection**: write "原文未报告" if the paper
  does not state it.
- 关键测量 / 操作化：<how each construct the card refers to was measured, including
  scales, items, and any non-obvious coding>.
- 样本与时间范围：<sample size, who is in the sample, sampling frame, attrition>.
  Do NOT infer the collection window from publication year, submission date, or
  cited-version dates.
- 核心分析步骤 / 模型 / 检验：<estimation method, identification strategy, the
  one or two robustness checks the paper itself treats as substantive>.
- 关键比较或推理步骤：<the main comparisons or reasoning moves that produce the
  result — e.g. the ceteris paribus move, the placebo test, the within-subject
  design, the simulation setup>.

<机械罗列方法细节是不允许的（不要把 "用了 R" 也写进来当证据）；但任何会改变结果解释
的步骤必须出现。>

# 边界与未解决问题

<three sub-buckets, each as its own bullet list:>

- 作者明确承认的限制：<things the authors wrote in a "limitations" section or
  explicitly flagged as a caveat.>
- 结果自身显示的限制：<things the results themselves reveal — e.g. a coefficient
  flips sign in a subsample, an effect is significant only after removing outliers,
  a robustness check fails.>
- 尚未被证据确认的问题：<open questions the paper raises in future-research,
  questions the data cannot answer, or items that remain "未确认" because the accessible
  source does not contain enough evidence.>

# 对当前研究可怎么用

<numbered list of directly reusable items. Each item must be one of:>

- 理论论点：<a theoretical claim the authors defend that your work could cite or test>.
- 可引用证据：<a specific effect size, sample, or finding with numbers, with the
  source anchor, that you could cite>.
- 变量 / 概念定义：<how a construct was defined or measured that you could borrow>.
- 方法启发：<a design choice, model, or robustness check you could adopt>.
- 反例 / 边界条件：<a context where the effect did NOT hold, useful to scope your
  own claim>.
- 研究空白：<a gap the authors flag that your work could fill>.

<This section is the only place where forward-looking interpretation is allowed.
It must be marked clearly as "对当前研究的启发" framing and must NOT mix with the
"作者已经证明的内容" in the previous sections. If a user later wants to use this
card, they should be able to read §6 alone and know what is established vs.
inspirational.>
```

# 复核记录（appendix — required when §3 is compressed）

Required whenever §3 is constrained to 3–5 items OR when coefficients / robustness
results / control-variable details were moved out of the main sections. This
appendix is the place where no number gets lost.

```markdown
# 复核记录

<organize as numbered "R" entries that §3, §4, §5 can point to. Each entry preserves
the original number, direction, significance, source anchor, and limitation notes.
Suggested entry shape:>

R1. **<table / figure / model the numbers come from>**
   - 来源：<section, page anchor, table/figure number>.
   - 全部系数 / 数值：<list every coefficient, SE / t-ratio / p / CI, fit statistic
     the paper reports>.
   - 显著性 / 方向：<which are significant and in which direction>.
   - 备注 / 限定：<subsample conditions, baseline choice, anything the paper itself
     flags>.

R2. **<robustness / alternative baseline / Appendix table>**
   - …

R3. **<control variables, fit statistics, anything moved out of §4>**
   - …

<General rules for this appendix:>

- 数字必须照搬原文，不四舍五入、不省略小数位精度（除非原文如此）。
- 显著性用原文的星号体系：`*` / `**` / `***`，并保留 p 值范围。
- 任何在 §3、§4、§5 中因"压缩"而只剩一个指针的内容，这里必须有完整记录。
- 任何在原文中互相矛盾、超出图形范围、或 Markdown / PDF 抽取异常的数字，只在可以
  从可访问文本中定位来源时保留，并在备注中说明矛盾或抽取异常；不能定位时不要写入。
```

**Footer (always include):**

```markdown
---

## 蒸馏元数据

- 源文件：<relative or absolute path to original .md or .pdf>
- 中间Markdown：<PDF input only: extracted .md path; otherwise "不适用">
- 输出文件：<relative or absolute path>
- 蒸馏规则版本：paper-evidence-distiller v1
- 阅读深度：<describe ONLY what was actually accessible — e.g. "正文及可访问表图",
  "PDF抽取文本：Page 1–18；表格以抽取文本为准">。
  Never write "whole paper" if appendices, formulas, footnotes, or table cells are
  missing or partially unreadable.
- 已知问题：<list only evidence-relevant gaps or contradictions found in the accessible text, or "无" if none>
```

---

## 6. Self-audit checklist (run before writing the file)

For each candidate output, ask:

1. **信息完整性**：Is there a claim in the paper that, if missing from the card, would
   change how a later reader interprets the conclusion? If yes, it's missing **or** it
   lives in 复核记录.
2. **重复 / 填充**：Is the same finding repeated in two sections, or is a generic line
   filling space? Cut.
3. **回链**：Can I open the original paper and find the spot this claim came from in
   under 30 seconds using only the anchor I wrote? If not, the anchor is too vague.
4. **用词边界**：Did I write "证明 / 导致" for something the authors only describe as
   "相关 / 暗示 / 推测"? Downgrade.
5. **作者 vs. 我们**：Did I sneak my own interpretation into §3 or §4? Move it to §6
   and mark it as "对当前研究的启发".
6. **多研究 / 多数据集**：If the paper reports Study 1 and Study 2, are they listed
   separately, or did I merge them? Separate.
7. **抽取边界**：Are any tables / figures / equations / page numbers absent from the
   supplied or extracted Markdown? Do not use them as evidence and do not invent a
   substitute.
8. **未确认项**：Any place where I had to fill in a number or quote I did not see?
   Replace with "未确认" or "原文未报告".
9. **压缩不丢数**：Is the §3 list at most 5 items? If §3 has been compressed, does
   复核记录 contain every coefficient / p-value / CI / sample size / robustness
   result that used to be in the body? Search the body for any number not also
   recorded in 复核记录 — if you find one, add it.
10. **等效 / 相同 / 复制**（precision）：Anywhere I wrote "相同 / 等效 / 同样 /
    可完全复制" — does the original paper actually run an equivalence test or
    provide explicit equivalence evidence? If not, downgrade to "未检测到显著差异"
    or "证据不足以区分".
11. **补全 / 推断**：Any time / sample / methodological detail that came from
    publication year, submission date, cited version dates, citation years, or
    "common sense" rather than the paper's own text — rewrite to "原文未报告" or
    "未确认".
12. **数字一致性**：Any number, unit, direction, significance, table cell, or
    figure readout that contradicts another, exceeds the figure's range, looks like
    an extraction artifact, or cannot be cross-checked — keep it only if the source
    anchor is visible, note the contradiction in 复核记录, and do not fix or guess.
13. **阅读深度诚实**：Does the "阅读深度" field describe only what was actually
    accessible? If appendices, formulas, footnotes, or table cells were unreadable,
    the field must say so (e.g. "正文及可访问表图"). Never write "whole paper" in
    that case.

If any check fails, edit the card and re-audit before writing.

---

## 9. Precision and compression rules (binding)

These rules override any temptation to make the card look cleaner. They apply to
§3, §4, §5, §6, and the footer.

1. **§3 cap and merge.**
   - §3 keeps at most 3–5 numbered items.
   - Findings backed by the same table, the same model, or the same argument chain
     must be merged into a single item. A claim that survives only when the
     baseline is changed, only in a subsample, or only after dropping controls is
     not a top-level claim — it goes to 复核记录.
   - All specific coefficients, p-values, CIs, t-ratios, model fit statistics,
     control-variable results, and robustness estimates must be moved into 复核记录
     and pointed to from §3. They must not be deleted.

2. **No "等效 / 相同 / 复制" without equivalence evidence.**
   - "未显著差异" must be written as "未检测到显著差异" or "证据不足以区分".
   - "相同 / 等效 / 同样 / 可完全复制" is only allowed when the original paper runs
     an equivalence test (TOST, two-one-sided test, non-inferiority margin, etc.) or
     provides explicit equivalence evidence (e.g. a Bayes factor favoring the
     null, a pre-registered equivalence margin). If the paper only reports a
     non-significant p-value, the card must say so without upgrading the language.
   - Same rule for "支持" vs. "被拒": the paper's own verdict on the hypothesis is
     preserved; do not re-interpret.

3. **No inference from outside the text.**
   - Data collection window, submission date, revision date, sample frame
     geography beyond what the paper states, statistical conclusions, or any
     "obvious" detail must come from the paper. Otherwise write "原文未报告" or
     "未确认". Publication year, citation year, and the like cannot be used as
     evidence for any of the above.
   - This applies to numeric values, units, sample sizes, time ranges, effect
     directions, and significance verdicts.

4. **When numbers disagree or look wrong, preserve only anchored evidence.**
   - If a number contradicts another number in the paper, exceeds the figure's
     plotted range, looks like a Markdown / PDF extraction artifact, or cannot be
     cross-checked against an adjacent table, keep the original reading only when
     it has a visible source anchor and note the inconsistency in 复核记录. Do not
     correct, round, or guess.
   - This rule overrides §3's compression: a contradictory number must appear in
     复核记录 with its source anchor and limitation note, not be silently dropped.

5. **"阅读深度" must be honest.**
   - "whole paper" is allowed only when the supplied or extracted Markdown is fully readable:
     every section, table, figure, formula, footnote, and appendix is accessible.
   - Otherwise write the precise subset that was readable, e.g. "正文及可访问
     表图（Table 1–3, Figs. 1–3）；Appendix A/B 不可访问".

---

## 7. Example: minimum viable output

Below is the *shape* of an acceptable card, taken from a DCE paper on hotel ZPE. This
is for layout reference, not content to copy.

```markdown
# 论文要回答什么

在旅游业和酒店业的促销场景里，传统的"两阶实验"无法测试 *ceteris paribus* 的
"零价格效应"（ZPE）；本文以中国库车的 3 晚酒店套餐为情境，第一次在酒店需求上
检验 ceteris paribus 下的 ZPE，并把"免费"与"象征性价格"和"等价折扣"两种促销
表述做对比。

# 作者的核心回答

ZPE 在酒店需求上存在。"Free" 显著优于 "1 RMB"，但与"33.3% Off"的差异不显著。
即免费定价并非唯一最有效的促销策略；通过心理参考效应，等价折扣也能复现
类似的"非理性"消费反应。

# 关键主张与证据

1. **ZPE 在酒店需求中存在（H1a）**：在 3 晚套餐中、把总价和其它属性固定，
   "Enjoy 1 Night For Free!"的处理比无促销处理显著提升被选概率。
   - 支撑证据：Free 处理的 deal 系数 = 0.116, t=-4.253, p<0.01（表 3）。
   - 原文位置：Section 4.1, Table 3, p. 6。
   - 限定：样本为中国家庭年收入 ≥10 万元的 570 名受访者；地点固定为新疆库车。

2. **"Free" 比 "1 RMB" 更强，但与 "33.3% Off" 差异不显著（H2a 支持, H2b 被拒）**：
   Pooled 模型中 deal 系数 = 0.115；Free × deal 差分 0；1RMB × deal = -0.094（p<0.01）；
   Discount × deal = -0.012（p>0.1）。
   - 支撑证据：Pooled 模型中 1rmb × deal = -0.094*** (t=-2.831)；discount × deal = -0.012
     (t=-0.358)。
   - 原文位置：Section 4.1, Table 3, p. 6。
   - 限定：差异大小依赖于统计功效，作者承认无法严格排除"两者等效"的备择假设。
```

(Full example continues with §4–§6 — see the trial run file for a real one.)

---

## 8. What this skill will not do

- It will not call external APIs or scrape references.
- It will not summarize the literature review.
- It will not score the paper's quality.
- It will not translate the paper.
- It will not invent hypotheses, sample sizes, or coefficients.

If a user asks for any of those, say so explicitly and recommend a different skill.
