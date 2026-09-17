# Economics Table System

Use these defaults unless a journal template, established paper style, or explicit user preference takes precedence. The system combines AEA-like restraint with the strongest structures in the supplied CLL, Kleven, Sha, and Wang examples.

If a target journal is named, consult its current official author/style guide before laying out the table. The journal profile overrides these defaults for title/number placement, significance stars, allowed column count and font size, notes, accessibility, and required editable/source formats. Do not rely on remembered or sample-era rules for a current submission.

## Page hierarchy

- Place the table number and informative title above the table. Keep the title descriptive rather than interpretive.
- Use black text on white with no cell fills, gradients, or decorative boxes.
- Use booktabs-style horizontal rules: top rule, header rule, selective panel/section rules, and bottom rule. Never use vertical rules.
- Center a narrow table rather than stretching it artificially. Align a full-width table to the manuscript text block.
- Keep the stub left-aligned and numerical columns aligned on decimal points. Center short column labels and `Yes`/`No` entries.
- Put `Notes:` below the bottom rule, aligned with the table width. Italicize only the label when consistent with the manuscript, not the full note.
- Use serif type in tables when the manuscript is serif. Do not mix more than the manuscript serif plus the figure sans serif.

## Physical size and width

| Result columns | Default width | Guidance |
|---:|---:|---|
| 2–4 | 70–85% of text width | Center; keep a comfortable stub |
| 5–6 | 85–100% | Normal full-width main table |
| 7–8 | 100% | Use only with short headers and a concise stub |
| More than 8 | Split, panel, landscape, or continuation | Do not solve with indiscriminate shrinking |

- At final size, body text should normally be 8–9 pt; notes may be 1–1.5 pt smaller but should not fall below about 7.5 pt.
- The stub usually needs 28–38% of the width. Preserve enough width for numerical columns to avoid collisions between estimates and stars.
- Keep coefficient and standard-error lines tight; use slightly more vertical space between variable families, panels, and the specification block.
- Avoid `\resizebox` as a default. Redesign headers, split outcome families, use panels, or rotate to landscape first.
- A main results table should normally occupy its own float. Two short, closely related tables may share a page only if neither requires a smaller font. Do not split a row or coefficient/SE pair across pages.
- When continuation is unavoidable, repeat all headers and label it `Table X—Continued` or the journal equivalent.

## Column headers and panels

Build headers from meaning to model number:

1. first-level spanner: outcome family, sample, estimand, or `Ex ante`/`Ex post` group;
2. second-level header: specific dependent variable or sample restriction;
3. final level: model number `(1)`, `(2)`, and so on.

Use short partial rules under spanners. Wrap a long header onto two balanced lines; do not rotate header text. Put technical sample/radius details in a specification row when that is clearer than crowding the header.

Use `Panel A. …`, `Panel B. …` when:

- the same column grammar is repeated for distinct outcomes/samples;
- results have different dependent variables or estimands but form one argument;
- summary statistics come from different units of observation or data sources;
- reduced-form, first-stage, second-stage, mechanism, or mediation blocks need separation.

Panel order should follow the research argument, not significance.

## Numeric formatting

- Default to three decimals for coefficients/SEs. Use four for very small effects when three would conceal relevant variation, and two for naturally large quantities. Keep precision consistent within a coefficient family.
- Include a leading zero: `0.037`, not `.037`. Use a true minus sign in rendered output. Convert rounded negative zero to `0.000`.
- Align decimal points and keep stars from shifting numeric alignment. In LaTeX, use a numeric column tool or an equivalent phantom-width strategy.
- Format counts as integers with thousands separators when supported. Do not add decimals to `N`, number of clusters, or group counts.
- Format p-values to three decimals; use `<0.001` rather than `0.000`. Label one- versus two-sided tests when nonstandard.
- Percentages may use one decimal unless greater precision is substantively important. Put `%` in the header/unit, not in every cell.
- Round only in the presentation layer. Compute transformations, linear combinations, and tests at full precision.

## Cells, blanks, and symbols

- Estimate on the first line; `(standard error)` directly below. Use `[confidence interval]` only when that is the chosen table-wide convention.
- Leave a structurally inapplicable/not-estimated cell blank. Use an em dash for a true missing/unavailable value when readers must see that it is missing. Define unusual symbols in the note.
- Do not write zero for an omitted category, absorbed effect, failed model, or unavailable statistic.
- Use `Yes`/`No` or a compact checkmark convention consistently for controls and fixed effects. `Yes`/`No` is the safer cross-format default.
- Do not shade or bold significant cells. Use panel headings, spacing, and rules—not decoration—to create hierarchy.

## Default row order for regression tables

1. focal treatment, exposure, or policy coefficient;
2. pre-specified interactions or other core coefficients;
3. required contrasts, linear combinations, equality tests, or joint-test p-values;
4. a separated specification block: controls, fixed effects, trends, weights, sample/control group, estimator, SE clustering;
5. diagnostics: first-stage F, weak-IV statistic, pre-trend p-value, overidentification test, or multiple-testing family as relevant;
6. observations, number of clusters/groups, and fit statistics.

Use adjusted `R²` for OLS when that is the project's convention. For absorbed fixed-effects models, distinguish adjusted overall `R²` from adjusted within `R²` and select the statistic that matches the table's stated purpose; never label either generically if ambiguity remains. Label pseudo-`R²` and other variants accurately. Do not compare fit measures across incompatible model families without explanation.

## Notes

Write notes in this order, omitting only genuinely irrelevant items:

1. unit of observation, sample period, and key restrictions;
2. dependent-variable units, transformations, and reported estimand;
3. treatment, interaction, omitted/reference group, and any linear combination;
4. controls, fixed effects, trends, weights, and sample construction not already visible in rows;
5. uncertainty method, clustering level, bootstrap/re-randomization repetitions, and test sidedness;
6. multiple-testing adjustment or outcome family when applicable;
7. significance thresholds;
8. data source if the journal or table type requires it.

Prefer a complete but compact note. Avoid duplicating definitions that are already clear from row labels and the paper. Never write merely `Robust SE`; write, for example, `Heteroskedasticity-robust standard errors clustered at the county level are reported in parentheses.`

## Significance and uncertainty

The sample papers often use `* 10%`, `** 5%`, and `*** 1%`; Kleven's comparison table instead presents explicit difference rows and standard errors without stars. Choose the convention that best serves the argument and the target journal.

- If stars are used, attach them to coefficients only and define thresholds once.
- Do not mix threshold systems within a paper.
- Exact p-values are useful for primary contrasts, joint tests, randomization inference, and multiple-testing adjustments; put them in labeled rows rather than replacing every SE.
- Confidence intervals are often better than stars for a compact policy-results table. If used, state level and construction.

## Visual and numerical QA gate

Before delivery, verify:

- every displayed estimate, SE/CI, p-value, `N`, cluster count, and fit statistic against the model object;
- transformations, reference categories, model order, and column samples;
- star thresholds from full-precision p-values and correction of negative zero;
- decimal alignment and consistent rounding within row families;
- unambiguous blank versus missing cells;
- readable font size, balanced line breaks, no overfull cells, and no clipped notes;
- correct spanner ranges, panel rules, continuation labels, and table references;
- no temporary macro names, raw variable names, build warnings, watermarks, or hand-edited values;
- successful render in the manuscript's actual font and page geometry.
