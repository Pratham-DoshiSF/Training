from conversation_bot.state_schema.graph_state import agentState
from langgraph.types import Command , interrupt 

def humman_feedback(state:agentState)->agentState:
    generated_response = state["messages"][-1]

    # print("[generated response]" , generated_response)
    user_feedback = interrupt(
        {
            "generated_response" : generated_response,
            "message" : "Please provide feedback or done for finish"
        }
    )

    print(f"[human_node] Received human feedback: {user_feedback}")

        # If user types "done", transition to END node
    if user_feedback.lower() == "done": 
        return Command(update={"human_feedback": state["human_feedback"] + ["Finalised"]}, goto="end_node")

    # Otherwise, update feedback and return to model for re-generation
    return Command(update={"human_feedback": state["human_feedback"] + [user_feedback]}, goto="routing agent")

