"""Test Requires Update Comparison."""

# Standard Library
import asyncio

# Project
from routingpolicy.config import params
from routingpolicy.arista.compare import requires_update

if __name__ == "__main__":
    asyncio.run(requires_update(params.switches, params.participants).ag_await())
