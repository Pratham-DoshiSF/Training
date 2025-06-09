from typing import TypedDict , Annotated , List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from operator import add

class agentState(TypedDict):
    query : str
    messages : Annotated[list[AnyMessage], add_messages] 
    agent_used : Annotated[list[str] , add]