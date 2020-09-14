"""Test BGP Config Generation."""

# Standard Library
import asyncio

# Project
from routingpolicy.config import params
from routingpolicy.generate import bgp

if __name__ == "__main__":
    asyncio.run(bgp(params.participants[0]))
