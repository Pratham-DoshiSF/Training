import os
import streamlit as st
from langchain_core.messages import ToolMessage
from conversation_bot.workflow.workflow import workflow, WorkflowRunner
from conversation_bot.utils_function.logger_utility import get_logger
import uuid

user_id = str(uuid.uuid4())
# Logger setup
logger = get_logger("StreamlitUI")

# Page setup
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖", layout="centered")
st.title("🧠 LangGraph Multi-Agent Chatbot")

# Initialize session state
if "runner" not in st.session_state:
    wf = workflow()
    st.session_state.runner = WorkflowRunner(wf, {"configurable": {"thread_id": user_id}} ,True)
    st.session_state.chat_history = []
    st.session_state.awaiting_feedback = False
    st.session_state.last_result = None
    st.session_state.last_query = ""
    st.session_state.tool_call_id = None

# Show messages (user/assistant chat) with image rendering
for entry in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(entry["query"])
    with st.chat_message("assistant"):
        response = entry["response"]
        if isinstance(response, str) and response.strip().endswith((".png", ".jpg", ".jpeg")) and os.path.exists(response):
            st.image(response, caption="🖼️ Generated Image" ,width=500  )
        else:
            st.markdown(response)

st.divider()

# Main input logic
if not st.session_state.awaiting_feedback:
    user_input = st.chat_input("Ask something...")
    if user_input:
        result = st.session_state.runner.handle_query(user_input)

        if "__interrupt__" in result:
            tool_call = result["messages"][-1].tool_calls[0]
            st.session_state.awaiting_feedback = True
            st.session_state.last_result = result
            st.session_state.last_query = user_input
            st.session_state.tool_call_id = tool_call["id"]

            try:
                interrupt_msg = tool_call["args"]["state"].get("messages", [])
                if isinstance(interrupt_msg, list) and interrupt_msg:
                    st.warning(interrupt_msg[0])
                else:
                    st.warning("Clarification required. Please provide more input.")
            except Exception as e:
                st.warning("Clarification required, but message could not be parsed.")
                logger.error("Failed to extract interrupt message", exc_info=True)

        else:
            last_message = result["messages"][-1].content if "messages" in result else "[No response]"

            # Check if it's an image path and store accordingly
            if isinstance(last_message, str) and last_message.strip().endswith((".png", ".jpg", ".jpeg")):
                st.session_state.chat_history.append({
                    "query": user_input,
                    "response": last_message  # Save raw path
                })
            else:
                st.session_state.chat_history.append({
                    "query": user_input,
                    "response": last_message
                })

            st.rerun()

# Feedback mode
else:
    feedback_input = st.chat_input("Clarify your previous query...")
    if feedback_input:
        try:
            tool_msg = ToolMessage(tool_call_id=st.session_state.tool_call_id, content=feedback_input)
            result = st.session_state.runner.resume_with_feedback(tool_msg)

            if "__interrupt__" in result:
                st.warning(result["__interrupt__"][-1].value)
            else:
                last_message = result["messages"][-1].content if "messages" in result else "[No response]"

                if isinstance(last_message, str) and last_message.strip().endswith((".png", ".jpg", ".jpeg")):
                    st.session_state.chat_history.append({
                        "query": st.session_state.last_query,
                        "response": last_message
                    })
                else:
                    st.session_state.chat_history.append({
                        "query": st.session_state.last_query,
                        "response": last_message
                    })

                # Reset feedback state
                st.session_state.awaiting_feedback = False
                st.session_state.last_result = None
                st.session_state.tool_call_id = None
                st.session_state.last_query = ""

                st.rerun()

        except Exception as e:
            logger.error("Error while resuming with feedback", exc_info=True)
            st.error("An error occurred while processing your clarification.")
