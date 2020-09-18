"""Socket API Configuration & Validation."""

# Standard Library
from pathlib import Path

# Third Party
from pydantic import FilePath, BaseModel


class Api(BaseModel):
    """Socket API Configuration Paramenters."""

    port: int = 4801
    path: FilePath = Path("/tmp/48ix_routingpolicy_api.sock")
