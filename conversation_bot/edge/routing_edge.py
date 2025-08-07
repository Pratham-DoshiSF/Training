from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.utils_function.logger_utility import get_logger
import traceback

logger = get_logger("Router")

def should_continue(state: agentState) -> str:
    try:
        last_agent = state.get("agent_used", [])[-1] if "agent_used" in state else None

        logger.info(f"Routing decision based on last agent: {last_agent}")

        if last_agent == "llm_agent":
            return "llm_agent"
        elif last_agent == "web_agent":
            return "web_agent"
        elif last_agent == "image_agent":
            return "image_agent"
        else:
            logger.warning(f"Unknown agent type '{last_agent}', defaulting to 'llm_agent'")
            return "llm_agent"

    except Exception as e:
        logger.error(f"Error in router logic: {e}")
        logger.debug(traceback.format_exc())
        return "llm_agent"  
