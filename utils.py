import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import streamlit as st
from streamlit_javascript import st_javascript

from chat.assistant import ContextChatbot
from config import *
from lightning.alby_processor import AlbyProcessor
from lightning.lnbits_processor import LnbitsProcessor
import json 

def init_cache():
    if "ln_processor" not in st.session_state:
        alby_key = st.secrets["ALBY_API_KEY"]
        st.session_state.ln_processor = AlbyProcessor(alby_key)
    if "prompt_model" not in st.session_state:
        st.session_state["prompt_model"] = None
    if "chatbot" not in st.session_state:
        st.session_state["chatbot"] = ContextChatbot(None)
    if "model_name" not in st.session_state:
        st.session_state["model_name"] = "gpt-3.5-turbo"
    if "login" not in st.session_state:
        st.session_state["login"] = False
    if "messages" not in st.session_state:
        st.session_state["messages"] = []


def add_support_message():
    st.sidebar.write("Support: [Telegram group](https://t.me/+84Fwhhg3VyU3Mjdk)")

def add_warning_message(image_page=False):
    if image_page:
        return 
    st.sidebar.warning("Note: when you refresh the page, all messages are lost. Copy them manually or download the chat.")
    # Add a downlaod button to downlaod the chat history as a text file
    if st.session_state["messages"]:
        chat_history = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state["messages"] if msg["role"] != "system"]
        )
        st.sidebar.download_button(
            label="Download Chat History",
            data=chat_history,
            file_name="chat_history.txt",
            mime="text/plain"
        )
    
def init_page(image_page=False):
    st.set_page_config(page_title="PellikenAI", page_icon="⚡")
    init_cache()
    add_logo()
    add_warning_message(image_page=image_page)
    add_support_message()


def add_logo():
    st_theme = st_javascript(
        """window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")"""
    )
    if st_theme == "dark":
        logo_path = os.path.join(os.getcwd(), LOGO_PATH_WHITE)
    else:
        logo_path = os.path.join(os.getcwd(), LOGO_PATH_BLACK)
    logo_path = "./data/pelliken_logo2.png"
    st.logo(logo_path, link="https://www.pelliken.it/")
    # st.sidebar.image(logo_path, width=200)
