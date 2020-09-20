"""Services Entry."""

# Standard Library
import asyncio
from typing import Generator

# Third Party
from rpyc import Service

# Project
from routingpolicy.log import log
from routingpolicy.run import policy


class Updater(Service):
    """Route Server Agent Service."""

    def exposed_update_policy(self, wait: int = 60) -> Generator[str, None, None]:
        """Run a policy refresh & push it to route servers."""
        log.info("Received request to update routing policies")
        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(policy(wait))
        for result in results:
            yield result
