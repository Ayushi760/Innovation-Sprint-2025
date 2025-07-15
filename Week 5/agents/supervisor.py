from langgraph.prebuilt import create_react_agent
from config import get_azure_model
from utils.handoffs import create_supervisor_handoffs
from prompts import SUPERVISOR_PROMPT


def create_supervisor_agent():
    """
    Create the supervisor agent that classifies and routes user queries.

    The supervisor agent analyzes incoming queries and determines whether
    they should be handled by the IT agent or Finance agent.
    """

    model = get_azure_model()

    handoff_tools = create_supervisor_handoffs()

    supervisor_agent = create_react_agent(
        model=model,
        tools=handoff_tools,
        prompt=SUPERVISOR_PROMPT,
        name="supervisor"
    )

    return supervisor_agent
