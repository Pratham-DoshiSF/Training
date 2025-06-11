from typing import TypedDict , Annotated , List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from operator import add

class agentState(TypedDict):
    query : str
    messages : Annotated[list[AnyMessage], add_messages] 
    agent_used : Annotated[list[str] , add]



class testing_state():
    def __init__(self , state:agentState):
        self.state = state

    def print(self):
        print("---------------------")
        self.state["query"] = "HI"
        print(self.state["query"])


if __name__ == "__main__":
    dummy_state = {
        "query" : "HI"
    }
    abc = testing_state(dummy_state)
    abc.print()