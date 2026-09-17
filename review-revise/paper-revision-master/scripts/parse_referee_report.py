#!/usr/bin/env python3
"""
Parse Referee Report Script

Extracts structured comments from referee reports (PDF or text format).
Outputs JSON or CSV for import into revision tracker.

Usage:
    python parse_referee_report.py referee_report.pdf --output comments.json
    python parse_referee_report.py referee_report.txt --output comments.csv
    python parse_referee_report.py referee_report.pdf --format csv --output comments.csv

Requirements:
    pip install PyPDF2 pdfplumber  # For PDF parsing
"""

import sys
import json
import csv
import re
from pathlib import Path
from typing import List, Dict, Any

try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: pdfplumber not installed. PDF parsing unavailable.")
    print("Install with: pip install pdfplumber")


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from PDF file."""
    if not PDF_SUPPORT:
        raise ImportError("pdfplumber required for PDF parsing. Install with: pip install pdfplumber")

    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF or text file."""
    path = Path(file_path)

    if path.suffix.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def identify_reviewer_sections(text: str) -> Dict[str, str]:
    """
    Identify and separate different reviewer sections.
    Returns dict mapping reviewer names to their text.
    """
    sections = {}

    # Common patterns for reviewer sections
    patterns = [
        r'(Reviewer\s*\d+|Referee\s*\d+|Review\s*\d+).*?(?=(?:Reviewer\s*\d+|Referee\s*\d+|Review\s*\d+|Editor|Editor\'s|Recommendation|$))',
        r'(Editor|Editor\'s\s+Comments).*?(?=(?:Reviewer|Referee|Review|$))'
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            section_text = match.group(0)
            # Extract reviewer name/number
            name_match = re.match(r'(Reviewer\s*\d+|Referee\s*\d+|Review\s*\d+|Editor)', section_text, re.IGNORECASE)
            if name_match:
                reviewer_name = name_match.group(1).title()
                sections[reviewer_name] = section_text.strip()

    # If no sections found, treat entire text as "Reviewer 1"
    if not sections:
        sections['Reviewer 1'] = text

    return sections


def extract_comments_from_text(text: str) -> List[str]:
    """
    Extract individual comments from a reviewer's text.
    Attempts to identify numbered or bulleted comments.
    """
    comments = []

    # Try numbered pattern first (1., 2., 3., etc.)
    numbered_pattern = r'(?:^|\n)\s*(\d+[\.\)]\s+.+?)(?=(?:\n\s*\d+[\.\)]|$))'
    numbered_matches = re.findall(numbered_pattern, text, re.DOTALL)

    if numbered_matches:
        comments = [match.strip() for match in numbered_matches]
    else:
        # Try bullet points (-, *, •)
        bullet_pattern = r'(?:^|\n)\s*[-*•]\s+(.+?)(?=(?:\n\s*[-*•]|$))'
        bullet_matches = re.findall(bullet_pattern, text, re.DOTALL)

        if bullet_matches:
            comments = [match.strip() for match in bullet_matches]
        else:
            # If no clear structure, treat each paragraph as a comment
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 50]
            comments = paragraphs if paragraphs else [text.strip()]

    return comments


def parse_referee_report(file_path: str) -> List[Dict[str, Any]]:
    """
    Main parsing function.
    Returns list of comment dictionaries.
    """
    # Extract text
    text = extract_text_from_file(file_path)

    # Identify reviewer sections
    reviewer_sections = identify_reviewer_sections(text)

    # Extract comments from each section
    all_comments = []
    comment_id = 1

    for reviewer, section_text in reviewer_sections.items():
        comments = extract_comments_from_text(section_text)

        for comment in comments:
            all_comments.append({
                'reviewer': reviewer,
                'comment_id': comment_id,
                'original_comment': comment,
                'paraphrased_suggestion': '',  # To be filled by user
                'section': '',  # To be filled by user
                'classification': '',  # To be filled by user
                'response_action': '',  # To be filled by user
                'status': 'Pending',
                'notes': ''
            })
            comment_id += 1

    return all_comments


def save_as_json(comments: List[Dict], output_path: str):
    """Save comments to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(comments)} comments to {output_path}")


def save_as_csv(comments: List[Dict], output_path: str):
    """Save comments to CSV file."""
    if not comments:
        print("No comments to save")
        return

    fieldnames = list(comments[0].keys())

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comments)

    print(f"Saved {len(comments)} comments to {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python parse_referee_report.py <input_file> --output <output_file>")
        print("\nOptions:")
        print("  --format json   Output as JSON (default: auto-detect from file extension)")
        print("  --format csv    Output as CSV")
        print("\nExamples:")
        print("  python parse_referee_report.py referee_report.pdf --output comments.json")
        print("  python parse_referee_report.py referee_report.txt --output comments.csv")
        print("  python parse_referee_report.py report.pdf --format csv --output comments.csv")
        sys.exit(1)

    # Parse arguments
    input_file = sys.argv[1]
    output_file = None
    output_format = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--format' and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1].lower()
            i += 2
        else:
            i += 1

    if not output_file:
        print("Error: --output argument required")
        sys.exit(1)

    # Determine output format
    if not output_format:
        output_format = 'json' if output_file.endswith('.json') else 'csv'

    # Parse referee report
    try:
        print(f"Parsing {input_file}...")
        comments = parse_referee_report(input_file)

        if not comments:
            print("Warning: No comments extracted")
        else:
            print(f"Extracted {len(comments)} comments")

            # Save results
            if output_format == 'json':
                save_as_json(comments, output_file)
            else:
                save_as_csv(comments, output_file)

            # Print summary
            print("\nSummary by reviewer:")
            reviewers = {}
            for comment in comments:
                reviewer = comment['reviewer']
                reviewers[reviewer] = reviewers.get(reviewer, 0) + 1

            for reviewer, count in reviewers.items():
                print(f"  {reviewer}: {count} comments")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
