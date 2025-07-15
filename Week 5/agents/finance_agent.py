from langgraph.prebuilt import create_react_agent
from config import get_azure_model
from tools.read_file import create_read_file_tool
from tools.web_search import create_finance_web_search_tool
from utils.handoffs import create_finance_agent_handoffs
from prompts import FINANCE_AGENT_PROMPT


def create_finance_agent():
    """
    Create the Finance specialist agent that handles financial support queries.

    The Finance agent has access to internal finance documentation and web search
    capabilities to provide comprehensive financial support and guidance.
    """

    model = get_azure_model()

    read_finance_docs = create_read_file_tool(
        "data/finance_docs", "read_finance_docs")
    web_search = create_finance_web_search_tool()
    handoff_tools = create_finance_agent_handoffs()

    tools = [read_finance_docs, web_search] + handoff_tools

    finance_agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=FINANCE_AGENT_PROMPT,
        name="finance_agent"
    )

    return finance_agent
