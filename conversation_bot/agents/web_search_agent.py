from langgraph.prebuilt import create_react_agent
from conversation_bot.tools.web_search_tools import tavily_search_tool_func
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.prompts.feedback_memory_prompt import general_prompt
from conversation_bot.memory.local_memory import save_message
from conversation_bot.state_schema.graph_state import agentState


llm = get_llm()

web_search_agent = create_react_agent(model=llm, tools=[tavily_search_tool_func], name="web_expert")

def web_agent(state:agentState) -> agentState:

    feedback = state["human_feedback"] if "human_feedback" in state else ["No feedback yey"]

    prompt_formated = general_prompt.format(
        feedback = feedback ,
        query = state["query"] ,
        messages = state["messages"],
    )
    
    result = web_search_agent.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": prompt_formated
                    }
                ]
            })

    save_message(state["user_id"] , "user" , state["query"])
    save_message(state["user_id"] , "ai" , result["messages"][-1].content)
    # state["messages"].append(result["messages"][-1])
    return {"messages" : [result["messages"][-1]]}
