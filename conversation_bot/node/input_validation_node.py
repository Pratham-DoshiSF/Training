from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.input_validation_prompt import validation_prompt
from langchain_core.messages import AIMessage, ToolMessage
from conversation_bot.utils_function.logger_utility import get_logger
import traceback

logger = get_logger("ValidationNode")

def get_validation_node(llm_with_tool):
    def validation_node(state: agentState) -> agentState:
        try:
            feedback_chain = validation_prompt | llm_with_tool
            messages = state.get("messages", [])
            prev_len = len(messages)

            result = feedback_chain.invoke({"query": state["query"]})

            if isinstance(result, AIMessage):
                last_tool_call_names = [
                    tc["name"]
                    for m in messages
                    if isinstance(m, AIMessage)
                    for tc in getattr(m, "tool_calls", [])
                ]
                current_tool_calls = [tc["name"] for tc in result.tool_calls]

                if not any(name in last_tool_call_names for name in current_tool_calls):
                    messages.append(result)
                    logger.info("New tool call added to messages.")
                else:
                    logger.warning("Duplicate tool call detected. Skipping.")
            else:
                messages.append(result)
                logger.info("Non-AIMessage result appended.")

            # Process new messages only
            for msg in messages[prev_len:]:
                if isinstance(msg, ToolMessage) and msg.name == "human_feedback":
                    logger.info(f"Received human clarification: {msg.content}")
                    return {
                        "messages": messages,
                        "query": msg.content
                    }

            logger.info("No tool or feedback intervention. Continuing with same query.")
            return {
                "messages": messages,
                "query": state["query"]
            }

        except Exception as e:
            logger.error(f"Validation node error: {e}")
            logger.debug(traceback.format_exc())
            return {
                "messages": state.get("messages", []),
                "query": state.get("query", "")
            }

    return validation_node
