---
name: stata
description: Use when writing, running, or debugging Stata code, do files, ado files, packages, or Mata programs in this environment. Use when loading Stata datasets, running regressions, managing data, developing Stata commands or packages, or working with Stata/Mata syntax.
---

# Stata
- Author：Wenli Xu
- Email： wlxu@cityu.edu.mo
- 2026-03-11
---

## Overview

Stata is a statistical software package for data management, analysis, and graphics. This environment runs **StataNow 19.5 MP** (Parallel Edition, 16-core), the latest version as of 2025.

## Running Stata in This Environment

**From terminal (interactive REPL):**
```bash
stata-mp
```

**Run a do file non-interactively:**
```bash
stata-mp -b do myfile.do          # batch mode, output to myfile.log
stata-mp -e do myfile.do          # batch mode, no log
```

**Executable path:**
```
/Applications/StataNow/StataMP.app/Contents/MacOS/stata-mp
```

**PATH is already configured** in `~/.zshrc`:
```zsh
export PATH="/Applications/StataNow/StataMP.app/Contents/MacOS:$PATH"
```

## Creating and Running Do Files

A do file is a plain text script with `.do` extension containing Stata commands.

**Basic do file structure:**
```stata
* my_analysis.do
* Description: Example analysis

clear all
set more off

* Load data
use "/path/to/data.dta", clear

* Data exploration
describe
summarize
list in 1/5

* Analysis
regress y x1 x2
estimates store model1

* Save results
log using "output/results.log", replace
  regress y x1 x2
log close

* Export
outsheet using "output/results.csv", comma replace
```

**Run from terminal:**
```bash
stata-mp -b do my_analysis.do
```

**Run from within Stata REPL:**
```stata
. do my_analysis.do
. run my_analysis.do    // silent (no output echo)
```

## Bundled Example Datasets

Located at `/Applications/StataNow/ado/base/` (organized by first letter of filename).

**Load with `sysuse` (no path needed):**
```stata
sysuse auto, clear          // 1978 automobile data (74 obs, price/mpg/weight...)
sysuse nlsw88, clear        // NLS Women 1988 (wage, education, occupation...)
sysuse lifeexp, clear       // Life expectancy by country
sysuse census, clear        // US census data by state
sysuse cancer, clear        // Drug trial survival data
sysuse bplong, clear        // Blood pressure (long format)
sysuse bpwide, clear        // Blood pressure (wide format)
sysuse voter, clear         // Voter turnout data
sysuse sp500, clear         // S&P 500 stock data (time series)
sysuse gnp96, clear         // US GNP time series
sysuse uslifeexp, clear     // US life expectancy over time
sysuse citytemp, clear      // US city temperature data
sysuse educ99gdp, clear     // Education and GDP by country
sysuse pop2000, clear       // US population 2000 census
```

Also available directly: `/Applications/StataNow/auto.dta`

**List all available system datasets:**
```stata
sysuse dir
```

## Documentation (PDF Manuals)

All manuals are in `/Applications/StataNow/docs/`:

| File | Pages | Content |
|------|-------|---------|
| `u.pdf` | ~900 | User's Guide — start here |
| `d.pdf` | ~700 | Data management |
| `r.pdf` | 3503 | Statistics reference (very large) |
| `g.pdf` | ~600 | Graphics |
| `ts.pdf` | ~700 | Time series |
| `xt.pdf` | ~600 | Panel/longitudinal data |
| `st.pdf` | ~500 | Survival analysis |
| `me.pdf` | ~500 | Mixed-effects models |
| `mi.pdf` | ~400 | Multiple imputation |
| `svy.pdf` | ~400 | Survey data |
| `bayes.pdf` | ~600 | Bayesian analysis |
| `lasso.pdf` | ~300 | LASSO and regularization |
| `causal.pdf` | ~300 | Causal inference |
| `meta.pdf` | ~300 | Meta-analysis |
| `fn.pdf` | 193 | Functions reference |
| `p.pdf` | ~800 | Programming (Mata, macros) |
| `m.pdf` | ~600 | Mata reference |

**IMPORTANT: Do NOT use the Read tool to load entire PDFs.** Large manuals consume enormous context. Use the targeted methods below instead.

### Choosing the Right Tool

| Task | Tool | Notes |
|------|------|-------|
| Search keyword across a manual | pdfplumber Python API | Fast, returns page numbers + lines |
| Extract specific pages | pdfplumber Python API | Use after finding page from search |
| Read small section | Read tool with `pages:` param | Only for small PDFs (fn.pdf, causal.pdf etc.) |
| Convert PDF to clean markdown | `uvx "markitdown[pdf]"` | Works on all sizes; large PDFs take minutes but output is clean with proper spaces |
| Install search tools | brew | `brew install pdfgrep pandoc` if needed |

**markitdown vs pdfplumber output quality:**
- `markitdown[pdf]` → clean markdown, proper spaces, best for reading/understanding
- `pdfplumber` → fast but run-together words (`"LinearregressionwithMany..."`), best for search/grep

