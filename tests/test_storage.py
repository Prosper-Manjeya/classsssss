from gradetracker import storage
from gradetracker.models import GradeBook


def test_round_trip(tmp_path):
    path = tmp_path / "grades.json"
    book = GradeBook()
    book.add_student("S001", "Ada")
    book.add_grade("S001", "Programming 1", 72, 20)
    storage.save(book, path)

    loaded = storage.load(path)
    student = loaded.get_student("S001")
    assert student.name == "Ada"
    assert student.grades[0].mark == 72
    assert student.grades[0].credits == 20


def test_load_missing_file_returns_empty_book(tmp_path):
    book = storage.load(tmp_path / "does_not_exist.json")
    assert book.students == {}
