"""Project-local runtime configuration."""

from __future__ import annotations

import logging
from pathlib import Path

from dotenv import load_dotenv


def load_project_environment() -> bool:
    """Load the current project's ``.env`` without overriding shell variables."""
    dotenv_path = Path.cwd() / ".env"
    if not dotenv_path.is_file():
        return False
    previous_disable_level = logging.root.manager.disable
    # A project .env is optional configuration. Ignore parser warnings for
    # malformed lines while still allowing valid assignments to load.
    logging.disable(logging.WARNING)
    try:
        return load_dotenv(dotenv_path=dotenv_path, override=False)
    finally:
        logging.disable(previous_disable_level)
