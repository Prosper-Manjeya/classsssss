import os
import subprocess
import sys

import pytest

from gradetracker import __version__
from gradetracker.cli import main


def test_full_workflow(tmp_path, capsys):
    f = str(tmp_path / "g.json")
    assert main(["--file", f, "add-student", "S001", "Ada"]) == 0
    assert main(["--file", f, "add-grade", "S001", "Programming 1", "72", "--credits", "20"]) == 0
    assert main(["--file", f, "report", "S001"]) == 0
    out = capsys.readouterr().out
    assert "Programming 1" in out
    assert "72.00" in out
    assert "First" in out


def test_unknown_student_returns_error(tmp_path, capsys):
    f = str(tmp_path / "g.json")
    assert main(["--file", f, "report", "S404"]) == 1
    assert "No student" in capsys.readouterr().err


def test_report_for_student_without_grades(tmp_path, capsys):
    f = str(tmp_path / "g.json")
    main(["--file", f, "add-student", "S002", "Bob"])
    assert main(["--file", f, "report", "S002"]) == 0
    assert "0.00" in capsys.readouterr().out


def test_edit_and_remove_grade(tmp_path, capsys):
    f = str(tmp_path / "g.json")
    main(["--file", f, "add-student", "S001", "Ada"])
    main(["--file", f, "add-grade", "S001", "Databases", "50"])
    assert main(["--file", f, "edit-grade", "S001", "Databases", "--mark", "65"]) == 0
    assert main(["--file", f, "edit-grade", "S001", "Databases"]) == 1
    assert main(["--file", f, "remove-grade", "S001", "Databases"]) == 0
    assert main(["--file", f, "remove-grade", "S001", "Databases"]) == 1


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_run_as_module(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "gradetracker", "--file", str(tmp_path / "g.json"),
         "add-student", "S001", "Ada"],
        capture_output=True, text=True, env={**os.environ, "PYTHONPATH": "src"},
    )
    assert result.returncode == 0
    assert "Added student S001" in result.stdout


def test_list_students(tmp_path, capsys):
    f = str(tmp_path / "g.json")
    main(["--file", f, "add-student", "S001", "Ada"])
    main(["--file", f, "add-student", "S002", "Bob"])
    main(["--file", f, "add-grade", "S002", "Maths", "80"])
    capsys.readouterr()
    assert main(["--file", f, "list", "--sort", "average"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("S002")
    assert "1 modules" in lines[0]


def test_list_empty(tmp_path, capsys):
    assert main(["--file", str(tmp_path / "g.json"), "list"]) == 0
    assert "No students yet" in capsys.readouterr().out
