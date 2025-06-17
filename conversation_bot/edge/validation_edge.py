from conversation_bot.state_schema.graph_state import agentState
from langchain_core.messages import AIMessage
from conversation_bot.utils_function.logger_utility import get_logger
import traceback

logger = get_logger("HumanRouter")

def should_continue_human(state: agentState) -> str:
    try:
        logger.debug("[STATE RECEIVED] %s", state)

        last_msg = state["messages"][-1] if state["messages"] else [""]
        logger.debug("[LAST MESSAGE] %s", last_msg)

        if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
            logger.info("AIMessage contains tool_calls, routing to 'tools'")
            logger.debug("[LAST MSG TO TOOL] %s", last_msg)
            return "tools"
        else:
            logger.info("No tool_calls found, routing to 'routing'")
            logger.debug("[LAST MSG TO ROUTING] %s", last_msg)
            return "routing"

    except Exception as e:
        logger.exception("Exception in should_continue_human: %s", str(e))
        return "routing"  # Safe fallback
