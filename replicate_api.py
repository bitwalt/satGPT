import os

import replicate
import requests
import streamlit as st

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

FACE_RESTORE_MODEL = (
    "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c"
)


def restore_image_http(base64_image: str, scale: int):
    # Get the API token from an environment variable
    api_token = st.secrets["REPLICATE_API_TOKEN"]
    if not api_token:
        raise ValueError("API token is not set in the environment variables.")

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    image_data = f"data:application/octet-stream;base64,{base64_image}"

    data = {
        "version": "0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
        "input": {
            "img": image_data,  # Assuming the image is already a Base64 string
            "scale": scale,
            "version": "v1.4",
        },
    }

    response = requests.post(
        "https://api.replicate.com/v1/predictions", json=data, headers=headers
    )

    if response.status_code == 200:
        return response.json()  # Return the JSON response if successful
    else:
        return response.text  # Return the text response in case of an error


def restore_image(base64_image: str, scaling_factor: int):
    image_data = f"data:application/octet-stream;base64,{base64_image}"
    input = {
        "img": image_data,
        "scale": scaling_factor,
    }
    return replicate.run(FACE_RESTORE_MODEL, input=input)


def upscale_image(base64_image, scaling_factor):
    upscale_model = "nightmareai/real-esrgan:350d32041630ffbe63c8352783a26d94126809164e54085352f8326e53999085"
    image_data = f"data:application/octet-stream;base64,{base64_image}"
    upscale_input = {
        "image": image_data,
        "scale": scaling_factor,
    }
    return replicate.run(upscale_model, input=upscale_input)
