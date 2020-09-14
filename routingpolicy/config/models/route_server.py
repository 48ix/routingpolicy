"""Route Server Parameter Configuration Model."""
from ipaddress import IPv4Network, IPv6Network
from pydantic import BaseModel, StrictStr, StrictInt


class RouteServer(BaseModel):
    """48 IX Route Server Parameters."""

    id: StrictInt
    name: StrictStr
    metro_id: StrictInt
    loc_id: StrictInt
    ipv4_peering: IPv4Network
    ipv6_peering: IPv6Network
