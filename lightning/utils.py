import io
import time

import qrcode
import requests
import streamlit as st
from PIL import Image

from config import DEV, PRICING


def generate_qr(url: str):
    img = qrcode.make(url)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    img = Image.open(img_bytes)
    return img


async def handle_payment(processor, cfg, debug=DEV):
    """Handle the payment process."""
    if debug:
        return True
    if not cfg:
        raise ValueError("Invalid configuration.")
    mode = cfg.get("mode")
    if mode == "image_generation":
        price = int(
            (PRICING.get("image_generation", 0) * cfg.get("num_of_images"))
            / get_sat_price()
        )
    else:
        price = int(PRICING.get(mode, 0) / get_sat_price())
    view = st.empty()
    if price == 0:
        st.warning("Invalid payment mode.")
        return False
    if not processor.active:
        st.warning("Processor not active.")
        return False
    payment_request = await processor.create_invoice(price, "Chatbot Payment")
    payment_hash = payment_request.get("payment_hash")
    invoice = payment_request.get("payment_request")
    view.write("Please pay the invoice below to continue:")
    view.text(invoice)
    payment_url = f"lightning:{invoice}"
    qr_image = generate_qr(payment_url)
    st.image(qr_image, width=300)
    view.write(f"Or click on this [Payment Link]({payment_url})")

    payment_received = False
    retry = 0
    with st.spinner("Waiting for payment... (2 minutes timeout)"):
        while not payment_received:
            has_paid = await processor.has_been_paid(payment_hash)
            if has_paid:
                payment_received = True
                view.empty()
                break
            else:
                retry += 1
                time.sleep(1)
                if retry > 120:
                    st.error("Payment elapsed. Please try again.")
                    break
    return payment_received


@st.cache_data(ttl=30)
def get_sat_price():
    # Get price of 1 BTC from bitfinex
    response = requests.get("https://api-pub.bitfinex.com/v2/ticker/tBTCUSD")
    btc_price = response.json()[2]
    # return price of 1 sat in usd
    return btc_price / 10**8
