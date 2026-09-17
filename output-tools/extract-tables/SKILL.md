---
name: extract-tables
description: Extract all tables from a Word (.docx) document into a single Markdown file. Use this skill whenever the user asks to extract, pull, or export tables from a .docx file, or when they say "get the tables from Word" or "convert DOCX tables to markdown". Also use when the user mentions tables in a Word document and wants them in a usable format for slides, analysis, or reference. Trigger even if they don't explicitly say "extract" — any request to get tables out of a .docx qualifies.
---

# Extract Tables from DOCX to Markdown

Extracts every table from a Word document into a clean, structured Markdown file. Handles merged cells (both horizontal gridSpan and vertical vMerge) that trip up naive approaches.

## Why This Skill Exists

DOCX tables are notoriously hard to extract correctly. The common pitfalls:

1. **pandoc alone creates 300+ phantom tables** — pandoc splits complex DOCX tables into hundreds of 1-row fragments because it can't handle merged cells.
2. **python-docx `table.rows[i].cells` duplicates text** — when cells are horizontally merged, iterating `row.cells` returns the same text multiple times (python-docx returns a reference to the first cell in the merge for each grid position).
3. **Vertical merges are invisible without XML parsing** — `vMerge` elements in the XML tell you which cells continue a vertical span. Without reading them, continuation cells appear empty or get wrong text.
4. **Column counts from `len(table.columns)` are unreliable** — merged cells mean the logical column count differs from the physical cell count. Must compute from `gridSpan` attributes.

The correct approach: parse the raw XML of each table (`table._tbl`), read `gridSpan` and `vMerge` attributes, and build a proper grid before rendering to Markdown.

## Prerequisites

- Python with `python-docx` installed (`pip install python-docx`)
- UTF-8 output encoding (Windows defaults to GBK in some locales — must set explicitly)

## Process

### Step 1: Verify the DOCX file exists

Use Glob to confirm the path. If the user gives a relative path, resolve it from the project root.

### Step 2: Run the extraction script

Execute the Python script below. It handles all the tricky parts internally.

**Key parameters to set:**
- `DOCX_PATH`: absolute path to the input .docx file
- `OUTPUT_PATH`: where to write the markdown (default: same directory as input, named `<filename>_tables.md`)

