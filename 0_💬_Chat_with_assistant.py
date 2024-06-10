import asyncio

import streamlit as st

from chat.basic_chatbot import handle_chat
from chat.utils import load_prompt_models, setup_prompt_model_selection
from utils import init_page


async def main():
    init_page(image_page=False)
    st.title("💬 Chat with assistants")
    st.text(
        "Chat with different GPTs assistants and pay with bitcoin using the Lightning Network."
    )

    # Prompt Selection
    prompt_models = load_prompt_models()
    prompt_models = {
        k: v
        for k, v in prompt_models.items()
        if v.name not in ["🌍 Translator", "👩🏼‍💻 Code Assistant"]
    }
    prompt_model = setup_prompt_model_selection(prompt_models)

    await handle_chat(prompt_model)


if __name__ == "__main__":
    asyncio.run(main())
