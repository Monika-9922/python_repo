"""
app.py - HR Report Generator (Project 1)

Uses:
- Jinja2      -> generate an employee report from a template
- PrettyTable -> display all employees as a formatted table
"""

from jinja2 import Environment, FileSystemLoader
from prettytable import PrettyTable

from employee_system.employee import get_all_employees


def generate_jinja_report(employee):
    """Render the employee_report.txt template for a single employee."""
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("employee_report.txt")
    return template.render(employee=employee)


def generate_pretty_table(employees):
    """Build a PrettyTable from the list of employee records."""
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Department", "Salary"]

    for emp in employees:
        table.add_row([emp["id"], emp["name"], emp["department"], emp["salary"]])

    return table


def main():
    employees = get_all_employees()

    print("=" * 40)
    print(" HR EMPLOYEE REPORT")
    print("=" * 40)

    # Jinja2-generated report for each employee
    for emp in employees:
        print(generate_jinja_report(emp))

    # PrettyTable summary of all employees
    print("Employee Table")
    print("==============")
    table = generate_pretty_table(employees)
    print(table)


if __name__ == "__main__":
    main()