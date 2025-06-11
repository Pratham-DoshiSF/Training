from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

system_prompt = (
    "You are a helpful assistant.YOu are provided the history as list of message , So use it whenever the query need history " \
    "for output always return path to images " \
    "for example **generated_images/bcfc234dca554652a72a456177d97ee9.png**"
)

image_system_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{query}")
])