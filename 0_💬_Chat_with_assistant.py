import asyncio

import streamlit as st

from chat.assistant import ContextChatbot
from chat.utils import load_prompt_models, setup_prompt_model_selection
from utils import init_page
from openai import OpenAI
from lightning.utils import handle_payment



async def main():
    init_page(image_page=False)
    st.title("💬 Chat with assistants")
    st.text(
        "Chat with different GPTs assistants and pay with bitcoin using the Lightning Network."
    )

    # Prompt Selection
    prompt_models = load_prompt_models()
    prompt_models = {k: v for k, v in prompt_models.items() if v.name not in ["🌍 Translator", "👩🏼‍💻 Code Assistant"]}
    prompt_model = setup_prompt_model_selection(prompt_models)

    if st.session_state["prompt_model"] != prompt_model:
        st.session_state.prompt_model = prompt_model
        st.session_state.messages = [{"role": "system", "content": prompt_model.prompt_start}]

    with st.expander("Show Prompt"):
        st.write(prompt_model.prompt_start)

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message..."):
        payment_received = await handle_payment(st.session_state.ln_processor, {"mode": "chat"})
        if payment_received:
            st.balloons()
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],

                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    asyncio.run(main())
