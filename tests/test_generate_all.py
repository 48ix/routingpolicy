"""Test Generation of All Configuration Templates."""

import asyncio
from routingpolicy.generate import generate_all

if __name__ == "__main__":
    asyncio.run(generate_all())
