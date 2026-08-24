"""
salary.py
---------
Handles salary and bonus calculations for employees.
"""


def calculate_salary(base_salary, deductions=0):
    """
    Calculate the net salary after deductions (e.g. tax, insurance).

    Args:
        base_salary (float): The employee's base salary
        deductions (float): Total deductions to subtract (default 0)

    Returns:
        float: Net salary after deductions
    """
    net_salary = base_salary - deductions
    return max(net_salary, 0)  # never return a negative salary


def calculate_bonus(base_salary, performance_rating=3):
    """
    Calculate a bonus based on a simple performance rating scale (1-5).

    Rating 5 -> 20% of base salary
    Rating 4 -> 15% of base salary
    Rating 3 -> 10% of base salary
    Rating 2 -> 5% of base salary
    Rating 1 -> 0% of base salary

    Args:
        base_salary (float): The employee's base salary
        performance_rating (int): Rating from 1 to 5 (default 3)

    Returns:
        float: Calculated bonus amount
    """
    bonus_rates = {
        5: 0.20,
        4: 0.15,
        3: 0.10,
        2: 0.05,
        1: 0.00
    }
    rate = bonus_rates.get(performance_rating, 0.10)
    return base_salary * rate