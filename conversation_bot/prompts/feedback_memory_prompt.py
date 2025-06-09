from langchain_core.prompts import PromptTemplate

general_prompt = PromptTemplate(
    input_variables=[  "query" , "messages"] , 
    template="""
    whenever the question looks like incomplete or need clarity 
    chat history : {messages} ,
    generate a structure and well written response based on history 
    User query : {query}
    """
)

image_prompt = PromptTemplate(
    input_variables=[ "query" , "messages"] , 
    template="""
    whenever the question looks like incomplete or need clarity 
    chat history : {messages} ,
    generate a structure and well written response based on  history 
    User query : {query}

    instruction:
    For final answer return only image path without any surrounding extras
    """
)

