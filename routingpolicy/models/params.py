"""Configuration Parameters Validation Model."""

# Standard Library
import os
from typing import Any, Dict, List, Tuple, Generator

# Third Party
from pydantic import (
    BaseModel,
    SecretStr,
    StrictStr,
    StrictBool,
    IPvAnyAddress,
    IPvAnyNetwork,
    root_validator,
)

# Project
from routingpolicy.dotenv import load_env
from routingpolicy.models.agent import Agent

# from routingpolicy.contentful import get_data
from routingpolicy.models.participant import Participant
from routingpolicy.models.route_server import RouteServer

_RSNetG = Generator[IPvAnyNetwork, None, None]
_RSNetT = Tuple[IPvAnyNetwork, ...]
_NetMember = Generator[bool, None, None]

_IPError = "IP {} from participant {} is not contained within any RS Peering LANs:\n{}"


def get_networks(route_servers: List[RouteServer]) -> _RSNetG:
    """Get all peering networks assigned to a route server."""
    for rs in route_servers:
        for family in (4, 6):
            yield getattr(rs, f"ipv{family}_peering")


def network_member(networks: _RSNetT, address: IPvAnyAddress) -> _NetMember:
    """Verify if address is a member of any networks."""
    for net in networks:
        yield address in net


class Contentful(BaseModel):
    """Contentful API Parameters."""

    space: StrictStr
    access_token: SecretStr

    @root_validator(pre=True)
    def validate_contentful(cls, values: Any) -> Dict[str, str]:
        """Load Contentful environment variables."""
        if (
            "CONTENTFUL_SPACE" not in os.environ
            or "CONTENTFUL_ACCESS_TOKEN" not in os.environ
        ):
            load_env()
        try:
            return {
                "space": os.environ["CONTENTFUL_SPACE"],
                "access_token": os.environ["CONTENTFUL_ACCESS_TOKEN"],
            }
        except KeyError as key:
            raise ValueError(f"{key} is missing from environment variables.")


class MaxLen(BaseModel):
    """Maximum Prefix Length Parameters."""

    ipv4: int = 24
    ipv6: int = 48


class Params(BaseModel):
    """Configuration Parameters."""

    debug: StrictBool = False
    max_length: MaxLen = MaxLen()
    route_servers: List[RouteServer]
    contentful: Contentful = Contentful()
    participants: List[Participant]
    agent: Agent

    @root_validator
    def validate_model(cls, values: Dict) -> Dict:
        """Ensure Participant addresses are contained within RS networks."""

        networks = tuple(get_networks(values["route_servers"]))

        for family in (4, 6):
            for participant in values["participants"]:
                for addr in getattr(participant, f"ipv{family}"):
                    if not any(network_member(networks, addr)):
                        raise ValueError(
                            _IPError.format(
                                str(addr),
                                f"{participant.name} (AS{participant.asn})",
                                "\n".join("\t - " + str(n) for n in networks) + "\n",
                            )
                        )
        return values
