import traceback

from langchain_tavily import TavilySearch
from langchain_core.tools import tool

from conversation_bot.utils_function.logger_utility import get_logger

logger = get_logger("TavilySearchTool")

@tool
def tavily_search_tool_func(query: str) -> str:
    """Search the web for up-to-date information using Tavily."""
    try:
        logger.info(f"Executing Tavily web search for query: {query}")
        search_results = TavilySearch(max_results=5, topic="general").invoke(query)
        logger.info("Tavily search completed successfully.")
        return search_results
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        logger.debug(traceback.format_exc())
        return "ERROR: Tavily search failed."
