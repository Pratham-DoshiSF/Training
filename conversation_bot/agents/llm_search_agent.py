from langgraph.prebuilt import create_react_agent
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.system_prompt import system_prompt_template

class baseagent():
    def __init__(self , llm , tools , name , system_promot = system_prompt_template , instruction = ""):
        self.llm = llm
        self.tools = tools
        self.name = name
        self.system_prompt = system_promot
        self.instruction = instruction
        self.create_agent()
        print("[Intialization done]" , self.llm , self.tools , self.name )

    def create_agent(self):

        self.agent = create_react_agent(model=self.llm, tools= self.tools , name=self.name , prompt=self.instruction)
        print("[AGENT CREARION DONE]")

    def __call__(self , state:agentState) -> agentState:
        print("{ENTEWR}")
        print("[RUNNING AGENT]" , state["query"])
        chain = self.system_prompt | self.agent
        print(f"[QUERY] USER: {state['query']}")

        # Run the chain with structured inputs
        result = chain.invoke({
            "messages": state["messages"][:-5],  # past messages
            "query": state["query"]         # current query
        })
            
        new_state = state.copy()
        new_state["messages"].append(result["messages"][-1])  
        return new_state


