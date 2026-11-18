import pytest

from gradetracker.models import Grade, GradeBook, GradeError, Student, classify


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


@pytest.mark.parametrize(
    "average, expected",
    [
        (85, "First"),
        (70, "First"),
        (69.99, "Upper second (2:1)"),
        (60, "Upper second (2:1)"),
        (55, "Lower second (2:2)"),
        (40, "Third"),
        (39.5, "Fail"),
        (0, "Fail"),
    ],
)
def test_classify(average, expected):
    assert classify(average) == expected


def _book_with_grade():
    book = GradeBook()
    book.add_student("S001", "Ada")
    book.add_grade("S001", "Networks", 58, 15)
    return book


def test_edit_grade_mark():
    book = _book_with_grade()
    book.edit_grade("S001", "networks", mark=64)
    g = book.get_student("S001").grades[0]
    assert (g.mark, g.credits) == (64, 15)


def test_edit_grade_validates():
    book = _book_with_grade()
    with pytest.raises(GradeError):
        book.edit_grade("S001", "Networks", mark=120)
    assert book.get_student("S001").grades[0].mark == 58


def test_remove_grade():
    book = _book_with_grade()
    book.remove_grade("S001", "Networks")
    assert book.get_student("S001").grades == []


def test_remove_missing_grade():
    with pytest.raises(GradeError):
        _book_with_grade().remove_grade("S001", "Maths")


def test_sorted_students():
    book = GradeBook()
    book.add_student("S002", "bob")
    book.add_student("S001", "Ada")
    book.add_grade("S002", "Maths", 80)
    book.add_grade("S001", "Maths", 60)
    assert [s.student_id for s in book.sorted_students()] == ["S001", "S002"]
    assert [s.name for s in book.sorted_students("name")] == ["Ada", "bob"]
    assert [s.student_id for s in book.sorted_students("average")] == ["S002", "S001"]


def test_sorted_students_bad_key():
    with pytest.raises(GradeError):
        GradeBook().sorted_students("height")
