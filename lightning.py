import asyncio
from aiohttp.client import ClientSession
from pylnbits.config import Config
from pylnbits.user_wallet import UserWallet
import streamlit as st


class LnbitsProcessor:
    def __init__(self) -> None:
        self.cfg = Config(
            in_key=st.secrets["LNBITS_INVOICE_KEY"],
            admin_key=st.secrets["LNBITS_ADMIN_KEY"],
            lnbits_url=st.secrets["LNBITS_URL"],
        )

    async def create_invoice(self, amt: int, memo: str, webhook: str = "") -> dict:
        async with ClientSession() as session:
            uw = UserWallet(self.cfg, session)
            invoice = await uw.create_invoice(
                direction=False, amt=amt, memo=memo, webhook=webhook
            )
            return invoice

    async def check_invoice(self, payment_hash: str):
        async with ClientSession() as session:
            uw = UserWallet(self.cfg, session)
            invoice_result = await uw.check_invoice(payment_hash)
            return invoice_result


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        LnbitsProcessor(cfg).check_invoice(
            "abf873c905f1f7f31a921fbe499c09ad86913552bb93c4e39b83307454b8796c"
        )
    )
