from langchain_core.tools import tool
from conversation_bot.utils_function.utils import get_llm

llm = get_llm()

@tool
def llm_based_search_func(query: str) -> str:
    """Answer general knowledge queries using LLM."""
    return llm.invoke(query).content
