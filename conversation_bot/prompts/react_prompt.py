from langchain.prompts import PromptTemplate

react_prompt_template = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tool_names", "tools", "chat_history"],
    template=(
        "You are an intelligent agent designed to reason step-by-step and solve complex problems using external tools.\n\n"
        "If the user's current question depends on earlier conversation, refer to the relevant context provided in the chat history.\n"
        "Use prior information, clarifications, and tool results as needed to build on earlier steps.\n\n"
        "Conversation history (if relevant):\n"
        "{chat_history}\n\n"
        "You have access to the following tools:\n"
        "{tools}\n\n"
        "When solving a problem, follow this structured format:\n\n"
        "Question: the user’s question\n"
        "Thought: your reasoning about what to do next (including references to chat history if helpful)\n"
        "Action: the action to take, should be one of [{tool_names}]\n"
        "Action Input: the input required for the action\n"
        "Observation: the result of the action\n"
        "... (repeat Thought/Action/Action Input/Observation as needed)\n"
        "Thought: I now know the final answer\n"
        "Final Answer: your final response to the user\n\n"
        "Begin below:\n\n"
        "Question: {input}\n"
        "Thought: {agent_scratchpad}"
    )
)