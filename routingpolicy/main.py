"""48 IX Particpant Route Server Config Management."""

from routingpolicy.generate import generate_all
from routingpolicy.combine import generate_combined


async def policy() -> None:
    """Generate participant policies and config files."""
    await generate_all()
    await generate_combined()
