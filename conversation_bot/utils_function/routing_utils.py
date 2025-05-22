from conversation_bot.utils_function.utils import get_llm
from conversation_bot.prompts.routing_prompt import router_prompt
from conversation_bot.agents.image_gen_agent import agent_executor_image
from conversation_bot.agents.llm_search_agent import agent_executor_llm
from conversation_bot.agents.web_search_agent import agent_executor_web

llm = get_llm()

def route_agent(query: str):
    """Dynamically routes the query to the appropriate agent using the LLM."""

    chain = router_prompt | llm
    output = chain.invoke(query)
    return output.content

def supervised_router(query: str):
    """Routes the query dynamically and executes the chosen agent."""
    chosen_agent = route_agent(query)
    print(f"\n[Router]: Dynamically routing query '{query}' to '{chosen_agent}' Agent.")

    try:
        if chosen_agent == "web_search_agent":
            result = agent_executor_web.invoke({"input": query})
        elif chosen_agent == "llm_search_agent":
            result = agent_executor_llm.invoke({"input": query})
        elif chosen_agent == "image_gen_agent":
            result = agent_executor_image.invoke({"input": query})
        else:
            return {"output": f"Error: Unknown agent '{chosen_agent}'.", "agent": "unknown"}

        # Ensure output is a string
        output_text = result.get("output") if isinstance(result, dict) else str(result)

        return {
            "output": output_text,
            "agent": chosen_agent
        }

    except Exception as e:
        return {
            "output": f"An error occurred while processing: {e}",
            "agent": "error"
        }