### pdfplumber — Search a Manual (pdfgrep equivalent)

pdfplumber is available via `uvx`. Use the Python API (the CLI returns blank for Stata's PDFs):

```bash
uvx --with pdfplumber python3 - << 'EOF'
import pdfplumber

PDF = "/Applications/StataNow/docs/r.pdf"
QUERY = "regress"

with pdfplumber.open(PDF) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ""
        if QUERY.lower() in text.lower():
            lines = [l for l in text.splitlines() if QUERY.lower() in l.lower()]
            print(f"  p{i}: {lines[:2]}")
EOF
```

### pdfplumber — Extract Specific Pages

After finding the relevant page numbers via search, extract just those pages:

```bash
uvx --with pdfplumber python3 - << 'EOF'
import pdfplumber

PDF = "/Applications/StataNow/docs/r.pdf"
PAGES = range(2800, 2810)   # 0-indexed page numbers

with pdfplumber.open(PDF) as pdf:
    for i in PAGES:
        text = pdf.pages[i].extract_text() or ""
        # Collapse whitespace (Stata PDFs have no spaces between words in raw text)
        import re
        print(f"--- Page {i+1} ---")
        print(text[:1000])
        print()
EOF
```

**Note:** Stata's PDFs produce run-together text (e.g. `"LinearregressionwithmanyIndicators"`). This is a PDF encoding issue — the content is correct but spaces are missing. It's still searchable and readable with context.

### markitdown — Convert PDF to Markdown

Works on all Stata manuals including large ones (r.pdf, 3503 pages). Large PDFs take several minutes but complete successfully. Output has correct spaces and clean markdown — much more readable than pdfplumber.

```bash
# Small manual — fast
uvx "markitdown[pdf]" /Applications/StataNow/docs/fn.pdf > fn.md

# Large manual — takes a few minutes, run in background
uvx "markitdown[pdf]" /Applications/StataNow/docs/r.pdf > r.md

# Then grep the markdown (much faster for repeated searches)
grep -n "regress" r.md | head -20
```

**Best practice:** Convert once, save as `.md`, then use standard text search tools on the result.

### pdfgrep / pandoc — Install if Needed

These are not currently installed. Install with:

```bash
brew install pdfgrep   # grep-like search across PDFs
brew install pandoc    # general document conversion
```

Once installed, pdfgrep provides simpler syntax:
```bash
pdfgrep -n "regress" /Applications/StataNow/docs/r.pdf
pdfgrep -rn "margins" /Applications/StataNow/docs/
```

### Recommended Workflow for Looking Up Documentation

1. **Know which manual?** → search that PDF with pdfplumber
2. **Don't know which manual?** → search `r.pdf` (statistics) or `u.pdf` (general)
3. **Found page number?** → extract ±5 pages around it with pdfplumber
4. **Small manual (<300p)?** → use Read tool with `pages:` param directly

## Common Commands Quick Reference

```stata
* Data
use "file.dta", clear
import delimited "file.csv", clear
save "output.dta", replace

* Exploration
describe
codebook varname
summarize varname, detail
tab varname
list varname in 1/10

* Data management
keep if condition
drop varname
gen newvar = expression
replace var = val if condition
rename old new
reshape long/wide

* Analysis
regress y x1 x2
logit y x1 x2
ttest y, by(group)
anova y group

* Output
log using "file.log", replace text
log close
outreg2 using "table.doc", replace    // requires outreg2 package
esttab using "table.tex", replace     // requires estout package
```

## User Ado Path

User-installed packages go in:
`~/Library/Application Support/Stata/Stata 19/`

Install packages from within Stata:
```stata
ssc install outreg2
ssc install estout
net install package_name
```

---

## Ado File Development

Ado files implement Stata commands. Each `.ado` file defines one command (same name as file).

**Minimal ado file structure (`mycommand.ado`):**
```stata
*! version 1.0.0  YYYY-MM-DD  Author Name
program define mycommand
    version 19
    syntax varlist [if] [in] [, Option1 Option2(string)]

    marksample touse          // respect if/in/weights

    // your code here
    summarize `varlist' if `touse'
end
```

**Key `syntax` tokens:**
| Token | Meaning |
|-------|---------|
| `varlist` | one or more variable names |
| `varname` | exactly one variable |
| `[if]` | optional if qualifier |
| `[in]` | optional in range |
| `[fw= ] [aw= ] [pw= ] [iw=]` | weights |
| `, Option` | flag option |
| `, Opt(string)` | option with string argument |
| `, Opt(integer 0)` | option with integer (default 0) |
| `, Opt(real 1.0)` | option with real |

**e-class command (stores estimation results):**
```stata
program define myest, eclass
    version 19
    syntax varlist [if] [in] [aw fw pw iw]
    marksample touse

    // ... estimation ...

    ereturn post `b' `V', obs(`N') esample(`touse')
    ereturn local cmd "myest"
    ereturn local depvar "`depvar'"
    ereturn display
end
```

**r-class command (stores returned results):**
```stata
program define mystat, rclass
    version 19
    syntax varname [if] [in]
    marksample touse

    quietly summarize `varlist' if `touse'
    return scalar mean = r(mean)
    return scalar sd   = r(sd)
end
```

**Where to put ado files during development:**
```stata
. adopath               // shows current search path
. adopath + "/path/to/myproject"   // add project dir temporarily
```
Or place files in `~/Library/Application Support/Stata/Stata 19/ado/personal/`
for permanent personal commands.

**Reload a changed ado during development:**
```stata
. cap program drop mycommand
. do mycommand.ado
```

---

## Package Structure

A distributable Stata package consists of:

```
mypkg/
  mypkg.pkg          // package manifest
  stata.toc          // table of contents (for net install)
  mycommand.ado      // command(s)
  mycommand.sthlp    // help file
  mycommand2.ado
  mycommand2.sthlp
```

**Package manifest (`mypkg.pkg`):**
```
v 3
d mypkg: Short description of the package
d Author Name <email@example.com>
d Distribution-Date: YYYYMMDD
d
f mycommand.ado
f mycommand.sthlp
f mycommand2.ado
f mycommand2.sthlp
```

**Table of contents (`stata.toc`):**
```
v 3
d Packages in this collection
p mypkg Short description of the package
```

**Install local package:**
```stata
net install mypkg, from("/path/to/mypkg/") replace
```

**Install from GitHub:**
```stata
net install mypkg, from("https://raw.githubusercontent.com/user/repo/main/") replace
```

---

## Help File (.sthlp)

```stata
{smcl}
{* *! version 1.0.0  YYYY-MM-DD}{...}
{title:Title}

{phang}
{bf:mycommand} {hline 2} Brief description

{title:Syntax}

{p 8 17 2}
{cmdab:mycommand}
{varlist}
{ifin}
[{cmd:,} {it:options}]

{title:Description}

{pstd}
Longer description of what the command does.

{title:Options}

{phang}
{opt option1} description of option1.

{title:Examples}

{phang2}{cmd:. sysuse auto, clear}{p_end}
{phang2}{cmd:. mycommand price mpg}{p_end}

{title:Author}

{pstd}Name, Institution{p_end}
{pstd}email@example.com{p_end}
```

---

## Mata

Mata is Stata's compiled matrix language, used for performance-critical code or complex algorithms.

**Enter/exit Mata interactively:**
```stata
. mata
: // now in Mata
: end
```

**Mata in a do file:**
```stata
mata:
    // Mata code here
end
```

**Basic Mata syntax:**
```mata
// Variables and types
real scalar   x
real vector   v
real matrix   A
string scalar s
pointer(real matrix) scalar p

// Arithmetic
A = J(3, 3, 0)          // 3×3 zeros
A = I(3)                // 3×3 identity
v = (1, 2, 3)           // row vector
v = (1 \ 2 \ 3)         // column vector

// Functions
rows(A), cols(A)
A'                      // transpose
invsym(A)               // inverse of symmetric matrix
cross(X, X)             // X'X
quadcross(X, X)         // more numerically stable X'X
cholesky(A)
eigenvalues(A, V, L)    // eigenvectors V, eigenvalues L

// Control flow
for (i=1; i<=rows(A); i++) { ... }
while (cond) { ... }
if (cond) { ... } else { ... }
```

**Passing data between Stata and Mata:**
```mata
// Stata → Mata
st_view(X=., ., "varlist")          // zero-copy view (preferred)
X = st_data(., "varlist")           // copy

// Mata → Stata
st_store(., "varname", vector)      // store into existing variable
st_addvar("double", "newvar")       // create variable first
st_store(., "newvar", vector)
st_numscalar("r(result)", value)    // return scalar to Stata
```

**Mata function definition:**
```mata
real matrix myfunction(real matrix X, real scalar k) {
    real matrix result
    result = X * k
    return(result)
}
```

**Mata library (`.mlib`) for distribution:**
```stata
// Compile and save Mata library
mata mosave myfunction(), dir(.) replace
// Creates myfunction.mo (object file)

// For package distribution: create mypkg.mlib
mata mata mlib create lmypkg, dir(.) replace
mata mata mlib add lmypkg myfunction()
```

**Calling Mata from ado:**
```stata
program define mycommand, eclass
    version 19
    syntax varlist [if] [in]
    marksample touse

    mata: _mycommand_work("`varlist'", "`touse'")

    ereturn post `r(b)' `r(V)'
end

mata:
void _mycommand_work(string scalar varnames, string scalar touse) {
    real matrix X, y
    st_view(y=., ., tokens(varnames)[1], touse)
    st_view(X=., ., tokens(varnames)[2..cols(tokens(varnames))], touse)
    // ... estimation logic ...
}
end
```

**Useful Mata references:** `/Applications/StataNow/docs/m.pdf` (Mata reference), `/Applications/StataNow/docs/p.pdf` (Programming)
