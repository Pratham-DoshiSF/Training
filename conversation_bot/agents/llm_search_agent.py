from langgraph.prebuilt import create_react_agent
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.state_schema.graph_state import agentState



def create_llm_agent(llm):

    return create_react_agent(model=llm, tools= [], name="llm_expert" )


def llm_agent(state:agentState , llm_search_agent) -> agentState:



    result = llm_search_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": state["query"]
                }
            ]
        })

    return {"messages" : [result["messages"][-1].content]}
