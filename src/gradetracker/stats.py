"""Statistics for a module across all students."""

from __future__ import annotations

import statistics
from dataclasses import dataclass

from .models import GradeBook, GradeError


@dataclass
class ModuleStats:
    module: str
    count: int
    mean: float
    median: float
    minimum: float
    maximum: float
    pass_rate: float  # percentage of marks >= 40


def module_stats(book: GradeBook, module: str) -> ModuleStats:
    marks = [
        g.mark
        for student in book.students.values()
        for g in student.grades
        if g.module.lower() == module.lower()
    ]
    if not marks:
        raise GradeError(f"No grades recorded for {module}")
    passed = sum(1 for m in marks if m >= 40)
    return ModuleStats(
        module=module,
        count=len(marks),
        mean=round(statistics.mean(marks), 2),
        median=round(statistics.median(marks), 2),
        minimum=min(marks),
        maximum=max(marks),
        pass_rate=round(100 * passed / len(marks), 1),
    )


def module_names(book: GradeBook) -> list[str]:
    """All module names in the grade book, de-duplicated case-insensitively."""
    seen: dict[str, str] = {}
    for student in book.students.values():
        for g in student.grades:
            seen.setdefault(g.module.lower(), g.module)
    return sorted(seen.values(), key=str.lower)
