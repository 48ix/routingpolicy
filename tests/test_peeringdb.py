"""Test PeeringDB API Data Collection."""
# Standard Library
import asyncio

# Project
from routingpolicy.peeringdb import max_prefixes

if __name__ == "__main__":
    test_asn = 2914
    max4, max6 = asyncio.run(max_prefixes(asn=test_asn))
    print(f"Max IPv4 Prefixes for AS{test_asn}: {max4}")
    print(f"Max IPv6 Prefixes for AS{test_asn}: {max6}")
