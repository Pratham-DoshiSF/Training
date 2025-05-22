from conversation_bot.utils_function.agent_utils import build_agent_executor
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.image_gen_tools import image_tool
from conversation_bot.prompts.image_react_prompt import image_react_prompt_template

llm = get_llm()

agent_executor_image = build_agent_executor(llm, image_react_prompt_template , image_tool)

