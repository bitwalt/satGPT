import asyncio

import aiohttp

from lightning.processor import Processor


class AlbyProcessor(Processor):
    BASE_URL = "https://api.getalby.com"

    def __init__(self, api_key: str):
        super().__init__()
        self.token = api_key
        self.active = True
        self.session = None

    async def init_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def create_invoice(
        self,
        amt: int,
        memo: str,
        description: str = "",
        description_hash: str = "",
        currency: str = "btc",
        comment: str = "",
        metadata: dict = {},
        payer_name: str = "",
        payer_email: str = "",
        payer_pubkey: str = "",
    ) -> dict:
        await self.init_session()
        url = f"{self.BASE_URL}/invoices"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        data = {
            "amount": amt,
            "memo": memo,
            "description": description,
            "description_hash": description_hash,
            "currency": currency,
            "comment": comment,
            "metadata": metadata,
            "payer_name": payer_name,
            "payer_email": payer_email,
            "payer_pubkey": payer_pubkey,
        }

        async with self.session.post(url, headers=headers, json=data) as response:
            if response.status in [200, 201]:
                return await response.json()
            else:
                response_text = await response.text()
                raise Exception(
                    f"Error creating invoice: {response.status} - {response_text}"
                )

    async def has_been_paid(self, payment_hash: str) -> bool:
        await self.init_session()
        url = f"{self.BASE_URL}/invoices/{payment_hash}"
        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        async with self.session.get(url, headers=headers) as response:
            if response.status in [200, 201]:
                invoice = await response.json()
                return invoice.get("settled", False)
            elif response.status == 404:
                return False
            else:
                response_text = await response.text()
                raise Exception(
                    f"Error checking invoice status: {response.status} - {response_text}"
                )

    async def get_invoice(self, payment_hash: str) -> dict:
        await self.init_session()
        url = f"{self.BASE_URL}/invoices/{payment_hash}"
        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                response_text = await response.text()
                raise Exception(
                    f"Error retrieving invoice: {response.status} - {response_text}"
                )

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


async def main():
    cfg = {"token": "your_api_key_here"}
    alby_processor = AlbyProcessor(cfg["token"])

    try:
        # Create an invoice
        invoice = await alby_processor.create_invoice(
            amt=1000, memo="Test Invoice", description="This is a test"
        )
        print(invoice)

        # Check if the invoice has been paid
        payment_hash = invoice["payment_hash"]
        paid = await alby_processor.has_been_paid(payment_hash)
        print(f"Has been paid: {paid}")

        # Get invoice details
        invoice_details = await alby_processor.get_invoice(payment_hash)
        print(invoice_details)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await alby_processor.close()


if __name__ == "__main__":
    asyncio.run(main())
