from conversation_bot.utils_function.utils import get_llm
from conversation_bot.agents.image_gen_agent import image_gen_agent
from conversation_bot.agents.llm_search_agent import llm_search_agent
from conversation_bot.agents.web_search_agent import web_search_agent
from langgraph_supervisor import create_supervisor
from conversation_bot.memory.in_memory import checkpointer ,store

llm = get_llm()

def supervisor_agent():
    workflow = create_supervisor(
        [web_search_agent, llm_search_agent , image_gen_agent],
        model=llm,
        output_mode="full_history" 
    )

    return workflow.compile(checkpointer=checkpointer , store=store , debug=True)
