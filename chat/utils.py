import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import langchain
import openai
import streamlit as st
import yaml
from langchain.schema import ChatMessage

from chat.streaming import StreamHandler
from config import *
from lightning.utils import handle_payment


# decorator
async def enable_chat_history(func):
    if st.secrets.get("OPENAI_API_KEY"):

        # to clear chat history after swtching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "How can I help you?"}
            ]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    async def execute(*args, **kwargs):
        func(*args, **kwargs)

    return await execute


def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)


async def handle_chat_interaction(llm, prompt_model):
    """Handle the chat interaction logic."""
    ln_processor = st.session_state["ln_processor"]
    if prompt := st.chat_input():
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        # write_chat()
        cfg = {"mode": "chat"}
        payment_received = await handle_payment(ln_processor, cfg)
        if payment_received:
            if ln_processor.active:
                st.balloons()
                st.success("Payment received!")
            process_chat_response(llm, prompt_model)


def process_chat_response(llm, prompt_model):
    """Process and display chat response."""
    with st.chat_message("assistant"):
        container = st.empty()
        stream_handler = StreamHandler(container)
        llm.streaming = True
        llm.callbacks = [stream_handler]
        response = llm(st.session_state.messages)
        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response.content)
        )
        container.markdown(response.content)


def setup_prompt_model_selection(prompt_models):
    """Set up UI for selecting prompt model and managing the prompt."""
    assistant_role = st.selectbox(
        label="Select assistant", key="role", options=list(prompt_models.keys())
    )
    prompt_model = prompt_models[assistant_role]
    return prompt_model


def write_chat():
    if "messages" in st.session_state:
        for msg in st.session_state.messages:
            if msg.role == "system":
                continue
            st.chat_message(msg.role).write(msg.content)


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
        if not config_yaml:
            raise Exception("No models found in config file.")
        for value in config_yaml["models"].values():
            model = PromptModel(
                name=value["name"],
                welcome_message=value["welcome_message"],
                prompt_start=value["prompt_start"],
            )
            models[value["name"]] = model
    return models
