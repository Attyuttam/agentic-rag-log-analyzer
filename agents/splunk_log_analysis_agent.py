# agent_splunk_assistant.py
from langchain import hub
from langchain.agents import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI

# Custom tool wrappers (to be implemented)
from tools.splunk_query_generator import generate_splunk_query
from tools.splunk_query_executor import execute_splunk_query
from tools.splunk_log_analyzer import analyze_logs

def log_analysis(user_input:str) -> str:
    # Step 1: Define the LLM
    llm = ChatGoogleGenerativeAI(temperature=0)

    # Step 2: Define Tools
    tools: list[Tool] = [
        Tool.from_function(
            func=generate_splunk_query,
            name="SplunkQueryGenerator",
            description="Generate a Splunk query from a natural language prompt"
        ),
        Tool.from_function(
            func=execute_splunk_query,
            name="SplunkQueryExecutor",
            description="Execute a Splunk search query and return matching logs"
        ),
        Tool.from_function(
            func=analyze_logs,
            name="SplunkLogAnalyzer",
            description="Analyze the logs and answer the user’s question"
        ),
    ]

    # Step 3: Create ReAct agent
    react_prompt = hub.pull("hwchase17/react")
    react_agent: Runnable = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

    # Step 4: Wrap it in an AgentExecutor
    agent_executor: AgentExecutor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)

    # Step 5: Use this function to run the assistant
    result = agent_executor.invoke({"input": user_input})

    return result["output"]
