"""Create & Send Encrypted Policy Payload to a 48 IX Route Server."""

# Standard Library
import time
import hashlib
from socket import gaierror
from typing import Tuple
from pathlib import Path

# Third Party
import rpyc
from rpyc.core import Connection
from cryptography.fernet import Fernet

# Project
from routingpolicy.log import log
from routingpolicy.config import params
from routingpolicy.models.route_server import RouteServer


def create_payload(policy: str) -> Tuple[bytes, str, str]:
    """Create encrypted payload & digests.

    Both the pre-encryption & post-encryption SHA256 digests are sent
    ahead of the payload itself to ensure data integrity on both ends.
    """
    encrypted = Fernet(params.agent.key.get_secret_value()).encrypt(policy.encode())
    predigest = hashlib.sha256(policy.encode()).hexdigest()
    postdigest = hashlib.sha256(encrypted).hexdigest()
    return encrypted, predigest, postdigest


async def send_policy(route_server: RouteServer, wait: int) -> str:
    """Read a generated policy & send it to a route server."""
    result = ""
    # Optionally block pause of execution.
    if wait:
        log.info("Waiting {} seconds before proceeding with update", wait)
        time.sleep(wait)

    try:
        connection: Connection = rpyc.connect(
            route_server.name, params.agent.port, ipv6=True
        )
    except ConnectionRefusedError:
        result = "Connection refused to {}:{}".format(
            route_server.name, params.agent.port
        )
    except gaierror:
        result = "Route Server {}:{} is unreachable".format(
            route_server.name, params.agent.port
        )

    # If an error has occurred, stop here & return a valuable error
    # message.
    if result:
        log.critical(result)
        return result

    config_file = (
        Path(__file__).parent.parent.parent
        / "policies"
        / route_server.name
        / "_all.ios"
    )

    # Read the combined configuration file & generate a SHA256 digest of
    # its content. Then, encrypt the content, and generate another
    # SHA256 digest of the encrypted contents.
    with config_file.open("r") as f:
        payload, predigest, postdigest = create_payload(f.read())

    log.debug("Pre Encryption Digest: {}", predigest)
    log.debug("Post Encryption Digest: {}", postdigest)

    while not connection.closed:
        log.info("Sending Policy to Route Server {} ({})", route_server.name, predigest)

        # Send the preflight payload digests.
        connection.root.set_digest(postdigest, predigest)

        # Send the encrypted payload.
        response = connection.root.push_policy(payload)
        log.success(response)
        result = "Deployed Policy to Route Server {}".format(route_server.name)
        break

    # Gracefully close the connection.
    connection.close()
    return result
