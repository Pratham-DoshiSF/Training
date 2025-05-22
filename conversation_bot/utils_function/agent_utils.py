from langchain.agents import create_react_agent, AgentExecutor , Tool

from conversation_bot.memory.in_memory import conversation_memory 

def build_agent_executor(llm , prompt, tool: Tool, verbose: bool = True, handle_errors: bool = True ) -> AgentExecutor:
    """Creates a reusable agent executor with standard config."""
    
    agent = create_react_agent(llm, [tool], prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=[tool],
        memory=conversation_memory,
        verbose=verbose,
        handle_parsing_errors=handle_errors
    )