"""
Two customers are pre-registered. The user picks one, browses
available vehicles, chooses how many days to rent, pays, and
receives an invoice -- all through console prompts.
"""

from datetime import timedelta

from vehicle import Car, Bike, Van
from customer import Customer
from payment import CardPayment, UpiPayment, PaymentError
from rental_service import RentalService
from rental import RentalError
from invoice import Invoice


def build_seed_data(service: RentalService) -> None:
    """Pre-register the fleet and two customers before the CLI starts."""
    service.add_vehicle(Car("V101", "KA01AB1234", "Toyota", "Etios", 2000))
    service.add_vehicle(Bike("V102", "KA01BC5678", "Yamaha", "FZ", 700))
    service.add_vehicle(Van("V103", "KA01CD9012", "Tata", "Winger", 3000, service_charge=500))

    service.register_customer(Customer("C001", "Ananya Sharma", "ananya@example.com", "DL1234567"))
    service.register_customer(Customer("C002", "Rohit Verma", "rohit@example.com", "DL7654321"))


def register_new_customer(service: RentalService):
    """Collect details for a first-time customer and register them."""
    print("\nNew customer registration")
    while True:
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        licence_number = input("Driving licence number: ").strip()
        try:
            new_id = f"C{len(service._customers) + 1:03d}"
            customer = Customer(new_id, name, email, licence_number)
            service.register_customer(customer)
            print(f"Registered successfully. Your Customer ID is {new_id}.")
            return customer
        except ValueError as exc:
            print(f"Could not register: {exc}. Please try again.")


def prompt_customer(service: RentalService):
    """Ask the user to identify themselves, or register if they're new."""
    print("\nRegistered customers")
    print("-" * 30)
    for cust_id, customer in service._customers.items():
        print(f"{cust_id} | {customer.name}")

    while True:
        customer_id = input("\nEnter your Customer ID (or press Enter to register): ").strip().upper()
        if not customer_id:
            return register_new_customer(service)

        customer = service._customers.get(customer_id)
        if customer:
            return customer

        choice = input("Customer ID not found. Register as a new customer? (y/n): ").strip().lower()
        if choice == "y":
            return register_new_customer(service)


def prompt_vehicle(service: RentalService):
    """Show available vehicles and let the user pick one by ID."""
    service.display_available_vehicles()

    while True:
        vehicle_id = input("\nEnter the Vehicle ID you want to rent: ").strip().upper()
        vehicle = service._vehicles.get(vehicle_id)
        if vehicle is None:
            print("No such vehicle. Please try again.")
        elif not vehicle.is_available:
            print("That vehicle is currently unavailable. Please pick another.")
        else:
            return vehicle


def prompt_days() -> int:
    """Ask for a valid, positive number of rental days."""
    while True:
        raw = input("Enter number of rental days: ").strip()
        try:
            days = int(raw)
            if days <= 0:
                print("Days must be greater than zero.")
                continue
            return days
        except ValueError:
            print("Please enter a whole number.")


def prompt_payment_processor():
    """Ask which payment method to use and collect the needed detail."""
    print("\nPayment methods: 1) Card   2) UPI")
    while True:
        choice = input("Choose a payment method (1/2): ").strip()
        try:
            if choice == "1":
                card_number = input("Enter card number: ").strip()
                return CardPayment(card_number)
            elif choice == "2":
                upi_id = input("Enter UPI ID: ").strip()
                return UpiPayment(upi_id)
            else:
                print("Please enter 1 or 2.")
        except ValueError as exc:
            print(f"Invalid payment details: {exc}")


def handle_rent(service: RentalService) -> None:
    """Full rent flow: pick customer, vehicle, days, pay, confirm booking."""
    customer = prompt_customer(service)
    print(f"\nWelcome, {customer.name}!")

    vehicle = prompt_vehicle(service)
    days = prompt_days()
    payment_processor = prompt_payment_processor()

    try:
        rental = service.rent_vehicle(customer.customer_id, vehicle.vehicle_id,
                                       days, payment_processor)
        print("\nPayment completed successfully.")
        print(f"Your Rental ID is {rental.rental_id} -- keep it to return the vehicle.")
        print(f"Vehicle booked: {vehicle.vehicle_type()} {vehicle.brand} {vehicle.model} "
              f"for {days} day(s).")
    except (RentalError, PaymentError) as exc:
        print(f"\nRental could not be completed: {exc}")


def prompt_active_rental(service: RentalService):
    """Show active rentals and let the user pick one by Rental ID."""
    active_rentals = [r for r in service._rentals.values() if r.status == "ACTIVE"]
    if not active_rentals:
        print("\nThere are no active rentals to return.")
        return None

    print("\nActive rentals")
    print("-" * 55)
    for r in active_rentals:
        print(f"{r.rental_id} | {r.customer.name} | {r.vehicle.vehicle_type()} "
              f"{r.vehicle.brand} {r.vehicle.model} | booked for {r.days} day(s)")

    while True:
        rental_id = input("\nEnter the Rental ID to return: ").strip().upper()
        match = next((r for r in active_rentals if r.rental_id == rental_id), None)
        if match:
            return match
        print("Rental ID not found among active rentals. Please try again.")


def prompt_days_used(booked_days: int) -> int:
    """Ask how many days actually passed between pickup and return."""
    while True:
        raw = input(f"Enter total days from pickup to return "
                     f"(booked for {booked_days} day(s)): ").strip()
        try:
            days_used = int(raw)
            if days_used <= 0:
                print("Days must be greater than zero.")
                continue
            return days_used
        except ValueError:
            print("Please enter a whole number.")


def handle_return(service: RentalService) -> None:
    """Full return flow: pick rental, work out the actual return date, show invoice."""
    rental = prompt_active_rental(service)
    if rental is None:
        return

    days_used = prompt_days_used(rental.days)
    return_date = rental.start_date + timedelta(days=days_used)

    try:
        completed_rental = service.return_vehicle(rental.rental_id, return_date=return_date)
        late_days = days_used - rental.days
        if late_days > 0:
            print(f"\nVehicle returned {late_days} day(s) late.")
        else:
            print("\nVehicle returned on time.")
        Invoice(completed_rental).display()
    except RentalError as exc:
        print(f"\nReturn could not be completed: {exc}")


def main() -> None:
    service = RentalService()
    build_seed_data(service)

    print("=" * 40)
    print(" VEHICLE RENTAL SYSTEM")
    print("=" * 40)

    while True:
        print("\n1) Rent a vehicle")
        print("2) Return a vehicle")
        print("3) Exit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            handle_rent(service)
        elif choice == "2":
            handle_return(service)
        elif choice == "3":
            print("\nThank you for using the Vehicle Rental System.")
            break
        else:
            print("Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()