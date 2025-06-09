from langgraph.prebuilt import create_react_agent
from conversation_bot.tools.web_search_tool import tavily_search_tool_func
from conversation_bot.prompts.feedback_memory_prompt import general_prompt
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.tools.human_feedback_tool import human_feedback
from conversation_bot.prompts.system_prompt import system_prompt



def create_web_agent(llm ):
    return create_react_agent(model=llm, tools=[tavily_search_tool_func], name="web_expert" , prompt=system_prompt)

def web_agent(state:agentState , web_search_agent) -> agentState:

    prompt_formated = general_prompt.format(
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


    return {"messages" : [result["messages"][-1]]}
