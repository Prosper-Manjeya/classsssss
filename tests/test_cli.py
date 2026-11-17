from gradetracker.cli import main


def test_full_workflow(tmp_path, capsys):
    f = str(tmp_path / "g.json")
    assert main(["--file", f, "add-student", "S001", "Ada"]) == 0
    assert main(["--file", f, "add-grade", "S001", "Programming 1", "72", "--credits", "20"]) == 0
    assert main(["--file", f, "report", "S001"]) == 0
    out = capsys.readouterr().out
    assert "Programming 1" in out
    assert "72.00" in out


def test_unknown_student_returns_error(tmp_path, capsys):
    f = str(tmp_path / "g.json")
    assert main(["--file", f, "report", "S404"]) == 1
    assert "No student" in capsys.readouterr().err
