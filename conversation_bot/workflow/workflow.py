from conversation_bot.memory.in_memory import checkpointer
from conversation_bot.edge.conditional_edge import should_continue
from conversation_bot.agents.image_gen_agent import image_agent
from conversation_bot.agents.web_search_agent import web_agent
from conversation_bot.agents.llm_search_agent import llm_agent
from conversation_bot.node.supervisor_node import supervisor_node
from conversation_bot.node.human_feedback_node import humman_feedback
from conversation_bot.node.end_node import end_node
from conversation_bot.state_schema.graph_state import agentState
from langgraph.graph import StateGraph , END
graph = StateGraph(agentState)

graph.set_entry_point("routing agent")

graph.add_node("routing agent" , supervisor_node)
graph.add_node("ending" , end_node)
graph.add_node("humman_feedback" , humman_feedback)
graph.add_conditional_edges(
    "routing agent",
    should_continue,
    {
        "llm_agent" : "llm generation",
        "image_agent" : "image generation",
        "web_agent" : "web generation",

    }
)
graph.add_node("llm generation" , llm_agent)
graph.add_node("web generation" , web_agent)
graph.add_node("image generation" , image_agent)

graph.add_edge("web generation" , "humman_feedback")
graph.add_edge("llm generation" , "humman_feedback")
graph.add_edge("image generation" , "humman_feedback")

graph.add_edge("humman_feedback" , "ending")
graph.add_edge("ending" , END)


app = graph.compile(checkpointer=checkpointer )