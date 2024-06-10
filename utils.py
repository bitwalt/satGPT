import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import streamlit as st
from streamlit_javascript import st_javascript

from chat.assistant import ContextChatbot
from config import *
from lightning.alby_processor import AlbyProcessor
from lightning.lnbits_processor import LnbitsProcessor


def init_cache():
    if "ln_processor" not in st.session_state:
        alby_key = st.secrets["ALBY_API_KEY"]
        st.session_state.ln_processor = AlbyProcessor(alby_key)
    if "prompt_model" not in st.session_state:
        st.session_state["prompt_model"] = None
    if "chatbot" not in st.session_state:
        st.session_state["chatbot"] = ContextChatbot()
    if "model_name" not in st.session_state:
        st.session_state["model_name"] = "gpt-3.5-turbo"
    if "login" not in st.session_state:
        st.session_state["login"] = False
    if "old_messages" not in st.session_state:
        st.session_state["old_messages"] = []


def add_support_message():
    st.sidebar.write("Support: [chat@in.pelliken.it](chat@in.pelliken.it)")


def init_page():
    init_cache()
    add_logo()
    add_support_message()


def add_logo():
    st_theme = st_javascript(
        """window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")"""
    )
    if st_theme == "dark":
        logo_path = os.path.join(os.getcwd(), LOGO_PATH_WHITE)
    else:
        logo_path = os.path.join(os.getcwd(), LOGO_PATH_BLACK)
    st.logo(logo_path, link="https://www.pelliken.it/")
    st.sidebar.image(logo_path, width=200)
