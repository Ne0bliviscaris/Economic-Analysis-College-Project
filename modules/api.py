import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
bdl_api_key = os.getenv("BDL_API_KEY")


def get_variable_data(variable_id, page_size=100):
    """Return all results for a variable from BDL API as a DataFrame."""
    all_results = []
    page_nr = 0
    while True:
        url = f"https://bdl.stat.gov.pl/api/v1/data/by-variable/{variable_id}?format=json&page={page_nr}&page-size={page_size}"
        headers = {"X-ClientId": bdl_api_key}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        data = response.json()
        for entry in data.get("results", []):
            region_id = entry.get("id")
            region_name = entry.get("name")
            for value in entry.get("values", []):
                row = {"region_id": region_id, "region_name": region_name, **value}
                all_results.append(row)
        if len(all_results) >= data.get("totalRecords", 0):
            break
        page_nr += 1
    return pd.DataFrame(all_results) if all_results else None


def to_csv(data, filename):
    """Save list of dicts to CSV file."""
    df = pd.DataFrame(data)
    file_path = f"data\\{filename}.csv"
    df.to_csv(file_path, index=False, sep=";", encoding="utf-8")


if __name__ == "__main__":
    variable_id = 1615113  # Example variable ID
    data = get_variable_data(variable_id)
    if not data.empty:
        print(f"Retrieved {len(data)} records for variable ID {variable_id}.")
        to_csv(data, variable_id)
    else:
        print("No data retrieved or an error occurred.")
