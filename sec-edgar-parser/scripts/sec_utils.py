import requests
import pandas as pd
import json
import time

# SEC requires a proper User-Agent header
HEADERS = {
    "User-Agent": "MyResearchProject contact@example.com",
    "Accept-Encoding": "gzip, deflate"
}

def get_company_tickers():
    """Fetches the official SEC company tickers JSON file."""
    url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    
    # Convert dict of dicts to list of dicts
    tickers_list = []
    for key, value in data.items():
        tickers_list.append(value)
        
    return pd.DataFrame(tickers_list)

def get_cik(ticker):
    """Finds the CIK for a given ticker symbol."""
    df = get_company_tickers()
    ticker = ticker.upper()
    result = df[df['ticker'] == ticker]
    if not result.empty:
        # CIK must be 10 digits (padded with leading zeros) for URLs
        cik = result.iloc[0]['cik_str']
        return f"{cik:010d}"
    else:
        raise ValueError(f"Ticker {ticker} not found.")

def get_filings(cik, form_type=None, limit=10):
    """
    Fetches recent filings for a given CIK.
    Returns a DataFrame with accessionNumber, filingDate, form, and primaryDocument.
    """
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    
    filings = data['filings']['recent']
    df = pd.DataFrame(filings)
    
    if form_type:
        df = df[df['form'] == form_type]
    
    # Construct the document URL
    # https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number_no_hyphens}/{primary_document}
    base_url = "https://www.sec.gov/Archives/edgar/data"
    cik_int = int(cik) # URL uses unpadded CIK
    
    def make_url(row):
        acc_no_hyphen = row['accessionNumber'].replace('-', '')
        return f"{base_url}/{cik_int}/{acc_no_hyphen}/{row['primaryDocument']}"
    
    df['url'] = df.apply(make_url, axis=1)
    
    return df.head(limit)

def download_filing(url):
    """Downloads the content of a filing URL."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    # Example usage
    try:
        ticker = "AAPL"
        print(f"Fetching CIK for {ticker}...")
        cik = get_cik(ticker)
        print(f"CIK: {cik}")
        
        print(f"Fetching recent 10-K filings...")
        filings = get_filings(cik, form_type="10-K", limit=3)
        print(filings[['filingDate', 'form', 'accessionNumber', 'url']])
        
        if not filings.empty:
            latest_url = filings.iloc[0]['url']
            print(f"Downloading latest 10-K from {latest_url}...")
            content = download_filing(latest_url)
            print(f"Downloaded {len(content)} characters.")
            
    except Exception as e:
        print(f"Error: {e}")
