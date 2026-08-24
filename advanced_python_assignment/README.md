# Advanced Python Concepts

## 1. Iterator

The project implements a custom `EmployeeIterator` class.

An iterator is used to access elements one at a time.

The `EmployeeIterator` class implements two special methods:

```python
__iter__()
__next__()
```

### Implementation

```python
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
```

### How it works

First, an iterator object is created:

```python
iterator = EmployeeIterator(employees)
```

Then `next()` retrieves one employee at a time:

```python
print(next(iterator))
print(next(iterator))
```

The employees are returned in order:

```text
John
Mary
David
Sarah
Alex
Lisa
```

When there are no more employees, `__next__()` raises:

```python
StopIteration
```

This tells Python that the iterator has no more values to provide.

### `__iter__()` vs `__next__()`

`__iter__()` returns the iterator object itself.

```python
def __iter__(self):
    return self
```

`__next__()` retrieves the next value.

```python
def __next__(self):
    ...
```

Therefore:

```text
iter()
   ↓
gets the iterator
   ↓
next()
   ↓
gets the next value
```

---

## 2. Generator

The project implements the generator:

```python
employee_generator(employees)
```

A generator produces values one at a time using the `yield` keyword.

### Implementation

```python
def employee_generator(employees):
    for employee in employees:
        yield employee
```

Example:

```python
for employee in employee_generator(employees):
    print(employee["name"])
```

The generator produces:

```text
John
Mary
David
Sarah
Alex
Lisa
```

### Why use `yield`?

`yield` allows the values to be produced one at a time instead of creating and returning the complete result at once.

This is useful when processing a very large dataset because the program does not need to keep the complete generated result in memory.

The generator therefore performs **lazy processing**.

---

## 3. Filtering Generator

The project also implements:

```python
filter_by_department(employees, department)
```

This generator yields only employees belonging to the requested department.

### Implementation

```python
def filter_by_department(employees, department):
    for employee in employees:
        if employee["department"].lower() == department.lower():
            yield employee
```

Example:

```python
for employee in filter_by_department(employees, "IT"):
    print(employee["name"])
```

Output:

```text
John
David
Alex
```

Instead of creating a separate list containing all IT employees, the generator yields matching employees one at a time.

---

## 4. Generator vs Iterator

A generator is an iterator.

A generator automatically follows the iterator protocol and can therefore be used with `next()`.

For example:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Then:

```python
generator = numbers()

print(next(generator))
print(next(generator))
```

Output:

```text
1
2
```

The important difference is that in this assignment the `EmployeeIterator` is manually implemented using `__iter__()` and `__next__()`, whereas the generator uses `yield` and Python automatically manages the iterator behavior.

---

## 5. Closure

The project implements:

```python
create_salary_filter(min_salary)
```

A closure is an inner function that remembers a value from its enclosing function.

### Implementation

```python
def create_salary_filter(min_salary):

    def check(employee):
        return employee["salary"] >= min_salary

    return check
```

Example:

```python
high_salary = create_salary_filter(60000)
```

The returned `check()` function remembers:

```text
min_salary = 60000
```

even after `create_salary_filter()` has finished executing.

We can then use:

```python
print(high_salary(employees[0]))
print(high_salary(employees[2]))
```

John has a salary of `50000`:

```text
50000 >= 60000
False
```

David has a salary of `65000`:

```text
65000 >= 60000
True
```

### Why does the closure remember `min_salary`?

The inner function `check()` uses the variable `min_salary` from the outer function.

Python keeps access to that variable because the returned inner function still references it.

Therefore:

```text
create_salary_filter(60000)
          ↓
       check()
          ↓
remembers 60000
```

This allows the same function to be used later to test employees against the remembered minimum salary.

---

## 6. Decorator

The project implements the decorator:

```python
log_execution
```

The purpose of the decorator is to log when a function starts and finishes.

### Implementation

```python
from functools import wraps


def log_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print(f"[START] {func.__name__}")

        result = func(*args, **kwargs)

        print(f"[END] {func.__name__}")

        return result

    return wrapper
```

The decorator can be applied using:

```python
@log_execution
def generate_report():
    print("Generating employee report...")
```

The following:

```python
@log_execution
def generate_report():
```

is approximately equivalent to:

```python
generate_report = log_execution(generate_report)
```

The decorator adds extra behavior around the original function without changing its main implementation.

### Output

When the function is called:

```python
generate_report()
```

the output is:

```text
[START] generate_report
Generating employee report...
[END] generate_report
```

The assignment requires the decorator to be applied to at least two functions.

In this project it is applied to:

```python
@log_execution
def generate_employee_report(...):
    ...
```

and:

```python
@log_execution
def calculate_average_salary(...):
    ...
```

---

## 7. Context Manager

The project implements a custom context manager called:

```python
ReportFile
```

The context manager is responsible for opening and closing the employee report file.

It implements:

```python
__enter__()
__exit__()
```

### Implementation

```python
class ReportFile:

    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, "w")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
```

It is used with:

```python
with ReportFile("employee_report.txt") as report:
    report.write("Employee Report\n")
    report.write("John - IT - 50000\n")
```

### How it works

When Python enters the `with` block:

```python
with ReportFile("employee_report.txt") as report:
```

it calls:

```python
__enter__()
```

The file is opened and the file object is returned.

Then the report can be written:

```python
report.write("Employee Report\n")
```

When the `with` block finishes, Python automatically calls:

```python
__exit__()
```

which closes the file.

The complete flow is:

```text
with ReportFile(...)
        ↓
    __enter__()
        ↓
    File opened
        ↓
    Write report
        ↓
    __exit__()
        ↓
    File closed
```

### Why use a context manager?

Without a context manager, the programmer would have to manually open and close the file:

```python
file = open("employee_report.txt", "w")

file.write("Employee Report\n")

file.close()
```

The context manager automatically handles the cleanup when the `with` block finishes.

Therefore it makes resource handling more structured and reduces the possibility of forgetting to close the file.

---

# Connection Between the Five Concepts

The five concepts are combined in the employee processing pipeline.

```text
Employee List
     ↓
   Iterator
     ↓
  Generator
     ↓
Filter by Department
     ↓
   Closure
     ↓
Filter by Minimum Salary
     ↓
Context Manager
     ↓
Write Employee Report
```

The decorator surrounds the report-generation function:

```text
             @log_execution
                    ↓
       generate_employee_report()
                    ↓
              [START] log
                    ↓
                Generator
                    ↓
          Department Filtering
                    ↓
                 Closure
                    ↓
            Salary Filtering
                    ↓
             ReportFile
                    ↓
              Write Report
                    ↓
              Close File
                    ↓
               [END] log
```

Thus, each advanced Python concept has a specific role:

| Concept         | Implementation           | Purpose                                    |
| --------------- | ------------------------ | ------------------------------------------ |
| Iterator        | `EmployeeIterator`       | Retrieves employees one at a time          |
| Generator       | `employee_generator()`   | Lazily produces employees                  |
| Generator       | `filter_by_department()` | Lazily filters employees by department     |
| Closure         | `create_salary_filter()` | Remembers the minimum salary               |
| Decorator       | `@log_execution`         | Logs function execution                    |
| Context Manager | `ReportFile`             | Opens, manages, and closes the report file |
