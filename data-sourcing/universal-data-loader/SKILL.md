---
name: universal-data-loader
description: Downloads data from publicly accessible databases (FRED, World Bank, Yahoo Finance, Kaggle, etc.) or REST APIs by generating and executing custom Python scripts. Use when the user wants to "download data" from a specific source or URL.
---

# Universal Data Loader

This skill empowers the agent to fetch data from virtually any public source by dynamically creating and running Python scripts tailored to the specific database or API.

## Workflow

### 1. Source Identification & Research
1.  **Identify the Source:** What is the target database or URL? (e.g., "World Bank GDP", "Yahoo Finance AAPL", "a JSON API at example.com/api").
2.  **Check Availability:** If the source is a known library (like `yfinance` or `pandas_datareader`), skip to step 2.
3.  **Research API/Docs:** If the source is an API or website, use the `search` tool to find:
    *   API endpoints
    *   Authentication requirements (public/key-based)
    *   Data format (JSON, CSV, XML)
    *   Python libraries that might facilitate access.

### 2. Strategy Selection
Choose the best method:
*   **Specialized Libraries:** `yfinance`, `pandas_datareader`, `fredapi`, `wbdata`.
*   **Direct HTTP Requests:** `requests` module for REST APIs.
*   **Web Scraping:** `BeautifulSoup` or `pandas.read_html` for HTML tables (use only if no API exists).

### 3. Implementation
Write a Python script (`download_data.py`) that:
1.  Imports necessary libraries.
2.  Defines the target URL/Series/Ticker.
3.  Fetches the data.
4.  Handles errors (status codes, empty data).
5.  Cleans the data (converts dates, numeric columns).
6.  Saves to a local file (CSV, Excel, or JSON).
7.  Prints a summary (head of data, shape) to stdout.

### 4. Execution & Verification
1.  Run the script using the `RunCommand` tool.
2.  Check for errors.
    *   **Missing Libraries:** Install them via `pip install ...`.
    *   **API Errors:** Check documentation or API keys.
3.  Verify the output file exists and contains data.

## Common Libraries & Snippets

### Yahoo Finance (yfinance)
```python
import yfinance as yf
# Download historical data
data = yf.download("AAPL", start="2020-01-01")
data.to_csv("aapl_data.csv")
```

### World Bank (pandas_datareader)
```python
from pandas_datareader import wb
# Download GDP for US and China
data = wb.download(indicator='NY.GDP.MKTP.CD', country=['US', 'CN'], start=2020, end=2024)
data.to_csv("wb_gdp.csv")
```

### Generic REST API
```python
import requests
import pandas as pd
# Fetch JSON data
resp = requests.get("https://api.example.com/data")
if resp.status_code == 200:
    items = resp.json().get('items', [])
    df = pd.DataFrame(items)
    df.to_csv("data.csv", index=False)
```

### Kaggle (kaggle)
*Requires user to set `KAGGLE_USERNAME` and `KAGGLE_KEY` environment variables.*
```python
import kaggle
kaggle.api.dataset_download_files('dataset-owner/dataset-name', path='.', unzip=True)
```
