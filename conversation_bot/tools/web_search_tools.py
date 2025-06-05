from langchain_tavily import TavilySearch
from langchain_core.tools import tool

@tool
def tavily_search_tool_func(query: str) -> str:
    """Search the web for up-to-date information."""
    return TavilySearch(max_results=5, topic="general").invoke(query)
