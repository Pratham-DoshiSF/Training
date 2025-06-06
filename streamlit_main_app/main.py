import streamlit as st
from streamlit.logger import get_logger
from conversation_bot.workflow.workflow import app
from langchain.schema import HumanMessage
from langgraph.types import Command, Interrupt

# ---------------------------#
# Configuration and Constants
# ---------------------------#
logger = get_logger("DEBUG")
logger.info("✅ Logger initialized")

USER_ID = "123"
THREAD_ID = "1234"
THREAD_CONFIG = {"configurable": {"thread_id": THREAD_ID}}

# ---------------------------#
# Session State Initialization
# ---------------------------#
for key, default in {
    "messages": [],
    "awaiting_feedback": False,
    "partial_answer": None,
    "interrupt_prompt": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------#
# Helper Functions
# ---------------------------#
def already_handled_interrupt(partial, prompt):
    """Avoid double-adding messages during rerun."""
    return (
        len(st.session_state.messages) >= 2
        and st.session_state.messages[-2] == ("assistant", partial)
        and st.session_state.messages[-1] == ("assistant", prompt)
    )

def extract_text_from_node_val(node_val):
    actual_val = node_val[0] if isinstance(node_val, tuple) else node_val
    if isinstance(actual_val, dict):
        if "text" in actual_val:
            return actual_val["text"]
        elif "messages" in actual_val and isinstance(actual_val["messages"], list):
            return "\n\n".join(actual_val["messages"])
        return str(actual_val)
    elif isinstance(actual_val, HumanMessage):
        return actual_val.content
    return str(actual_val)

def handle_interrupt(interrupt_obj):
    logger.info("🛑 Handling interruption event")
    value = interrupt_obj.value

    # Safe extract
    response = (
        value.get("generated_response") if isinstance(value, dict) else getattr(value, "generated_response", None)
    )
    prompt = (
        value.get("message") if isinstance(value, dict) else getattr(value, "message", None)
    ) or "Please provide feedback or type `done`."

    partial = response.content if isinstance(response, HumanMessage) else str(response)

    if not already_handled_interrupt(partial, prompt):
        st.session_state.messages.extend([
            ("assistant", partial),
            ("assistant", f"✋ {prompt}")
        ])

    st.session_state.partial_answer = partial
    st.session_state.interrupt_prompt = prompt
    st.session_state.awaiting_feedback = True
    st.rerun()

def handle_feedback(feedback: str):
    logger.info("✍️ Handling feedback input")
    st.session_state.messages.append(("user", feedback))

    if feedback.strip().lower() == "done":
        logger.info("✅ Finalizing partial response")
        st.session_state.messages.append(("assistant", st.session_state.partial_answer))
        reset_feedback_state()
        st.rerun()
        return

    # Resume processing with feedback
    resumed = app.stream(Command(resume=feedback), config=THREAD_CONFIG)

    for chunk in resumed:
        for node_id, node_val in chunk.items():
            actual_val = node_val[0] if isinstance(node_val, tuple) else node_val
            if node_id == "__interrupt__" and isinstance(actual_val, Interrupt):
                handle_interrupt(actual_val)
                return
            else:
                text = extract_text_from_node_val(node_val)
                st.chat_message("assistant").markdown(text)
                st.session_state.messages.append(("assistant", text))

    reset_feedback_state()
    st.rerun()

def reset_feedback_state():
    logger.info("🧹 Resetting feedback-related session state")
    st.session_state.partial_answer = None
    st.session_state.awaiting_feedback = False
    st.session_state.interrupt_prompt = None

# ---------------------------#
# UI Rendering
# ---------------------------#
st.title("🧠 Feedback‐Driven Chatbot")

for role, text in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(text)

if st.session_state.awaiting_feedback:
    with st.chat_message("assistant"):
        st.markdown(f"✋ **{st.session_state.interrupt_prompt}**")

    feedback_input = st.chat_input("✍️ Provide feedback or type 'done'")
    if feedback_input:
        handle_feedback(feedback_input)

else:
    user_input = st.chat_input("💬 Type your message...")
    if user_input:
        logger.info(f"🗣️ User said: {user_input}")
        st.session_state.messages.append(("user", user_input))

        stream = app.stream(
            {
                "query": user_input,
                "agent_used": [],
                "user_id": USER_ID,
            },
            config=THREAD_CONFIG,
        )

        for chunk in stream:
            for node_id, node_val in chunk.items():
                try:
                    actual_val = node_val[0] if isinstance(node_val, tuple) else node_val

                    if node_id == "__interrupt__" and isinstance(actual_val, Interrupt):
                        handle_interrupt(actual_val)
                        st.stop()

                    text = extract_text_from_node_val(node_val)
                    st.chat_message("assistant").markdown(text)
                    st.session_state.messages.append(("assistant", text))

                except Exception as e:
                    logger.error(f"💥 Error processing chunk: {e}")
