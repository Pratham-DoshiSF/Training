import os
import webbrowser
from langchain.schema import AIMessage
from langgraph.types import Command, Interrupt
from conversation_bot.workflow.workflow import app
from conversation_bot.utils_function.utils import extract_image_path

# Thread Configuration
thread_config = {
    "configurable": {
        "thread_id": "1234"
    }
}

def handle_ai_message(msg: AIMessage):
    """Handles AIMessage content including image paths and displays them."""
    if isinstance(msg.content, str) and ".png" in msg.content:
        image_paths = [img.strip() for img in msg.content.split(",") if img.strip().endswith(".png")]
        for path in image_paths:
            print(f"\U0001F5BC\uFE0F Bot sent image: {path}")
            if os.path.exists(path):
                if os.name == 'nt':
                    os.startfile(path)
                else:
                    os.system(f'xdg-open "{path}"')
            else:
                print("\u26A0\uFE0F Image file not found locally.")
    else:
        print("Bot:", msg.content)

def display_image_paths(content):
    """Check and display image paths if present in bot response."""
    if isinstance(content, str) and ".png" in content:
        paths = [p.strip() for p in content.split(",") if p.strip().endswith(".png")]
        for path in paths:
            print(f"\U0001F5BC\uFE0F Image Path: {path}")
        return True
    return False

def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting conversation.")
            break

        stream = app.stream({
            "query": user_input,
            "agent_used": [],
            "user_id": "123"
        }, config=thread_config)

        for chunk in stream:
            for node_id, value in chunk.items():
                if node_id == "__interrupt__":
                    interrupted_message = value.message if isinstance(value, Interrupt) and value.message else None

                    while True:
                        user_feedback = input("Provide feedback (or type 'done' to continue): ")

                        if user_feedback.lower() == "done":
                            if interrupted_message:
                                print("Bot:", interrupted_message)
                            break

                        resumed_stream = app.stream(Command(resume=user_feedback), config=thread_config)

                        for resumed_chunk in resumed_stream:
                            for resumed_node_id, resumed_value in resumed_chunk.items():
                                if resumed_node_id == "__interrupt__":
                                    if isinstance(resumed_value, Interrupt) and resumed_value.message:
                                        print("Bot (interrupted again):", resumed_value.message)
                                else:
                                    if isinstance(resumed_value, dict):
                                        if "messages" in resumed_value:
                                            for msg in resumed_value["messages"]:
                                                if isinstance(msg, AIMessage):
                                                    handle_ai_message(msg)
                                        elif "text" in resumed_value:
                                            print("Bot (resumed):", resumed_value["text"])
                                        else:
                                            print("Bot (resumed):", resumed_value)
                                    else:
                                        print("Bot (resumed):", resumed_value)
                else:
                    if isinstance(value, dict):
                        if "messages" in value:
                            for msg in value["messages"]:
                                if isinstance(msg, AIMessage):
                                    handle_ai_message(msg)
                        elif "text" in value:
                            print("Bot:", value["text"])
                        else:
                            print("Bot:", value)
                    else:
                        print("Bot:", value)

if __name__ == "__main__":
    main()