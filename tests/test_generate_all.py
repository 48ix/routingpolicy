"""Test Generation of All Configuration Templates."""

# Standard Library
import asyncio

# Project
from routingpolicy.generate import generate_all

if __name__ == "__main__":
    asyncio.run(generate_all())
