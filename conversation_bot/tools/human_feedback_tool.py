from langchain_core.tools import tool
from langgraph.types import interrupt

@tool
def human_feedback(query: str) -> str:
    """
    Requests clarification or more details from the user for the given query.
    Logs all key steps for easier debugging.

    Parameters:
    - query (str): The ambiguous or unclear input/query.

    Returns:
    - str: User's feedback or clarification.
    """

    
    print("\n[🔎 Awaiting human input for clarification...]\n")
    prompt = f"❓ Please clarify: {query}"

    try:
        user_feedback = interrupt({query})
        print("[✅ Received human clarification]\n")
        return user_feedback

    except Exception as e:
        raise e