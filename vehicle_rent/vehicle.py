"""Vehicle hierarchy: abstract Vehicle plus Car, Bike, and Van."""

from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Abstract base class for all rentable vehicles.

    Holds the data and behaviour every vehicle type shares.
    Subclasses only need to implement calculate_rental_cost().
    """

    def __init__(self, vehicle_id: str, registration_number: str,
                 brand: str, model: str, daily_rate: float):
        if not registration_number.strip():
            raise ValueError("Registration number cannot be empty.")
        if daily_rate <= 0:
            raise ValueError("Daily rate must be greater than zero.")

        self._vehicle_id = vehicle_id
        self._registration_number = registration_number
        self._brand = brand
        self._model = model
        self._daily_rate = daily_rate
        self._available = True

    # ---- read-only access to private fields (encapsulation) ----
    @property
    def vehicle_id(self) -> str:
        return self._vehicle_id

    @property
    def brand(self) -> str:
        return self._brand

    @property
    def model(self) -> str:
        return self._model

    @property
    def daily_rate(self) -> float:
        return self._daily_rate

    @property
    def is_available(self) -> bool:
        return self._available

    # ---- behaviour ----
    @abstractmethod
    def calculate_rental_cost(self, days: int) -> float:
        """Each vehicle type prices itself differently (polymorphism)."""
        raise NotImplementedError

    def vehicle_type(self) -> str:
        return self.__class__.__name__

    def mark_as_rented(self) -> None:
        if not self._available:
            raise RuntimeError(f"Vehicle {self._vehicle_id} is already rented.")
        self._available = False

    def mark_as_available(self) -> None:
        self._available = True

    def display_details(self) -> str:
        status = "Available" if self._available else "Rented"
        return (f"{self._vehicle_id} | {self.vehicle_type()} | {self._brand} "
                f"{self._model} | Rs. {self._daily_rate:,.0f} per day | {status}")


class Car(Vehicle):
    """Standard pricing: daily rate x number of days."""

    def calculate_rental_cost(self, days: int) -> float:
        return self._daily_rate * days


class Bike(Vehicle):
    """5% discount is applied when the rental runs longer than 5 days."""

    DISCOUNT_THRESHOLD_DAYS = 5
    DISCOUNT_RATE = 0.05

    def calculate_rental_cost(self, days: int) -> float:
        cost = self._daily_rate * days
        if days > self.DISCOUNT_THRESHOLD_DAYS:
            cost -= cost * self.DISCOUNT_RATE
        return cost


class Van(Vehicle):
    """Daily rate plus a fixed service charge."""

    def __init__(self, vehicle_id: str, registration_number: str,
                 brand: str, model: str, daily_rate: float, service_charge: float):
        super().__init__(vehicle_id, registration_number, brand, model, daily_rate)
        if service_charge < 0:
            raise ValueError("Service charge cannot be negative.")
        self._service_charge = service_charge

    def calculate_rental_cost(self, days: int) -> float:
        return (self._daily_rate * days) + self._service_charge