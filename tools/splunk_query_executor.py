# tools/execute_splunk_query.py
from langchain_core.tools import tool
import requests
import os

SPLUNK_URL = os.getenv("SPLUNK_API_URL")  # Use environment variables for safety
TOKEN = os.getenv("SPLUNK_API_TOKEN")

@tool
def execute_splunk_query(spl_query: str) -> str:
    """Executes a given SPL query and returns raw results."""
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "search": spl_query,
        "output_mode": "json"
    }

    response = requests.post(f"{SPLUNK_URL}/services/search/jobs/export", headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    return response.text
