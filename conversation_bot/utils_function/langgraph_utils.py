from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.human_feedback_tool import human_feedback
from conversation_bot.utils_function.logger_utility import get_logger
import traceback

logger = get_logger("LLMWithTool")

def get_llm_with_tool():
    try:
        llm = get_llm()
        llm_with_tool = llm.bind_tools(tools=[human_feedback])
        logger.info("LLM successfully bound with human_feedback tool.")
        return llm_with_tool
    except Exception as e:
        logger.error(f"Failed to bind tools to LLM: {e}")
        logger.debug(traceback.format_exc())
        raise e  # or return llm (unbound) if fallback behavior is preferred
