from conversation_bot.state_schema.graph_state import agentState
from langchain_core.messages import AIMessage
from conversation_bot.utils_function.logger_utility import get_logger
import traceback

logger = get_logger("HumanRouter")

def should_continue_human(state: agentState) -> str:
    try:
        messages = state.get("messages", [])
        if not messages:
            logger.info("No messages found in state. Defaulting to 'routing agent'")
            return "routing agent"

        last_message = messages[-1]
        logger.debug(f"Last message: {last_message}")

        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            logger.info("Detected tool_calls in AIMessage. Routing to 'tools'")
            return "tools"

        logger.info("No tool_calls detected. Routing to 'routing agent'")
        return "routing agent"

    except Exception as e:
        logger.error(f"Error in should_continue_human: {e}")
        logger.debug(traceback.format_exc())
        return "routing agent"  # Safe fallback
