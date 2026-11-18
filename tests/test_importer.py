import pytest

from gradetracker.cli import main
from gradetracker.importer import import_csv
from gradetracker.models import GradeBook, GradeError


def write(tmp_path, text):
    path = tmp_path / "in.csv"
    path.write_text(text, encoding="utf-8")
    return path


def test_import_creates_students_and_grades(tmp_path):
    path = write(tmp_path, "student_id,name,module,mark,credits\n"
                           "S1,Ada,Maths,70,20\nS1,,Physics,65,\nS2,Bob,Maths,48,20\n")
    book = GradeBook()
    res = import_csv(book, path)
    assert (res.imported, res.new_students, res.errors) == (3, 2, [])
    assert book.get_student("S1").grades[1].credits == 10


def test_bad_rows_are_skipped(tmp_path):
    path = write(tmp_path, "student_id,name,module,mark\n"
                           "S1,Ada,Maths,abc\nS2,,Maths,50\nS3,Cy,Maths,150\nS4,Di,Maths,55\n")
    res = import_csv(GradeBook(), path)
    assert res.imported == 1
    assert [e.split(":")[0] for e in res.errors] == ["line 2", "line 3", "line 4"]


def test_missing_columns(tmp_path):
    with pytest.raises(GradeError, match="mark"):
        import_csv(GradeBook(), write(tmp_path, "student_id,module\nS1,Maths\n"))


def test_cli_import(tmp_path, capsys):
    path = write(tmp_path, "student_id,name,module,mark\nS1,Ada,Maths,70\n")
    data = str(tmp_path / "g.json")
    assert main(["--file", data, "import-csv", str(path)]) == 0
    assert "Imported 1 grades (1 new students)" in capsys.readouterr().out
    assert main(["--file", data, "report", "S1"]) == 0
