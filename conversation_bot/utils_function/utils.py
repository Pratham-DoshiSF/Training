import os
from dotenv import load_dotenv
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
load_dotenv()

def get_llm():
    # return ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
    return ChatOpenAI(model="gpt-4o-mini")

def get_image_llm():
    return ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_IMG_MODEL"))

def extract_image_path(text: str) -> str | None:
    """Extracts file path if it looks like an image path."""
    match = re.search(r"(generated_images/\S+\.png)", text)
    return match.group(1) if match else None
