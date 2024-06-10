from abc import ABC, abstractmethod


class Processor(ABC):
    def __init__(self):
        self.active = False

    @abstractmethod
    async def create_invoice(self, amt: int, memo: str, webhook: str = "") -> dict:
        pass

    @abstractmethod
    async def has_been_paid(self, payment_hash: str) -> bool:
        pass
