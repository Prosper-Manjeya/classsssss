"""Command-line interface for the grade tracker."""

from __future__ import annotations

import argparse
import sys

from . import __version__, export, stats, storage
from .models import GradeError, classify

DEFAULT_FILE = "grades.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gradetracker", description=__doc__)
    parser.add_argument("--file", default=DEFAULT_FILE, help="data file (default: grades.json)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-student", help="add a new student")
    p.add_argument("student_id")
    p.add_argument("name")

    p = sub.add_parser("add-grade", help="record a module mark")
    p.add_argument("student_id")
    p.add_argument("module")
    p.add_argument("mark", type=float)
    p.add_argument("--credits", type=int, default=10)

    p = sub.add_parser("edit-grade", help="change the mark or credits of a module")
    p.add_argument("student_id")
    p.add_argument("module")
    p.add_argument("--mark", type=float)
    p.add_argument("--credits", type=int)

    p = sub.add_parser("remove-grade", help="delete a module grade")
    p.add_argument("student_id")
    p.add_argument("module")

    p = sub.add_parser("list", help="list all students with their averages")
    p.add_argument("--sort", choices=["id", "name", "average"], default="id")

    p = sub.add_parser("stats", help="show statistics for a module (or list modules)")
    p.add_argument("module", nargs="?")

    p = sub.add_parser("report", help="show a student's grades and average")
    p.add_argument("student_id")
    p.add_argument("--csv", metavar="FILE", help="also save the report as a CSV file")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    book = storage.load(args.file)
    try:
        if args.command == "add-student":
            book.add_student(args.student_id, args.name)
            print(f"Added student {args.student_id}: {args.name}")
        elif args.command == "add-grade":
            book.add_grade(args.student_id, args.module, args.mark, args.credits)
            print(f"Recorded {args.mark} in {args.module} for {args.student_id}")
        elif args.command == "edit-grade":
            if args.mark is None and args.credits is None:
                raise GradeError("Give --mark and/or --credits to change")
            g = book.edit_grade(args.student_id, args.module, args.mark, args.credits)
            print(f"Updated {g.module} for {args.student_id}: {g.mark} ({g.credits} credits)")
        elif args.command == "remove-grade":
            g = book.remove_grade(args.student_id, args.module)
            print(f"Removed {g.module} for {args.student_id}")
        elif args.command == "list":
            students = book.sorted_students(args.sort)
            if not students:
                print("No students yet. Add one with add-student.")
            for st in students:
                avg = f"{st.weighted_average():6.2f}" if st.grades else "     -"
                print(f"{st.student_id:<8} {st.name:<25} {avg}  ({len(st.grades)} modules)")
        elif args.command == "stats":
            if args.module is None:
                names = stats.module_names(book)
                print("\n".join(names) if names else "No modules recorded yet.")
            else:
                ms = stats.module_stats(book, args.module)
                print(f"{ms.module}: {ms.count} students")
                print(f"  Mean {ms.mean:.2f} | Median {ms.median:.2f} | "
                      f"Min {ms.minimum:g} | Max {ms.maximum:g}")
                print(f"  Pass rate (40+): {ms.pass_rate:.1f}%")
        elif args.command == "report":
            student = book.get_student(args.student_id)
            print(f"Report for {student.name} ({student.student_id})")
            for g in student.grades:
                print(f"  {g.module:<25} {g.mark:>6.1f}  ({g.credits} credits)")
            average = student.weighted_average()
            print(f"  Weighted average: {average:.2f}")
            if student.grades:
                print(f"  Classification:   {classify(average)}")
            if args.csv:
                export.write_csv(student, args.csv)
                print(f"Saved CSV report to {args.csv}")
    except GradeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    storage.save(book, args.file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
