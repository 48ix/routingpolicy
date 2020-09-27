"""Query & parse data from IRRd server."""

# Standard Library
import asyncio
from typing import Tuple, Awaitable, AsyncGenerator
from datetime import datetime
from ipaddress import ip_network

# Project
from routingpolicy.log import log
from routingpolicy.rendering import Environment
from routingpolicy.models.participant import Participant

QUERY_ASN_IP4 = "\n!gas{}\n"
QUERY_ASN_IP6 = "\n!6as{}\n"
QUERY_AS_SET = "\n!i{}\n"


async def run_whois(asn: str, family: int) -> AsyncGenerator[str, None]:
    """Open raw socket to IRRd host and execute query."""

    # Construct bulk query
    query = QUERY_ASN_IP4.format(asn)
    if family == 6:
        query = QUERY_ASN_IP6.format(asn)

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
    for item in items:
        yield item


async def render_prefixes(
    participant: Participant, max_ipv4: int, max_ipv6: int, template_env: Environment
) -> AsyncGenerator[Tuple[int, Awaitable], None]:
    """Render prefix-list templates."""
    asn = str(participant.asn)
    for family in (4, 6):
        prefixes = (ip_network(n) async for n in run_whois(asn, family))
        max_len = {4: max_ipv4, 6: max_ipv6}[family]
        prefix_list = template_env.get_template(f"participant-prefix-list{family}.j2")
        yield family, prefix_list.render_async(
            p=participant,
            prefixes=prefixes,
            max_len=max_len,
            now=datetime.utcnow().isoformat(),
        )
