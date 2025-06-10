from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.routing_prompt import router_prompt

def routing_node(state: agentState , llm) -> agentState:

    try:
        router_chain = router_prompt | llm


        result = router_chain.invoke({"query": state["query"]})
        print(f"Agent selected by router: {result.content}")

        return {"agent_used": [result.content]}

    except Exception as e:
        raise e