from conversation_bot.state_schema.graph_state import agentState

def should_continue(state : agentState) -> agentState:

    if state["agent_used"][-1] == "llm_agent":
        return "llm_agent"
    elif state["agent_used"][-1] == "web_agent":
        return "web_agent"
    elif state["agent_used"][-1] == "image_agent":
        return "image_agent"
    
    else:
        return "llm_agent"