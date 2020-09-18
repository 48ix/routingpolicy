"""Services Entry."""
# Standard Library
import asyncio

# Third Party
from rpyc import Service

# Project
from routingpolicy.log import log
from routingpolicy.run import policy


class Updater(Service):
    """Route Server Agent Service."""

    def exposed_update_policy(self, wait: int = 60) -> str:
        """Run a policy refresh & push it to route servers."""
        log.info("Received request to update routing policies")

        asyncio.run(policy(wait))

        return "Successfully updated routing policies"
