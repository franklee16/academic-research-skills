#!/usr/bin/env python3
"""
Synthesize multiple reviewer reports into a consensus assessment.

This script:
1. Reads individual reviewer markdown reports
2. Extracts dimension scores from each reviewer
3. Identifies disagreements (score difference > 1)
4. Calculates weighted consensus scores
5. Outputs a summary for the discussion phase

Usage:
    python synthesize_reviews.py <review_dir> [--output consensus_summary.json]

Example:
    python synthesize_reviews.py quality_reports/reviews/2026-04-18
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Dimension weights for overall score calculation
DIMENSION_WEIGHTS = {
    "identification": 0.30,
    "data_quality": 0.20,
    "robustness": 0.20,
    "contribution": 0.20,
    "clarity": 0.10,
}

# Dimension name variations for parsing
DIMENSION_ALIASES = {
    "identification": ["identification", "identification strategy", "causal identification"],
    "data_quality": ["data quality", "data", "data construction"],
    "robustness": ["robustness", "robustness checks", "sensitivity"],
    "contribution": ["contribution", "novelty", "contribution to literature"],
    "clarity": ["clarity", "writing", "exposition"],
}


def parse_score_from_text(text: str, dimension: str) -> Optional[Tuple[int, str]]:
    """
    Parse a dimension score from reviewer text.

    Returns tuple of (score, confidence) or None if not found.
    """
    # Build regex pattern for dimension and score
    aliases = DIMENSION_ALIASES.get(dimension, [dimension])
    pattern = r"(?i)(?:{}).*?[:\-]?\s*(\d)(?:\s*/\s*5)?.*?(?:confidence[:\s]*(high|medium|low))?".format(
        "|".join(re.escape(a) for a in aliases)
    )

    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        score = int(match.group(1))
        confidence = (match.group(2) or "medium").lower()
        return (score, confidence)
    return None


def parse_reviewer_report(filepath: Path) -> Dict:
    """
    Parse a single reviewer report file.

    Returns dict with:
    - reviewer_type: str
    - scores: Dict[str, Tuple[int, str]]  # dimension -> (score, confidence)
    - major_comments: List[str]
    - minor_comments: List[str]
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract reviewer type from filename
    filename = filepath.stem
    if 'econometrician' in filename.lower():
        reviewer_type = 'econometrician'
    elif 'domain' in filename.lower() or 'expert' in filename.lower():
        reviewer_type = 'domain_expert'
    elif 'methodologist' in filename.lower():
        reviewer_type = 'methodologist'
    else:
        reviewer_type = 'unknown'

    # Parse scores
    scores = {}
    for dimension in DIMENSION_WEIGHTS.keys():
        result = parse_score_from_text(content, dimension)
        if result:
            scores[dimension] = result

    # Parse major comments
    major_pattern = r"##\s*Major[^#\n]*\n([\s\S]*?)(?=##|$)"
    major_match = re.search(major_pattern, content, re.IGNORECASE)
    major_comments = []
    if major_match:
        major_text = major_match.group(1)
        # Extract numbered items
        major_comments = re.findall(r"^\d+\.\s*(.+?)(?=\n\d+\.|\n\n|$)", major_text, re.MULTILINE | re.DOTALL)

    # Parse minor comments
    minor_pattern = r"##\s*Minor[^#\n]*\n([\s\S]*?)(?=##|$)"
    minor_match = re.search(minor_pattern, content, re.IGNORECASE)
    minor_comments = []
    if minor_match:
        minor_text = minor_match.group(1)
        minor_comments = re.findall(r"^\d+\.\s*(.+?)(?=\n\d+\.|\n\n|$)", minor_text, re.MULTILINE | re.DOTALL)

    return {
        "reviewer_type": reviewer_type,
        "scores": scores,
        "major_comments": major_comments,
        "minor_comments": minor_comments,
        "filepath": str(filepath),
    }


def identify_disagreements(reviews: List[Dict]) -> List[Dict]:
    """
    Identify dimensions where reviewers disagree (score diff > 1).

    Returns list of disagreement dicts with:
    - dimension: str
    - scores: List[Tuple[reviewer_type, score]]
    - difference: int
    """
    disagreements = []

    for dimension in DIMENSION_WEIGHTS.keys():
        dimension_scores = []
        for review in reviews:
            if dimension in review["scores"]:
                score, _ = review["scores"][dimension]
                dimension_scores.append((review["reviewer_type"], score))

        if len(dimension_scores) >= 2:
            scores = [s for _, s in dimension_scores]
            max_diff = max(scores) - min(scores)
            if max_diff > 1:
                disagreements.append({
                    "dimension": dimension,
                    "scores": dimension_scores,
                    "difference": max_diff,
                })

    return disagreements


def calculate_consensus_scores(reviews: List[Dict]) -> Dict[str, Dict]:
    """
    Calculate consensus scores across reviewers.

    Returns dict mapping dimension to:
    - score: float (average)
    - confidence: str (lowest confidence level)
    - range: Tuple[int, int] (min, max)
    """
    consensus = {}

    for dimension in DIMENSION_WEIGHTS.keys():
        dimension_data = []
        for review in reviews:
            if dimension in review["scores"]:
                score, confidence = review["scores"][dimension]
                dimension_data.append((score, confidence))

        if dimension_data:
            scores = [s for s, _ in dimension_data]
            confidences = [c for _, c in dimension_data]

            # Determine consensus confidence (lowest)
            confidence_order = {"high": 3, "medium": 2, "low": 1}
            lowest_confidence = min(confidences, key=lambda c: confidence_order.get(c, 2))

            consensus[dimension] = {
                "score": round(sum(scores) / len(scores), 2),
                "confidence": lowest_confidence,
                "range": (min(scores), max(scores)),
            }

    return consensus


