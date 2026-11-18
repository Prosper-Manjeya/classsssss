# Contributing

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Workflow

1. Open an issue describing the bug or feature.
2. Create a branch from `main`:
   - `feature/<short-name>` for new features
   - `fix/<short-name>` for bug fixes
   - `docs/<short-name>`, `ci/<short-name>`, `chore/<short-name>` for everything else
3. Commit in small steps with clear messages (imperative mood: "Add…", "Fix…").
4. Add or update tests. `pytest` must pass.
5. Open a pull request into `main` and link the issue (`Closes #N`).
6. Merge once CI is green.

## Code style

- Python 3.10+, type hints on public functions
- Keep CLI code in `cli.py` thin and put logic in the other modules so it can be tested
