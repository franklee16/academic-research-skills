# Decisions Derived from the Supplied Tables

This reference distinguishes reusable structure from source-specific artifacts.

File links, versions, page systems, and SHA-256 checksums are recorded in [sample-manifest.md](sample-manifest.md). The skill remains usable when the raw library is absent because all operative rules are distilled here and in the table system.

## `CLL_SNWT.pdf`

- Page 25, Table 1: two sample spanners, each with `Obs/Mean/SD`, and five bold panels organized by observation level and outcome family.
- Pages 26–30, Tables 2–11: three-line tables with two- and three-level outcome spanners, numbered models, coefficient/SE stacking, a separated controls/FE/observations block, and self-contained notes. Four- to five-column tables use less than full width; seven-column tables use the full text width.
- Pages 41–42, Tables A2–A3: balance tables with treated/control/difference columns; parentheses represent SDs under means and SEs under differences, requiring explicit notes.
- Pages 44–45, Tables A6–A7: dense heterogeneity evidence is organized into repeated outcome panels with only focal interactions and `N`; repeated specification detail is moved to the note.

Adopt the semantic panels, local spanner rules, and compact specification blocks. Increase font size or split when a page becomes dense.

## Kleven et al. (2021)

- PDF page 7, Table 1: Adoptive, Biological, and Weighted Biological sample spanners, each using `P25/Mean/P75`; parent categories form indented row groups.
- PDF page 11, Table 2: identical outcome columns across `Panel A. Short run (0–5)` and `Panel B. Long run (6–10)`, with Biological, Adoptive, and Difference rows plus SEs. It avoids stars and makes the cross-group difference the inferential object.

Adopt the compact AEA-like restraint, difference rows, window-defined panels, and notes that state reweighting/bootstrap construction. Do not stretch a four-column table to full width merely because space exists.

## Sha (2023)

- Tables 1–11 use descriptive subtitles and occasional source lines directly below the title, then outcome/sample spanners, numbered columns, and a lower block for treatment means, outcome moments, village/observation counts, fit, and fixed effects.
- Table 4 demonstrates an eight-column, two-outcome layout near the portrait readability limit.
- Tables 6–9 demonstrate control-sample spanners, multiple-outcome groups, and theory-driven interaction panels.

Adopt the journal-ready notes and header hierarchy. Do not copy red/blue journal hyperlinks, overlong definition blocks, or an eight-column layout when a panel split would be clearer.

## Wang et al. (2023)

- PDF page 44, Table 1: descriptive panels by data source/unit, with `Mean/SD/p10/Median/p90`.
- PDF pages 45–51, Tables 2–8: dependent-variable spanners, numbered models, theory/alternative panels, lower specification blocks, joint coefficients and `Prob > F`, `Ex ante/Ex post` groups, and reduced-form/mediation sections.
- The strongest reusable idea is to keep model-changing facts—matching radius, control group, pair count, fixed effects, trends—in a visible lower block.

Adopt the spanners, panel logic, and explicit joint tests. Do not copy the preprint watermark, excessively long notes, tiny type, or stray LaTeX/macro artifacts such as the residual `lndis / 5_no2` line visible in one table.

## Priority when sources conflict

1. Numerical/statistical correctness and the target journal's instructions.
2. Kleven/AEA restraint for top-journal main tables.
3. CLL's complex spanners and compact appendix panels.
4. Sha's published-journal notes and multi-outcome hierarchy.
5. Wang's conceptual blocks, after removing preprint artifacts.

The samples support stars as a common convention but also support explicit difference rows without stars. Choose the latter when the scientific question is a cross-group comparison.
