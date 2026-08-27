"""PaymentProcessor contract plus Card and UPI implementations.

RentalService depends only on the PaymentProcessor interface,
never on a specific payment class (dependency inversion).
"""

from abc import ABC, abstractmethod


class PaymentError(Exception):
    """Raised when a payment cannot be completed."""


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        """Attempt to charge `amount`. Returns a transaction reference.

        Raises PaymentError if the payment fails.
        """
        raise NotImplementedError


class CardPayment(PaymentProcessor):
    def __init__(self, card_number: str):
        if len(card_number) < 4:
            raise ValueError("Card number looks invalid.")
        # Never store sensitive details in plain text -- keep only a masked form.
        self._masked_card = "**** **** **** " + card_number[-4:]

    def process_payment(self, amount: float) -> str:
        if amount <= 0:
            raise PaymentError("Payment amount must be greater than zero.")
        # Simulated gateway call.
        return f"CARD-TXN using {self._masked_card} for Rs. {amount:,.2f}"


class UpiPayment(PaymentProcessor):
    def __init__(self, upi_id: str):
        if "@" not in upi_id:
            raise ValueError("UPI ID looks invalid.")
        self._upi_id = upi_id

    def process_payment(self, amount: float) -> str:
        if amount <= 0:
            raise PaymentError("Payment amount must be greater than zero.")
        # Simulated gateway call.
        return f"UPI-TXN via {self._upi_id} for Rs. {amount:,.2f}"