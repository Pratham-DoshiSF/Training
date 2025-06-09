from langchain_core.tools import tool
from pathlib import Path
import uuid
import base64
from langchain_core.messages import HumanMessage
from conversation_bot.utils_function.utils import get_image_llm

image_llm = get_image_llm()
OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

@tool
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

    # Decode base64 image content
    image_url = image_block["image_url"]["url"]
    if not image_url.startswith("data:image"):
        return "ERROR: Unexpected image format."

    image_base64 = image_url.split(",")[-1]
    try:
        image_bytes = base64.b64decode(image_base64)
    except base64.binascii.Error:
        return "ERROR: Failed to decode image."

    image_id = f"{uuid.uuid4().hex}.png"
    image_path = OUTPUT_DIR / image_id
    with open(image_path, "wb") as f:
        f.write(image_bytes)

    return str(image_path)


# Example usage
# if __name__ == "__main__":
#     result = image_gen_func("image of cat and dog")
#     print(result)

