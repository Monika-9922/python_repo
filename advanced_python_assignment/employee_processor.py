from functools import wraps


class EmployeeIterator:

    def __init__(self, employees):
        self.employees = employees
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.employees):
            raise StopIteration

        employee = self.employees[self.index]
        self.index += 1

        return employee


def employee_generator(employees):
    for employee in employees:
        yield employee


def filter_by_department(employees, department):
    for employee in employees:
        if employee["department"].lower() == department.lower():
            yield employee


def create_salary_filter(min_salary):

    def check(employee):
        return employee["salary"] >= min_salary

    return check


def log_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print(f"[START] {func.__name__}")

        result = func(*args, **kwargs)

        print(f"[END] {func.__name__}")

        return result

    return wrapper