"""RentalService: coordinates vehicles, customers, and rentals.

Depends on the PaymentProcessor interface only -- never on a concrete
payment class -- which is the dependency-inversion piece of the design.
"""

from rental import Rental, RentalError
from payment import PaymentProcessor, PaymentError


class RentalService:
    def __init__(self):
        self._vehicles = {}   # vehicle_id -> Vehicle
        self._customers = {}  # customer_id -> Customer
        self._rentals = {}    # rental_id -> Rental
        self._next_rental_number = 1

        

    # ---- registration ----
    def add_vehicle(self, vehicle) -> None:
        self._vehicles[vehicle.vehicle_id] = vehicle

    def register_customer(self, customer) -> None:
        self._customers[customer.customer_id] = customer

    # ---- search ----
    def list_available_vehicles(self, vehicle_type: str = None):
        vehicles = [v for v in self._vehicles.values() if v.is_available]
        if vehicle_type:
            vehicles = [v for v in vehicles if v.vehicle_type().lower() == vehicle_type.lower()]
        return vehicles

    def display_available_vehicles(self, vehicle_type: str = None) -> None:
        vehicles = self.list_available_vehicles(vehicle_type)
        print("\nAvailable Vehicles")
        print("-" * 55)
        if not vehicles:
            print("No vehicles available right now.")
        for v in vehicles:
            print(v.display_details())

    # ---- rental workflow ----
    def rent_vehicle(self, customer_id: str, vehicle_id: str, days: int,
                      payment_processor: PaymentProcessor, start_date=None) -> Rental:
        customer = self._customers.get(customer_id)
        vehicle = self._vehicles.get(vehicle_id)

        if customer is None:
            raise RentalError(f"No customer found with ID {customer_id}.")
        if vehicle is None:
            raise RentalError(f"No vehicle found with ID {vehicle_id}.")

        rental_id = f"R{self._next_rental_number:04d}"
        rental = Rental(rental_id, customer, vehicle, days, start_date)

        try:
            rental.confirm_with_payment(payment_processor)
        except PaymentError as exc:
            raise RentalError(f"Payment failed: {exc}") from exc

        self._rentals[rental_id] = rental
        self._next_rental_number += 1
        return rental

    def return_vehicle(self, rental_id: str, return_date=None) -> Rental:
        rental = self._rentals.get(rental_id)
        if rental is None:
            raise RentalError(f"No rental found with ID {rental_id}.")
        rental.complete_rental(return_date)
        return rental
    