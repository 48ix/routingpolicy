"""48 IX Particpant Route Server Config Management."""

# Standard Library
import asyncio
from typing import Sequence

# Project
from routingpolicy.agent import send_policies
from routingpolicy.combine import generate_combined
from routingpolicy.generate import generate_all


async def policy(wait: int = 0) -> Sequence[str]:
    """Generate participant policies and config files."""
    _, __, results = await asyncio.gather(
        generate_all(), generate_combined(), send_policies(wait)
    )
    return results
