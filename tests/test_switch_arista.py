"""Test Sending ACLs to Arista Switches."""

# Standard Library
import asyncio

# Project
from routingpolicy.config import params
from routingpolicy.arista.send import send_acls

if __name__ == "__main__":
    asyncio.run(send_acls(params.switches, params.participants))
