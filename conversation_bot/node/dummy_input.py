from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.input_validation_prompt import validation_prompt
from langchain_core.messages import AIMessage, ToolMessage
from conversation_bot.utils_function.logger_utility import get_logger
import traceback
from langgraph.types import interrupt

logger = get_logger("ValidationNode")

def get_validation_node(llm_with_tool):

    def validation_node(state: agentState ) -> agentState:
        feedback_chain = validation_prompt | llm_with_tool


        result = feedback_chain.invoke({"query": state["query"]})

        messages = state.get("messages", [])

        # ✅ Prevent duplicate tool calls
        if isinstance(result, AIMessage):
            last_tool_call_names = [
                tc["name"]
                for m in messages
                if isinstance(m, AIMessage)
                for tc in getattr(m, "tool_calls", [])
            ]
            current_tool_calls = [tc["name"] for tc in result.tool_calls]
        
            if any(name in last_tool_call_names for name in current_tool_calls):
                print("🔁 Skipping duplicate tool call from AIMessage.")
            else:
                messages.append(result)
        else:
            messages.append(result)
        

        # ✅ If human feedback is found, use it
        for msg in messages:
            if isinstance(msg, ToolMessage) and msg.name == "human_feedback":
                print(f"✅ Received human clarification: {msg.content}")
                return {
                    "messages": messages,
                    "query": msg.content
                }

        # Default: no intervention
        print("No tool or feedback intervention. Continuing with same query.")
        print("State query to be continue" , state["query"])
        return {
            "messages": messages,
            "query": state["query"]
        }
    return validation_node


if __name__ == "__main__":
    from conversation_bot.utils_function.langgraph_utils import get_llm_with_tool
    # from conversation_bot.state_schema.graph_state import agentState
    llm_with_tool = get_llm_with_tool()
    validation_node = get_validation_node(llm_with_tool)
