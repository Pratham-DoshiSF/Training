from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.routing_prompt import router_prompt
from conversation_bot.tools.human_feedback_tool import human_feedback


def supervisor_node(state:agentState , llm)->agentState:
    router_chain = router_prompt | llm
    result = router_chain.invoke({"query" : state["query"]})
    print(result.content)

    return {"agent_used": [result.content]}
    