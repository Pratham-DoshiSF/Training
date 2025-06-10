from conversation_bot.state_schema.graph_state import agentState
from langchain_core.messages import AIMessage

def should_continue_human(state: agentState) -> str:

    messages = state["messages"]
    if not messages:
        
        return "routing agent"

    last_message = messages[-1]
 
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"

    return "routing agent"