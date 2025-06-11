from conversation_bot.memory.in_memory import checkpointer
from conversation_bot.edge.routing_edge import should_continue
from conversation_bot.edge.validation_edge import should_continue_human
# from conversation_bot.agents.image_gen_agent import image_agent
# from conversation_bot.agents.web_search_agent import web_agent
from conversation_bot.agents.llm_search_agent import baseagent
from conversation_bot.node.input_validation_node import get_validation_node
from conversation_bot.node.query_routing_node import get_routing_node

from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.tools.human_feedback_tool import human_feedback
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph , END

from conversation_bot.utils_function.utils import get_llm , get_image_llm 
from conversation_bot.utils_function.langgraph_utils import get_llm_with_tool

from conversation_bot.tools.human_feedback_tool import human_feedback
from conversation_bot.tools.image_gen_tool import image_tool
from conversation_bot.tools.web_search_tool import tavily_search_tool_func
from langgraph.types import Command
from PIL import Image
from conversation_bot.prompts.system_prompt_image import image_system_prompt

thread_config = {"configurable" : { "thread_id" : "23555"}}


instruction = "When generating final answer always return image path without any extras " \
        "for example **generated_images/bcfc234dca554652a72a456177d97ee9.png**"
class workflow:
    def __init__(self):
        self.llm = get_llm()
        self.image_llm = get_image_llm()
        self.llm_With_tool = get_llm_with_tool()
        self.checkpointer = checkpointer
        self.setup_tool()
        self.setup_agents()
        self.setup_conditional_edge()
        self.setup_node()
    
    def setup_tool(self):
        self.image_gen_tool = image_tool(self.image_llm)
        self.human_feedback_tool = human_feedback

    def setup_agents(self):
        self.llm_agent =  baseagent(self.llm , [] , "llm_expert")
        self.image_agent =  baseagent(self.llm , [self.image_gen_tool] , "image_expert" , instruction=instruction)
        self.web_agent =  baseagent(self.llm , [tavily_search_tool_func] , "web_expert")

    def setup_node(self):
        self.validation_node = get_validation_node(self.llm_With_tool)
        self.routing_node = get_routing_node(self.llm)

    def setup_conditional_edge(self):
        self.should_continue_routing = should_continue
        self.should_continue_validation = should_continue_human

    def create_graph(self):
        graph = StateGraph(agentState)

        graph.set_entry_point("is feedback needed")

        graph.add_node("is feedback needed" , self.validation_node)
        graph.add_node("routing agent" , self.routing_node)

        tool = ToolNode([self.human_feedback_tool])
        graph.add_node("human_feedback" , tool)
                                                          
        graph.add_conditional_edges("is feedback needed" ,
                                    self.should_continue_validation ,
                                    {
                                        "tools" :"human_feedback" ,
                                        "routing agent" : "routing agent"
                                    })
            
        graph.add_edge("human_feedback" , "is feedback needed")

        graph.add_conditional_edges(
            "routing agent",
            self.should_continue_routing,
            {
                "llm_agent" : "llm generation",
                "image_agent" : "image generation",
                "web_agent" : "web generation",

            }
        )
        graph.add_node("llm generation" , self.llm_agent)
        graph.add_node("web generation" , self.web_agent)
        graph.add_node("image generation" , self.image_agent)

        graph.add_edge("llm generation" , END)
        graph.add_edge("web generation" , END)
        graph.add_edge("image generation" , END)

        return graph.compile(checkpointer=self.checkpointer )
    
checkpointer.list(config=thread_config ,)
class WorkflowRunner:
    def __init__(self, workflow, thread_config):
        self.workflow = workflow
        self.app = self.workflow.create_graph()
        self.thread_config = thread_config

    def handle_query(self, query: str):
        """Handles initial user query."""
        result = self.app.invoke({"query": query}, config=self.thread_config)
        return self._handle_result(result)

    def resume_with_feedback(self, feedback: str):
        """Handles resuming after human feedback."""
        result = self.app.invoke(Command(resume=feedback), config=self.thread_config)
        return self._handle_result(result)

    def check_for_interrupt(self):
        """Returns True if current state has interrupts (e.g., human needed)."""
        state = self.app.get_state(config=self.thread_config)
        return state.interrupts

    def _handle_result(self, result):
        """Handles output and returns useful data for downstream use."""
        from pprint import pprint
        pprint(result)

        last_agent = result.get("agent_used", [])[-1] if "agent_used" in result else None
        last_message = result["messages"][-1] if "messages" in result else None

        if "__interrupt__" in result:
            print(result["__interrupt__"][-1].value)

        elif last_agent == "image_agent" and "png" in last_message.content:
            image_path = last_message.content
            print("[🖼️ IMAGE GENERATED]", image_path)
            img = Image.open(image_path)
            img.show()
        else:
            print("[💬 Response]:", last_message)

        return result


import pprint
if __name__ == "__main__":
    wf= workflow()
    runner = WorkflowRunner(wf, thread_config)

    while True:
        query = input("Enter your query (or 'done'): ")
        if query.lower() == "done":
            break

        result = runner.handle_query(query)

        while runner.check_for_interrupt():
            feedback = input("Human input required. Provide clarification: ")
            result = runner.resume_with_feedback(feedback)

