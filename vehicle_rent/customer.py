"""Customer class: identity, contact details, and rental history."""


class Customer:
    def __init__(self, customer_id: str, name: str, email: str, licence_number: str):
        for label, value in [("name", name), ("email", email),
                              ("licence number", licence_number)]:
            if not value.strip():
                raise ValueError(f"Customer {label} cannot be empty.")

        self._customer_id = customer_id
        self._name = name
        self._email = email
        self._licence_number = licence_number
        self._rental_history = []  # list of Rental objects

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def name(self) -> str:
        return self._name

    def add_rental(self, rental) -> None:
        self._rental_history.append(rental)

    def display_rental_history(self) -> None:
        if not self._rental_history:
            print(f"{self._name} has no rental history yet.")
            return

        print(f"\nRental history for {self._name}")
        print("-" * 50)
        for rental in self._rental_history:
            print(rental.summary())