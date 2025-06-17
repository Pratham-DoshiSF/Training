from PIL import Image
import os
import streamlit as st
last_message = "generated_images/fd7c5c29c4a0474287503e2c328f4631.png"

if os.path.exists(last_message):
    try:
        image_obj = Image.open(last_message)
        st.image(image_obj, caption="🖼️ Generated Image")
    except Exception as e:
        st.warning(f"Image file found, but couldn't open it: {e}")
else:
    st.warning(f"⚠️ Image not found at path: `{last_message}`")
