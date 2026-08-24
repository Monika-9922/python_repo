# README – Employee Management & Reporting System

This project demonstrates Python modules, packages, third-party libraries,
and virtual environments using two independent applications that share the
same `employee_system` package:

- **hr_report_generator/** — generates employee reports (Jinja2 + PrettyTable)
- **employee_cli/** — displays employee data in the terminal (Tabulate + Rich)

---

## 1. What is a module?

A module is simply a single Python file (`.py`) that groups related code —
functions, classes, or variables — so it can be reused by importing it
elsewhere instead of rewriting the code. In this project, `employee.py`,
`salary.py`, and `attendance.py` are each modules: `employee.py` handles
employee records, `salary.py` handles salary/bonus calculations, and
`attendance.py` handles attendance tracking.

## 2. What is a package?

A package is a folder containing multiple related modules, along with a
special `__init__.py` file that tells Python to treat the folder as an
importable unit rather than just a plain directory. In this project,
`employee_system/` is a package — it bundles `employee.py`, `salary.py`, and
`attendance.py` together so they can be imported as:

```python
from employee_system.employee import get_all_employees
from employee_system.salary import calculate_salary
```

## 3. What is a virtual environment?

A virtual environment (`.venv`) is an isolated, self-contained Python
installation for a single project. Any libraries installed inside it (via
`pip install`) are only available to that project — they don't affect the
system-wide Python installation or any other project's environment. This
prevents version conflicts between projects that may need different versions
of the same library.

## 4. Why are two virtual environments used?

`hr_report_generator` and `employee_cli` are treated as two completely
independent applications, even though they share the same `employee_system`
package. Each has its own dependencies (Jinja2/PrettyTable vs.
Tabulate/Rich), and keeping them in separate `.venv` folders proves that:

- Installing a library in one project's environment does not make it
  available in the other.
- Each project can be deployed, shared, or reproduced on its own, without
  needing to know or care what the other project depends on.
- If one project later needs a different version of a shared dependency, it
  won't break the other.

## 5. What is Jinja2 used for?

Jinja2 is a templating engine used to generate dynamic text from a template
file. Instead of hardcoding report text directly in Python, the HR Report
Generator loads `templates/employee_report.txt`, which contains placeholders
like `{{ employee.name }}`, and Jinja2 fills them in with real employee data
at runtime. This keeps the report's layout separate from the application
logic.

## 6. What is PrettyTable used for?

PrettyTable is a library that generates clean, ASCII box-style tables
(`+---+---+`) from Python data. The HR Report Generator uses it to display
all employees in a single formatted table, without manually building the
table borders and spacing by hand.

## 7. What is Tabulate used for?

Tabulate is a library for formatting tabular data for the command line. It
supports multiple predefined table styles (e.g. `grid`, `simple`) from the
same data, which the Employee CLI application uses to display employee
records in more than one style.

## 8. What is Rich used for?

Rich is a library for building richly styled terminal output — colored text,
styled tables, alignment, panels, progress bars, and more. The Employee CLI
application uses Rich's `Table` class to display employee data with column
colors, a title, and aligned salary figures, going beyond what plain-text
table libraries can do.

## 9. What is requirements.txt?

`requirements.txt` is a plain-text file listing every third-party package (and
its exact version) that a project depends on, generated with:

```
pip freeze > requirements.txt
```

Anyone (or any machine) can then recreate the exact same environment with:

```
pip install -r requirements.txt
```

This makes the project's dependencies explicit, portable, and reproducible,
rather than relying on "whatever happens to be installed" on a given machine.

## 10. Why should package versions be specified?

Without a pinned version (e.g. `prettytable==3.10.0` instead of just
`prettytable`), `pip install` grabs whatever the latest version happens to be
at install time — which can change over weeks or months. A newer version
might introduce breaking changes, renamed functions, or different default
behavior, silently breaking the application on a teammate's machine or in
production, even though the code never changed. Pinning versions guarantees
that everyone installing the project gets the exact same, tested behavior.

---

## Project Structure

```
python_training/
│
├── hr_report_generator/
│   ├── .venv/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   │   └── employee_report.txt
│   └── employee_system/
│       ├── __init__.py
│       ├── employee.py
│       ├── salary.py
│       └── attendance.py
│
└── employee_cli/
    ├── .venv/
    ├── app.py
    ├── requirements.txt
    └── employee_system/
        ├── __init__.py
        ├── employee.py
        ├── salary.py
        └── attendance.py
```

## Running Each Project

```bash
# From inside hr_report_generator/ or employee_cli/
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
python app.py
```
