import streamlit as st
import os

from conversation_bot.utils_function.routing_utils import supervised_router
from conversation_bot.utils_function.utils import extract_image_path


# streamlit code
st.set_page_config(page_title="Multi-Agent AI Assistant", layout="centered")

st.title("🤖 Multi-Agent AI Assistant with Supervised Router")

st.markdown("""
This assistant uses a router to determine the best specialized agent for your query:
- **Web Search Agent:** For factual questions, current events, or searching the internet.
- **LLM Agent:** For general knowledge, creative tasks, or summaries (uses the LLM directly).
- **Image Generation Agent:** For generating image concepts or descriptions (simulated image generation).

""")
# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"].startswith("[IMAGE_PATH]"):
            image_path = message["content"].replace("[IMAGE_PATH]", "")
            if os.path.exists(image_path):
                st.image(image_path, width=350)
                st.markdown("🖼️ Your image has been generated above.")
            else:
                st.markdown("⚠️ Image not found.")
        else:
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What can I help you with?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        try:
            full_response = supervised_router(prompt)
            agent_name = full_response.get("agent", "unknown")
            agent_response_content = full_response.get("output", "No specific output found in agent response.")
        except Exception as e:
            agent_name = "error"
            agent_response_content = f"An error occurred while processing: {e}"
            st.error(f"Error: {e}")

    with st.chat_message("assistant"):
        image_path = None
        caption = ""

        # Only attempt to extract image if image generation agent was used
        if agent_name == "image_gen_agent":
            if isinstance(agent_response_content, dict):
                image_path = agent_response_content.get("image_path")
                caption = agent_response_content.get("caption", "")
            else:
                image_path = extract_image_path(str(agent_response_content))
                caption = str(agent_response_content)

        if image_path and os.path.exists(image_path):
            st.image(image_path, width=350)
            st.markdown("🖼️ Your image has been generated above.")
            st.markdown(f"🤖 **Agent Used**: `{agent_name}`")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"[IMAGE_PATH]{image_path}"
            })
        else:
            st.markdown(str(agent_response_content))
            st.markdown(f"🤖 **Agent Used**: `{agent_name}`")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"{agent_response_content}\n\n🤖 Agent Used: `{agent_name}`"
            })
