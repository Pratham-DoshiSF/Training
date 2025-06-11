from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.input_validation_prompt import validation_prompt
from langchain_core.messages import AIMessage , ToolMessage


def get_validation_node(llm_with_tool):
    
    def validation_node(state: agentState) -> agentState:
        feedback_chain = validation_prompt | llm_with_tool

        messages = state.get("messages", [])
        prev_len = len(messages)  # Track old length

        result = feedback_chain.invoke({"query": state["query"]})

        # ✅ Avoid duplicate tool calls
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
            else:
                print("🔁 Skipping duplicate tool call from AIMessage.")
        else:
            messages.append(result)

        # ✅ Only check *new* messages for feedback
        for msg in messages[prev_len:]:
            if isinstance(msg, ToolMessage) and msg.name == "human_feedback":
                print(f"✅ Received human clarification: {msg.content}")
                return {
                    "messages": messages,
                    "query": msg.content
                }

        print("No tool or feedback intervention. Continuing with same query.")
        return {
            "messages": messages,
            "query": state["query"]
        }
    return validation_node