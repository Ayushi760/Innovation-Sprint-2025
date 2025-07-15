from langgraph.prebuilt import create_react_agent
from config import get_azure_model
from tools.read_file import create_read_file_tool
from tools.web_search import create_it_web_search_tool
from utils.handoffs import create_it_agent_handoffs
from prompts import IT_AGENT_PROMPT


def create_it_agent():
    """
    Create the IT specialist agent that handles technical support queries.

    The IT agent has access to internal IT documentation and web search
    capabilities to provide comprehensive technical support.
    """

    model = get_azure_model()

    read_it_docs = create_read_file_tool("data/it_docs", "read_it_docs")
    web_search = create_it_web_search_tool()
    handoff_tools = create_it_agent_handoffs()

    tools = [read_it_docs, web_search] + handoff_tools

    it_agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=IT_AGENT_PROMPT,
        name="it_agent"
    )

    return it_agent
