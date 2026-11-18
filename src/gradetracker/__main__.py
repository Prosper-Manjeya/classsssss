"""Allow running the tool with ``python -m gradetracker``."""

import sys

from .cli import main

sys.exit(main())
