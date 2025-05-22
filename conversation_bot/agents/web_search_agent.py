from conversation_bot.utils_function.agent_utils import build_agent_executor
from conversation_bot.tools.web_search_tools import tavily_tool
from conversation_bot.prompts.react_prompt import react_prompt_template
from conversation_bot.utils_function.utils import get_llm

llm = get_llm()

agent_executor_web = build_agent_executor(llm,react_prompt_template,tavily_tool)
