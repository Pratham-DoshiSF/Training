from langchain_core.tools import tool
from pathlib import Path
import uuid
import base64
from langchain_core.messages import HumanMessage
from conversation_bot.utils_function.utils import get_image_llm
from conversation_bot.utils_function.logger_utility import get_logger
import traceback

logger = get_logger("ImageTool")

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

def image_tool(image_llm):
    @tool
    def image_gen_func(query: str) -> str:
        """Generate image and return image path (not base64)."""
        try:
            enhanced_query = (
                "Create an image illustrating the following concept:\n\n"
                f"{query}\n\n"
                "All text in the image must be in English only. "
                "Avoid including foreign characters."
            )

            message = [HumanMessage(content=enhanced_query)]
            response = image_llm.invoke(
                message,
                generation_config={"response_modalities": ["TEXT", "IMAGE"]}
            )

            image_block = next(
                (block for block in response.content if isinstance(block, dict) and block.get("image_url")),
                None
            )

            if not image_block:
                logger.warning("Image generation failed: No image block returned.")
                return "ERROR: No image generated."

            image_url = image_block["image_url"]["url"]
            if not image_url.startswith("data:image"):
                logger.error(f"Unexpected image format returned: {image_url[:30]}...")
                return "ERROR: Unexpected image format."

            image_base64 = image_url.split(",")[-1]

            try:
                image_bytes = base64.b64decode(image_base64)
            except base64.binascii.Error as decode_error:
                logger.error(f"Failed to decode image base64: {decode_error}")
                return "ERROR: Failed to decode image."

            image_id = f"{uuid.uuid4().hex}.png"
            image_path = OUTPUT_DIR / image_id
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            logger.info(f"Image successfully saved at {image_path}")
            return str(image_path)

        except Exception as e:
            logger.error(f"Unhandled exception in image_gen_func: {e}")
            logger.debug(traceback.format_exc())
            return "ERROR: Image generation failed."

    return image_gen_func
