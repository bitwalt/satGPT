import asyncio

import streamlit as st

from chat.basic_chatbot import handle_chat
from chat.utils import load_prompt_models
from utils import init_page


async def main():
    init_page(image_page=False)
    st.title("🔡 Generate Code")
    st.text("Get code snippets for your programming needs using ChatGPT.")

    prompt_models = load_prompt_models()
    prompt_model = prompt_models["👩🏼‍💻 Code Assistant"]

    await handle_chat(prompt_model)


if __name__ == "__main__":
    asyncio.run(main())
