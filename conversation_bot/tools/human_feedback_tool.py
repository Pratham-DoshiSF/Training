from langchain_core.tools import tool
from langgraph.types import interrupt
from conversation_bot.utils_function.logger_utility import get_logger

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
    logger.info(f"🔁 Interrupting graph to request human clarification: {query}")
    # DO NOT CATCH — let it raise!
    value = interrupt({"query" : query})
    return value
