from langgraph.prebuilt import create_react_agent
from conversation_bot.state_schema.graph_state import agentState
from conversation_bot.prompts.system_prompt import system_prompt_template
from conversation_bot.utils_function.logger_utility import get_logger  # ✅ Updated path

import traceback

class baseagent:
    def __init__(self, llm, tools, name, system_promot=system_prompt_template, instruction=""):
        self.logger = get_logger(self.__class__.__name__)
        self.llm = llm
        self.tools = tools
        self.name = name
        self.system_prompt = system_promot
        self.instruction = instruction

        try:
            self.create_agent()
            self.logger.info(f"Initialization done | LLM: {llm} | Tools: {tools} | Name: {name}")
        except Exception as e:
            self.logger.error(f"Agent initialization failed: {e}")
            self.logger.debug(traceback.format_exc())
            raise

    def create_agent(self):
        try:
            self.agent = create_react_agent(
                model=self.llm,
                tools=self.tools,
                name=self.name,
                prompt=self.instruction
            )
            self.logger.info("Agent creation successful")
        except Exception as e:
            self.logger.error(f"Agent creation failed: {e}")
            self.logger.debug(traceback.format_exc())
            raise

    def __call__(self, state: agentState) -> agentState:
        self.logger.info(f"Agent invoked for query: {state.get('query')}")
        try:
            chain = self.system_prompt | self.agent
            query = state.get("query", "")
            messages = state.get("messages") or []
            history = messages[-5:] if messages else []

            self.logger.debug(f"History (last 5): {history}")

            result = chain.invoke({
                "messages": history,
                "query": query
            })

            new_state = state.copy()
            new_state["messages"].append(result["messages"][-1])

            self.logger.info("Agent response added to state messages.")
            return new_state

        except Exception as e:
            self.logger.error(f"Error during agent run for query '{state.get('query')}': {e}")
            self.logger.debug(traceback.format_exc())
            raise
