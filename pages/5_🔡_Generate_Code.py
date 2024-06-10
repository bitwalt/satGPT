import asyncio

import streamlit as st

from chat.assistant import ContextChatbot
from chat.utils import load_prompt_models, setup_prompt_model_selection
from utils import init_page
from openai import OpenAI
from lightning.utils import handle_payment
from chat.basic_chatbot import handle_chat


async def main():
    init_page(image_page=False)
    st.title("🔡 Generate Code")
    st.text(
        "Get code snippets for your programming needs using ChatGPT."
    )

    # Prompt Selection
    prompt_models = load_prompt_models()
    prompt_model = prompt_models["👩🏼‍💻 Code Assistant"]

    if st.session_state["prompt_model"] != prompt_model:
        st.session_state.prompt_model = prompt_model
        st.session_state.messages = [{"role": "system", "content": prompt_model.prompt_start}]

    with st.expander("Show Prompt"):
        st.write(prompt_model.prompt_start)

    await handle_chat()


if __name__ == "__main__":
    asyncio.run(main())
