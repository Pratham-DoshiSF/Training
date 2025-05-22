from conversation_bot.utils_function.routing_utils import supervised_router

while True:
    print("To exit type exit")
    user_input = input("Enter your query : ")

    if user_input.lower() == "exit":
        break
    else :
        response = supervised_router(user_input)
        agent_name = response.get("agent", "unknown")
        agent_response_content = response.get("output", "No specific output found in agent response.")
        print(agent_name)
        print(agent_response_content)