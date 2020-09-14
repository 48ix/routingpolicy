"""Test Route Map Generation."""
# Standard Library
import asyncio

# Project
from routingpolicy.config import params
from routingpolicy.generate import route_map

if __name__ == "__main__":
    asyncio.run(route_map(participant=params.participants[0]))
