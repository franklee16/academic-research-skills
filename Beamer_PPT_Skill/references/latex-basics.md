# LaTeX Basics for Beamer

## Document Structure

### Basic Beamer Document

```latex
\documentclass[aspectratio=169,11pt]{beamer}

% Theme setup
\usetheme{metropolis}
\usecolortheme{seahorse}

% Packages
\usepackage{ctex}  % For Chinese
\usepackage{graphicx}
\usepackage{amsmath}

% Title info
\title{Presentation Title}
\author{Author Name}
\institute{Institution}
\date{\today}

\begin{document}

\frame{\titlepage}

\begin{frame}{Outline}
\tableofcontents
\end{frame}

\section{Introduction}
\begin{frame}{Introduction}
Content here
\end{frame}

\end{document}
```

## Common Commands

### Frame Environment

```latex
\begin{frame}{Frame Title}
% Content
\end{frame}

\begin{frame}[fragile]{Code Frame}  % For verbatim/code
\begin{verbatim}
code here
\end{verbatim}
\end{frame}

\begin{frame}[allowframebreaks]{Long Content}  % Auto split
% Very long content
\end{frame}
```

### Text Formatting

```latex
\textbf{Bold text}
\textit{Italic text}
\texttt{Monospace/code}
\emph{Emphasis}
\alert{Highlighted text}  % Beamer specific
```

### Lists

```latex
% Itemize
\begin{itemize}
\item First item
\item Second item
\item Third item
\end{itemize}

% Enumerate
\begin{enumerate}
\item First
\item Second
\item Third
\end{enumerate}

% Description
\begin{description}
\item[Term] Definition
\item[Another] Another definition
\end{description}
```

### Columns

```latex
\begin{columns}[T]  % T=top, c=center, b=bottom
\column{0.5\textwidth}
Left content

\column{0.5\textwidth}
Right content
\end{columns}
```

### Blocks

```latex
\begin{block}{Block Title}
Regular block content
\end{block}

\begin{alertblock}{Warning}
Alert/highlighted block
\end{alertblock}

\begin{exampleblock}{Example}
Example block (green in default themes)
\end{exampleblock}
```

### Images

```latex
\includegraphics[width=0.8\textwidth]{image.png}

\includegraphics[height=5cm]{image.png}

\includegraphics[scale=0.5]{image.png}
```

### Tables

```latex
\begin{tabular}{lcr}  % left, center, right
\toprule
Header 1 & Header 2 & Header 3 \\
\midrule
Left & Center & Right \\
Data & Data & Data \\
\bottomrule
\end{tabular}
```

## Document Class Options

```latex
\documentclass[
    aspectratio=169,  % 16:9 (default), 43 for 4:3, 1610 for 16:10
    11pt,             % Font size: 8pt, 9pt, 10pt, 11pt, 12pt, 14pt, 17pt, 20pt
    t,                % Top alignment (c=center, b=bottom)
    compress,         % Compress navigation bars
    handout,          % Handout mode (no overlays)
    draft             % Draft mode (faster compilation)
]{beamer}
```

## Common Packages

```latex
\usepackage{amsmath}      % Math
\usepackage{amssymb}      % Math symbols
\usepackage{graphicx}     % Images
\usepackage{booktabs}     % Nice tables
\usepackage{tikz}         % Graphics
\usepackage{pgfplots}     % Plots
\usepackage{listings}     % Code listings
\usepackage{hyperref}     % Links
```

## Compilation

### Standard (no bibliography)
```bash
xelatex -interaction=nonstopmode main.tex
```

### With Bibliography
```bash
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

### Extract Single Page
```bash
pdftoppm -f 3 -l 3 -png -r 150 main.pdf page-3.png
```

## Error Messages

### Common Errors

**File not found:**
```
! LaTeX Error: File `xxx.sty' not found.
```
Solution: `tlmgr install xxx`

**Undefined control sequence:**
```
! Undefined control sequence.
l.15 \xxx
```
Solution: Check for typos or missing packages

**Overfull hbox:**
```
Overfull \hbox (10.234pt too wide) in paragraph
```
Solution: Text too wide, adjust spacing or use `\raggedright`

**Missing $ inserted:**
```
! Missing $ inserted.
```
Solution: Math symbol in text mode, wrap in `$...$`