def calculate_overall_score(consensus: Dict[str, Dict]) -> int:
    """
    Calculate overall weighted score on 100-point scale.
    """
    weighted_sum = 0.0
    total_weight = 0.0

    for dimension, weight in DIMENSION_WEIGHTS.items():
        if dimension in consensus:
            weighted_sum += consensus[dimension]["score"] * weight
            total_weight += weight

    if total_weight > 0:
        # Convert to 100-point scale (5-point scale * 20)
        return int((weighted_sum / total_weight) * 20)
    return 0


def get_recommendation(overall_score: int) -> str:
    """
    Get recommendation based on overall score.
    """
    if overall_score >= 95:
        return "Accept / Ready for submission"
    elif overall_score >= 90:
        return "Minor revision recommended"
    elif overall_score >= 80:
        return "Major revision recommended"
    elif overall_score >= 70:
        return "Revise and resubmit"
    else:
        return "Reject / Not ready for submission"


def synthesize_reviews(review_dir: Path) -> Dict:
    """
    Main synthesis function.

    Returns complete synthesis dict.
    """
    # Find reviewer report files
    reviewer_files = list(review_dir.glob("*_reviewer-*.md"))

    if not reviewer_files:
        raise ValueError(f"No reviewer reports found in {review_dir}")

    # Parse all reviews
    reviews = [parse_reviewer_report(f) for f in reviewer_files]

    # Calculate consensus
    consensus = calculate_consensus_scores(reviews)

    # Identify disagreements
    disagreements = identify_disagreements(reviews)

    # Calculate overall score
    overall_score = calculate_overall_score(consensus)

    # Aggregate major comments
    all_major_comments = []
    for review in reviews:
        for i, comment in enumerate(review["major_comments"], 1):
            all_major_comments.append({
                "reviewer": review["reviewer_type"],
                "number": i,
                "comment": comment.strip() if isinstance(comment, str) else str(comment).strip(),
            })

    # Build synthesis
    synthesis = {
        "timestamp": datetime.now().isoformat(),
        "review_dir": str(review_dir),
        "reviewers": [r["reviewer_type"] for r in reviews],
        "dimension_scores": consensus,
        "overall_score": overall_score,
        "recommendation": get_recommendation(overall_score),
        "disagreements": disagreements,
        "major_comments": all_major_comments,
        "needs_discussion": len(disagreements) > 0,
    }

    return synthesis


def format_discussion_prompt(synthesis: Dict) -> str:
    """
    Format a discussion prompt for reviewers.
    """
    prompt = "# Discussion Phase\n\n"

    if synthesis["disagreements"]:
        prompt += "## Disagreements to Resolve\n\n"
        for d in synthesis["disagreements"]:
            prompt += f"### {d['dimension'].replace('_', ' ').title()}\n\n"
            prompt += "Reviewer scores:\n"
            for reviewer, score in d["scores"]:
                prompt += f"- **{reviewer}**: {score}/5\n"
            prompt += f"\nDifference: {d['difference']} points (threshold: >1)\n\n"
            prompt += "**Discussion question:** What evidence would resolve this disagreement?\n\n"
    else:
        prompt += "No significant disagreements detected. Proceed to consensus report.\n"

    prompt += f"\n## Current Assessment\n\n"
    prompt += f"**Overall Score:** {synthesis['overall_score']}/100\n"
    prompt += f"**Recommendation:** {synthesis['recommendation']}\n\n"

    prompt += "## Consensus Scores by Dimension\n\n"
    prompt += "| Dimension | Score | Confidence | Range |\n"
    prompt += "|-----------|-------|------------|-------|\n"
    for dim, data in synthesis["dimension_scores"].items():
        prompt += f"| {dim.replace('_', ' ').title()} | {data['score']}/5 | {data['confidence'].title()} | {data['range'][0]}-{data['range'][1]} |\n"

    return prompt


def main():
    parser = argparse.ArgumentParser(
        description="Synthesize multiple reviewer reports into consensus"
    )
    parser.add_argument(
        "review_dir",
        type=Path,
        help="Directory containing reviewer report files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output JSON file (default: review_dir/consensus_summary.json)",
    )
    parser.add_argument(
        "--discussion",
        action="store_true",
        help="Also output discussion prompt",
    )

    args = parser.parse_args()

    if not args.review_dir.is_dir():
        print(f"Error: {args.review_dir} is not a directory")
        return 1

    # Run synthesis
    synthesis = synthesize_reviews(args.review_dir)

    # Determine output path
    output_path = args.output or (args.review_dir / "consensus_summary.json")

    # Write JSON output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(synthesis, f, indent=2)

    print(f"Synthesis complete: {output_path}")
    print(f"Overall score: {synthesis['overall_score']}/100")
    print(f"Recommendation: {synthesis['recommendation']}")

    if synthesis["disagreements"]:
        print(f"\nDisagreements found: {len(synthesis['disagreements'])}")
        for d in synthesis["disagreements"]:
            print(f"  - {d['dimension']}: {d['difference']} point difference")

    if args.discussion:
        discussion_path = args.review_dir / "discussion_prompt.md"
        with open(discussion_path, 'w', encoding='utf-8') as f:
            f.write(format_discussion_prompt(synthesis))
        print(f"\nDiscussion prompt: {discussion_path}")

    return 0


if __name__ == "__main__":
    exit(main())
