# Workbook specification

`scripts/make_example_workbook.py` accepts UTF-8 JSON with this structure:

```json
{
  "metadata": {
    "source_image": "figure.png",
    "data_mode": "synthetic look-alike",
    "random_seed": 20260815,
    "notes": "Values approximate the visible geometry; they are not source data."
  },
  "sheets": [
    {
      "name": "line_data",
      "columns": {
        "x": [0, 1, 2, 3],
        "control": [1.1, 1.6, 1.4, 2.0],
        "treatment": [0.9, 1.2, 1.8, 2.4]
      }
    },
    {
      "name": "annotations",
      "rows": [
        {"x": 2, "y": 1.8, "label": "peak"}
      ]
    }
  ]
}
```

Rules:

- `metadata` is optional; every value is written to a `README` sheet.
- `sheets` must be a non-empty list.
- Each sheet requires a unique Excel-safe `name` of at most 31 characters.
- Supply exactly one of `columns` or `rows` per sheet.
- Arrays in `columns` must have equal lengths.
- Every item in `rows` must be an object. Column order follows the first appearance of keys.
- Values may be strings, numbers, booleans, or null. Nested objects and arrays are rejected.
- The utility adds filters, frozen headers, sensible widths, and numeric formatting.

For a matrix heatmap, use either a long table (`row`, `column`, `value`) or a rectangular wide table. Prefer long form when annotations or missing cells matter.
