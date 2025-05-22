from conversation_bot.utils_function.agent_utils import build_agent_executor
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.llm_search_tools import llm_tool 
from conversation_bot.prompts.react_prompt import react_prompt_template 

llm = get_llm()

agent_executor_llm = build_agent_executor(llm, react_prompt_template , llm_tool)

