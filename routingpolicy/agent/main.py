"""Interact with Route Servers."""

# Standard Library
import asyncio
from typing import Sequence

# Project
from routingpolicy.config import params
from routingpolicy.agent.send import send_policy


async def send_policies(wait: int = 0) -> Sequence[str]:
    """Send generated policies to each defined route server."""
    tasks = (send_policy(r, wait) for r in params.route_servers)
    return await asyncio.gather(*tasks)
