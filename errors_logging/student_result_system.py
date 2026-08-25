"""
Student Result Processing System
---------------------------------
Demonstrates Python exception handling (try/except/else/finally)
combined with the logging module.
"""

import logging

# ---------------------------------------------------------------------------
# Configure logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    filename="student_app.log",
    level=logging.DEBUG,          # change to logging.ERROR for the level exercise
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)


# ---------------------------------------------------------------------------
# Challenge 2: Create a Function for Average
# ---------------------------------------------------------------------------
def calculate_average(marks):
    """Accepts a list of marks, returns the average (float)."""
    try:
        total = sum(marks)
        average = total / len(marks)
    except ZeroDivisionError:
        # Challenge 5: guard against dividing by zero subjects
        logging.error("Attempted to calculate average with zero subjects.")
        return 0.0
    else:
        return average


# ---------------------------------------------------------------------------
# Challenge 3: Create a Result Function
# ---------------------------------------------------------------------------
def get_result(average):
    """Maps an average score to a result category."""
    if 90 <= average <= 100:
        return "Excellent"
    elif 75 <= average < 90:
        return "Very Good"
    elif 50 <= average < 75:
        return "Pass"
    else:
        return "Fail"


# ---------------------------------------------------------------------------
# Helper: get a validated integer from the user (handles ValueError)
# ---------------------------------------------------------------------------
def get_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            logging.error("Invalid input: could not convert input to an integer.")
        else:
            return value


# ---------------------------------------------------------------------------
# Helper: get a validated mark (0-100) from the user
# ---------------------------------------------------------------------------
def get_valid_mark(subject_number):
    while True:
        try:
            mark = float(input(f"Enter marks for subject {subject_number}: "))
        except ValueError:
            print("Please enter a valid number.")
            logging.error("Invalid input: mark entered was not a number.")
            continue

        if mark < 0 or mark > 100:
            print("Marks must be between 0 and 100.")
            print("Please enter the marks again.")
            logging.warning(f"Out-of-range mark entered: {mark}")
            continue

        # Warn (but accept) marks very close to the failing threshold
        if 50 <= mark < 55:
            logging.warning("Student entered a mark close to the minimum passing mark.")

        return mark


# ---------------------------------------------------------------------------
# Process a single student (core logic + Challenge 4 logging)
# ---------------------------------------------------------------------------
def process_student():
    try:
        logging.info("Student processing started.")

        name = input("Enter student name: ").strip()
        if not name:
            name = "Unknown"
        logging.info(f"Student name received: {name}")

        num_subjects = get_valid_int("Enter number of subjects: ")
        logging.info(f"Number of subjects received: {num_subjects}")

        # Challenge 5: handle 0 subjects without crashing
        if num_subjects <= 0:
            print("Number of subjects must be greater than 0.")
            logging.error("Student entered zero or negative subjects.")
            raise ZeroDivisionError("Number of subjects cannot be zero.")

        marks = []
        for i in range(1, num_subjects + 1):
            mark = get_valid_mark(i)
            marks.append(mark)
        logging.info("Marks entered successfully.")

    except ZeroDivisionError as zde:
        print("An error occurred: number of subjects cannot be zero.")
        logging.critical(f"Student processing could not be completed: {zde}")
        return  # stop processing this student

    except Exception as e:
        # Catch-all safety net for anything truly unexpected
        print("An unexpected error occurred. Please try again.")
        logging.critical(f"Unexpected failure while processing student: {e}")
        return

    else:
        # Runs only if the try block above completed with no exception
        average = calculate_average(marks)
        result = get_result(average)
        logging.info("Calculation completed.")

        print("\n----- Student Result -----")
        print(f"Student Name : {name}")
        print(f"Average      : {average:.2f}")
        print(f"Result       : {result}")

        # Bonus Task: highest, lowest, average mark
        highest = max(marks)
        lowest = min(marks)
        print("\n----- Student Statistics -----")
        print(f"Highest Mark : {highest}")
        print(f"Lowest Mark  : {lowest}")
        print(f"Average Mark : {average:.2f}")
        print(f"Result       : {result}")
        logging.info("Student statistics calculated successfully.")

    finally:
        print("Processing completed.")
        logging.info("Student processing finished (finally block executed).\n")


# ---------------------------------------------------------------------------
# Challenge 1: Handle Multiple Students
# ---------------------------------------------------------------------------
def main():
    logging.info("===== Application started =====")

    while True:
        process_student()

        again = input("\nDo you want to enter another student? (yes/no): ").strip().lower()
        if again != "yes":
            break

    logging.info("===== Application completed =====")
    print("\nThank you for using the Student Result Processing System.")


if __name__ == "__main__":
    main()
