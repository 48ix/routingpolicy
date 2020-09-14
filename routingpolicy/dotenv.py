"""Import Environment Variables from Local Files."""

# Standard Library
import os
import re
from typing import Generator
from pathlib import Path

ENV_FILES = (".env", ".env.local")

REPO = Path(__file__).parent.parent


def find_env() -> Generator[Path, None, None]:
    """Locate environment files."""
    for file in ENV_FILES:
        path = REPO / file
        if path.exists():
            yield path


def load_env() -> None:
    """Parse env files & set env variables."""
    for file in find_env():
        with file.open("r") as f:
            for line in f.readlines():
                key, value = line.strip().rstrip().split("=")
                key = re.sub(r"[^A-Za-z0-9_]", "_", key).upper()
                os.environ[key] = value
