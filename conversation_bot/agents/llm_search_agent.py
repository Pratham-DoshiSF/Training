from langgraph.prebuilt import create_react_agent
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.llm_search_tool import llm_based_search_func
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.feedback_memory_prompt import general_prompt
from conversation_bot.tools.human_feedback_tool import human_feedback
from conversation_bot.prompts.system_prompt import system_prompt

llm = get_llm()

llm_search_agent = create_react_agent(model=llm, tools=[llm_based_search_func, human_feedback], name="llm_expert" , prompt=system_prompt)

def llm_agent(state:agentState) -> agentState:


    prompt_formated = general_prompt.format(
        query = state["query"] ,
        messages = state["messages"],
    )

    result = llm_search_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": prompt_formated
                }
            ]
        })

    return {"messages" : [result["messages"][-1].content]}
     