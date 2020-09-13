"""Configuration Parameters Validation Model."""

# Standard Library
from typing import List

# Third Party
from pydantic import BaseModel, StrictBool

from .participant import Participant
from .route_server import RouteServer


class MaxLen(BaseModel):
    """Maximum Prefix Length Parameters."""

    ipv4: int = 24
    ipv6: int = 48


class Params(BaseModel):
    """Configuration Parameters."""

    debug: StrictBool = False
    max_length: MaxLen = MaxLen()
    participants: List[Participant]
    route_servers: List[RouteServer]
