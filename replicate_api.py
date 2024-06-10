import os

import replicate
import requests
import streamlit as st

# Set the Replicate API token from Streamlit secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

# Constants for model versions
FACE_RESTORE_MODEL = (
    "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c"
)
UPSCALE_MODEL = "nightmareai/real-esrgan:350d32041630ffbe63c8352783a26d94126809164e54085352f8326e53999085"


def get_api_headers():
    """Retrieve the API headers for making requests to the Replicate API."""
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        raise ValueError("API token is not set in the environment variables.")
    return {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }


def restore_image_http(base64_image: str, scale: int):
    """Restore an image using an HTTP request to the Replicate API."""
    headers = get_api_headers()
    image_data = f"data:application/octet-stream;base64,{base64_image}"

    data = {
        "version": "0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
        "input": {
            "img": image_data,
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
        response.raise_for_status()  # Raise an HTTPError if the request returned an unsuccessful status code


def restore_image(base64_image: str, scaling_factor: int):
    """Restore an image using the Replicate library."""
    image_data = f"data:application/octet-stream;base64,{base64_image}"
    input_data = {
        "img": image_data,
        "scale": scaling_factor,
    }
    return replicate.run(FACE_RESTORE_MODEL, input=input_data)


def upscale_image(base64_image: str, scaling_factor: int):
    """Upscale an image using the Replicate library."""
    image_data = f"data:application/octet-stream;base64,{base64_image}"
    upscale_input = {
        "image": image_data,
        "scale": scaling_factor,
    }
    return replicate.run(UPSCALE_MODEL, input=upscale_input)
