"""Jinja & Template Utilities/Helpers."""

# Standard Library
from pathlib import Path

# Third Party
from jinja2 import Environment, PackageLoader

# Project
from routingpolicy import APP_DIR

template_env = Environment(
    loader=PackageLoader("routingpolicy", "templates"),
    enable_async=True,
    trim_blocks=True,
)

POLICIES_DIR = APP_DIR / "policies"
GLOBALS_DIR = Path(__file__).parent / "global_policy"
