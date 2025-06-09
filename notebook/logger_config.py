# logger_config.py

from loguru import logger
import sys
from pathlib import Path

# Create logs directory
Path("logs").mkdir(exist_ok=True)

# Remove default
logger.remove()

# Console Logger
logger.add(sys.stdout, level="DEBUG", colorize=True,
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
                  "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

# File Logger with rotation
logger.add("logs/app.log", level="DEBUG", rotation="1 day", retention="7 days", compression="zip",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}")
