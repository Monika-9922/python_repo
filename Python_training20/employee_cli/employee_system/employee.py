"""
employee.py
------------
Handles employee records using a simple in-memory list of dictionaries.
No database is used, as per the assignment requirements.
"""

# In-memory "database" of employees
employees = [
    {
        "id": "E001",
        "name": "John",
        "department": "IT",
        "salary": 50000
    },
    {
        "id": "E002",
        "name": "Alice",
        "department": "HR",
        "salary": 45000
    },
    {
        "id": "E003",
        "name": "Bob",
        "department": "Finance",
        "salary": 55000
    }
]


def add_employee(emp_id, name, department, salary):
    """
    Add a new employee to the employees list.

    Args:
        emp_id (str): Unique employee ID, e.g. "E004"
        name (str): Employee name
        department (str): Department name
        salary (float/int): Base salary

    Returns:
        dict: The newly added employee record
    """
    new_employee = {
        "id": emp_id,
        "name": name,
        "department": department,
        "salary": salary
    }
    employees.append(new_employee)
    return new_employee


def get_employee(emp_id):
    """
    Retrieve a single employee by ID.

    Args:
        emp_id (str): Employee ID to search for

    Returns:
        dict or None: The employee record if found, else None
    """
    for emp in employees:
        if emp["id"] == emp_id:
            return emp
    return None


def get_all_employees():
    """
    Retrieve the full list of employees.

    Returns:
        list[dict]: All employee records
    """
    return employees