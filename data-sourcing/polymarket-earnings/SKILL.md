---
name: polymarket-earnings
description: |
  Scrape the Polymarket earnings calendar and export to CSV.
  Extracts earnings announcement date, timing (Pre/Post Market),
  ticker symbol, EPS estimate, and beat probability.
---

# Polymarket Earnings Calendar Scraper

Scrapes earnings calendar data from Polymarket and exports to a well-formatted CSV file.

## When to use

- User needs earnings calendar data from Polymarket
- User wants to analyze earnings beat probabilities
- User needs upcoming earnings dates and estimates

## Usage

```
/polymarket-earnings
```

Or with a specific output path:

```
/polymarket-earnings --output path/to/output.csv
```

## What it does

1. Scrapes the Polymarket earnings calendar page
2. Parses all earnings entries including:
   - **Date**: Earnings announcement date (YYYY-MM-DD)
   - **Timing**: Pre Market or Post Market
   - **Ticker**: Stock ticker symbol
   - **EPS Estimate**: Expected EPS value
   - **Beat Probability**: Market-implied probability of beating estimates
3. Exports data to a CSV file

## Output

A CSV file with columns:
- `Date` - Earnings date (YYYY-MM-DD format)
- `Timing` - Pre Market or Post Market
- `Ticker` - Stock symbol
- `EPS Estimate` - Expected EPS
- `Beat Probability` - Probability of beating estimates

## Prerequisites

- Firecrawl CLI installed and authenticated
- Or use Tavily as fallback for web scraping

## Example output

```csv
Date,Timing,Ticker,EPS Estimate,Beat Probability
2026-04-22,Post Market,TSLA,$0.39,20%
2026-04-29,Post Market,GOOGL,$2.66,96%
2026-04-29,Post Market,META,$6.62,91%
2026-04-30,Post Market,AAPL,$1.94,87%
```

## Instructions for Claude

When this skill is invoked:

1. **Scrape the earnings page**:
   ```bash
   mkdir -p .firecrawl
   firecrawl scrape "https://polymarket.com/earnings" -o .firecrawl/earnings-page.md
   ```

2. **Read the scraped content** and parse it using the Python script below.

3. **Create the parsing script** (save as `parse_earnings.py`):

```python
#!/usr/bin/env python3
"""Parse Polymarket earnings calendar and export to CSV."""

import re
import csv
from pathlib import Path

# Read the scraped markdown file
content = Path(".firecrawl/earnings-page.md").read_text(encoding="utf-8")

# Parse the data
earnings_data = []
lines = content.split("\n")
current_date = None
current_timing = None

i = 0
while i < len(lines):
    line = lines[i].strip()

    # Check for day headers like "Monday30", "Tuesday31", etc.
    day_match = re.match(r"^(Monday|Tuesday|Wednesday|Thursday|Friday)(\d+)$", line)
    if day_match:
        day_num = int(day_match.group(2))

        # Determine month based on calendar context
        if day_num == 1 and day_match.group(1) == "Friday":
            month = "05"  # May 1
        elif day_num >= 30 and not any(e["Date"].startswith("2026-04") for e in earnings_data):
            month = "03"  # March 30-31 (first week)
        else:
            month = "04"  # April

        current_date = f"2026-{month}-{str(day_num).zfill(2)}"
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

            prob_match = re.match(r"^(\d+)%$", next_line)
            if prob_match and eps:
                beat_prob = prob_match.group(1) + "%"
                break

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

# Sort by date and timing
earnings_data.sort(key=lambda x: (x["Date"], 0 if x["Timing"] == "Pre Market" else 1, x["Ticker"]))

# Write to CSV
output_path = "earnings_calendar.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Date", "Timing", "Ticker", "EPS Estimate", "Beat Probability"])
    writer.writeheader()
    writer.writerows(earnings_data)

print(f"Exported {len(earnings_data)} earnings entries to {output_path}")
```

4. **Run the parser**:
   ```bash
   python parse_earnings.py
   ```

5. **Clean up** and present results to user.

## Notes

- The year is determined from the page header (e.g., "April 2026")
- Dates at the end of March (30-31) and beginning of April (1-3) require careful month assignment
- Negative EPS estimates are formatted as `-$X.XX`
- Beat probability is the market-implied probability from Polymarket prediction markets
