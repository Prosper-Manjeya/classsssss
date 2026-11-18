import pytest

from gradetracker.cli import main
from gradetracker.models import GradeBook, GradeError
from gradetracker.stats import module_names, module_stats


@pytest.fixture
def book():
    b = GradeBook()
    for sid, mark in [("S1", 35), ("S2", 60), ("S3", 72), ("S4", 81)]:
        b.add_student(sid, sid)
        b.add_grade(sid, "Databases", mark)
    b.add_grade("S1", "networks", 50)
    return b


def test_module_stats(book):
    ms = module_stats(book, "databases")
    assert ms.count == 4
    assert ms.mean == 62.0
    assert ms.median == 66.0
    assert (ms.minimum, ms.maximum) == (35, 81)
    assert ms.pass_rate == 75.0


def test_unknown_module(book):
    with pytest.raises(GradeError):
        module_stats(book, "Astrophysics")


def test_module_names(book):
    assert module_names(book) == ["Databases", "networks"]


def test_cli_stats(tmp_path, capsys):
    f = str(tmp_path / "g.json")
    main(["--file", f, "add-student", "S1", "Ada"])
    main(["--file", f, "add-grade", "S1", "Maths", "64"])
    capsys.readouterr()
    assert main(["--file", f, "stats"]) == 0
    assert capsys.readouterr().out.strip() == "Maths"
    assert main(["--file", f, "stats", "Maths"]) == 0
    assert "Pass rate (40+): 100.0%" in capsys.readouterr().out
    assert main(["--file", f, "stats", "Physics"]) == 1
