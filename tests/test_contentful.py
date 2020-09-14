"""Test Contentful API Data Collection."""

# Standard Library
import json
import asyncio

# Project
from routingpolicy.contentful import get_data

if __name__ == "__main__":
    participants, route_servers = asyncio.run(get_data())
    print(json.dumps([p.dict() for p in participants], default=str, indent=2))
    print(json.dumps([r.dict() for r in route_servers], default=str, indent=2))
