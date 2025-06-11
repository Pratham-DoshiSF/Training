from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.human_feedback_tool import human_feedback

llm = get_llm()
def get_llm_with_tool():
    return llm.bind_tools(tools=[human_feedback])
    