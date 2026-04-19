#!/usr/bin/env python3
r"""
Cross-Reference Validator for LaTeX Documents

Validates:
- All \ref{} have matching \label{}
- All \label{} are referenced at least once
- All \cite{} keys exist in bibliography
- Table/figure numbering is sequential

Output: JSON report of validation issues
"""

import re
import json
import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass, asdict


@dataclass
class Issue:
    """A validation issue"""
    severity: str  # major, medium, minor
    category: str
    location: str
    description: str
    details: Dict[str, Any] = None


class CrossRefValidator:
    """Validate cross-references in LaTeX documents"""

    def __init__(self, tex_file: str, bib_file: str = None):
        self.tex_path = Path(tex_file)
        self.bib_path = Path(bib_file) if bib_file else None
        self.content = ""
        self.lines = []
        self.issues: List[Issue] = []

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

    def extract_labels(self) -> Set[str]:
        r"""Extract all \label{} definitions"""
        pattern = re.compile(r'\\label\{([^}]+)\}')
        return set(pattern.findall(self.content))

    def extract_references(self) -> Set[str]:
        r"""Extract all \ref{}, \eqref{}, etc."""
        pattern = re.compile(r'\\(?:eqref|ref|pageref|autoref|cref|Cref)\{([^}]+)\}')
        return set(pattern.findall(self.content))

    def extract_citations(self) -> Set[str]:
        """Extract all citation keys"""
        pattern = re.compile(r'\\(?:cite[tp]?|parencite|textcite|citealp|citealt|citeauthor|citeyear)?\{([^}]+)\}')
        keys = set()
        for match in pattern.finditer(self.content):
            # Handle multiple keys in one \cite{key1,key2}
            for key in match.group(1).split(','):
                keys.add(key.strip())
        return keys

    def extract_bib_keys(self) -> Set[str]:
        """Extract all @type{key, entries from bibliography"""
        if not self.bib_path or not self.bib_path.exists():
            return set()

        try:
            with open(self.bib_path, 'r', encoding='utf-8', errors='replace') as f:
                bib_content = f.read()
        except Exception:
            return set()

        # Match @article{key, @book{key, etc.
        pattern = re.compile(r'@\w+\{([^,]+),', re.IGNORECASE)
        return set(k.strip() for k in pattern.findall(bib_content))

    def validate_label_ref_consistency(self) -> List[Issue]:
        """Check that all refs have labels and vice versa"""
        issues = []
        labels = self.extract_labels()
        refs = self.extract_references()

        # References without labels (MAJOR)
        missing_labels = refs - labels
        for ref in sorted(missing_labels):
            # Find line number
            for i, line in enumerate(self.lines, 1):
                if f'\\ref{{{ref}}}' in line or f'\\eqref{{{ref}}}' in line:
                    issues.append(Issue(
                        severity='major',
                        category='cross-reference',
                        location=f'Line {i}',
                        description=f'Reference to undefined label: {ref}',
                        details={'label': ref, 'line': i}
                    ))
                    break

        # Labels without references (MEDIUM - could be intentional)
        orphan_labels = labels - refs
        for label in sorted(orphan_labels):
            issues.append(Issue(
                severity='medium',
                category='cross-reference',
                location=f'Label: {label}',
                description=f'Label defined but never referenced (orphan label)',
                details={'label': label}
            ))

        return issues

    def validate_citation_consistency(self) -> List[Issue]:
        """Check that all citations exist in bibliography"""
        issues = []
        cited_keys = self.extract_citations()
        bib_keys = self.extract_bib_keys()

        if not bib_keys:
            # Can't validate without bibliography file
            if cited_keys:
                issues.append(Issue(
                    severity='minor',
                    category='citation',
                    location='Bibliography',
                    description='Bibliography file not found or empty - citation validation skipped',
                    details={'cited_keys': len(cited_keys)}
                ))
            return issues

        # Citations not in bibliography (MAJOR)
        missing_citations = cited_keys - bib_keys
        for key in sorted(missing_citations):
            # Find line number
            for i, line in enumerate(self.lines, 1):
                if key in line and '\\cite' in line:
                    issues.append(Issue(
                        severity='major',
                        category='citation',
                        location=f'Line {i}',
                        description=f'Citation key not in bibliography: {key}',
                        details={'key': key, 'line': i}
                    ))
                    break

        # Bibliography entries never cited (MINOR)
        uncited = bib_keys - cited_keys
        for key in sorted(uncited):
            issues.append(Issue(
                severity='minor',
                category='citation',
                location=f'Bibliography entry: {key}',
                description=f'Bibliography entry never cited',
                details={'key': key}
            ))

        return issues

    def validate_table_numbering(self) -> List[Issue]:
        """Check table numbering is sequential"""
        issues = []
        table_nums = []

        # Find all table labels with numbers
        # Pattern: \label{tab:...} or Table \ref{...}
        table_ref_pattern = re.compile(r'Table\s+(\d+)', re.IGNORECASE)
        table_label_pattern = re.compile(r'\\label\{tab[^}]*\}', re.IGNORECASE)

        # Find table numbers in text
        for match in table_ref_pattern.finditer(self.content):
            num = int(match.group(1))
            table_nums.append(num)

        # Check for gaps
        if table_nums:
            table_nums = sorted(set(table_nums))
            expected = list(range(1, max(table_nums) + 1))
            gaps = set(expected) - set(table_nums)

            for gap in sorted(gaps):
                issues.append(Issue(
                    severity='medium',
                    category='table-numbering',
                    location='Document',
                    description=f'Table numbering gap: Table {gap} not found',
                    details={'missing_number': gap}
                ))

        return issues

    def validate_figure_numbering(self) -> List[Issue]:
        """Check figure numbering is sequential"""
        issues = []
        figure_nums = []

        figure_ref_pattern = re.compile(r'Figure\s+(\d+)', re.IGNORECASE)

        for match in figure_ref_pattern.finditer(self.content):
            num = int(match.group(1))
            figure_nums.append(num)

        if figure_nums:
            figure_nums = sorted(set(figure_nums))
            expected = list(range(1, max(figure_nums) + 1))
            gaps = set(expected) - set(figure_nums)

            for gap in sorted(gaps):
                issues.append(Issue(
                    severity='medium',
                    category='figure-numbering',
                    location='Document',
                    description=f'Figure numbering gap: Figure {gap} not found',
                    details={'missing_number': gap}
                ))

        return issues

    def check_table_text_consistency(self) -> List[Issue]:
        """Check for common table/text mismatches"""
        issues = []

        # Check for significance level mismatches
        # Pattern: "significant at the X% level" vs stars in tables
        sig_patterns = [
            (r'significant at the 1% level', '***'),
            (r'significant at the 5% level', '**'),
            (r'significant at the 10% level', '*'),
        ]

        for text_pattern, expected_stars in sig_patterns:
            for i, line in enumerate(self.lines, 1):
                if re.search(text_pattern, line, re.IGNORECASE):
                    # This is a semantic check - we flag for LLM verification
                    issues.append(Issue(
                        severity='minor',
                        category='table-text',
                        location=f'Line {i}',
                        description=f'Verify significance level matches table stars: "{text_pattern}"',
                        details={'expected_stars': expected_stars, 'line': i}
                    ))

        return issues

    def validate_all(self) -> Dict[str, Any]:
        """Run all validations"""
        all_issues = []
        all_issues.extend(self.validate_label_ref_consistency())
        all_issues.extend(self.validate_citation_consistency())
        all_issues.extend(self.validate_table_numbering())
        all_issues.extend(self.validate_figure_numbering())
        all_issues.extend(self.check_table_text_consistency())

        # Group by severity
        by_severity = {'major': [], 'medium': [], 'minor': []}
        for issue in all_issues:
            by_severity[issue.severity].append(asdict(issue))

        return {
            'source_file': str(self.tex_path),
            'bibliography_file': str(self.bib_path) if self.bib_path else None,
            'summary': {
                'total_issues': len(all_issues),
                'major': len(by_severity['major']),
                'medium': len(by_severity['medium']),
                'minor': len(by_severity['minor'])
            },
            'issues_by_severity': by_severity,
            'all_issues': [asdict(i) for i in all_issues]
        }


def main():
    parser = argparse.ArgumentParser(description='Validate cross-references in LaTeX documents')
    parser.add_argument('tex_file', help='Path to LaTeX file')
    parser.add_argument('--bib', help='Path to bibliography file', default=None)
    parser.add_argument('--output', '-o', help='Output JSON file (default: stdout)', default=None)

    args = parser.parse_args()

    validator = CrossRefValidator(args.tex_file, args.bib)
    if not validator.load_file():
        sys.exit(1)

    result = validator.validate_all()

    json_output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(json_output)

    # Exit with error code if major issues found
    if result['summary']['major'] > 0:
        sys.exit(2)


if __name__ == '__main__':
    main()
