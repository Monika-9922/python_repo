"""Invoice: presents the final cost breakdown for a completed rental."""


class Invoice:
    def __init__(self, rental):
        self._rental = rental

    def generate(self) -> str:
        r = self._rental
        lines = [
            "=" * 45,
            "                INVOICE",
            "=" * 45,
            f"Customer:          {r.customer.name}",
            f"Vehicle:           {r.vehicle.vehicle_type()} - "
            f"{r.vehicle.brand} {r.vehicle.model}",
            f"Rental duration:   {r.days} day(s)",
            f"Base rental amount: Rs. {r.base_amount:,.2f}",
            f"Late fee:           Rs. {r.late_fee:,.2f}",
            "-" * 45,
            f"Final amount:       Rs. {r.final_amount:,.2f}",
            "=" * 45,
        ]
        return "\n".join(lines)

    def display(self) -> None:
        print(self.generate())