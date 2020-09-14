"""Test Combined Configuration Generation."""

# Standard Library
import asyncio

# Project
from routingpolicy.combine import generate_combined

if __name__ == "__main__":
    asyncio.run(generate_combined())
