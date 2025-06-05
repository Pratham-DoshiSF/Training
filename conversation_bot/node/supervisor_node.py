from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.routing_prompt import router_prompt
from conversation_bot.utils_function.utils import get_llm

llm = get_llm()

def supervisor_node(state:agentState)->agentState:
    router_chain = router_prompt | llm
    result = router_chain.invoke({"query" : state["query"]})
    print(result.content)

    return {"agent_used": [result.content]}
    