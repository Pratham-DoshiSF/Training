from langchain_core.tools import tool
from langgraph.types import interrupt
from conversation_bot.utils_function.logger_utility import get_logger
import traceback

logger = get_logger("HumanFeedback")

@tool
def human_feedback(query: str) -> str:
    """
    Requests clarification or more details from the user for the given query.

    Parameters:
    - query (str): The ambiguous or unclear input/query.

    Returns:
    - str: User's feedback or clarification.
    """
    logger.info(f"Requesting human clarification for query: {query}")
    prompt = f"❓ Please clarify: {query}"

    try:
        user_feedback = interrupt({query})
        logger.info("✅ Received human clarification.")
        return user_feedback

    except Exception as e:
        logger.error(f"Error while waiting for human clarification: {e}")
        logger.debug(traceback.format_exc())
        return "Unable to receive feedback. Please try again."

