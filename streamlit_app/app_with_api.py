import streamlit as st
import requests
from app.utils.constant import API_BASE 


st.set_page_config(page_title="AI Chatbot", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "interrupted" not in st.session_state:
    st.session_state.interrupted = False

if "user_id" not in st.session_state:
    import uuid
    st.session_state.user_id = str(uuid.uuid4())

st.title("AI Chatbot")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")

def send_query(query):
    try:
        res = requests.post(f"{API_BASE}/query", json={
            "user_id": st.session_state.user_id,
            "query": query
        })
        return res
    except Exception as e:
        st.error("Failed to reach server.")
        return None

def send_feedback(feedback):
    try:
        res = requests.post(f"{API_BASE}/feedback", json={
            "user_id": st.session_state.user_id,
            "feedback": feedback
        })
        return res
    except Exception as e:
        st.error("Failed to reach server.")
        return None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if not st.session_state.interrupted:
        res = send_query(user_input)
    else:
        res = send_feedback(user_input)
        st.session_state.interrupted = False

    if res and res.ok:
        data = res.json()
        bot_msg = data.get("result", "No response.")
        if data.get("status") == "interrupted":
            st.session_state.interrupted = True
            bot_msg += "\n\n⚠️ Awaiting further clarification."

        st.session_state.messages.append({"role": "assistant", "content": bot_msg})
        with st.chat_message("assistant"):
            st.markdown(bot_msg)
    elif res and res.status_code == 404:
        st.error("Session not found. Start with a new query.")
    else:
        st.error("An error occurred. Check server logs.")
