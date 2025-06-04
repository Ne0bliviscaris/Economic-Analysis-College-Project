import os

import requests
from dotenv import load_dotenv

load_dotenv()

bdl_api_key = os.getenv("BDL_API_KEY")


def build_bdl_query_url(table_ids, region_ids, years):
    """Builds BDL API query URL."""
    base_url = "https://bdl.stat.gov.pl/api/v1/data/by-unit"
    tables = ",".join(table_ids)
    regions = ",".join(region_ids)
    return f"{base_url}?unit-ids={regions}&var-ids={tables}&year={years}"


header = f"""
GET https://bdl.stat.gov.pl/api/v1/data/by-variable/3643?format=json&year=2000&year=2010 HTTP/1.1
Host: hostname
X-ClientId: {bdl_api_key}
"""

main_api = "https://bdl.stat.gov.pl/"
endpoint = "/data/by-variable/3643?format=xml&year=2000&year=2010"
response = requests.get(
    f"{main_api}/api/v1/subjects?parent-id=K4&page-size=100",
    headers={"X-ClientId": bdl_api_key},
)
if response.status_code == 200:
    print("Response:")
    print(response.text)
