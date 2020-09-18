"""Routing Policy Socket API Entrypoint."""

# Third Party
from rpyc.utils.server import ThreadedServer

# Project
from routingpolicy.log import log
from routingpolicy.config import params
from routingpolicy.api.services.updater import Updater


def start_api() -> None:
    """Start the socket API server."""
    log.info("Starting Socket API")
    server = ThreadedServer(
        Updater,
        hostname="::",
        port=params.api.port,
        ipv6=True,
    )
    server.start()
