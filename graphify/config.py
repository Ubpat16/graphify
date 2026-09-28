"""Project-local runtime configuration."""

from __future__ import annotations

import logging
from pathlib import Path

from dotenv import load_dotenv


_GRAPHIFY_ROOT = Path(__file__).resolve().parents[1]


def load_project_environment() -> bool:
    """Load project ``.env``, falling back to Graphify's own configuration."""
    project_dotenv = Path.cwd() / ".env"
    dotenv_path = project_dotenv if project_dotenv.is_file() else _GRAPHIFY_ROOT / ".env"
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
