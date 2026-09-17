# LaTeX Best Practices for Empirical Finance

## Table of Contents

1. [Citations](#citations)
2. [Equations](#equations)
3. [Tables](#tables)
4. [Cross-References](#cross-references)
5. [Formatting](#formatting)
6. [Compilation](#compilation)

---

## Citations

### Citation Commands (biblatex with natbib=true)

```latex
% Author in sentence
\citet{fama1993} show that a five-factor model captures...

% Parenthetical citation
...the three-factor model~\citep{fama1993}.

% Never write this:
% (Fama and French, 1993) show that...  <- WRONG
```

**Rules:**
- Use `~\citep{}` (non-breaking space + parenthetical) when citation is not part of the sentence
- Use `\citet{}` when authors are grammatically part of the sentence
- Never manually write "(Author, Year)" -- always use citation commands
- Cite the published version, not the working paper version, when available

### Citation Style

- Use `biblatex` with `biber` backend (not `natbib` + `bibtex`)
- `style=authoryear` with `natbib=true` preserves `\citet` / `\citep` compatibility
- `maxcitenames=3`, `mincitenames=1` for standard economics citation format

## Equations

### When to Display

- Display important equations that are referenced later
- Display equations that define key quantities
- Keep simple expressions inline: $r_{i,t} = \alpha + \beta \cdot DS_{i,t} + \epsilon_{i,t}$
- Do not display every algebraic manipulation

### Formatting Rules

```latex
% Numbered equation (if you reference it)
\begin{equation}
  \label{eq:ewma}
  DS_{i,t} = \lambda \cdot ds_{i,t} + (1 - \lambda) \cdot DS_{i,t-1}
\end{equation}

% Unnumbered (if never referenced)
\begin{equation*}
  r_{i,t} = \alpha + \beta_1 DS_{i,t-1} + \gamma' X_{i,t-1} + \epsilon_{i,t}
\end{equation*}
```

- **No blank line** after `\end{equation}` -- it creates an extra paragraph break
- Use `\stackrel{?}{=}` or explain steps for non-trivial equality/inequality transitions
- Mathematical equations follow punctuation rules: periods and commas after equations

### Common Finance Equations

```latex
% Fama-MacBeth regression
r_{i,t} = \alpha_t + \beta_t DS_{i,t-1} + \gamma_t' X_{i,t-1} + \epsilon_{i,t}

% Factor model
r_{i,t} - r_{f,t} = \alpha_i + \beta_{i,M} (r_{M,t} - r_{f,t})
  + \beta_{i,SMB} SMB_t + \beta_{i,HML} HML_t + \epsilon_{i,t}

% Portfolio sort notation
R_{L/S,t} = R_{Q5,t} - R_{Q1,t}
```

## Tables

### Finance Table Template

```latex
\begin{table}[htbp]
\centering
\caption{Portfolio Sorts on DS Score}
\label{tab:sort}
\begin{threeparttable}
\begin{tabular}{@{} l cccc @{}}
\toprule
& Raw Return & CAPM $\alpha$ & FF3 $\alpha$ & FF5 $\alpha$ \\
\midrule
Q1 (Low)  & 0.52  & 0.11  & 0.08  & 0.03  \\
          & (2.14)& (0.89)& (0.67)& (0.28)\\
[6pt]
Q5 (High) & 1.85  & 1.42  & 1.38  & 1.28  \\
          & (5.91)& (4.82)& (4.65)& (4.31)\\
[6pt]
L/S       & 1.33*** & 1.31*** & 1.30*** & 1.25*** \\
          & (4.12) & (4.05) & (3.98) & (3.84) \\
\midrule
\multicolumn{5}{@{}l}{\textit{Controls:} Firm and month FE} \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]\small
\item This table reports monthly returns (\%) from portfolio sorts on DS Score.
Quintile portfolios are formed monthly from April 2011 to December 2019.
t-statistics in parentheses. * p<0.10, ** p<0.05, *** p<0.01.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

**Key conventions:**
- Use `booktabs` rules only (`\toprule`, `\midrule`, `\bottomrule`)
- No vertical rules, no `\hline`
- t-statistics in parentheses below coefficients
- Stars on the coefficient, not the t-stat
- Table notes via `threeparttable`

## Cross-References

### Using cleveref

```latex
\usepackage{cleveref} % Load after hyperref

% In text:
\Cref{tab:sort} reports portfolio sorts.
We estimate the model in \cref{eq:ewma}.
Results in \cref{fig:cumret} show...
```

**Benefits:**
- Automatically handles singular/plural
- Consistent formatting
- `\Cref{}` capitalizes (start of sentence), `\cref{}` does not

### Labels

Use descriptive prefixes:
- `eq:` for equations
- `tab:` for tables
- `fig:` for figures
- `sec:` for sections
- `app:` for appendices

## Formatting

### General Rules

- Use correct quotation marks: `` `quoted text' `` or `\enquote{quoted text}` with `csquotes`
- Footnotes after punctuation: `sentence.\footnote{Note text}`
- `\label{}` after `\caption{}` in figures
- Use `\left(` and `\right)` for auto-sizing parentheses, or explicit `\big(`, `\Big(` for fine control
- Check for broken references (indicated by `??`)
- Minimize white space; fill the page efficiently

### Chinese Text (if applicable)

- Use `inputenc[utf8]` with `lmodern` for pdflatex -- avoids CJK package crashes
- Or use XeLaTeX with `fontspec` for full Unicode support
- Set `PYTHONIOENCODING=utf-8` when processing Chinese CSV files

### Packages to Load

Essential for finance papers:
```latex
\usepackage{booktabs}       % Professional tables
\usepackage{threeparttable}  % Table notes
\usepackage{siunitx}         % Number alignment
\usepackage{amsmath}         % Equations
\usepackage{graphicx}        % Figures
\usepackage{hyperref}        % Links (load last)
\usepackage{cleveref}        % Cross-refs (after hyperref)
\usepackage{caption}         % Caption formatting
\usepackage{subcaption}      % Sub-figures
```

## Compilation

### Standard sequence

```bash
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

Note: `biber` replaces `bibtex` when using `biblatex`.

### Common Issues

- **Undefined references**: Run biber, then recompile twice
- **Overfull hbox**: Break long URLs, adjust margins, or use `microtype`
- **Missing fonts**: Install `lmodern` or switch to XeLaTeX with `fontspec`
- **CJK errors**: Do not use `CJKutf8` package with MiKTeX; use `inputenc[utf8]` instead
