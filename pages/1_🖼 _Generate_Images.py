import asyncio
import base64
import os
from typing import List

import requests
import streamlit as st
from openai import OpenAI

from config import *
from lightning.utils import handle_payment
from utils import init_page

client = OpenAI()


def generate_images(
    model: str, prompt: str, n: int = 1, size: str = "256x256"
) -> List[str]:
    """Generate images from prompt and return base64 encoded images"""
    if not size:
        size = "256x256"
    if not n:
        n = 1
    if size not in IMAGE_SIZE.keys():
        raise ValueError(f"Size {size} not found")
    if n < 1 or n > 4:
        raise ValueError(f"n must be between 1 and 4")
    if len(prompt) < 1:
        raise ValueError(f"Prompt must be at least 1 character long")
    if len(prompt) > 1000:
        raise ValueError(f"Prompt must be at most 1000 characters long")
    images = []
    model_name = "dall-e-3" if model.startswith("DALL-E 3") else "dall-e-2"
    quality = "hd" if model.endswith("HD") else "standard"
    try:
        response = client.images.generate(
            model=model_name, quality=quality, prompt=prompt, n=n, size=size
        )
        if not response:
            raise ValueError("No images generated")

        for image_response in response.data:
            image_url = image_response.url
            response = requests.get(image_url)
            image = base64.b64encode(response.content).decode("utf-8")
            images.append(image)
    except Exception as e:
        st.error(e)
    return images


def get_download_image_link(image, filename, text):
    b64 = base64.b64encode(image).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'
    return href


async def image_generation() -> None:
    init_page(image_page=True)
    st.title("🖼 Generate Images")
    input_text = st.text_input(
        "Insert text to generate an image",
        value="Iron man portrait, highly detailed, science fiction landscape",
    )
    # image_model = st.selectbox("Select model", [i for i in IMAGE_MODELS.keys()])
    image_model = "DALL-E 2"
    num_of_images = st.number_input("Number of images", min_value=1, step=1)
    image_size = st.selectbox(
        "Select image size", options=[i for i in IMAGE_MODELS[image_model].keys()]
    )
    ln_processor = st.session_state["ln_processor"]
    cfg = {
        "model": image_model,
        "num_of_images": num_of_images,
        "image_size": image_size,
        "mode": "image_generation",
    }
    if st.button("Generate Images"):
        payment_received = await handle_payment(ln_processor, cfg)
        if payment_received:
            st.balloons()
            st.success("Payment successful! Generating images...")
            with st.spinner("Generating images..."):
                images = generate_images(
                    image_model, input_text, int(num_of_images), str(image_size)
                )
                if not images:
                    st.error("No images generated")
                st.subheader("Images")
                for i, image in enumerate(images):
                    decoded_image = base64.b64decode(image)
                    width = int(image_size.split("x")[0])
                    st.image(decoded_image, width=width)
                    # Download image
                    image_name = f"{input_text.replace(' ', '_')}_image_{i}.png"
                    st.markdown(
                        get_download_image_link(
                            decoded_image, image_name, "Download Image"
                        ),
                        unsafe_allow_html=True,
                    )
        else:
            st.error("Payment failed or was not completed. Please try again.")


if __name__ == "__main__":
    asyncio.run(image_generation())
