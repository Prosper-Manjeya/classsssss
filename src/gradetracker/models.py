"""Core data models for the grade tracker."""

from __future__ import annotations

from dataclasses import dataclass, field


CLASSIFICATION_BOUNDARIES = [
    (70, "First"),
    (60, "Upper second (2:1)"),
    (50, "Lower second (2:2)"),
    (40, "Third"),
]


def classify(average: float) -> str:
    """Return the UK degree classification for a weighted average."""
    for boundary, label in CLASSIFICATION_BOUNDARIES:
        if average >= boundary:
            return label
    return "Fail"


class GradeError(ValueError):
    """Raised when a grade or student operation is invalid."""


@dataclass
class Grade:
    module: str
    mark: float
    credits: int = 10

    def __post_init__(self) -> None:
        if not self.module.strip():
            raise GradeError("Module name cannot be empty")
        if not 0 <= self.mark <= 100:
            raise GradeError(f"Mark must be between 0 and 100, got {self.mark}")
        if self.credits <= 0:
            raise GradeError(f"Credits must be positive, got {self.credits}")


@dataclass
class Student:
    student_id: str
    name: str
    grades: list[Grade] = field(default_factory=list)

    def add_grade(self, grade: Grade) -> None:
        self.grades.append(grade)

    def total_credits(self) -> int:
        return sum(g.credits for g in self.grades)

    def weighted_average(self) -> float:
        """Credit-weighted average mark across all modules (0.0 if none)."""
        total = self.total_credits()
        if total == 0:
            return 0.0
        weighted = sum(g.mark * g.credits for g in self.grades)
        return round(weighted / total, 2)


class GradeBook:
    """A collection of students, keyed by student ID."""

    def __init__(self) -> None:
        self.students: dict[str, Student] = {}

    def add_student(self, student_id: str, name: str) -> Student:
        if student_id in self.students:
            raise GradeError(f"Student {student_id} already exists")
        student = Student(student_id, name)
        self.students[student_id] = student
        return student

    def get_student(self, student_id: str) -> Student:
        try:
            return self.students[student_id]
        except KeyError:
            raise GradeError(f"No student with ID {student_id}") from None

    def add_grade(self, student_id: str, module: str, mark: float, credits: int = 10) -> Grade:
        grade = Grade(module, mark, credits)
        self.get_student(student_id).add_grade(grade)
        return grade
