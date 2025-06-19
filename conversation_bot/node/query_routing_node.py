import traceback

from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.routing_prompt import router_prompt
from conversation_bot.utils_function.logger_utility import get_logger

logger = get_logger("RoutingNode")


def get_routing_node(llm):

    def routing_node(state: agentState) -> agentState:
        try:
            router_chain = router_prompt | llm
            result = router_chain.invoke({"query": state["query"]})
            logger.info(f"Agent selected by router: {result.content}")
            print("[QUERY]" , state["query"])

            return {"agent_used": [result.content]}

        except Exception as e:
            logger.error(f"Error in routing node: {e}")
            logger.debug(traceback.format_exc())

            return {"agent_used": ["llm_agent"]}

    return routing_node
