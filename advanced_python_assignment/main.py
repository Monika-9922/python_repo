from employee_processor import EmployeeIterator
from report import generate_employee_report, calculate_average_salary


employees = [
    {"id": 101, "name": "John", "department": "IT", "salary": 50000},
    {"id": 102, "name": "Mary", "department": "HR", "salary": 45000},
    {"id": 103, "name": "David", "department": "IT", "salary": 65000},
    {"id": 104, "name": "Sarah", "department": "Finance", "salary": 55000},
    {"id": 105, "name": "Alex", "department": "IT", "salary": 75000},
    {"id": 106, "name": "Lisa", "department": "HR", "salary": 48000},
]


# Iterator demonstration

print("Iterator demonstration:")

iterator = EmployeeIterator(employees)

print(next(iterator))
print(next(iterator))
print(next(iterator))


# Calculate average salary

average_salary = calculate_average_salary(employees)

print("\nAverage salary:", average_salary)


# Generate employee report

print("\nGenerating employee report...")

generate_employee_report(
    employees,
    "IT",
    60000
)

print("\nReport saved successfully.")