"""Get Participant Information via the PeeringDB API."""

# Standard Library
from typing import Tuple, Sequence

# Third Party
from httpx import AsyncClient

# Project
from routingpolicy.log import log


async def max_prefixes(asn: int) -> Tuple[int, int]:
    """Search PeeringDB for an entry matching an ASN and return its max prefixes."""
    prefixes = (200, 20)
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
                    data.get("info_prefixes4", 200),
                    data.get("info_prefixes6", 20),
                )
    return prefixes


async def get_as_set(asn: str) -> Sequence[str]:
    """Search PeeringDB for an entry matching an ASN and return its IRR AS_Set."""
    result = []
    async with AsyncClient(
        http2=True,
        verify=True,
        base_url="https://peeringdb.com",
        headers={"Accept": "application/json"},
    ) as client:
        log.debug("Getting max prefixes for AS{}", asn)
        res = await client.get("/api/net", params={"asn__contains": asn})
        res.raise_for_status()
        for data in res.json()["data"]:
            if "asn" in data and str(data["asn"]) == asn:
                log.debug("Matched AS{} to {}", str(asn), data["name"])
                log.debug(
                    "AS{} PeeringDB Org ID {}, last updated {}",
                    str(asn),
                    str(data["org_id"]),
                    data["updated"],
                )
                as_set = data.get("irr_as_set", "")
                if as_set != "":
                    result = as_set.split(" ")
                    log.debug("Found AS-Set(s) {} for {}", result, data["name"])
                break
    return result
