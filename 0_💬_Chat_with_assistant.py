import asyncio

import streamlit as st

from chat.assistant import ContextChatbot
from chat.utils import load_prompt_models, setup_prompt_model_selection
from utils import init_page

st.set_page_config(page_title="SatGPT", page_icon="⚡")


async def main():
    init_page()
    st.title("💬 Chat with assistants")
    st.text(
        "Chat with different GPTs assistants and pay with bitcoin using the Lightning Network."
    )

    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ContextChatbot()

    chatbot: ContextChatbot = st.session_state.chatbot
    if not chatbot:
        st.error("Chatbot not initialized. Please restart the app.")
        return

    # Prompt Selection
    prompt_models = load_prompt_models()
    prompt_model = setup_prompt_model_selection(prompt_models)

    if st.session_state["prompt_model"] != prompt_model:
        st.session_state.prompt_model = prompt_model

    with st.expander("Show Prompt"):
        st.write(prompt_model.prompt_start)

    await chatbot.main(prompt_model)


if __name__ == "__main__":
    asyncio.run(main())
