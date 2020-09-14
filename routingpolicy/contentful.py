"""Get Participant Information via Contentful API."""
# Standard Library
import os
from typing import Dict, List, Tuple, AsyncGenerator

# Third Party
from httpx import AsyncClient

# Project
from routingpolicy.dotenv import load_env
from routingpolicy.models.participant import Participant
from routingpolicy.models.route_server import RouteServer


async def get_participants(data: Dict) -> AsyncGenerator[Participant, None]:
    """Validate Participants from Contentful."""
    if data["total"] == 0:
        raise LookupError("Unable to load participants from Contentful")
    for entry in data["includes"]["Entry"]:
        yield Participant(**entry["fields"])


async def get_route_servers(data: Dict) -> AsyncGenerator[RouteServer, None]:
    """Validate Route Servers from Contentful."""
    if data["total"] == 0:
        raise LookupError("Unable to load route servers from Contentful")
    for entry in data["includes"]["Entry"]:
        yield RouteServer(**entry["fields"])


async def get_data() -> Tuple[List[Participant], List[RouteServer]]:
    """Get Configuration Data from Contentful."""
    load_env()

    async with AsyncClient(
        http2=True,
        verify=True,
        base_url="https://cdn.contentful.com",
        headers={"accept": "application/json"},
        params={"access_token": os.environ["CONTENTFUL_ACCESS_TOKEN"]},
    ) as client:
        uri = f'/spaces/{os.environ["CONTENTFUL_SPACE"]}/entries'

        res_participants = await client.get(
            uri,
            params={"content_type": "participants", "fields.main": "1"},
        )
        res_participants.raise_for_status()

        participants = sorted(
            [p async for p in get_participants(res_participants.json())],
            key=lambda i: i.id,
        )

        res_route_servers = await client.get(
            uri,
            params={"content_type": "route_servers", "fields.main": "1"},
        )
        res_route_servers.raise_for_status()
        route_servers = sorted(
            [r async for r in get_route_servers(res_route_servers.json())],
            key=lambda i: i.id,
        )

        return participants, route_servers
