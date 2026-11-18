"""Export student reports to CSV."""

from __future__ import annotations

import csv
from pathlib import Path

from .models import Student, classify

HEADER = ["student_id", "name", "module", "mark", "credits"]


def report_rows(student: Student) -> list[list[str]]:
    rows = [[student.student_id, student.name, g.module, f"{g.mark:g}", str(g.credits)]
            for g in student.grades]
    if student.grades:
        avg = student.weighted_average()
        rows.append([student.student_id, student.name, "WEIGHTED AVERAGE", f"{avg:.2f}",
                     str(student.total_credits())])
        rows.append([student.student_id, student.name, "CLASSIFICATION", classify(avg), ""])
    return rows


def write_csv(student: Student, path: str | Path) -> int:
    """Write a student's report to ``path``. Returns the number of data rows."""
    rows = report_rows(student)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)
    return len(rows)
