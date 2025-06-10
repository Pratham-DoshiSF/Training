from langgraph.prebuilt import create_react_agent
from conversation_bot.tools.web_search_tool import tavily_search_tool_func
from conversation_bot.state_schema.graph_state import agentState
from 



def create_web_agent(llm ):
    return create_react_agent(model=llm, tools=[tavily_search_tool_func], name="web_expert" )

def web_agent(state:agentState , web_search_agent) -> agentState:
    
    result = web_search_agent.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": state["query"]
                    }
                ]
            })


    return {"messages" : [result["messages"][-1]]}
