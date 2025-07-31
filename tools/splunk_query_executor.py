# tools/execute_splunk_query.py
from langchain_core.tools import tool
import requests
import os

SPLUNK_URL = os.getenv("SPLUNK_API_URL")  # Use environment variables for safety
TOKEN = os.getenv("SPLUNK_API_TOKEN")

@tool
def execute_splunk_query(spl_query: str) -> str:
    """Executes a given SPL query and returns raw results."""
    # headers = {
    #     "Authorization": f"Bearer {TOKEN}",
    #     "Content-Type": "application/json"
    # }
    #
    # payload = {
    #     "search": spl_query,
    #     "output_mode": "json"
    # }
    #
    # response = requests.post(f"{SPLUNK_URL}/services/search/jobs/export", headers=headers, json=payload)
    #
    # if response.status_code != 200:
    #     return f"Error: {response.status_code} - {response.text}"
    #
    # return response.text
    dummy_logs = [
        "index=trading_logs TIMESTAMP=2025-07-21T14:58:35.409283 APPLICATION=trade-engine ACTION=ERROR_EVENT EVENT_ID=EVT000004 USER_ID=U0477 SYMBOL=AMZN QTY=480 PRICE=1181.91",
        "index=trading_logs TIMESTAMP=2025-07-21T14:58:38.409283 APPLICATION=order-service ACTION=ERROR_EVENT EVENT_ID=EVT000005 USER_ID=U0196 SYMBOL=AMZN QTY=850 PRICE=504.61",
        "index=trading_logs TIMESTAMP=2025-07-21T14:58:41.409283 APPLICATION=order-service ACTION=ERROR_EVENT EVENT_ID=EVT000006 USER_ID=U0452 SYMBOL=AAPL QTY=187 PRICE=714.68",
        "index=trading_logs TIMESTAMP=2025-07-21T14:58:44.409283 APPLICATION=order-service ACTION=ERROR_EVENT EVENT_ID=EVT000007 USER_ID=U0039 SYMBOL=TSLA QTY=66 PRICE=1182.0"
    ]
    return "\n".join(dummy_logs)
