from langgraph.prebuilt import create_react_agent
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.image_gen_tool import image_gen_func
from conversation_bot.state_schema.graph_state import agentState


llm = get_llm()

def create_image_agent(llm):
    
    return create_react_agent(model=llm, tools=[image_gen_func ], name="image_gen_expert" )


def image_agent(state:agentState , image_agent) -> agentState:
    
    print(state)
    result = image_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": state["query"]
                }
            ]
        })

    return {"messages": [result["messages"][-1]]} 
