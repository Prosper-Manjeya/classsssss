"""Saving and loading a GradeBook as JSON."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import Grade, GradeBook, Student


def save(book: GradeBook, path: str | Path) -> None:
    data = {sid: asdict(student) for sid, student in book.students.items()}
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def load(path: str | Path) -> GradeBook:
    book = GradeBook()
    path = Path(path)
    if not path.exists():
        return book
    data = json.loads(path.read_text(encoding="utf-8"))
    for sid, record in data.items():
        grades = [Grade(**g) for g in record.get("grades", [])]
        book.students[sid] = Student(sid, record["name"], grades)
    return book
