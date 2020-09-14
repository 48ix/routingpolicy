"""Test All Policy Generation."""
import asyncio

from routingpolicy.main import policy

if __name__ == "__main__":
    asyncio.run(policy())
