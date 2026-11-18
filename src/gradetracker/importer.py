"""Bulk import of grades from a CSV file."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from .models import GradeBook, GradeError

REQUIRED = {"student_id", "module", "mark"}


@dataclass
class ImportResult:
    imported: int = 0
    new_students: int = 0
    errors: list[str] = field(default_factory=list)


def import_csv(book: GradeBook, path: str | Path) -> ImportResult:
    """Import rows of ``student_id,name,module,mark,credits``.

    ``name`` is only needed for students that don't exist yet and
    ``credits`` defaults to 10. Bad rows are skipped and reported.
    """
    result = ImportResult()
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise GradeError(f"CSV is missing columns: {', '.join(sorted(missing))}")
        for line, row in enumerate(reader, start=2):
            try:
                sid = row["student_id"].strip()
                if sid not in book.students:
                    name = (row.get("name") or "").strip()
                    if not name:
                        raise GradeError(f"new student {sid} needs a name")
                    book.add_student(sid, name)
                    result.new_students += 1
                credits = int(row.get("credits") or 10)
                book.add_grade(sid, row["module"].strip(), float(row["mark"]), credits)
                result.imported += 1
            except (GradeError, ValueError) as exc:
                result.errors.append(f"line {line}: {exc}")
    return result
