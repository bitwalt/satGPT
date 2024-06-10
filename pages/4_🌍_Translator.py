import asyncio

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage

from chat.utils import *
from config import MAX_TOKENS, MODELS, PRICE
from utils import init_page


async def main():
    init_page()
    st.title("🌍 Translator")
    model_name = st.session_state["model_name"]
    api_base = MODELS[model_name]

    llm = ChatOpenAI(
        openai_api_key=st.session_state["OPENAI_API_KEY"],
        openai_api_base=api_base,
        max_tokens=MAX_TOKENS,
    )

    # Prompt Selection
    clean_chat = False
    prompt_models = load_prompt_models()
    prompt_model = prompt_models["🌍 Translator"]

    with st.expander("Show Prompt"):
        st.write(prompt_model.prompt_start)

    if clean_chat or "messages" not in st.session_state:
        st.session_state["messages"] = [
            ChatMessage(role="system", content=prompt_model.prompt_start),
            ChatMessage(role="assistant", content=prompt_model.welcome_message),
        ]

    write_chat()

    await handle_chat_interaction(llm, prompt_model)


if __name__ == "__main__":
    asyncio.run(main())
