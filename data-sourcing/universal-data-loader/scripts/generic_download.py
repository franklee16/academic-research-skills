import pandas as pd
import requests
import json
import os
import sys

def download_generic(url, output_path="data.csv"):
    """
    Generic function to download JSON data from a URL and save it as CSV.
    This is a template and may need modification based on the specific API structure.
    """
    print(f"Downloading data from {url}...", flush=True)
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Try to parse JSON
        data = response.json()
        
        # Check if data is a list of dicts or wrapped in a key
        if isinstance(data, dict):
            # Look for common keys that might hold the list of items
            for key in ['data', 'items', 'results', 'value']:
                if key in data and isinstance(data[key], list):
                    data = data[key]
                    break
        
        if isinstance(data, list):
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
            print(f"Data saved to {output_path}", flush=True)
            print(df.head(), flush=True)
        else:
            print("Could not automatically convert JSON to DataFrame. Structure might be complex.", flush=True)
            # Save raw JSON
            with open("data.json", "w") as f:
                json.dump(data, f, indent=2)
            print("Saved raw JSON to data.json", flush=True)

    except Exception as e:
        print(f"Error downloading data: {e}", flush=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        download_generic(url)
    else:
        print("Usage: python generic_download.py <url>")
