import traceback
from PIL import Image
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from pymongo.errors import DocumentTooLarge

from conversation_bot.utils_function.logger_utility import get_logger
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.memory.in_memory import checkpointer
from conversation_bot.edge.routing_edge import should_continue
from conversation_bot.edge.validation_edge import should_continue_human
from conversation_bot.agents.base_agent import baseagent
from conversation_bot.node.input_validation_node import get_validation_node
from conversation_bot.node.query_routing_node import get_routing_node
from conversation_bot.utils_function.utils import get_llm, get_image_llm
from conversation_bot.utils_function.langgraph_utils import get_llm_with_tool
from conversation_bot.tools.human_feedback_tool import human_feedback
from conversation_bot.tools.image_gen_tool import image_tool
from conversation_bot.tools.web_search_tool import tavily_search_tool_func
from conversation_bot.prompts.image_agent_prompt import instruction


logger = get_logger("Workflow")




class workflow:
    def __init__(self):
        try:
            logger.info("Initializing workflow...")
            self.llm = get_llm()
            self.image_llm = get_image_llm()
            self.llm_With_tool = get_llm_with_tool(self.llm)
            self.checkpointer = checkpointer

            self.setup_tool()
            self.setup_agents()
            self.setup_conditional_edge()
            self.setup_node()
            logger.info("Workflow initialized successfully.")
        except Exception as e:
            logger.error(f"Workflow initialization failed: {e}")
            logger.debug(traceback.format_exc())
            raise

    def setup_tool(self):
        self.image_gen_tool = image_tool(self.image_llm)
        self.human_feedback_tool = human_feedback

    def setup_agents(self):
        self.llm_agent = baseagent(self.llm, [], "llm_expert")
        self.image_agent = baseagent(self.llm, [self.image_gen_tool], "Image_Generation", instruction=instruction)
        self.web_agent = baseagent(self.llm, [tavily_search_tool_func], "web_expert")

    def setup_node(self):
        self.validation_node = get_validation_node(self.llm_With_tool)
        self.routing_node = get_routing_node(self.llm)

    def setup_conditional_edge(self):
        self.should_continue_routing = should_continue
        self.should_continue_validation = should_continue_human

    def create_graph(self):
        try:
            graph = StateGraph(agentState)

            graph.set_entry_point("is feedback needed")
            graph.add_node("is feedback needed", self.validation_node)
            graph.add_node("routing agent", self.routing_node)

            graph.add_node("human_feedback", self.human_feedback_tool)

            graph.add_conditional_edges("is feedback needed",
                                        self.should_continue_validation,
                                        {
                                            "tools": "human_feedback",
                                            "routing": "routing agent"
                                        })

            graph.add_edge("human_feedback", "is feedback needed")

            graph.add_conditional_edges("routing agent", self.should_continue_routing, {
                "llm_agent": "llm generation",
                "image_agent": "image generation",
                "web_agent": "web generation",
            })

            graph.add_node("llm generation", self.llm_agent)
            graph.add_node("web generation", self.web_agent)
            graph.add_node("image generation", self.image_agent)

            graph.add_edge("llm generation", END)
            graph.add_edge("web generation", END)
            graph.add_edge("image generation", END)

            logger.info("Graph created and compiled.")
            return graph.compile(checkpointer=self.checkpointer)

        except Exception as e:
            logger.error(f"Failed to create LangGraph: {e}")
            logger.debug(traceback.format_exc())
            raise


class WorkflowRunner:
    def __init__(self, workflow, user_id , is_streamlit : bool = False):
        try:
            logger.info("Initializing WorkflowRunner...")
            self.workflow = workflow
            self.app = self.workflow.create_graph()
            self.thread_config = {"configurable": {"thread_id": user_id}}
            self.is_streamlit = is_streamlit
            logger.info("WorkflowRunner ready.")
        except Exception as e:
            logger.error(f"WorkflowRunner initialization failed: {e}")
            logger.debug(traceback.format_exc())
            raise

    def handle_query(self, query: str):
        try:
            logger.info(f"Handling user query: {query}")
            result = self.app.invoke({"query": query}, config=self.thread_config)
            return self._handle_result(result)

        except DocumentTooLarge as e:
            logger.error("MongoDB DocumentTooLarge error occurred", exc_info=True)
            return {"__error__": "Your session is too large to continue. Please refresh the page to start a new one."}

        except Exception as e:
            logger.error(f"Error during query handling: {e}")
            logger.debug(traceback.format_exc())
            return {"__error__": str(e)}

    def resume_with_feedback(self, feedback: str):
        try:
            logger.info(f"Resuming with human feedback: {feedback}")

            result = self.app.invoke(Command(resume=feedback), config=self.thread_config)
            return self._handle_result(result)
        except Exception as e:
            logger.error(f"Error resuming with feedback: {e}")
            logger.debug(traceback.format_exc())
            return {"error": str(e)}


    def check_for_interrupt(self):
        try:
            state = self.app.get_state(config=self.thread_config)
            return state.interrupts
        except Exception as e:
            logger.error(f"Error checking for interrupts: {e}")
            logger.debug(traceback.format_exc())
            return False

    def _handle_result(self, result):
        try:
            agent_list = result.get("agent_used", [])
            last_agent = agent_list[-1] if agent_list else None
            last_message = result["messages"][-1] if "messages" in result else None

            if "__interrupt__" in result:
                logger.warning(" Awaiting human feedback...")
                print(result["__interrupt__"][-1].value)

            elif last_agent == "image_agent" and "png" in last_message.content:
                image_path = last_message.content
                logger.info(f"[ IMAGE GENERATED] {image_path}")
                print("[ IMAGE GENERATED]", image_path)
                if not self.is_streamlit:
                    Image.open(image_path).show()

            else:
                logger.info(f"[ RESPONSE] {last_message.content}")
                print("[ Response]:", last_message)

            return result

        except Exception as e:
            logger.error(f"Error while processing result: {e}")
            logger.debug(traceback.format_exc())
            return {"error": str(e)}


if __name__ == "__main__":
    user_id = "12345688"
    try:
        wf = workflow()
        runner = WorkflowRunner(wf, user_id )

        while True:
            query = input("Enter your query (or 'done'): ")
            if query.lower() == "done":
                break

            result = runner.handle_query(query)

            while runner.check_for_interrupt():
                feedback = input("Human input required. Provide clarification: ")
                result = runner.resume_with_feedback(feedback)

    except Exception as e:
        logger.critical("Critical failure in main loop.", exc_info=True)
