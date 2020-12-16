"""Test Gathering of Prefixes from IRR Data."""

# Standard Library
import sys
import asyncio

# Project
from routingpolicy.irr import get_prefixes
from routingpolicy.log import log


async def _run_test(asn: str) -> None:
    for family in (4, 6):
        prefixes = get_prefixes(asn, family)
        log.info("IPv{} prefixes for {}:", str(family), f"AS{asn}")
        async for prefix in prefixes:
            log.info(prefix)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        asn = sys.argv[1].replace("AS", "")
    else:
        asn = "14525"
    task = _run_test(asn)
    try:
        asyncio.run(task)
    except KeyboardInterrupt:
        task.close()
        log.critical("Stopped")
