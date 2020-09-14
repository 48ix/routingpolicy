"""Test All Policy Generation."""
# Standard Library
import asyncio

# Project
from routingpolicy.main import policy

if __name__ == "__main__":
    asyncio.run(policy())
