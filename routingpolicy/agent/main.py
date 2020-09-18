"""Interact with Route Servers."""

# Standard Library
import asyncio

# Project
from routingpolicy.log import log
from routingpolicy.config import params
from routingpolicy.agent.send import send_policy


async def send_policies() -> None:
    """Send generated policies to each defined route server."""
    tasks = (send_policy(r) for r in params.route_servers)
    try:
        await asyncio.gather(*tasks)
    except ConnectionError as err:
        log.critical(str(err))
