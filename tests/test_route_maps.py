"""Test Route Map Generation."""
# Standard Library
import asyncio

# Project
from routingpolicy.config import params
from routingpolicy.generate import route_map

if __name__ == "__main__":
    asyncio.run(
        route_map(participant=params.participants[0], rs_id=1, loc_id=1, metro_id=1)
    )
