from langchain.agents import Tool
from pathlib import Path
import uuid
import base64
from langchain_core.messages import HumanMessage

from conversation_bot.utils_function.utils import get_image_llm

image_llm = get_image_llm()

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

def image_gen_func(query: str) -> str:
    """Generate image and return image path (not base64)."""
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
        return "ERROR: No image generated."

    image_url = image_block["image_url"]["url"]
    image_base64 = image_url.split(",")[-1]
    image_bytes = base64.b64decode(image_base64)

    # Save image
    image_id = f"{uuid.uuid4().hex}.png"
    image_path = OUTPUT_DIR / image_id

    with open(image_path, "wb") as f:
        f.write(image_bytes)

    return image_path

image_tool = Tool(
    name="ImageGen",
    func=image_gen_func,
    description="Generates an image based on a textual description."
)
image_gen_func("image of cat and dog")
