"""Participant Parameter Configuration Model."""

# Standard Library
from typing import Union, List
from ipaddress import IPv4Address, IPv6Address

# Third Party
from pydantic import BaseModel, StrictInt, StrictStr, conint

ASN16 = conint(strict=True, ge=1, lt=64512)
ASN32 = conint(strict=True, ge=65536, lt=4200000000)


class Participant(BaseModel):
    """48 IX Participant Parameters."""

    id: StrictInt
    name: StrictStr
    asn: Union[ASN16, ASN32]
    ipv4: List[IPv4Address]
    ipv6: List[IPv6Address]
