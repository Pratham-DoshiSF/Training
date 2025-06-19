import traceback

from conversation_bot.prompts.input_validation_prompt import validation_prompt
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.utils_function.logger_utility import get_logger

logger = get_logger("ValidationNode")

def get_validation_node(llm_with_tool):
    def validation_node(state: agentState) -> agentState:
        feedback_chain = validation_prompt | llm_with_tool

        try:
            logger.debug("Running validation for query: %s", state["query"])
            result = feedback_chain.invoke({"query": state["query"]})
            logger.info("Validation result obtained successfully")
            logger.debug("Validation result: %s", result)

        except Exception:
            logger.error("Error during validation chain:\n%s", traceback.format_exc())
            return state

        return {"messages": [result]}

    return validation_node


if __name__ == "__main__":
    from conversation_bot.utils_function.langgraph_utils import get_llm_with_tool
    llm_with_tool = get_llm_with_tool()
    validation_node = get_validation_node(llm_with_tool)
    logger.info("Validation node initialized in standalone mode")
