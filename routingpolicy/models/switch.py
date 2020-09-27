"""Configuration Models for IX Switches."""

# Third Party
from pydantic import BaseModel, SecretStr, StrictStr


class Switch(BaseModel):
    """Configuration model for an IX switch."""

    name: StrictStr
    address: StrictStr
    username: StrictStr
    password: SecretStr
