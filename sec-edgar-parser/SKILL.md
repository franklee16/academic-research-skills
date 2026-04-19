---
name: sec-edgar-parser
description: Skill for accessing, downloading, and parsing financial filings from the SEC EDGAR database. Helps users retrieve 10-K, 10-Q, 8-K, and other forms using the SEC's JSON API.
---

# SEC EDGAR Parser

This skill enables the agent to interact with the SEC's EDGAR system to retrieve corporate filings and extract financial data.

## Workflow

### 1. Identify Company & Filing
*   **Find CIK:** Use the company ticker (e.g., AAPL, TSLA) to find the Central Index Key (CIK). The SEC maps tickers to CIKs via a public JSON file (`company_tickers.json`).
*   **Select Filing Type:** Determine which form is needed (e.g., `10-K` for annual reports, `10-Q` for quarterly, `8-K` for current events).

### 2. Fetch Filing Metadata
*   Use the SEC's submission history API: `https://data.sec.gov/submissions/CIK{cik_padded}.json`
*   This JSON contains a list of all recent filings with their accession numbers, filing dates, and form types.

### 3. Locate & Download Document
*   Construct the URL for the specific filing document. The format typically involves the CIK (without leading zeros) and the Accession Number (with hyphens removed).
*   **HTML URL Pattern:** `https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_document}`
*   **Interactive Data (XBRL):** Often available as XML or JSON.

### 4. Parse Content
*   **Text Extraction:** Use `BeautifulSoup` to strip HTML tags and extract sections (e.g., "Item 1A. Risk Factors", "Item 7. MD&A").
*   **Table Extraction:** Use `pd.read_html()` to convert HTML tables into Pandas DataFrames.

## Key Requirements
*   **User-Agent:** The SEC requires a valid User-Agent header in the format `Sample Company Name AdminContact@sample.com`. Requests without this will be blocked.
*   **Rate Limiting:** The SEC limits requests to ~10 per second. Scripts should include slight delays if making many requests.

## Bundled Scripts

### `scripts/sec_utils.py`
A utility script to:
1.  Get CIK from Ticker.
2.  Get recent filings list for a company.
3.  Download a specific filing's text.

## Example Usage

### Get Recent 10-K Filings
```python
from scripts.sec_utils import get_cik, get_filings

cik = get_cik("AAPL")
filings = get_filings(cik, form_type="10-K")
print(filings.head())
```

### Download a Filing
```python
from scripts.sec_utils import download_filing
# Use the URL from the filings dataframe
text = download_filing(filings.iloc[0]['url'])
```
