from conversation_bot.state_schema.graph_state import agentState

def end_node(state: agentState): 
    """ Final node """
    print("\n[end_node] Process finished")
    print("Final Generated Post:", state["messages"][-1])
    print("Final Human Feedback", state["human_feedback"])
    return {"generated_post": state["messages"], "human_feedback": state["human_feedback"]}