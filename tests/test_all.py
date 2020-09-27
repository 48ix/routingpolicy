"""Test all policy generation."""

# Standard Library
import asyncio

# Project
from routingpolicy.run import policy

if __name__ == "__main__":
    asyncio.run(policy())
