from langchain.agents import Tool
from conversation_bot.utils_function.utils import get_llm

llm = get_llm()

def llm_based_search_func(query: str) -> str:
    """LLM-only answer generation."""
    return llm.invoke(query)

llm_tool = Tool(
    name="LLM",
    func=llm_based_search_func,
    description="Useful for generating answers from a language model."
)
