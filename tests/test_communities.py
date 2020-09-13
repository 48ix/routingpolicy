"""Test BGP Community Generation."""
# Standard Library
import asyncio

# Project
from routingpolicy.config import params
from routingpolicy.generate import communities

if __name__ == "__main__":
    asyncio.run(communities(participant=params.participants[0]))
