# Assignment Answers: Exception Handling and Logging

1. What is exception handling?

Exception handling is a way of dealing with errors that occur while a program
is running (called "exceptions") without letting the program crash. Python
lets you "try" a block of risky code, "catch" specific errors if they happen,
and decide how the program should respond — instead of stopping abruptly.


2. Why should we use exception handling?

Without it, a single bad input or unexpected condition (like dividing by
zero, or a user typing letters instead of numbers) would immediately stop
the entire program. Exception handling lets the program recover gracefully,
show a helpful message, and keep running.


3. What is the difference between try and except?

`try` contains code that might raise an error. `except` contains code that
runs only if a specific error occurs inside the `try` block.


4. When is the else block executed?

`else` runs only when the `try` block completes with no exception at all.
If an exception is raised and caught, `else` is skipped.


5. When is the finally block executed?

`finally` always runs, whether an exception occurred or not. It's used for
cleanup actions that must happen regardless of outcome.


6. What is logging? Why is it useful?

Logging records events, errors, and status messages to a file instead of
just the screen. It creates a permanent, timestamped record useful for
debugging, monitoring, and auditing an application after the fact.


7. What is the difference between print() and logging?

`print()` only displays text momentarily in the console. `logging` writes
persistent, timestamped records with severity levels to a file, and can be
filtered or redirected without changing the code that generates messages.


8. What happens when the logging level is set to ERROR?

Only ERROR and CRITICAL messages are recorded; DEBUG, INFO, and WARNING
are ignored because their severity is below the threshold.


9. What happens if we don't handle ValueError when converting input with int()?

The program crashes with an unhandled traceback, and any work in progress
is lost.


10. Why avoid `except: pass`?

It silently swallows every error, including unexpected bugs, with no
message or log entry — making problems very hard to diagnose later.
Catching specific exceptions is safer and clearer.

11. Why is logging useful in production?

Developers usually can't watch a live application run. Logs provide a
historical record for diagnosing issues, tracking error frequency, and
monitoring health after the fact.


12. What is the purpose of the finally block?

It guarantees cleanup code (closing files, releasing resources, printing
a completion message) runs no matter what happened in the try block.