#!/usr/bin/env python3
"""
LaTeX Extractor for Consistency Checking

Extracts structured data from LaTeX files for consistency auditing:
- Labels and references
- Table environments
- Figure environments
- Equations
- Citations
- Section structure

Output: JSON structure for LLM consumption
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import sys


@dataclass
class Label:
    r"""A \label{} definition"""
    name: str
    type: str  # table, figure, equation, section, other
    line_number: int
    context: str  # surrounding text


@dataclass
class Reference:
    r"""A \ref{}, \eqref{}, or similar reference"""
    name: str
    ref_type: str  # ref, eqref, pageref, etc.
    line_number: int
    context: str


@dataclass
class Table:
    """A table environment"""
    environment: str  # table, table*, longtable, etc.
    label: Optional[str]
    caption: Optional[str]
    line_start: int
    line_end: int
    content_preview: str  # first few lines of tabular content
    columns: int
    has_notes: bool


@dataclass
class Figure:
    """A figure environment"""
    environment: str  # figure, figure*, sidewayfigure
    label: Optional[str]
    caption: Optional[str]
    line_start: int
    line_end: int
    includes_graphics: bool
    graphics_path: Optional[str]


@dataclass
class Equation:
    """An equation environment"""
    environment: str  # equation, align, gather, etc.
    label: Optional[str]
    line_number: int
    numbered: bool


@dataclass
class Citation:
    r"""A \cite{} command"""
    keys: List[str]  # can be multiple keys in one \cite
    line_number: int
    cite_type: str  # cite, citet, citep, parencite, etc.


@dataclass
class Section:
    """A section heading"""
    level: str  # section, subsection, subsubsection
    number: Optional[str]
    title: str
    label: Optional[str]
    line_number: int


class LaTeXExtractor:
    """Extract structured data from LaTeX files"""

    # Regex patterns
    LABEL_PATTERN = re.compile(r'\\label\{([^}]+)\}')
    REF_PATTERN = re.compile(r'\\(?:eqref|ref|pageref|autoref|cref|Cref)\{([^}]+)\}')
    CITE_PATTERN = re.compile(r'\\(?:cite[tp]?|parencite|textcite|citealp|citealt|citeauthor|citeyear)?\{([^}]+)\}')
    SECTION_PATTERN = re.compile(r'\\(section|subsection|subsubsection|paragraph|chapter)\*?\{([^}]+)\}')

    # Table patterns
    TABLE_BEGIN = re.compile(r'\\begin\{(table\*?|longtable|tabular\*?|threeparttable|sidewaystable)\}')
    TABLE_END = re.compile(r'\\end\{(table\*?|longtable|tabular\*?|threeparttable|sidewaystable)\}')
    CAPTION_PATTERN = re.compile(r'\\caption(?:\[[^\]]*\])?\{([^}]+)\}')

    # Figure patterns
    FIGURE_BEGIN = re.compile(r'\\begin\{(figure\*?|sidewayfigure)\}')
    FIGURE_END = re.compile(r'\\end\{(figure\*?|sidewayfigure)\}')
    GRAPHICS_PATTERN = re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}')

    # Equation patterns
    EQUATION_BEGIN = re.compile(r'\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?)\}')

    # Bibliography
    BIBLIOGRAPHY_PATTERN = re.compile(r'\\bibliography\{([^}]+)\}')
    ADD_RESOURCE_PATTERN = re.compile(r'\\addbibresource\{([^}]+)\}')

    def __init__(self, tex_path: str):
        self.tex_path = Path(tex_path)
        self.content = ""
        self.lines = []

    def load_file(self) -> bool:
        """Load the LaTeX file"""
        try:
            with open(self.tex_path, 'r', encoding='utf-8', errors='replace') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
            return True
        except Exception as e:
            print(f"Error loading {self.tex_path}: {e}", file=sys.stderr)
            return False

    def extract_labels(self) -> List[Dict]:
        r"""Extract all \label{} definitions"""
        labels = []
        for i, line in enumerate(self.lines, 1):
            for match in self.LABEL_PATTERN.finditer(line):
                name = match.group(1)
                # Determine label type from context
                label_type = self._determine_label_type(name, i)
                labels.append(asdict(Label(
                    name=name,
                    type=label_type,
                    line_number=i,
                    context=line.strip()[:100]
                )))
        return labels

    def extract_references(self) -> List[Dict]:
        """Extract all \ref{} and similar commands"""
        refs = []
        for i, line in enumerate(self.lines, 1):
            for match in self.REF_PATTERN.finditer(line):
                ref_type = self._get_ref_type(line, match.start())
                refs.append(asdict(Reference(
                    name=match.group(1),
                    ref_type=ref_type,
                    line_number=i,
                    context=line.strip()[:100]
                )))
        return refs

    def extract_tables(self) -> List[Dict]:
        """Extract all table environments"""
        tables = []
        in_table = False
        current_table = None
        start_line = 0

        for i, line in enumerate(self.lines, 1):
            # Check for table begin
            if self.TABLE_BEGIN.search(line):
                if not in_table:
                    in_table = True
                    start_line = i
                    env_match = self.TABLE_BEGIN.search(line)
                    current_table = {
                        'environment': env_match.group(1),
                        'line_start': start_line,
                        'label': None,
                        'caption': None,
                        'content_preview': '',
                        'columns': 0,
                        'has_notes': False
                    }

            # Check for table end
            if in_table and self.TABLE_END.search(line):
                current_table['line_end'] = i

                # Extract label from table content
                table_content = '\n'.join(self.lines[start_line-1:i])
                label_match = self.LABEL_PATTERN.search(table_content)
                if label_match:
                    current_table['label'] = label_match.group(1)

                # Extract caption
                caption_match = self.CAPTION_PATTERN.search(table_content)
                if caption_match:
                    current_table['caption'] = caption_match.group(1)

                # Count columns from tabular
                tabular_match = re.search(r'\\begin\{tabular\}\{([clr|]+)\}', table_content)
                if tabular_match:
                    col_spec = tabular_match.group(1)
                    current_table['columns'] = col_spec.count('c') + col_spec.count('l') + col_spec.count('r')

                # Check for notes
                current_table['has_notes'] = 'tablenotes' in table_content or 'note:' in table_content.lower()

                # Content preview
                tabular_lines = [l for l in self.lines[start_line-1:i] if 'tabular' in l or l.strip().startswith('&') or l.strip().startswith('\\\\')]
                current_table['content_preview'] = '\n'.join(tabular_lines[:5])

                tables.append(current_table)
                in_table = False
                current_table = None

        return tables

    def extract_figures(self) -> List[Dict]:
        """Extract all figure environments"""
        figures = []
        in_figure = False
        current_figure = None
        start_line = 0

        for i, line in enumerate(self.lines, 1):
            if self.FIGURE_BEGIN.search(line):
                if not in_figure:
                    in_figure = True
                    start_line = i
                    env_match = self.FIGURE_BEGIN.search(line)
                    current_figure = {
                        'environment': env_match.group(1),
                        'line_start': start_line,
                        'label': None,
                        'caption': None,
                        'includes_graphics': False,
                        'graphics_path': None
                    }

            if in_figure and self.FIGURE_END.search(line):
                current_figure['line_end'] = i

                figure_content = '\n'.join(self.lines[start_line-1:i])

                label_match = self.LABEL_PATTERN.search(figure_content)
                if label_match:
                    current_figure['label'] = label_match.group(1)

                caption_match = self.CAPTION_PATTERN.search(figure_content)
                if caption_match:
                    current_figure['caption'] = caption_match.group(1)

                graphics_match = self.GRAPHICS_PATTERN.search(figure_content)
                if graphics_match:
                    current_figure['includes_graphics'] = True
                    current_figure['graphics_path'] = graphics_match.group(1)

                figures.append(current_figure)
                in_figure = False
                current_figure = None

        return figures

    def extract_equations(self) -> List[Dict]:
        """Extract all equation environments"""
        equations = []
        in_equation = False
        env_type = None
        start_line = 0

        for i, line in enumerate(self.lines, 1):
            if self.EQUATION_BEGIN.search(line):
                if not in_equation:
                    in_equation = True
                    start_line = i
                    env_match = self.EQUATION_BEGIN.search(line)
                    env_type = env_match.group(1)

            if in_equation:
                end_pattern = re.compile(r'\\end\{' + re.escape(env_type) + r'\}')
                if end_pattern.search(line):
                    eq_content = '\n'.join(self.lines[start_line-1:i])
                    label_match = self.LABEL_PATTERN.search(eq_content)

                    equations.append({
                        'environment': env_type,
                        'label': label_match.group(1) if label_match else None,
                        'line_start': start_line,
                        'line_end': i,
                        'numbered': not env_type.endswith('*')
                    })
                    in_equation = False
                    env_type = None

        return equations

    def extract_citations(self) -> List[Dict]:
        r"""Extract all \cite{} commands"""
        citations = []
        seen_keys = set()

        for i, line in enumerate(self.lines, 1):
            for match in self.CITE_PATTERN.finditer(line):
                keys_str = match.group(1)
                keys = [k.strip() for k in keys_str.split(',')]

                # Get cite command type
                cite_type = 'cite'
                cmd_match = re.search(r'\\(\w*cite\w*)', line[max(0, match.start()-20):match.start()])
                if cmd_match:
                    cite_type = cmd_match.group(1)

                citations.append({
                    'keys': keys,
                    'line_number': i,
                    'cite_type': cite_type,
                    'context': line.strip()[:100]
                })

                for key in keys:
                    seen_keys.add(key)

        return citations, list(seen_keys)

    def extract_sections(self) -> List[Dict]:
        """Extract all section headings"""
        sections = []
        section_counters = {'section': 0, 'subsection': 0, 'subsubsection': 0}

        for i, line in enumerate(self.lines, 1):
            match = self.SECTION_PATTERN.search(line)
            if match:
                level = match.group(1)
                title = match.group(2)

                # Update counters
                if level == 'section':
                    section_counters['section'] += 1
                    section_counters['subsection'] = 0
                    section_counters['subsubsection'] = 0
                elif level == 'subsection':
                    section_counters['subsection'] += 1
                    section_counters['subsubsection'] = 0
                elif level == 'subsubsection':
                    section_counters['subsubsection'] += 1

                # Generate section number
                if section_counters['section'] > 0:
                    if level == 'section':
                        number = str(section_counters['section'])
                    elif level == 'subsection':
                        number = f"{section_counters['section']}.{section_counters['subsection']}"
                    else:
                        number = f"{section_counters['section']}.{section_counters['subsection']}.{section_counters['subsubsection']}"
                else:
                    number = None

                # Check for label on same or next line
                label = None
                label_match = self.LABEL_PATTERN.search(line)
                if label_match:
                    label = label_match.group(1)
                elif i < len(self.lines):
                    next_line = self.lines[i]
                    label_match = self.LABEL_PATTERN.search(next_line)
                    if label_match:
                        label = label_match.group(1)

                sections.append({
                    'level': level,
                    'number': number,
                    'title': title,
                    'label': label,
                    'line_number': i
                })

        return sections

    def extract_bibliography_info(self) -> Dict:
        """Extract bibliography file references"""
        bib_files = []

        for line in self.lines:
            # Traditional BibTeX
            match = self.BIBLIOGRAPHY_PATTERN.search(line)
            if match:
                bib_files.extend([b.strip() for b in match.group(1).split(',')])

            # biblatex
            match = self.ADD_RESOURCE_PATTERN.search(line)
            if match:
                bib_files.append(match.group(1))

        return {'bib_files': bib_files}

    def _determine_label_type(self, name: str, line_num: int) -> str:
        """Determine the type of a label from context"""
        name_lower = name.lower()

        if 'tab' in name_lower or 'tbl' in name_lower:
            return 'table'
        if 'fig' in name_lower:
            return 'figure'
        if 'eq' in name_lower or 'equ' in name_lower:
            return 'equation'
        if 'sec' in name_lower or 'app' in name_lower:
            return 'section'

        # Check surrounding context
        context_start = max(0, line_num - 5)
        context_end = min(len(self.lines), line_num + 2)
        context = '\n'.join(self.lines[context_start:context_end])

        if '\\begin{table' in context or '\\begin{tabular' in context:
            return 'table'
        if '\\begin{figure' in context:
            return 'figure'
        if '\\begin{equation' in context or '\\begin{align' in context:
            return 'equation'

        return 'other'

    def _get_ref_type(self, line: str, pos: int) -> str:
        """Determine the type of reference command"""
        before = line[max(0, pos-15):pos]
        if '\\eqref' in before:
            return 'eqref'
        if '\\pageref' in before:
            return 'pageref'
        if '\\autoref' in before:
            return 'autoref'
        if '\\cref' in before:
            return 'cref'
        if '\\Cref' in before:
            return 'Cref'
        return 'ref'

    def extract_all(self) -> Dict[str, Any]:
        """Extract all structured data"""
        citations, unique_keys = self.extract_citations()

        return {
            'source_file': str(self.tex_path),
            'total_lines': len(self.lines),
            'labels': self.extract_labels(),
            'references': self.extract_references(),
            'tables': self.extract_tables(),
            'figures': self.extract_figures(),
            'equations': self.extract_equations(),
            'citations': citations,
            'unique_citation_keys': unique_keys,
            'sections': self.extract_sections(),
            'bibliography': self.extract_bibliography_info()
        }


def main():
    parser = argparse.ArgumentParser(description='Extract structured data from LaTeX files')
    parser.add_argument('tex_file', help='Path to LaTeX file')
    parser.add_argument('--appendix', help='Path to appendix LaTeX file', default=None)
    parser.add_argument('--output', '-o', help='Output JSON file (default: stdout)', default=None)

    args = parser.parse_args()

    extractor = LaTeXExtractor(args.tex_file)
    if not extractor.load_file():
        sys.exit(1)

    result = extractor.extract_all()

    # Add appendix data if provided
    if args.appendix:
        appendix_extractor = LaTeXExtractor(args.appendix)
        if appendix_extractor.load_file():
            appendix_data = appendix_extractor.extract_all()
            result['appendix'] = appendix_data

    # Output
    json_output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(json_output)


if __name__ == '__main__':
    main()
