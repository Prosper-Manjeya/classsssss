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

    def find_grade(self, module: str) -> Grade:
        for grade in self.grades:
            if grade.module.lower() == module.lower():
                return grade
        raise GradeError(f"{self.student_id} has no grade for {module}")

    def remove_grade(self, module: str) -> Grade:
        grade = self.find_grade(module)
        self.grades.remove(grade)
        return grade

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

    def sorted_students(self, by: str = "id") -> list[Student]:
        """Students sorted by ``id``, ``name`` or ``average`` (highest first)."""
        if by == "name":
            return sorted(self.students.values(), key=lambda s: s.name.lower())
        if by == "average":
            return sorted(self.students.values(), key=lambda s: s.weighted_average(), reverse=True)
        if by == "id":
            return sorted(self.students.values(), key=lambda s: s.student_id)
        raise GradeError(f"Cannot sort by {by!r}")

    def get_student(self, student_id: str) -> Student:
        try:
            return self.students[student_id]
        except KeyError:
            raise GradeError(f"No student with ID {student_id}") from None

    def add_grade(self, student_id: str, module: str, mark: float, credits: int = 10) -> Grade:
        grade = Grade(module, mark, credits)
        self.get_student(student_id).add_grade(grade)
        return grade

    def edit_grade(self, student_id: str, module: str, mark: float | None = None,
                   credits: int | None = None) -> Grade:
        student = self.get_student(student_id)
        old = student.find_grade(module)
        new = Grade(old.module,
                    old.mark if mark is None else mark,
                    old.credits if credits is None else credits)
        student.grades[student.grades.index(old)] = new
        return new

    def remove_grade(self, student_id: str, module: str) -> Grade:
        return self.get_student(student_id).remove_grade(module)
