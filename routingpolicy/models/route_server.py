"""Route Server Parameter Configuration Model."""
# Standard Library
from ipaddress import IPv4Network, IPv6Network

# Third Party
from pydantic import BaseModel, StrictInt, StrictStr


class RouteServer(BaseModel):
    """48 IX Route Server Parameters."""

    id: StrictInt
    name: StrictStr
    metro_id: StrictInt
    loc_id: StrictInt
    ipv4_peering: IPv4Network
    ipv6_peering: IPv6Network
