---
name: code-to-notation-table
description: Use when the user provides program code, scripts, or variable lists and wants a Word .docx correspondence table mapping code variables to paper-ready mathematical notation. The output must be a reusable notation dictionary with editable Word equation objects in the paper-symbol column, not plain LaTeX text, screenshots, or manuscript prose.
metadata:
  short-description: Create Word equation notation tables from code variables
---

# Code To Notation Table

Create a Word `.docx` notation dictionary that maps program variables to publication-style symbols. This skill does not write the manuscript. Its job is to produce the authoritative table that later manuscript writing must follow.

## Required Output

Deliver a `.docx` containing a table with these columns:

1. Code variable
2. Paper symbol
3. Meaning
4. Category
5. Notes

The **Paper symbol** cells must contain editable Word equation objects, equivalent to symbols inserted through Word's **Insert > Equation** feature. Do not leave LaTeX source as ordinary text in the final table.

## Workflow

1. Inspect the supplied code or variable list.
   - Prefer actual assignments, struct fields, config fields, function outputs, and variables used in formulas.
   - Ignore loop counters, temporary indices, file paths, plotting handles, and implementation-only UI/debug variables unless the paper discusses them.

2. Classify each relevant variable:
   - **Physical quantity**: real physical meaning, such as velocity, phase, amplitude, displacement, time, frequency, strain, force.
   - **Parameter/threshold**: configuration values, thresholds, window lengths, counts, rates, limits.
   - **State/flag**: boolean flags, enum labels, mode/status variables.
   - **Intermediate quantity**: computed processing stages that may or may not deserve a paper symbol.
   - **Implementation detail**: do not include unless needed for traceability.

3. Design symbols using shallow notation:
   - Physical quantities use conventional Greek or Latin symbols.
   - True values use a star or similar role marker, e.g. `v^\ast`.
   - Estimates use hats, e.g. `\hat{v}`.
   - Parameters use compact bases such as `T`, `N`, `\theta`, or `\lambda`, with upright text subscripts, e.g. `T_{\mathrm{hard}}`.
   - Flags are usually folded into a state variable such as `s(n)` or `s_k`, rather than receiving independent symbols.
   - Intermediate quantities are omitted unless they are part of the method's contribution.

4. Enforce notation depth:
   - Allow at most one subscript layer and one superscript/decorator layer.
   - Prefer `A^{(1)}, A^{(2)}` over descriptive multiword subscripts when several variants must be distinguished.
   - Reject symbols like `A_{\mathrm{env},\mathrm{base}}` or `\hat{v}_{k,\mathrm{est}}`; redesign them.

5. Generate and verify the Word table.
   - Use `scripts/make_notation_docx.py` when producing a fresh `.docx` from a JSON row file.
   - Render or inspect the `.docx` before delivery when possible. Confirm the paper-symbol column is not plain LaTeX text.
   - Include a short audit note in the final response: conflicts found, omitted variables, and any symbols intentionally folded into state notation.

## Script Usage

Prepare a JSON file with rows like:

```json
{
  "title": "Code Variable To Paper Symbol Table",
  "rows": [
    {
      "code": "v_true",
      "latex": "v^\\ast",
      "meaning": "True velocity",
      "category": "Physical quantity",
      "note": "True value marked by star."
    },
    {
      "code": "CFG.T_hard_limit",
      "latex": "T_{\\mathrm{hard}}",
      "meaning": "Hard-limit time threshold",
      "category": "Parameter/threshold",
      "note": "Upright text subscript."
    }
  ]
}
```

Then run:

```powershell
python scripts/make_notation_docx.py rows.json output.docx
```

The script supports common notation patterns used by this skill. If a symbol is too complex for the converter, simplify the notation first; do not paste raw LaTeX into the final Word table.

## References

For symbol choices and examples, read `references/symbol_conventions.md` only when needed.
