from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.input_validation_prompt import validation_prompt
from langchain_core.messages import AIMessage, ToolMessage
from conversation_bot.utils_function.logger_utility import get_logger
import traceback
from langgraph.types import interrupt

logger = get_logger("ValidationNode")

def get_validation_node(llm_with_tool):

    def validation_node(state: agentState) -> agentState:
        feedback_chain = validation_prompt | llm_with_tool

        try:
            result = feedback_chain.invoke({"query": state["query"]})
        except Exception as e:
            logger.error("Error during validation chain: %s", traceback.format_exc())
            return state

        messages = state["messages"]

        # Get last message only for decision making
        last_msg = messages[-1] if messages else None

        # ✅ Handle AIMessage result
        if isinstance(result, AIMessage):
            if isinstance(last_msg, AIMessage):
                last_tool_call_names = [
                    tc["name"]
                    for tc in getattr(last_msg, "tool_calls", [])
                ]
                current_tool_calls = [tc["name"] for tc in result.tool_calls]

                if any(name in last_tool_call_names for name in current_tool_calls):
                    logger.info("🔁 Skipping duplicate tool call from AIMessage.")
                else:
                    messages.append(result)
            else:
                messages.append(result)

        # ✅ If result is ToolMessage
        elif isinstance(result, ToolMessage):
            messages.append(result)

        # ✅ Check if latest message is human_feedback
        last_updated_msg = messages[-1] if messages else None
        if isinstance(last_updated_msg, ToolMessage) and last_updated_msg.name == "human_feedback":
            logger.info(f"✅ Received human clarification: {last_updated_msg.content}")
            return {
                "messages": messages,
                "query": last_updated_msg.content
            }

        # Default path: no intervention or feedback
        logger.info("No tool or feedback intervention. Continuing with same query.")
        return {
            "messages": messages,
            "query": state["query"]
        }

    return validation_node


if __name__ == "__main__":
    from conversation_bot.utils_function.langgraph_utils import get_llm_with_tool
    llm_with_tool = get_llm_with_tool()
    validation_node = get_validation_node(llm_with_tool)
