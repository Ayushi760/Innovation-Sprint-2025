from langgraph.graph import StateGraph, MessagesState, START, END
from agents import create_supervisor_agent, create_it_agent, create_finance_agent
import os
from dotenv import load_dotenv

load_dotenv()


def route_after_supervisor(state):
    """Route to appropriate agent based on supervisor's decision"""
    messages = state.get("messages", [])
    if not messages:
        return END
    
    last_message = messages[-1]
    
    # Check if the last message contains a tool call for transfer
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            if tool_call['name'] == 'transfer_to_it_agent':
                return "it_agent"
            elif tool_call['name'] == 'transfer_to_finance_agent':
                return "finance_agent"
    
    # If no transfer tool call, end the conversation
    return END


def create_support_system():
    """
    Create the multi-agent support system graph.

    Returns:
        Compiled LangGraph that can process support queries
    """

    supervisor = create_supervisor_agent()
    it_agent = create_it_agent()
    finance_agent = create_finance_agent()

    builder = StateGraph(MessagesState)

    builder.add_node("supervisor", supervisor)
    builder.add_node("it_agent", it_agent)
    builder.add_node("finance_agent", finance_agent)

    # Add edges
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "it_agent": "it_agent",
            "finance_agent": "finance_agent",
            END: END
        }
    )
    builder.add_edge("it_agent", END)
    builder.add_edge("finance_agent", END)

    support_system = builder.compile()

    return support_system


def run_query(support_system, user_query: str):
    """
    Process a user query through the support system.

    Args:
        support_system: Compiled LangGraph support system
        user_query: User's support question

    Returns:
        Response from the appropriate agent
    """

    input_message = {
        "messages": [
            {
                "role": "user",
                "content": user_query
            }
        ]
    }

    try:
        result = support_system.invoke(input_message)
        return result["messages"][-1].content
    except Exception as e:
        return f"Error processing query: {str(e)}"
