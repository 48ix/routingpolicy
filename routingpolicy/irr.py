"""Query & parse data from IRRd server."""

# Standard Library
import re
import asyncio
from typing import Tuple, Awaitable, AsyncGenerator
from datetime import datetime
from ipaddress import ip_network

# Project
from routingpolicy.log import log
from routingpolicy.peeringdb import get_as_set
from routingpolicy.rendering import Environment
from routingpolicy.models.participant import Participant

QUERY_ASN_IP4 = "\n!gas{}\n"
QUERY_ASN_IP6 = "\n!6as{}\n"
QUERY_AS_SET = "\n!i{},1\n"

TIER1 = (
    "174",
    "174",
    "701",
    "1299",
    "7018",
    "6939",
    "2914",
    "3356",
    "3257",
    "6453",
    "6762",
    "6461",
    "1273",
    "3320",
    "5511",
    "1239",
    "7922",
    "12956",
)


async def run_whois(query: str) -> AsyncGenerator[str, None]:
    """Open raw socket to IRRd host and execute query."""

    # Open the socket to IRRd
    log.debug("Opening connection to IRRd server")
    reader, writer = await asyncio.open_connection("rr.ntt.net", port=43)

    # Send the query
    writer.write(query.encode())
    await writer.drain()
    # Read the response
    response = b""
    while True:
        data = await reader.read(128)
        if data:
            response += data
        else:
            log.debug("Closing connection to IRRd server")
            writer.close()
            break

    if writer.can_write_eof():
        writer.write_eof()
    items = ",".join(response.decode().split()[1:-1]).split(",")
    for item in (i for i in items if i):
        yield item


async def query_as_set(as_set: str, family: int) -> AsyncGenerator[str, None]:
    """Run a whois query for an AS-Set & each member."""

    query = QUERY_AS_SET.format(as_set)
    async for member in run_whois(query):
        # Get the ASN without the AS prefix.
        member_query = member.replace("AS", "")
        if family == 4:
            sub_query = QUERY_ASN_IP4.format(member_query)
        else:
            sub_query = QUERY_ASN_IP6.format(member_query)
        # Query the AS-Set's member ASN directly.
        async for net in run_whois(sub_query):
            yield net


async def get_prefixes(asn: str, family: int) -> AsyncGenerator[str, None]:
    """Get the prefixes for an ASN."""
    # Check PeeringDB for an AS-Set.
    as_sets = await get_as_set(asn)

    if len(as_sets) > 0:
        for as_set in as_sets:
            # Strip out the registry prefix, e.g. ARIN::AS-EXAMPLE
            if re.match("^.+::.+$", as_set):
                as_set = as_set.split("::")[1]
            results = query_as_set(as_set, family)
            async for result in results:
                yield result
    else:
        # If there is no AS-Set, query the ASN directly.
        query = QUERY_ASN_IP4.format(asn)
        if family == 6:
            query = QUERY_ASN_IP6.format(asn)

        results = run_whois(query)

        async for result in results:
            yield result


async def render_prefixes(
    participant: Participant, max_ipv4: int, max_ipv6: int, template_env: Environment
) -> AsyncGenerator[Tuple[int, Awaitable], None]:
    """Render prefix-list templates."""

    asn = str(participant.asn)

    for family in (4, 6):
        max_len = {4: max_ipv4, 6: max_ipv6}[family]
        """
        Because tier 1 carriers are likely to export extremely large
        amounts of prefixes, we don't want to build a prefix-list based
        on their AS-Set. Instead, Route Origin Validation (RPKI) and
        bogon/martian filtering is preferable. The tier1-prefix-list
        templates will deploy a single statement prefix-list allowing
        any prefixes.
        """
        if asn in TIER1:
            prefix_list = template_env.get_template(f"tier1-prefix-list{family}.j2")
            yield family, prefix_list.render_async(
                p=participant,
                max_len=max_len,
                now=datetime.utcnow().isoformat(),
            )
        else:
            prefixes = (ip_network(n) async for n in get_prefixes(asn, family))
            prefix_list = template_env.get_template(
                f"participant-prefix-list{family}.j2"
            )
            yield family, prefix_list.render_async(
                p=participant,
                max_len=max_len,
                prefixes=prefixes,
                now=datetime.utcnow().isoformat(),
            )
