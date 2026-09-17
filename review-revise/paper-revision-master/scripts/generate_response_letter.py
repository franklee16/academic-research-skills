#!/usr/bin/env python3
"""
Generate Response Letter Script

Reads completed revision tracker (Excel/CSV) and generates formatted LaTeX response letter.

Usage:
    python generate_response_letter.py revision_tracker.xlsx --output response_letter.tex
    python generate_response_letter.py revision_tracker.csv --output response_letter.tex

Requirements:
    pip install pandas openpyxl  # For Excel support
"""

import sys
import re
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

try:
    import pandas as pd
    PANDAS_SUPPORT = True
except ImportError:
    PANDAS_SUPPORT = False
    print("Warning: pandas not installed. Excel/CSV support unavailable.")
    print("Install with: pip install pandas openpyxl")


def load_revision_tracker(file_path: str) -> List[Dict]:
    """Load revision tracker from Excel or CSV."""
    if not PANDAS_SUPPORT:
        raise ImportError("pandas required. Install with: pip install pandas openpyxl")

    path = Path(file_path)

    if path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    elif path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    # Convert to list of dictionaries
    comments = df.to_dict('records')
    return comments


def group_comments_by_reviewer(comments: List[Dict]) -> Dict[str, List[Dict]]:
    """Group comments by reviewer."""
    grouped = defaultdict(list)
    for comment in comments:
        reviewer = comment.get('reviewer', 'Unknown')
        grouped[reviewer].append(comment)
    return dict(grouped)


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    if not isinstance(text, str):
        return str(text)

    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def format_comment_for_latex(comment: Dict, comment_num: int) -> str:
    """Format a single comment for LaTeX response letter."""
    original = escape_latex(comment.get('original_comment', ''))
    response = escape_latex(comment.get('response_action', ''))
    status = comment.get('status', 'Pending')

    # Only include completed responses
    if status.lower() not in ['completed', 'done', 'finished']:
        return ''

    latex = f"""
\\textbf{{Comment {comment_num}:}} {original}

\\textbf{{Response:}} {response}
"""

    return latex


def generate_latex_response_letter(comments: List[Dict], paper_title: str = "[Paper Title]",
                                    manuscript_id: str = "[Manuscript ID]",
                                    author_name: str = "[Your Name]",
                                    author_affiliation: str = "[Your Affiliation]",
                                    author_email: str = "[Your Email]") -> str:
    """Generate complete LaTeX response letter."""

    # Group comments by reviewer
    grouped_comments = group_comments_by_reviewer(comments)

    # Build the response sections
    response_sections = []

    for reviewer in sorted(grouped_comments.keys()):
        reviewer_comments = grouped_comments[reviewer]

        section = f"\\textbf{{Response to {reviewer}}}\n\\vspace{{0.5em}}\n"

        comment_num = 1
        for comment in reviewer_comments:
            formatted = format_comment_for_latex(comment, comment_num)
            if formatted:
                section += formatted
                section += "\\vspace{0.5em}\n"
                comment_num += 1

        response_sections.append(section)

    # Combine all sections
    responses_text = "\n\\vspace{1em}\n\n".join(response_sections)

    # Build complete LaTeX document
    latex_document = f"""\\documentclass[11pt]{{letter}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{setspace}}
\\usepackage{{times}}
\\usepackage{{hyperref}}

\\signature{{{author_name}\\\\{author_affiliation}\\\\{author_email}}}

\\address{{[Your Department]\\\\[Your Institution]\\\\[Your Address]}}

\\begin{{document}}

\\begin{{letter}}{{[Editor Name]\\\\[Journal Name]}}

\\opening{{Dear [Editor Name],}}

Thank you for the opportunity to revise and resubmit our manuscript entitled \\textbf{{"{paper_title}"}} (Manuscript ID: {manuscript_id}). We appreciate the thoughtful and constructive comments from the reviewers and the editor. We have carefully addressed all the suggestions and believe the manuscript has been substantially improved.

Below, we provide a detailed response to each comment. All changes in the revised manuscript are highlighted in \\textbf{{bold}} for easy identification.

\\vspace{{1em}}

{responses_text}

\\vspace{{1em}}

We believe these revisions have substantially strengthened the manuscript. We thank you and the reviewers for the valuable feedback and hope the revised manuscript meets the standards for publication in [Journal Name].

\\closing{{Sincerely,}}

\\end{{letter}}

\\end{{document}}
"""

    return latex_document


def save_latex_file(content: str, output_path: str):
    """Save LaTeX content to file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Response letter saved to {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_response_letter.py <tracker_file> --output <output.tex>")
        print("\nOptions:")
        print("  --title \"Paper Title\"")
        print("  --id \"Manuscript ID\"")
        print("  --author \"Your Name\"")
        print("  --affiliation \"Your Affiliation\"")
        print("  --email \"Your Email\"")
        print("\nExamples:")
        print("  python generate_response_letter.py revision_tracker.xlsx --output response_letter.tex")
        print("  python generate_response_letter.py tracker.csv --output response.tex --title \"My Paper\"")
        sys.exit(1)

    # Parse arguments
    tracker_file = sys.argv[1]
    output_file = None
    paper_title = "[Paper Title]"
    manuscript_id = "[Manuscript ID]"
    author_name = "[Your Name]"
    author_affiliation = "[Your Affiliation]"
    author_email = "[Your Email]"

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--title' and i + 1 < len(sys.argv):
            paper_title = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--id' and i + 1 < len(sys.argv):
            manuscript_id = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--author' and i + 1 < len(sys.argv):
            author_name = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--affiliation' and i + 1 < len(sys.argv):
            author_affiliation = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--email' and i + 1 < len(sys.argv):
            author_email = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    if not output_file:
        print("Error: --output argument required")
        sys.exit(1)

    try:
        print(f"Loading revision tracker from {tracker_file}...")
        comments = load_revision_tracker(tracker_file)

        print(f"Loaded {len(comments)} comments")

        # Count completed comments
        completed = sum(1 for c in comments if c.get('status', '').lower() in ['completed', 'done', 'finished'])
        print(f"Completed: {completed}/{len(comments)} comments")

        # Generate response letter
        print("\nGenerating LaTeX response letter...")
        latex_content = generate_latex_response_letter(
            comments,
            paper_title=paper_title,
            manuscript_id=manuscript_id,
            author_name=author_name,
            author_affiliation=author_affiliation,
            author_email=author_email
        )

        # Save to file
        save_latex_file(latex_content, output_file)

        # Print summary
        print("\nSummary:")
        grouped = group_comments_by_reviewer(comments)
        for reviewer in sorted(grouped.keys()):
            count = len(grouped[reviewer])
            completed_count = sum(1 for c in grouped[reviewer] if c.get('status', '').lower() in ['completed', 'done', 'finished'])
            print(f"  {reviewer}: {completed_count}/{count} comments addressed")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