```python
import sys, io, re
from xml.etree import ElementTree as ET

# Windows UTF-8 fix — prevent UnicodeEncodeError on CJK/special chars
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document

NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NSP = '{' + NS + '}'

def cell_text_from_xml(tc):
    """Extract text from a <w:tc> element by reading <w:t> children directly.
    This avoids python-docx's merged-cell duplication problem."""
    texts = []
    for t in tc.iter(f'{NSP}t'):
        if t.text:
            texts.append(t.text)
    text = ''.join(texts).strip()
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text

def get_grid_span(tc):
    """Read horizontal gridSpan from cell XML. Default is 1."""
    tcPr = tc.find(f'{NSP}tcPr')
    if tcPr is not None:
        gs = tcPr.find(f'{NSP}gridSpan')
        if gs is not None:
            return int(gs.get(f'{NSP}val', '1'))
    return 1

def get_vmerge_type(tc):
    """Read vertical merge status. Returns 'restart', 'continue', or None."""
    tcPr = tc.find(f'{NSP}tcPr')
    if tcPr is not None:
        vm = tcPr.find(f'{NSP}vMerge')
        if vm is not None:
            val = vm.get(f'{NSP}val', '')
            if val == 'restart':
                return 'restart'
            else:
                return 'continue'
    return None

def table_to_markdown(table):
    """Convert a docx table to markdown using raw XML for correct merged-cell handling."""
    tbl = table._tbl
    trs = tbl.findall(f'{NSP}tr')

    if not trs:
        return ""

    parsed_rows = []
    for tr in trs:
        tcs = tr.findall(f'{NSP}tc')
        row_cells = []
        for tc in tcs:
            row_cells.append({
                'text': cell_text_from_xml(tc),
                'hspan': get_grid_span(tc),
                'vmerge': get_vmerge_type(tc),
            })
        parsed_rows.append(row_cells)

    # Total columns = max row width (sum of gridSpans)
    total_cols = 0
    for row in parsed_rows:
        row_total = sum(c['hspan'] for c in row)
        total_cols = max(total_cols, row_total)

    # Build expanded grid
    grid = []
    vmerge_stack = {}  # col -> text from the 'restart' cell

    for row_idx, row in enumerate(parsed_rows):
        expanded = [''] * total_cols
        col_idx = 0
        for cell in row:
            text = cell['text']
            hspan = cell['hspan']
            vmerge = cell['vmerge']

            if vmerge == 'continue':
                for c in range(col_idx, col_idx + hspan):
                    expanded[c] = vmerge_stack.get(c, '')
            elif vmerge == 'restart':
                for c in range(col_idx, col_idx + hspan):
                    vmerge_stack[c] = text
                expanded[col_idx] = text
                for c in range(col_idx + 1, col_idx + hspan):
                    expanded[c] = ''
            else:
                expanded[col_idx] = text
                for c in range(col_idx + 1, col_idx + hspan):
                    expanded[c] = ''

            col_idx += hspan

        grid.append(expanded)

    # Render markdown
    lines = []
    for i, row in enumerate(grid):
        line = '| ' + ' | '.join(r.replace('|', '-') for r in row) + ' |'
        lines.append(line)
        if i == 0:
            sep = '| ' + ' | '.join(['---'] * total_cols) + ' |'
            lines.append(sep)

    return '\n'.join(lines)

def find_table_titles(doc):
    """Scan document body for paragraph text preceding each <w:tbl>."""
    body = doc.element.body
    titles = {}
    tbl_count = 0
    children = list(body)
    for idx, child in enumerate(children):
        if child.tag == f'{NSP}tbl':
            tbl_count += 1
            title_parts = []
            for j in range(idx - 1, max(idx - 6, -1), -1):
                if children[j].tag == f'{NSP}p':
                    texts = []
                    for t in children[j].iter(f'{NSP}t'):
                        if t.text:
                            texts.append(t.text)
                    para_text = ''.join(texts).strip()
                    if para_text:
                        title_parts.insert(0, para_text)
                    else:
                        break
                else:
                    break
            titles[tbl_count] = ' — '.join(title_parts) if title_parts else ''
    return titles

# --- MAIN ---
DOCX_PATH = r"REPLACE_WITH_ACTUAL_PATH"
OUTPUT_PATH = DOCX_PATH.replace('.docx', '_tables.md').replace('.DOCX', '_tables.md')

doc = Document(DOCX_PATH)
titles = find_table_titles(doc)

output = []
output.append(f"# Tables Extracted from {DOCX_PATH.split('/')[-1].split(chr(92))[-1]}\n")
output.append(f"Total tables: {len(doc.tables)}\n")

for i, table in enumerate(doc.tables):
    num = i + 1
    rows = len(table.rows)

    # Get actual column count from XML (not len(table.columns))
    tbl = table._tbl
    first_tr = tbl.find(f'{NSP}tr')
    if first_tr is not None:
        actual_cols = sum(get_grid_span(tc) for tc in first_tr.findall(f'{NSP}tc'))
    else:
        actual_cols = len(table.columns)

    title = titles.get(num, '')

    output.append(f"## Table {num} ({rows} rows x {actual_cols} cols)")
    if title:
        output.append(f"**Title:** {title}\n")

    md = table_to_markdown(table)
    output.append(md)
    output.append("\n")

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"Extracted {len(doc.tables)} tables to {OUTPUT_PATH}")
```

### Step 3: Verify the output

1. Read the first ~100 lines of the output file to confirm structure
2. Spot-check that:
   - No duplicate columns from merged headers (the #1 sign of failure)
   - Regression tables have the right column count (typically 4-5 cols for econ papers)
   - Key coefficients are present and not garbled
   - Table titles/captions from preceding paragraphs were captured
3. Report the table count and a brief summary to the user

## Common Failure Modes and Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| 300+ tiny tables instead of ~20 | Using pandoc instead of python-docx | Use python-docx with XML parsing |
| Duplicate text in merged cells | Using `row.cells` iteration | Read `<w:tc>` XML directly via `tbl.findall` |
| Empty cells where text should be | Not handling `vMerge` continuation | Use `vmerge_stack` to propagate text down |
| Wrong column count | Using `len(table.columns)` | Sum `gridSpan` from first row's XML |
| UnicodeEncodeError on Windows | Default GBK encoding on Chinese Windows | Set `sys.stdout` to UTF-8 wrapper |
| Pipe characters breaking markdown tables | Table cells containing `|` | Replace `|` with `-` in cell text |

## Output Format

The markdown file has this structure:

```markdown
# Tables Extracted from <filename>

Total tables: N

## Table 1 (M rows x K cols)
**Title:** <caption from preceding paragraph>

| Col1 | Col2 | ... |
|------|------|-----|
| ...  | ...  | ... |

## Table 2 (M rows x K cols)
...
```

Each table gets a heading with its dimensions, an optional title (captured from paragraphs immediately before the table in the document), and the full markdown table.
