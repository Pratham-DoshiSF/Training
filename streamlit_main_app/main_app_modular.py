import streamlit as st
st.set_page_config(page_title="LangGraph Chatbot", page_icon="🧠", layout="centered")

from PIL import Image
import traceback

from conversation_bot.workflow.workflow import workflow, WorkflowRunner
from conversation_bot.utils_function.logger_utility import get_logger


logger = get_logger("StreamlitApp")

# Initialize workflow
@st.cache_resource
def get_runner():
    wf = workflow()
    runner = WorkflowRunner(wf, {"configurable": {"thread_id": "2055"}})
    return runner

runner = get_runner()

# Sidebar info
with st.sidebar:
    st.title("💬 Multi-Agent Chatbot")
    st.markdown("""
    - Handles LLM, Web Search, and Image Generation
    - Supports human feedback interrupts
    - Logs actions internally
    """)

# App state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "awaiting_feedback" not in st.session_state:
    st.session_state.awaiting_feedback = False

st.title("🧠 Conversational Workflow Agent")

# Input field
with st.form("chat_form", clear_on_submit=True):
    if st.session_state.awaiting_feedback:
        user_input = st.text_input("📝 Provide clarification:", "")
        submit = st.form_submit_button("Send Clarification")
    else:
        user_input = st.text_input("💬 Ask me something:", "")
        submit = st.form_submit_button("Ask")

# Handle query or feedback
if submit and user_input:
    try:
        if st.session_state.awaiting_feedback:
            st.session_state.chat_log.append(("🧍 You (clarification)", user_input))
            result = runner.resume_with_feedback(user_input)
            st.session_state.awaiting_feedback = False
        else:
            st.session_state.chat_log.append(("🧍 You", user_input))
            result = runner.handle_query(user_input)

        # Handle interrupt
        if runner.check_for_interrupt():
            interrupt_text = result["__interrupt__"][-1].value
            st.session_state.chat_log.append(("🤖 Bot", interrupt_text))
            st.session_state.awaiting_feedback = True
        else:
            last_msg = result["messages"][-1].content
            agent = result.get("agent_used", [])[-1] if result.get("agent_used") else "Unknown"
            if "png" in last_msg and "generated_images/" in last_msg:
                st.session_state.chat_log.append((f"🤖 {agent}", "🖼️ Image generated:"))
                st.image(last_msg, use_column_width=True)
            else:
                st.session_state.chat_log.append((f"🤖 {agent}", last_msg))

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        st.session_state.chat_log.append(("⚠️ System", error_msg))
        logger.error("Streamlit interaction failed", exc_info=True)

# Display chat log
st.divider()
for speaker, message in st.session_state.chat_log:
    with st.chat_message("user" if "You" in speaker else "assistant"):
        st.markdown(f"**{speaker}**\n\n{message}")
