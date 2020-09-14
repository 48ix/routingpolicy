"""Participant Parameter Configuration Model."""

# Standard Library
from typing import List
from ipaddress import IPv4Address, IPv6Address

# Third Party
from pydantic import BaseModel, StrictInt, StrictStr

# Project
from routingpolicy.models.asn import Asn


class Participant(BaseModel):
    """48 IX Participant Parameters."""

    id: StrictInt
    name: StrictStr
    asn: Asn
    ipv4: List[IPv4Address]
    ipv6: List[IPv6Address]
    port_speed: StrictInt
    circuit_id: StrictStr

    @property
    def pretty(self) -> str:
        """Generate a pretty display name for the participant."""
        return f"{self.name} ({self.asn.prefixed()})"
