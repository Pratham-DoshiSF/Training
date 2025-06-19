import os
import traceback
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from conversation_bot.utils_function.logger_utility import get_logger

load_dotenv()
logger = get_logger("Utils")

def get_llm():
    """Initializes the text-based LLM."""
    try:
        model = os.getenv("GOOGLE_MODEL")
        if not model:
            raise ValueError("Environment variable 'GOOGLE_MODEL' is not set.")
        
        logger.info(f"Initializing LLM with model: {model}")
        return ChatGoogleGenerativeAI(model=model)
    except Exception as e:
        logger.error(f"Failed to initialize text LLM: {e}")
        logger.debug(traceback.format_exc())
        raise e

def get_image_llm():
    """Initializes the image generation LLM."""
    try:
        model = os.getenv("GOOGLE_IMG_MODEL")
        if not model:
            raise ValueError("Environment variable 'GOOGLE_IMG_MODEL' is not set.")

        logger.info(f"Initializing image LLM with model: {model}")
        return ChatGoogleGenerativeAI(model=model)
    except Exception as e:
        logger.error(f"Failed to initialize image LLM: {e}")
        logger.debug(traceback.format_exc())
        raise e

