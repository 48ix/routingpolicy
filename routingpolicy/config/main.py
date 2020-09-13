"""Initialize & Validate Configuration."""
# Standard Library
from pathlib import Path

# Third Party
import yaml

# Project
from routingpolicy.log import log, set_log_level
from routingpolicy.config.models.params import Params

CONFIG_FILE = Path("/etc/48ix-routingpolicy/config.yaml")


def get_config() -> Params:
    """Read config file and validate against config model."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"'{str(CONFIG_FILE)}' not found.")

    with CONFIG_FILE.open("r") as cf:
        raw = yaml.safe_load(cf)

    config = Params(**raw)

    return config


params = get_config()

set_log_level(log, params.debug)
