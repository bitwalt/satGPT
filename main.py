import os
import langchain
import streamlit as st
from config import MODELS, MAX_TOKENS, PRICE
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from utils import init_page, load_prompt_models, write_chat, StreamHandler, generate_qr
from lightning import LnbitsProcessor
import asyncio
import time


async def main():
    openai_api_key = init_page()
    lnbits_processor = LnbitsProcessor()
    model_name = st.session_state["model_name"]
    api_base = MODELS[model_name]

    st.title("⚡ Sat-GPT")

    prompt_models = load_prompt_models()

    assistant_role = st.selectbox(
        label="Select assistant", key="role", options=[p for p in prompt_models.keys()]
    )

    prompt_assistant = True if "Prompt Provider" == assistant_role else False
    add_prompt = True if "Add Prompt" == assistant_role else False

    prompt_model = prompt_models[assistant_role]

    if add_prompt:
        # Let the user add the prompt
        user_prompt = st.text_input("Please add your prompt here")
        prompt_model.prompt_start = user_prompt

    clean_chat = False
    if st.session_state["prompt_model"] != prompt_model:
        st.session_state.prompt_model = prompt_model
        clean_chat = True

    with st.expander("Show Prompt"):
        st.write(prompt_model.prompt_start)

    if clean_chat or "messages" not in st.session_state:
        st.session_state["messages"] = [
            ChatMessage(role="system", content=prompt_model.prompt_start),
            ChatMessage(role="assistant", content=prompt_model.welcome_message),
        ]

    write_chat()

    if prompt := st.chat_input():
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        st.chat_message("user").write(prompt)

        payment_request = await lnbits_processor.create_invoice(PRICE, "Chatbot Payment")
        payment_hash = payment_request.get("payment_hash")
        invoice = payment_request.get("payment_request")
        st.write("Please pay the invoice below to continue chatting")
        st.write(invoice)
        payment_url = f"lightning:{invoice}"
        qr_image = generate_qr(payment_url)
        st.image(qr_image, width=300)
        st.write(f"Or click on this [Payment Link]({payment_url})")

        payment_received = False
        retry = 0
        with st.spinner("Waiting for payment... (2 minutes timeout)"):
            while not payment_received:
                has_paid = await lnbits_processor.has_been_paid(payment_hash)
                if has_paid:
                    payment_received = True
                    break
                else:
                    retry += 1
                    time.sleep(1)
                    if retry > 120:
                        st.error("Payment elapsed. Please try again.")
                        break

        if payment_received:
            st.balloons()
            st.success("Payment received!")

            if not openai_api_key:
                st.info("OpenAI API not found!")
                st.stop()

            with st.chat_message("assistant"):
                container = st.empty()
                stream_handler = StreamHandler(container)
                llm = ChatOpenAI(
                    openai_api_key=openai_api_key,
                    openai_api_base=api_base,
                    streaming=True,
                    callbacks=[stream_handler],
                    max_tokens=MAX_TOKENS,
                )
                response = llm(st.session_state.messages)
                st.session_state.messages.append(
                    ChatMessage(role="assistant", content=response.content)
                )
                container.markdown(response.content)

                if prompt_assistant:
                    st.markdown(
                        "Select add prompt on the select list above and copy and paste the prompt if you are satisfied with it"
                    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
