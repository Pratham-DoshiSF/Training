from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

system_prompt = (
    "You are a helpful assistant.YOu are provided the history as list of message , So use it whenever the query need history"
)

system_prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{query}")
])
