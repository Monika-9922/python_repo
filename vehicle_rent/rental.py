"""Rental record: composes a Customer, a Vehicle, and payment/return info."""

from datetime import date


class RentalError(Exception):
    """Raised for invalid rental operations (bad days, unavailable vehicle, etc.)."""


class Rental:
    LATE_FEE_RATE = 1.20  # 120% of daily rate per late day

    def __init__(self, rental_id: str, customer, vehicle, days: int,
                 start_date: date = None):
        if days <= 0:
            raise RentalError("Rental days must be greater than zero.")
        if not vehicle.is_available:
            raise RentalError(f"Vehicle {vehicle.vehicle_id} is unavailable.")

        self._rental_id = rental_id
        self._customer = customer
        self._vehicle = vehicle
        self._days = days
        self._start_date = start_date or date.today()
        self._base_amount = vehicle.calculate_rental_cost(days)
        self._late_fee = 0.0
        self._final_amount = self._base_amount
        self._status = "PENDING_PAYMENT"
        self._payment_reference = None
        self._return_date = None

    # ---- read-only access ----
    @property
    def rental_id(self) -> str:
        return self._rental_id

    @property
    def start_date(self) -> date:
        return self._start_date

    @property
    def base_amount(self) -> float:
        return self._base_amount

    @property
    def late_fee(self) -> float:
        return self._late_fee

    @property
    def final_amount(self) -> float:
        return self._final_amount

    @property
    def status(self) -> str:
        return self._status

    @property
    def customer(self):
        return self._customer

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def days(self) -> int:
        return self._days

    # ---- workflow ----
    def confirm_with_payment(self, payment_processor) -> None:
        """Charges the customer, then confirms the rental only on success."""
        self._payment_reference = payment_processor.process_payment(self._base_amount)
        self._vehicle.mark_as_rented()
        self._status = "ACTIVE"
        self._customer.add_rental(self)

    def complete_rental(self, return_date: date = None) -> None:
        """Records the return, calculates late fee, and frees up the vehicle."""
        if self._status != "ACTIVE":
            raise RentalError("Only an active rental can be returned.")

        self._return_date = return_date or date.today()
        expected_return = self._start_date.toordinal() + self._days
        actual_return = self._return_date.toordinal()
        late_days = max(0, actual_return - expected_return)

        self._late_fee = late_days * self.LATE_FEE_RATE * self._vehicle.daily_rate
        self._final_amount = self._base_amount + self._late_fee
        self._vehicle.mark_as_available()
        self._status = "COMPLETED"

    def summary(self) -> str:
        return (f"{self._rental_id} | {self._vehicle.vehicle_type()} "
                f"{self._vehicle.brand} {self._vehicle.model} | {self._days} day(s) "
                f"| Status: {self._status} | Final: Rs. {self._final_amount:,.2f}")