import streamlit as st
from conversation_bot.workflow.workflow import WorkflowRunner, workflow

# Initialize session state
if "runner" not in st.session_state:
    wf = workflow()
    st.session_state.runner = WorkflowRunner(wf, {"configurable": {"thread_id": "2555"}})
    st.session_state.chat_history = []
    st.session_state.last_result = None
    st.session_state.awaiting_feedback = False

st.set_page_config(page_title="Multi-Agent Chatbot", layout="centered")
st.title("🧠 Multi-Agent Chatbot (LangGraph)")

# Reverse order: newest at bottom, oldest at top
for entry in reversed(st.session_state.chat_history):
    st.markdown("---")
    st.markdown(f"**User:** {entry['query']}")
    st.markdown(f"**Bot:** {entry['response']}")

st.markdown("---")

# Input box (or feedback prompt if awaiting feedback)
if not st.session_state.awaiting_feedback:
    user_input = st.text_input("Ask something:", key="query_input")
    if st.button("Submit") and user_input:
        result = st.session_state.runner.handle_query(user_input)

        if "__interrupt__" in result:
            st.session_state.awaiting_feedback = True
            st.session_state.last_result = result
            st.session_state.last_query = user_input
            st.warning(result["__interrupt__"][-1].value)
        else:
            last_message = result["messages"][-1].content if "messages" in result else "[No response]"
            st.session_state.chat_history.append({"query": user_input, "response": last_message})
            st.rerun()
else:
    feedback = st.text_input("Clarify your previous query:", key="feedback_input")
    if st.button("Submit Feedback") and feedback:
        result = st.session_state.runner.resume_with_feedback(feedback)

        if "__interrupt__" in result:
            st.warning(result["__interrupt__"][-1].value)
        else:
            last_message = result["messages"][-1].content if "messages" in result else "[No response]"
            st.session_state.chat_history.append({"query": st.session_state.last_query, "response": last_message})
            st.session_state.awaiting_feedback = False
            st.session_state.last_result = None
            st.session_state.last_query = None
            st.rerun()

# Scroll to the bottom when rerun
st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)
