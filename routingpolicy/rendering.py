"""Jinja & Template Utilities/Helpers."""

# Standard Library
from pathlib import Path

# Third Party
from jinja2 import Environment, PackageLoader

template_env = Environment(
    loader=PackageLoader("routingpolicy", "templates"),
    enable_async=True,
    trim_blocks=True,
)

POLICIES_DIR = Path(__file__).parent.parent / "policies"
GLOBALS_DIR = Path(__file__).parent / "global_policy"
