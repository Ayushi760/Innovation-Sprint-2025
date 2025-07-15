from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.graph import MessagesState
from langgraph.types import Command


def create_handoff_tool(agent_name: str, description: str = None):
    """
    Create a handoff tool for transferring control to another agent.

    Args:
        agent_name: Name of the target agent to transfer to
        description: Description of when to use this handoff tool

    Returns:
        A tool function that can be used by agents to transfer control
    """
    tool_name = f"transfer_to_{agent_name}"

    if description is None:
        description = f"Transfer the conversation to the {agent_name} agent"

    @tool(description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        """
        Transfer control to another agent.

        This tool creates a handoff command that routes the conversation
        to the specified agent while maintaining conversation context.
        """
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name} agent",
            "name": tool_name,
            "tool_call_id": tool_call_id,
        }

        return Command(
            goto=agent_name,
            update={"messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,
        )

    handoff_tool.name = tool_name
    return handoff_tool


def create_supervisor_handoffs():
    """Create handoff tools for the supervisor agent"""
    return [
        create_handoff_tool(
            "it_agent",
            "Transfer to IT agent for technical support queries (VPN, software, hardware, troubleshooting)"
        ),
        create_handoff_tool(
            "finance_agent",
            "Transfer to Finance agent for financial queries (reimbursements, budgets, payroll, expenses)"
        )
    ]


def create_it_agent_handoffs():
    """Create handoff tools for the IT agent"""
    return [
        create_handoff_tool(
            "supervisor",
            "Transfer back to supervisor if the query is not IT-related or needs reclassification"
        ),
        create_handoff_tool(
            "finance_agent",
            "Transfer to Finance agent if the query involves financial aspects of IT (software costs, budget approvals)"
        )
    ]


def create_finance_agent_handoffs():
    """Create handoff tools for the Finance agent"""
    return [
        create_handoff_tool(
            "supervisor",
            "Transfer back to supervisor if the query is not finance-related or needs reclassification"
        ),
        create_handoff_tool(
            "it_agent",
            "Transfer to IT agent if the query involves technical aspects of finance systems"
        )
    ]
