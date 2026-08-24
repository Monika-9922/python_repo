# Part 3 – Library Comparison

## Comparison Table

| Library | Purpose | Output Style | Used In |
| **Jinja2** | Template-based text/report generation | Dynamic text, rendered from a `.txt` template with placeholders | HR Report Generator |
| **PrettyTable** | Table formatting | ASCII box-style table (`+---+---+`) | HR Report Generator |
| **Tabulate** | CLI table formatting | Multiple predefined table styles (grid, simple, etc.) | Employee CLI |
| **Rich** | Rich terminal UI | Styled, colored terminal table with borders and alignment | Employee CLI |

## Why the Company Might Choose One Library Over Another

### Jinja2 vs. hardcoding text in Python
Jinja2 separates the report's *layout* from the application's *logic*. The HR
team can edit the wording or structure of `employee_report.txt` without
touching Python code at all — useful when non-developers (like HR staff) need
to tweak report formatting. It's also the standard choice when reports need
to be generated as files (for printing, emailing, or archiving), not just
shown on screen.

### PrettyTable vs. Tabulate
Both draw ASCII tables, but they serve slightly different needs:

- **PrettyTable** is simple and predictable — one consistent box style, easy
  to build row-by-row, good when you just need "a clean table" without
  configuration.
- **Tabulate** offers multiple output formats (`grid`, `simple`, `github`,
  `pipe`, etc.) from the same data, which is useful when the same data needs
  to appear differently in different contexts — e.g., a plain terminal vs. a
  Markdown file vs. a GitHub README.

The HR team picked PrettyTable because their output is a fixed report format
(consistency matters more than flexibility). The Operations team picked
Tabulate because they wanted to experiment with formats for a CLI tool people
will actually look at interactively.

### Rich vs. plain text tables
Rich goes further than Tabulate/PrettyTable — it supports color, styling,
alignment, and richer terminal UI elements (progress bars, panels, etc.,
beyond just tables). It's the right choice for an **interactive CLI
application** meant to be pleasant to use day-to-day, where visual clarity
(colored columns, aligned numbers) helps users scan data quickly. It would be
overkill for a one-shot text report meant to be saved to a file or printed,
since the color/styling only renders in a terminal — which is exactly why the
HR team, generating a plain report, didn't need it.

### General Principle
The choice depends on the *output destination* — Jinja2 + PrettyTable produce
plain, portable text suited for reports/files; Tabulate + Rich are suited for
live terminal interaction, with Rich chosen specifically when visual polish
adds real value.
