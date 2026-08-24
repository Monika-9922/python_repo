"""
attendance.py
-------------
Handles attendance marking and reporting for employees.
Attendance is stored in-memory as {employee_id: [list of records]}.
"""

# In-memory attendance store
# Example: {"E001": [{"date": "2026-08-01", "status": "Present"}, ...]}
attendance_records = {}


def mark_attendance(emp_id, date, status):
    """
    Mark attendance for an employee on a given date.

    Args:
        emp_id (str): Employee ID
        date (str): Date string, e.g. "2026-08-20"
        status (str): "Present" or "Absent"

    Returns:
        dict: The attendance record that was added
    """
    record = {"date": date, "status": status}

    if emp_id not in attendance_records:
        attendance_records[emp_id] = []

    attendance_records[emp_id].append(record)
    return record


def get_attendance(emp_id):
    """
    Get the full attendance history for an employee.

    Args:
        emp_id (str): Employee ID

    Returns:
        list[dict]: List of attendance records (empty list if none found)
    """
    return attendance_records.get(emp_id, [])


def calculate_attendance_percentage(emp_id):
    """
    Calculate the attendance percentage for an employee.

    Args:
        emp_id (str): Employee ID

    Returns:
        float: Percentage of days marked "Present" out of total records.
               Returns 0.0 if no records exist.
    """
    records = get_attendance(emp_id)
    if not records:
        return 0.0

    present_days = sum(1 for r in records if r["status"].lower() == "present")
    total_days = len(records)

    return round((present_days / total_days) * 100, 2)