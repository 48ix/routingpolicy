"""Test ACL deployment via RPC client."""

# Third Party
import rpyc
from rpyc.core import Connection

# Project
from routingpolicy.log import log


def test_rpc_acl() -> None:
    """Open an RPC connection and request and ACL update."""
    connection: Connection = rpyc.connect("localhost", "4801", ipv6=True)
    result = connection.root.update_acls()
    log.info(result)


if __name__ == "__main__":
    test_rpc_acl()
