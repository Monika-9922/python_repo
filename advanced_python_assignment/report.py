from employee_processor import (
    employee_generator,
    filter_by_department,
    create_salary_filter,
    log_execution
)


class ReportFile:

    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, "w")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


@log_execution
def generate_employee_report(employees, department, min_salary):

    salary_filter = create_salary_filter(min_salary)

    generated_employees = employee_generator(employees)

    department_employees = filter_by_department(
        generated_employees,
        department
    )

    filtered_employees = (
        employee
        for employee in department_employees
        if salary_filter(employee)
    )

    with ReportFile("employee_report.txt") as report:

        report.write("Employee Report\n")
        report.write("===============\n")
        report.write(f"Department: {department}\n")
        report.write(f"Minimum Salary: {min_salary}\n")

        for employee in filtered_employees:

            report.write(
                f"{employee['id']} - "
                f"{employee['name']} - "
                f"{employee['department']} - "
                f"{employee['salary']}\n"
            )


@log_execution
def calculate_average_salary(employees):

    total_salary = 0
    count = 0

    for employee in employee_generator(employees):
        total_salary += employee["salary"]
        count += 1

    if count == 0:
        return 0

    return total_salary / count