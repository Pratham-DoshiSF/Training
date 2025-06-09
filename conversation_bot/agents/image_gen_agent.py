from langgraph.prebuilt import create_react_agent
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.image_gen_tool import image_gen_func
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.feedback_memory_prompt import image_prompt
from conversation_bot.tools.human_feedback_tool import human_feedback
from conversation_bot.prompts.system_prompt import system_prompt

llm = get_llm()

image_gen_agent = create_react_agent(model=llm, tools=[image_gen_func , human_feedback], name="image_gen_expert" , prompt=system_prompt)

def image_agent(state:agentState) -> agentState:

    prompt_formated = image_prompt.format(
        query = state["query"] ,
        messages = state["messages"],
    )
    
    print(state)
    result = image_gen_agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": prompt_formated
                }
            ]
        })

    return {"messages": [result["messages"][-1]]} 
