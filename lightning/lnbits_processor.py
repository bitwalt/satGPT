import asyncio

from aiohttp.client import ClientSession
from pylnbits.config import Config
from pylnbits.user_wallet import UserWallet

from lightning.processor import Processor


class LnbitsProcessor(Processor):
    def __init__(self, in_key, admin_key, lnbits_url) -> None:
        self.cfg = Config(
            in_key=in_key,
            admin_key=admin_key,
            lnbits_url=lnbits_url,
        )
        self.active = False

    async def create_invoice(self, amt: int, memo: str, webhook: str = "") -> dict:
        async with ClientSession() as session:
            uw = UserWallet(self.cfg, session)
            invoice = await uw.create_invoice(
                direction=False, amt=amt, memo=memo, webhook=webhook
            )
            return invoice

    async def has_been_paid(self, payment_hash: str) -> bool:
        async with ClientSession() as session:
            uw = UserWallet(self.cfg, session)
            invoice_result = await uw.check_invoice(payment_hash)
            if "paid" in invoice_result and invoice_result["paid"] is True:
                return True
            else:
                return False


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        LnbitsProcessor(cfg).check_invoice(
            "abf873c905f1f7f31a921fbe499c09ad86913552bb93c4e39b83307454b8796c"
        )
    )
