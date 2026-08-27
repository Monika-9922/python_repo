   


# Vehicle Rental Management System

A console-based, menu-driven system for renting cars, bikes, and vans
to customers, built to demonstrate object-oriented design in Python.

## Project description

The system lets a company register vehicles and customers, rent out
available vehicles, take payment before confirming a rental, and
handle returns (including late fees) with a final invoice generated
only once the vehicle actually comes back. Each vehicle type prices
itself differently, and the code is structured so a new vehicle or
payment type can be added without touching existing classes.

## How to run

```bash
cd src
python3 main.py
```

You'll see a menu:

```
1) Rent a vehicle
2) Return a vehicle
3) Exit
```

**Rent a vehicle** — pick an existing customer (or register a new one
on the spot), browse available vehicles, choose the number of days,
pay by card or UPI, and get a Rental ID back to use later.

**Return a vehicle** — pick an active rental by its Rental ID, enter
the actual number of days from pickup to return, and see the invoice
with base amount, any late fee, and the final amount.

The menu loops so multiple customers can rent and return vehicles in
the same session, and vehicle availability updates live as each
person books or returns.

## Project structure

```
src/
  vehicle.py         Vehicle (abstract), Car, Bike, Van
  customer.py         Customer
  payment.py          PaymentProcessor interface, CardPayment, UpiPayment
  rental.py           Rental (composition of Customer + Vehicle)
  invoice.py          Invoice
  rental_service.py   RentalService (orchestration layer)
  main.py             Interactive console entry point
```

## Class responsibilities

| Class | Responsibility |
| `Vehicle` (abstract) | Shared vehicle data and behaviour; declares `calculate_rental_cost()` |
| `Car`, `Bike`, `Van` | Override `calculate_rental_cost()` with their own pricing rule |
| `Customer` | Identity, contact details, validation, rental history |
| `PaymentProcessor` (interface) | Contract for `process_payment(amount)` |
| `CardPayment`, `UpiPayment` | Two concrete payment methods |
| `Rental` | Composes a Customer + Vehicle; runs the rent/return workflow and late-fee math |
| `Invoice` | Formats a completed rental's cost breakdown |
| `RentalService` | Orchestrates vehicles, customers, and rentals; depends only on `PaymentProcessor` |

`main.py` is the console layer on top of all of this — it collects
user input, calls into `RentalService`, and prints results. It holds
no business logic of its own.

## OOP concepts and where they live

- **Encapsulation** — every class stores its data in private fields
  (`self._field`) and exposes only what's needed through methods or
  `@property`. Validation happens in constructors (e.g. `Customer`
  rejects empty names, `Vehicle` rejects a non-positive daily rate).
- **Abstraction** — `Vehicle` and `PaymentProcessor` are abstract
  base classes (`abc.ABC`); neither can be instantiated directly.
- **Inheritance** — `Car`, `Bike`, and `Van` inherit from `Vehicle`.
  `CardPayment` and `UpiPayment` inherit from `PaymentProcessor`.
- **Polymorphism** — `RentalService` and `Rental` never check "is this
  a car or a bike?" They just call `vehicle.calculate_rental_cost(days)`
  and the correct override runs. Same for payment: `rental` calls
  `payment_processor.process_payment(amount)` without knowing whether
  it's a card or UPI. This removes long if/else chains and lets a new
  vehicle or payment type be added by writing one new class — nothing
  existing has to change.
- **Interface / dependency inversion** — `PaymentProcessor` is the
  contract. `RentalService.rent_vehicle()` takes a `PaymentProcessor`
  parameter, never a concrete `CardPayment`/`UpiPayment` type.
- **Composition** — a `Rental` holds a `Customer` and a `Vehicle`
  (and produces an `Invoice` on return); it cannot exist without them.
- **Exception handling** — `RentalError` covers invalid days, an
  unavailable vehicle, or a missing customer/vehicle/rental ID;
  `PaymentError` covers a failed charge. Both are caught in `main.py`
  with readable messages instead of crashing.

## Business rules implemented

- Rental days must be greater than zero (`RentalError` otherwise).
- A vehicle already rented cannot be rented again until returned.
- Payment must succeed before a rental is confirmed
  (`Rental.confirm_with_payment` charges first, then marks the
  vehicle unavailable).
- The invoice is generated only once, at return time, so it reflects
  the true final amount including any late fee.
- Late fee = late days × 20% of the vehicle's daily rate.
- A returned vehicle becomes available again immediately.
- Card numbers are masked before being stored — never kept as plain text.

## Test cases

| # | Action | Input | Expected result | Actual result |
|---|---|---|---|---|
| 1 | Rent a car for 3 days | days=3, rate=2000 | Base amount Rs. 6,000 | Rs. 6,000 |
| 2 | Rent a bike for 6 days (over threshold) | days=6, rate=700 | 5% discount applied | Rs. 3,990 |
| 3 | Rent a bike for 5 days (at threshold) | days=5, rate=700 | No discount | Rs. 3,500 |
| 4 | Rent a van for 2 days | days=2, rate=3000, service=500 | Rs. 6,500 | Rs. 6,500 |
| 5 | Rent with 0 days | days=0 | Re-prompted for valid input | Re-prompted |
| 6 | Rent an already-rented vehicle | vehicle rented twice | "unavailable", re-prompted | Re-prompted |
| 7 | Book 4 days, return after 5 | booked=4, returned after 5 | Late fee = 1 × 20% × 2000 = Rs. 400 | Rs. 400 |
| 8 | Return on time | returned exactly on booked day | Late fee = Rs. 0 | Rs. 0 |
| 9 | Payment amount ≤ 0 | amount=0 | `PaymentError` raised | Raised |
| 10 | Register customer with empty name | name="" | Re-prompted, not registered | Re-prompted |
| 11 | Unknown Customer ID | typo'd ID | Offered option to register | Offered |

## Polymorphism write-up

`RentalService` and `Rental` work with vehicles and payment methods
purely through their abstract interfaces (`Vehicle.calculate_rental_cost`,
`PaymentProcessor.process_payment`). Neither class contains a single
`if vehicle_type == "car"` check. This means:

1. Adding a new vehicle type (e.g. `Truck`) or payment method
   (e.g. `WalletPayment`) requires writing one new class — no existing
   class is touched, satisfying the open/closed principle.
2. The pricing and payment logic can't drift out of sync across
   scattered conditionals, because each rule lives in exactly one
   place: the subclass that owns it.
