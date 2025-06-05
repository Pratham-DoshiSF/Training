from conversation_bot.workflow.workflow import app
from conversation_bot.memory.local_memory import retrieve_last_5_pairs
from langgraph.types import Command, Interrupt

thread_config = {
    "configurable": {
        "thread_id": "1234"
    }
}

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Exiting conversation.")
        break

    stream = app.stream({
        "query": user_input,
        "messages": retrieve_last_5_pairs("123"),
        "agent_used": [],
        "user_id": "123"
    }, config=thread_config)

    for chunk in stream:
        for node_id, value in chunk.items():
            if node_id == "__interrupt__":
                interrupted_message = None

                if isinstance(value, Interrupt) and value.message:
                    interrupted_message = value.message

                while True:
                    user_feedback = input("Provide feedback (or type 'done' to continue): ")

                    if user_feedback.lower() == "done":
                        if interrupted_message:
                            print("Bot:", interrupted_message)
                        break

                    # Resume execution with the feedback
                    resumed_stream = app.stream(Command(resume=user_feedback), config=thread_config)

                    for resumed_chunk in resumed_stream:
                        for resumed_node_id, resumed_value in resumed_chunk.items():
                            if resumed_node_id == "__interrupt__":
                                if isinstance(resumed_value, Interrupt) and resumed_value.message:
                                    print("Bot (interrupted again):", resumed_value.message)
                            else:
                                if isinstance(resumed_value, dict) and "text" in resumed_value:
                                    print("Bot (resumed):", resumed_value["text"])
                                else:
                                    print("Bot (resumed):", resumed_value)
            else:
                # ✅ PRINT NON-INTERRUPT RESPONSES HERE
                if isinstance(value, dict) and "text" in value:
                    print("Bot:", value["text"])
                else:
                    print("Bot:", value)
