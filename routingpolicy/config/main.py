"""Initialize & Validate Configuration."""

# Standard Library
import asyncio
from pathlib import Path

# Third Party
import yaml
from pydantic import MissingError, ValidationError
from pydantic.error_wrappers import ErrorWrapper

# Project
from routingpolicy.log import log, setup_logging
from routingpolicy.contentful import get_data
from routingpolicy.models.params import Params

CONFIG_FILE = Path("/etc/48ix-routingpolicy/config.yaml")


def get_config() -> Params:
    """Read config file and validate against config model."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"'{str(CONFIG_FILE)}' not found.")

    with CONFIG_FILE.open("r") as cf:
        raw = yaml.safe_load(cf) or {}
    contentful = raw.get("contentful", {})
    for key in ("space", "access_token"):
        if key not in contentful:
            raise ValidationError([ErrorWrapper(MissingError(), key)], Params)
    participants, route_servers = asyncio.run(
        get_data(space=contentful["space"], access_token=contentful["access_token"])
    )
    config = Params(**raw, participants=participants, route_servers=route_servers)

    return config


params = get_config()

setup_logging(
    log,
    debug=params.debug,
    logfile=params.logfile,
    logsize=params.logsize.human_readable(),
)
