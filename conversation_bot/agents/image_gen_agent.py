from langgraph.prebuilt import create_react_agent
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.tools.image_gen_tools import image_gen_func
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.feedback_memory_prompt import general_prompt
from conversation_bot.memory.local_memory import save_message

llm = get_llm()

image_gen_agent = create_react_agent(model=llm, tools=[image_gen_func], name="image_gen_expert")

def image_agent(state:agentState) -> agentState:

    feedback = state["human_feedback"] if "human_feedback" in state else ["No feedback yey"]

    prompt_formated = general_prompt.format(
        feedback = feedback ,
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

    save_message(state["user_id"], "user" , state["query"])
    save_message(state["user_id"] , "assistant" ,result["messages"][-1].content)

    return {"messages": [result["messages"][-1]]} 
