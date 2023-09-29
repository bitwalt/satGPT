import base64
import io

import langchain
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st
import yaml
from config import CHAT_MODELS, MODELS
from PIL import Image
import qrcode


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


def init_cache():
    # Store the API key in session state
    if "OPENAI_API_KEY" not in st.session_state:
        st.session_state.OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

    if "prompt_model" not in st.session_state:
        st.session_state["prompt_model"] = None
    if "model_name" not in st.session_state:
        st.session_state["model_name"] = "gpt-3.5-turbo"
    if "login" not in st.session_state:
        st.session_state["login"] = False


def write_chat():
    if "messages" in st.session_state:
        for msg in st.session_state.messages:
            if msg.role == "system":
                continue
            st.chat_message(msg.role).write(msg.content)


def init_page():
    init_cache()
    st.set_page_config(page_title="SatGPT", page_icon="🔍", layout="wide")
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    st.session_state["OPENAI_API_KEY"] = openai_api_key
    if not openai_api_key:
        st.warning("Invalid OpenAI API Key, please check environment variables.")
        st.stop()
    model_name = st.sidebar.selectbox("Model", options=list(MODELS.keys()))
    st.session_state["model_name"] = model_name
    return openai_api_key


def generate_qr(url: str):
    # Genera il codice QR
    img = qrcode.make(url)
    # Covert image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    # Reimposta la posizione del cursore all'inizio del file
    img_bytes.seek(0)
    # Leggi l'immagine da BytesIO
    img = Image.open(img_bytes)
    return img


@dataclass
class PromptModel:
    name: str
    welcome_message: str
    prompt_start: str


def load_prompt_models() -> Dict[str, PromptModel]:
    models = {}
    # load yaml config
    with open(CHAT_MODELS, "r") as f:
        config_yaml = yaml.safe_load(f)

        for value in config_yaml["models"].values():
            model = PromptModel(
                name=value["name"],
                welcome_message=value["welcome_message"],
                prompt_start=value["prompt_start"],
            )
            models[value["name"]] = model
    return models
