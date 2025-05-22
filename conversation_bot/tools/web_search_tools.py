from langchain_tavily import TavilySearch
from langchain.agents import Tool

def tavily_search_tool_func(query: str) -> str:
    """Web search tool using Tavily."""
    return TavilySearch(max_results=5, topic="general").invoke(query)

tavily_tool = Tool(
    name="Search",
    func=tavily_search_tool_func,
    description="Useful for general-purpose web searches."
)
