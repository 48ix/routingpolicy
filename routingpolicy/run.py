"""48 IX Particpant Route Server Config Management."""

# Standard Library
import asyncio

# Project
from routingpolicy.agent import send_policies
from routingpolicy.combine import generate_combined
from routingpolicy.generate import generate_all


async def policy(wait: int = 0) -> None:
    """Generate participant policies and config files."""
    await generate_all()
    await generate_combined()
    await send_policies(wait)


if __name__ == "__main__":
    asyncio.run(policy())
