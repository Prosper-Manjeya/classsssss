# Grade Tracker

A small command-line application for recording university module marks and
calculating credit-weighted averages. Built as a software development
coursework project to practise Python, testing, Git branching and pull requests.

## Features

- Add students with an ID and name
- Record a mark (0–100) for each module, weighted by credits
- Generate a report with a credit-weighted average
- Data saved locally as JSON

## Getting started

Requires **Python 3.10+**.

```bash
git clone https://github.com/Prosper-Manjeya/classsssss.git
cd classsssss
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```bash
gradetracker add-student S001 "Ada Lovelace"
gradetracker add-grade S001 "Programming 1" 72 --credits 20
gradetracker add-grade S001 "Databases" 65 --credits 10
gradetracker report S001
```

By default data is stored in `grades.json` in the current folder. Use
`--file path/to/data.json` to choose another location.

## Running the tests

```bash
pytest
```

## Project structure

```
src/gradetracker/   application code
tests/              pytest test suite
```

## Development workflow

Work happens on short-lived branches (`feature/…`, `fix/…`, `docs/…`, `ci/…`)
that are merged into `main` through pull requests linked to issues.

## Author

Prosper Manjeya
