import os
from langchain.schema import AIMessage
from langgraph.types import Command, Interrupt
from conversation_bot.workflow.workflow import app
import pprint
import os

USER_ID = 123
thread_config = {"configurable": {
    "thread_id": USER_ID
}}


if __name__ == "__main__":
    user_input = input("Enter user query")

    result = app.invoke({"query" : user_input} , config=thread_config)
    
    if result["__interrupt__"]:
        user_feedback = ""  # Initialize before loop

    while user_feedback.lower() != "done":
        user_feedback = input("Provide feedback (or type 'done' when finished): ")

        resumed_result = app.invoke(Command(resume=user_feedback), config=thread_config)
        if resumed_result["agent_used"][-1] == "image_agent":
            resumed_result = resumed_result["messages"][-1].content 
            
            continue
        pprint.pprint(resumed_result)
    
    else:
        if result["agent_used"][-1] == "image_agent":
            pass

        pprint.pprint(result)