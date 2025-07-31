# tools/analyze_logs.py
from langchain_core.tools import tool
from config.config import llm

@tool
def analyze_logs(log_data: str) -> str:
    """Analyze logs and summarize what is happening across microservices, highlighting key flows, anomalies, or issues."""
    prompt = f"""
You are an expert in analyzing distributed system logs. The logs follow this structure:

    index=abc APPLICATION=<microservice name> ACTION=<action like OUTPUT_EVENT, INPUT_EVENT, EVENT_PROCESSED, etc> <Other key=value pairs> EVENT_ID=<UUID>

Meaning of key fields:
- APPLICATION: Name of the microservice emitting the log.
- ACTION: Describes the type of action or phase in the process (e.g., INPUT_EVENT means the microservice has received an event, EVENT_PROCESSED means it finished processing).
- EVENT_ID: Unique identifier for the event/message as it travels across services.

Analyze the logs below. Summarize:
1. What process or flow is taking place.
2. Which microservices are involved and in what sequence.
3. Any inconsistencies, errors, or potential anomalies.

Logs:
------------------
{log_data}
------------------

Return a clear and concise explanation and do not provide irrelevant analysis if you do not find anything. Simply reply what you have found. If possible, mention the overall flow using the EVENT_IDs to correlate steps across services.
"""

    response = llm.invoke(prompt)
    return response.content.strip()
