from langgraph.prebuilt import create_react_agent
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.llm_search_tools import llm_based_search_func
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.feedback_memory_prompt import general_prompt

llm = get_llm()

llm_search_agent = create_react_agent(model=llm, tools=[llm_based_search_func], name="llm_expert")

def llm_agent(state:agentState) -> agentState:

    feedback = state["human_feedback"] if "human_feedback" in state else ["No feedback yey"]

    prompt_formated = general_prompt.format(
        feedback = feedback ,
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
    print("-----------------------------------")
    print(state["agent_used"])

    return {"messages" : [result["messages"][-1].content]}
     