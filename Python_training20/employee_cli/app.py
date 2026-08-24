"""
app.py - Employee CLI Application (Project 2)

Uses:
- Tabulate -> simple CLI table (demonstrated with two formats)
- Rich     -> richly styled terminal table
"""

from tabulate import tabulate
from rich.console import Console
from rich.table import Table

from employee_system.employee import get_all_employees


def show_tabulate_table(employees, tablefmt="grid"):
    """Print employee data using Tabulate with the given format."""
    print(tabulate(employees, headers="keys", tablefmt=tablefmt))


def show_rich_table(employees):
    """Print employee data using a styled Rich table."""
    console = Console()

    table = Table(title="Employee Details")

    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Department", style="green")
    table.add_column("Salary", style="yellow", justify="right")

    for emp in employees:
        table.add_row(
            emp["id"],
            emp["name"],
            emp["department"],
            str(emp["salary"])
        )

    console.print(table)


def main():
    employees = get_all_employees()

    print("=" * 40)
    print(" EMPLOYEE CLI APPLICATION")
    print("=" * 40)

    print("\nEmployee List - Tabulate (grid format)")
    print("-" * 40)
    show_tabulate_table(employees, tablefmt="grid")

    print("\nEmployee List - Tabulate (simple format)")
    print("-" * 40)
    show_tabulate_table(employees, tablefmt="simple")

    print("\nEmployee List - Rich")
    print("-" * 40)
    show_rich_table(employees)


if __name__ == "__main__":
    main()