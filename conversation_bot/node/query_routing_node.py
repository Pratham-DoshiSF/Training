from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.routing_prompt import router_prompt
from conversation_bot.utils_function.utils import get_llm

llm = get_llm()

def get_routing_node(llm):

    def routing_node(state: agentState ) -> agentState:

        try:
            router_chain = router_prompt | llm


            result = router_chain.invoke({"query": state["query"]})
            print(f"Agent selected by router: {result.content}")

            return {"agent_used": [result.content]}

        except Exception as e:
            raise e
    return routing_node