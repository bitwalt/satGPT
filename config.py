import os

import streamlit as st

DEV = st.secrets["DEV"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
ALBY_API_KEY = st.secrets["ALBY_API_KEY"]

CHAT_MODELS = "./data/models.yml"
MAX_TOKENS = 1000

LOGO_PATH_WHITE = "./data/pelliken_logo.png"
LOGO_PATH_BLACK = "./data/pelliken_logo2.png"

IMAGE_SIZE = {"SMALL": "256x256", "MEDIUM": "512x512", "LARGE": "1024x1024"}
IMAGE_MODELS = ["DALLE-2", "DALLE-3"]

PRICING = {
    "image_editor": 0.05,
    "image_generation": 0.20,
    "chat": 0.03,
}


IMAGE_SIZE = {
    "1024x1024": "Standard (1024x1024)",
    "1024x1792": "Wide (1024x1792)",
    "1792x1024": "Wide (1792x1024)",
    "512x512": "Medium (512x512)",
    "256x256": "Small (256x256)",
}

IMAGE_MODELS = {
    "DALL-E 3 Standard": {"1024x1024": 0.040, "1024x1792": 0.080, "1792x1024": 0.080},
    "DALL-E 3 HD": {"1024x1024": 0.080, "1024x1792": 0.120, "1792x1024": 0.120},
    "DALL-E 2": {"1024x1024": 0.020, "512x512": 0.018, "256x256": 0.016},
}

FEES = 0.01
