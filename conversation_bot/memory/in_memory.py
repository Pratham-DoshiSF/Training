from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from conversation_bot.utils_function.logger_utility import get_logger
import traceback

logger = get_logger("MongoCheckpointer")

load_dotenv()

try:
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not found in environment variables.")

    client = MongoClient(mongo_uri)
    checkpointer = MongoDBSaver(client)

    logger.info("MongoDB checkpointer initialized successfully.")

except Exception as e:
    logger.error(f"Failed to initialize MongoDB checkpointer: {e}")
    logger.debug(traceback.format_exc())
    checkpointer = None  
