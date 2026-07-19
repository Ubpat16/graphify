"""Project-local runtime configuration."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv


def load_project_environment() -> bool:
    """Load the current project's ``.env`` without overriding shell variables."""
    dotenv_path = Path.cwd() / ".env"
    if not dotenv_path.is_file():
        return False
    return load_dotenv(dotenv_path=dotenv_path, override=False)
