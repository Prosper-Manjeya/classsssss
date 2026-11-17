import csv

from gradetracker.cli import main
from gradetracker.export import HEADER, report_rows, write_csv
from gradetracker.models import Grade, Student


def _student():
    s = Student("S001", "Ada")
    s.add_grade(Grade("Programming 1", 72, 20))
    s.add_grade(Grade("Databases", 65, 10))
    return s


def test_report_rows_include_summary():
    rows = report_rows(_student())
    assert rows[0] == ["S001", "Ada", "Programming 1", "72", "20"]
    assert rows[-2] == ["S001", "Ada", "WEIGHTED AVERAGE", "69.67", "30"]
    assert rows[-1][3] == "Upper second (2:1)"


def test_report_rows_empty_student():
    assert report_rows(Student("S002", "Bob")) == []


def test_write_csv(tmp_path):
    path = tmp_path / "ada.csv"
    assert write_csv(_student(), path) == 4
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows[0] == HEADER
    assert len(rows) == 5


def test_cli_report_csv(tmp_path, capsys):
    data, out = str(tmp_path / "g.json"), tmp_path / "r.csv"
    main(["--file", data, "add-student", "S001", "Ada"])
    main(["--file", data, "add-grade", "S001", "Maths", "55"])
    assert main(["--file", data, "report", "S001", "--csv", str(out)]) == 0
    assert out.exists()
    assert "Saved CSV report" in capsys.readouterr().out
