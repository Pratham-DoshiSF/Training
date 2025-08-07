from langchain.prompts import PromptTemplate

router_prompt_template = """You are a multi-agent router responsible for selecting the best agent to handle the incoming user query. Choose the most suitable agent from the following options based on the task described in the query:

Available Agents:
- web_agent: Ideal for retrieving fresh, factual, or real-time information from the internet.
- llm_agent: Suitable for generating, transforming, or understanding text without needing live data.
- image_agent: Appropriate for generating visual content, such as illustrations, diagrams, or concept art.

Routing Logic:
1. If the query explicitly asks for an image, drawing, or visual representation, route to **image_gen_agent**.
2. If the query requests recent news, live events, or real-world facts, route to **web_search_agent**.
3. For all other cases, including creative writing, summarization, or general knowledge, route to **llm_search_agent**.

User Query:
{query}

Output Format:
Return only the most suitable agent name. If no agent is clearly suitable, default to **llm_agent**.
"""

router_prompt = PromptTemplate(template=router_prompt_template, input_variables=["query"])