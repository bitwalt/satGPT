import asyncio
import base64
import io

import aiohttp
import streamlit as st

from chat.utils import *
from lightning.utils import handle_payment
from replicate_api import restore_image, upscale_image
from utils import init_page

EDITOR_MODES = ["⏫ Upscale Images", "💫 Restore Images"]


async def process_image(editor_mode, image_b64, scaling_factor):
    if editor_mode == "⏫ Upscale Images":
        return upscale_image(image_b64, scaling_factor)
    elif editor_mode == "💫 Restore Images":
        return restore_image(image_b64, scaling_factor)


async def main():
    init_page(image_page=True)
    st.title("✏️ Editor Images")
    ln_processor = st.session_state["ln_processor"]
    editor_mode = st.selectbox("Select Editor Mode", EDITOR_MODES)
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        image = io.BytesIO(image_file.read())
        st.image(image, caption="Uploaded Image", use_column_width=True)
        image.seek(0)
        image_b64 = base64.b64encode(image.read()).decode("utf-8")
    else:
        st.warning("Please upload an image.")
        st.stop()

    scaling_factor = st.select_slider("Scaling Factor", options=[2, 3, 5, 10], value=2)
    restored_image = None
    if st.button("Edit Image"):
        if ln_processor:
            cfg = {"mode": "image_editor"}
            payment_received = await handle_payment(ln_processor, cfg)
            if not payment_received:
                st.error("Payment failed or was not completed. Please try again.")
                st.stop()
            else:
                st.balloons()
                with st.spinner("Generating images..."):
                    restored_image = await process_image(
                        editor_mode, image_b64, scaling_factor
                    )
                    st.session_state["restored_image"] = restored_image
                    if not restored_image:
                        st.warning("Failed to restore the image.")

    last_restored_image = st.session_state.get("restored_image")
    if last_restored_image is not None:
        st.subheader("Last Restored Image")
        st.image(last_restored_image, caption="Restored Image", use_column_width=True)

        # Download image from URL
        image_data = await download_image(last_restored_image)
        image_bytes = io.BytesIO(image_data)
        image_name = "restored_image.png"

        # Provide download button
        st.download_button(
            label="Download Image",
            data=image_bytes,
            file_name=image_name,
            mime="image/png",
        )


async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise Exception(f"Failed to download image: {response.status}")


def start():
    asyncio.run(main())


if __name__ == "__main__":
    start()
