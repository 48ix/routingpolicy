"""Configuration Parameters Validation Model."""

# Standard Library
from typing import List

# Third Party
from pydantic import BaseModel, StrictBool

from .participant import Participant


class MaxLen(BaseModel):
    ipv4: int = 24
    ipv6: int = 48


class Params(BaseModel):
    """Configuration Parameters."""

    debug: StrictBool = False
    participants: List[Participant]
    max_length: MaxLen = MaxLen()
