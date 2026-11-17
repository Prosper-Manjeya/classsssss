import pytest

from gradetracker.models import Grade, GradeBook, GradeError, Student


def test_valid_grade():
    g = Grade("Programming 1", 72, 20)
    assert g.mark == 72
    assert g.credits == 20


@pytest.mark.parametrize("mark", [-1, 100.5, 250])
def test_mark_out_of_range(mark):
    with pytest.raises(GradeError):
        Grade("Maths", mark)


@pytest.mark.parametrize("credits", [0, -10])
def test_non_positive_credits(credits):
    with pytest.raises(GradeError):
        Grade("Maths", 50, credits)


def test_empty_module_name():
    with pytest.raises(GradeError):
        Grade("   ", 50)


def test_weighted_average():
    s = Student("S001", "Ada")
    s.add_grade(Grade("Programming 1", 72, 20))
    s.add_grade(Grade("Databases", 65, 10))
    assert s.weighted_average() == pytest.approx(69.67)
    assert s.total_credits() == 30


def test_weighted_average_no_grades():
    s = Student("S002", "Bob")
    assert s.weighted_average() == 0.0


def test_add_and_get_student():
    book = GradeBook()
    book.add_student("S001", "Ada")
    assert book.get_student("S001").name == "Ada"


def test_duplicate_student_rejected():
    book = GradeBook()
    book.add_student("S001", "Ada")
    with pytest.raises(GradeError):
        book.add_student("S001", "Someone else")


def test_unknown_student():
    with pytest.raises(GradeError):
        GradeBook().get_student("NOPE")


def test_add_grade_through_book():
    book = GradeBook()
    book.add_student("S001", "Ada")
    book.add_grade("S001", "Networks", 58, 15)
    assert book.get_student("S001").grades[0].module == "Networks"
