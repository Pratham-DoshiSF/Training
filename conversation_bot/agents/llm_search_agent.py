from langgraph.prebuilt import create_react_agent
from conversation_bot.utils_function.utils import get_llm
from conversation_bot.state_schema.graph_state import agentState

class baseagent():
    def __init__(self , llm , tools , name , state):
        self.llm = llm
        self.tools = tools
        self.name = name
        self.state = state
        self.create_agent()
        print("[Intialization done]" , self.llm , self.tools , self.name ,self.state)

    def create_agent(self):

        self.agent = create_react_agent(model=self.llm, tools= self.tools , name=self.name )
        print("[AGENT CREARION DONE]")

    def run_agent(self):
        print("{ENTEWR}")
        print("[RUNNING AGENT]" , self.state["query"])
        result = self.agent.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": self.state["query"]
                    }
                ]
            })
        print("[RESUKT]" , result)
        return {"messages" : [result["messages"][-1].content]}


