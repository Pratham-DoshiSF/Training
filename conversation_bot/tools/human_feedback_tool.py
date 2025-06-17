from langchain_core.messages import ToolMessage 
from langgraph.types import interrupt
from conversation_bot.utils_function.logger_utility import get_logger
from conversation_bot.state_schema.graph_state import agentState

logger = get_logger("HumanFeedback")

def human_feedback(state: agentState) -> agentState:
    """This tool is used whenever information is ambiguous or the query is unclear."""

    logger.debug("[STATE BEFORE TOOL] %s", state)

    last_msg = state["messages"][-1] if state["messages"] else [""]
    logger.debug("[MSG TO BE USED BY TOOL] %s", last_msg)

    for tool_call in last_msg.tool_calls:
        if tool_call["name"] == "human_feedback":
            original_query = state["query"]
            logger.info("Triggering human feedback for query: %s", original_query)

            # Trigger the human interrupt — asking user for clarification
            updated_query = interrupt({
                "reason": f"Clarify your query: {original_query}"
            })

            logger.debug("Received updated query from human: %s", updated_query)

            # Save updated query
            state["query"] = updated_query

            # Append the ToolMessage to maintain the conversation chain
            tool_msg = ToolMessage(
                tool_call_id=tool_call["id"],
                content=updated_query
            )
            state["messages"].append(tool_msg)

            logger.info("Appended ToolMessage to state: %s", tool_msg)


    return state
