import streamlit as st
from PIL import Image
from conversation_bot.workflow.workflow import app
from langgraph.types import Command

thread_config = {"configurable": {"thread_id": "12334"}}

st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("🧠 LangGraph Chatbot")

# ------------------- Session State Init -------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "awaiting_clarification" not in st.session_state:
    st.session_state.awaiting_clarification = False

if "clarification_instruction" not in st.session_state:
    st.session_state.clarification_instruction = ""

if "last_rendered_image" not in st.session_state:
    st.session_state.last_rendered_image = None


# ------------------- Helpers -------------------
def add_to_chat(speaker, message):
    st.session_state.chat_history.append((speaker, message))

def display_response(content, agent_used):
    add_to_chat("Agent", content)

    # Force rerun if it's an image so it renders immediately
    if "image_agent" in agent_used and isinstance(content, str) and content.endswith(".png"):
        st.session_state.last_rendered_image = content
        st.rerun()


def handle_user_query(user_query):
    add_to_chat("You", user_query)
    result = app.invoke({"query": user_query}, config=thread_config)

    if "__interrupt__" in result:
        st.session_state.awaiting_clarification = True
        st.session_state.clarification_instruction = list(result["__interrupt__"][-1].value)[-1]
        st.rerun()
    else:
        content = result["messages"][-1].content
        agent_used = result["agent_used"][-1]
        display_response(content, agent_used)

def handle_clarification(feedback):
    add_to_chat("You (clarified)", feedback)
    resumed_result = app.invoke(Command(resume=feedback), config=thread_config)
    content = resumed_result["messages"][-1].content
    agent_used = resumed_result["agent_used"][-1]
    display_response(content, agent_used)

    # Reset state for next cycle
    st.session_state.awaiting_clarification = False
    st.session_state.clarification_instruction = ""
    st.rerun()


# ------------------- Chat History (Grouped) -------------------
i = 0
while i < len(st.session_state.chat_history):
    speaker, text = st.session_state.chat_history[i]

    if "You" in speaker:
        st.markdown(f"**🧍 {speaker}:** {text}")

        # Check if agent responds
        if i + 1 < len(st.session_state.chat_history) and st.session_state.chat_history[i + 1][0] == "Agent":
            agent_text = st.session_state.chat_history[i + 1][1]
            st.markdown(f"**🤖 Agent:** {agent_text}")

            if isinstance(agent_text, str) and agent_text.endswith(".png"):
                try:
                    st.image(Image.open(agent_text), caption="Generated Image", width=400)
                except Exception as e:
                    st.warning(f"⚠️ Couldn't display image: {e}")
            st.divider()
            i += 1  # Skip agent next loop
    i += 1


# ------------------- Dynamic Input Section -------------------
if st.session_state.awaiting_clarification:
    st.markdown("### 🤖 Clarification Needed")
    st.markdown(f"**Instruction:** {st.session_state.clarification_instruction}")
    clarification_input = st.chat_input("Please clarify:")
    if clarification_input:
        handle_clarification(clarification_input)
else:
    user_query = st.chat_input("Ask me anything...")
    if user_query:
        handle_user_query(user_query)
