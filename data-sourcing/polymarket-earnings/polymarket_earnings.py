#!/usr/bin/env python3
"""
Polymarket Earnings Calendar Scraper

Scrapes earnings calendar data from Polymarket and exports to CSV.

Usage:
    python polymarket_earnings.py [options]

Options:
    --output PATH    Output CSV file path (default: earnings_calendar.csv)
    --year YEAR      Year for the calendar (default: auto-detect from page)
    --keep-raw       Keep the raw scraped markdown file

Requirements:
    - Firecrawl CLI installed and authenticated
    - Or scraped markdown file already present at .firecrawl/earnings-page.md
"""

import re
import csv
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


def scrape_earnings_page():
    """Scrape the Polymarket earnings page using Firecrawl."""
    print("Scraping Polymarket earnings calendar...")

    # Ensure .firecrawl directory exists
    Path(".firecrawl").mkdir(exist_ok=True)

    # Run firecrawl scrape
    result = subprocess.run(
        ["firecrawl", "scrape", "https://polymarket.com/earnings",
         "-o", ".firecrawl/earnings-page.md"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error scraping: {result.stderr}")
        return False

    print("Scrape complete.")
    return True


def parse_earnings_data(content: str, year: int = None) -> list:
    """
    Parse the scraped markdown content and extract earnings data.

    Args:
        content: The markdown content from the scraped page
        year: The year for the calendar (auto-detected if not provided)

    Returns:
        List of dictionaries with earnings data
    """
    earnings_data = []
    lines = content.split("\n")
    current_date = None
    current_timing = None

    # Auto-detect year from page header
    if year is None:
        for line in lines:
            year_match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s*(\d{4})", line)
            if year_match:
                year = int(year_match.group(2))
                break
        if year is None:
            year = datetime.now().year

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check for day headers like "Monday30", "Tuesday31", etc.
        day_match = re.match(r"^(Monday|Tuesday|Wednesday|Thursday|Friday)(\d+)$", line)
        if day_match:
            day_name = day_match.group(1)
            day_num = int(day_match.group(2))

            # Determine month based on calendar context
            if day_num == 1 and day_name == "Friday":
                # May 1 (end of April earnings season)
                month = "05"
            elif day_num >= 30 and not any(e["Date"].startswith(f"{year}-04") for e in earnings_data):
                # March 30-31 (first week of Q1 earnings)
                month = "03"
            else:
                # April (main earnings season)
                month = "04"

            current_date = f"{year}-{month}-{str(day_num).zfill(2)}"
            i += 1
            continue

        # Check for timing headers
        if line == "Pre Market":
            current_timing = "Pre Market"
            i += 1
            continue
        elif line == "Post Market":
            current_timing = "Post Market"
            i += 1
            continue

        # Check for ticker entries
        ticker_match = re.match(r"^#### ([A-Z]+)$", line)
        if ticker_match and current_timing and current_date:
            ticker = ticker_match.group(1)
            eps = None
            beat_prob = None

            j = i + 1
            while j < len(lines) and j < i + 5:
                next_line = lines[j].strip()
                if not next_line:
                    j += 1
                    continue

                # Parse EPS: "$0.61EPS" or "-$0.59EPS" or "$0.00EPS"
                eps_match = re.match(r"^\$?([\d.]+)EPS$", next_line)
                neg_eps_match = re.match(r"^-\$?([\d.]+)EPS$", next_line)

                if eps_match:
                    eps = "$" + eps_match.group(1)
                    j += 1
                    continue
                elif neg_eps_match:
                    eps = "-$" + neg_eps_match.group(1)
                    j += 1
                    continue

                # Parse beat probability: "100%" or "0%" etc.
                prob_match = re.match(r"^(\d+)%$", next_line)
                if prob_match and eps:
                    beat_prob = prob_match.group(1) + "%"
                    break

                # Stop if we hit another ticker or timing
                if next_line.startswith("#### ") or next_line in ["Pre Market", "Post Market"]:
                    break

                j += 1

            if eps and beat_prob:
                earnings_data.append({
                    "Date": current_date,
                    "Timing": current_timing,
                    "Ticker": ticker,
                    "EPS Estimate": eps,
                    "Beat Probability": beat_prob
                })

            i = j
            continue

        i += 1

    return earnings_data


def export_to_csv(earnings_data: list, output_path: str):
    """Export earnings data to CSV file."""
    # Sort by date and timing
    earnings_data.sort(
        key=lambda x: (x["Date"], 0 if x["Timing"] == "Pre Market" else 1, x["Ticker"])
    )

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Date", "Timing", "Ticker", "EPS Estimate", "Beat Probability"]
        )
        writer.writeheader()
        writer.writerows(earnings_data)

    print(f"Exported {len(earnings_data)} earnings entries to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape Polymarket earnings calendar and export to CSV"
    )
    parser.add_argument(
        "--output", "-o",
        default="earnings_calendar.csv",
        help="Output CSV file path (default: earnings_calendar.csv)"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Year for the calendar (default: auto-detect from page)"
    )
    parser.add_argument(
        "--keep-raw",
        action="store_true",
        help="Keep the raw scraped markdown file"
    )
    parser.add_argument(
        "--no-scrape",
        action="store_true",
        help="Use existing scraped file instead of re-scraping"
    )

    args = parser.parse_args()

    # Check if we need to scrape
    raw_file = Path(".firecrawl/earnings-page.md")

    if not args.no_scrape or not raw_file.exists():
        if not scrape_earnings_page():
            print("Failed to scrape earnings page. Check Firecrawl installation.")
            return 1

    # Read and parse the content
    print("Parsing earnings data...")
    content = raw_file.read_text(encoding="utf-8")
    earnings_data = parse_earnings_data(content, args.year)

    if not earnings_data:
        print("No earnings data found in scraped content.")
        return 1

    # Export to CSV
    export_to_csv(earnings_data, args.output)

    # Clean up if requested
    if not args.keep_raw and raw_file.exists():
        raw_file.unlink()

    # Print summary
    from collections import Counter
    date_counts = Counter(e["Date"] for e in earnings_data)
    print("\nEntries by date:")
    for date in sorted(date_counts.keys())[:5]:
        print(f"  {date}: {date_counts[date]} entries")
    if len(date_counts) > 5:
        print(f"  ... and {len(date_counts) - 5} more dates")

    return 0


if __name__ == "__main__":
    exit(main())
