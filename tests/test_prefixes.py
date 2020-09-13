"""Test Prefix List Generation."""

import asyncio
from routingpolicy.config import params
from routingpolicy.generate import prefixes

if __name__ == "__main__":
    asyncio.run(prefixes(params.participants[0]))
