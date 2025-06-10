from conversation_bot.memory.in_memory import checkpointer
from conversation_bot.edge.routing_edge import should_continue
from conversation_bot.edge.validation_edge import should_continue_human
# from conversation_bot.agents.image_gen_agent import image_agent
# from conversation_bot.agents.web_search_agent import web_agent
from conversation_bot.agents.llm_search_agent import baseagent
from conversation_bot.node.input_validation_node import validation_node
from conversation_bot.node.query_routing_node import routing_node

from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.tools.human_feedback_tool import human_feedback
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph , END

from conversation_bot.utils_function.utils import get_llm , get_image_llm

thread_config = {"configurable" : { "thread_id" : "23"}}
llm_agent = baseagent(get_llm , [] , "LLM EXPERT" , agentState)
print("[AGENT INTIALIZED]")
graph = StateGraph(agentState)
graph.set_entry_point("is feedback needed")

graph.add_node("is feedback needed" , validation_node)
graph.add_node("routing agent" , routing_node)

tool = ToolNode([human_feedback])
graph.add_node("human_feedback" , tool)

graph.add_conditional_edges("is feedback needed" ,
                            should_continue_human ,
                            {
                                "tools" :"human_feedback" ,
                                "routing agent" : "routing agent"
                            })
    
# graph.add_edge("is feedback needed" , "human_feedback")
graph.add_edge("human_feedback" , "is feedback needed")


graph.add_conditional_edges(
    "routing agent",
    should_continue,
    {
        "llm_agent" : "llm generation",
        # "image_agent" : "image generation",
        # "web_agent" : "web generation",

    }
)
graph.add_node("llm generation" , llm_agent.run_agent())
# graph.add_node("web generation" , web_agent)
# graph.add_node("image generation" , image_agent)

graph.add_edge("llm generation" , END)
# graph.add_edge("web generation" , END)
# graph.add_edge("image generation" , END)

app = graph.compile(checkpointer=checkpointer )


if __name__ == "__main__":
    result = app.invoke({"query" : "What is ai in stocks"} , config=thread_config)
    print(result)
# class conversation_bot():

#     def __init__(self):
#         self.llm = get_llm()
#         self.image_llm = get_image_llm()
#         self.state = agentState
    
#     def setup_tool(self):

