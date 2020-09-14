"""Get Participant Information via the PeeringDB API."""

# Standard Library
from typing import Tuple

# Third Party
from httpx import AsyncClient

# Project
from routingpolicy.log import log


async def max_prefixes(asn: int) -> Tuple[int, int]:
    """Search PeeringDB for an entry matching an ASN and return its max prefixes."""
    prefixes = (0, 0)
    async with AsyncClient(
        http2=True,
        verify=True,
        base_url="https://peeringdb.com",
        headers={"Accept": "application/json"},
    ) as client:
        log.debug("Getting max prefixes for AS{}", str(asn))
        res = await client.get("/api/net", params={"asn__contains": asn})
        res.raise_for_status()
        for data in res.json()["data"]:
            if "asn" in data and data["asn"] == asn:
                log.debug("Matched AS{} to {}", str(asn), data["name"])
                log.debug(
                    "AS{} PeeringDB Org ID {}, last updated {}",
                    str(asn),
                    str(data["org_id"]),
                    data["updated"],
                )
                prefixes = (
                    data.get("info_prefixes4", 0),
                    data.get("info_prefixes6", 0),
                )
    return prefixes
