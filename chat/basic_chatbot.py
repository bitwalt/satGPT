import streamlit as st
from openai import OpenAI

from chat.utils import PromptModel
from config import MAX_TOKENS
from lightning.utils import handle_payment


async def handle_chat(prompt_model: PromptModel):

    if st.session_state["prompt_model"] != prompt_model:
        st.session_state.prompt_model = prompt_model
        st.session_state.messages = [
            {"role": "system", "content": prompt_model.prompt_start}
        ]

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
        payment_received = await handle_payment(
            st.session_state.ln_processor, {"mode": "chat"}
        )
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
                    max_tokens=MAX_TOKENS,
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
