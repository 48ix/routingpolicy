"""Generate 48 IX Route Server Configs."""

# Standard Library
import asyncio
from pathlib import Path

# Project
from routingpolicy.irr import render_prefixes
from routingpolicy.log import log
from routingpolicy.config import params
from routingpolicy.peeringdb import max_prefixes
from routingpolicy.rendering import POLICIES_DIR, template_env
from routingpolicy.models.participant import Participant


def verify_complete(file: Path) -> bool:
    """Verify a template exists and isn't empty."""
    complete = False
    if file.exists() and file.stat().st_size != 0:
        complete = True
    return complete


def create_file_structure() -> bool:
    """Gracefully create output policy file structure."""
    for rs in params.route_servers:
        rs_dir = POLICIES_DIR / rs.name
        if not rs_dir.exists():
            log.debug("Creating {}", str(rs_dir))
            rs_dir.mkdir()
        for participant in params.participants:
            participant_dir = rs_dir / str(participant.asn)
            if not participant_dir.exists():
                log.debug("Creating {}", str(participant_dir))
                participant_dir.mkdir()
    return True


async def communities(
    participant: Participant,
) -> None:
    """Generate Participant-specific BGP Community Lists."""
    log.info("Generating Communities for {}", participant.pretty)
    create_file_structure()

    participant_comms = template_env.get_template("participant-communities.j2")

    for rs in params.route_servers:
        result = await participant_comms.render_async(p=participant)
        output_file = POLICIES_DIR / rs.name / str(participant.asn) / "communities.ios"

        log.debug("Communities for {}: {}\n{}", participant.pretty, result)

        with output_file.open("w+") as of:
            of.write(result)

        if verify_complete(output_file):
            log.success(
                "Generated Communities for AS{}: {} at {}",
                participant.asn,
                participant.name,
                str(output_file),
            )


async def route_map(participant: Participant) -> None:
    """Generate Participant-specific Route Maps."""
    log.info("Generating Route Maps for {}", participant.pretty)
    create_file_structure()
    participant_route_map = template_env.get_template("participant-route-map.j2")
    for rs in params.route_servers:

        result = await participant_route_map.render_async(
            p=participant, rs=rs.id, loc=rs.loc_id, metro=rs.metro_id
        )
        output_file = POLICIES_DIR / rs.name / str(participant.asn) / "route-map.ios"

        log.debug("Route Maps for {}\n{}", participant.pretty, result)

        with output_file.open("w+") as of:
            of.write(result)

        if verify_complete(output_file):
            log.success(
                "Generated Route Maps for AS{}: {} at {}",
                participant.asn,
                participant.name,
                str(output_file),
            )


async def prefixes(participant: Participant) -> None:
    """Generate Participant-specific Prefix Lists."""
    log.info("Generating Prefix Lists for {}", participant.pretty)
    create_file_structure()
    for rs in params.route_servers:
        async for family, render in render_prefixes(
            participant,
            max_ipv4=params.max_length.ipv4,
            max_ipv6=params.max_length.ipv6,
            template_env=template_env,
        ):
            output_file = (
                POLICIES_DIR
                / rs.name
                / str(participant.asn)
                / f"prefix-list-ipv{family}.ios"
            )
            rendered = await render

            log.debug(
                "IPv{} Prefix List for {}\n{}",
                family,
                participant.pretty,
                rendered,
            )

            with output_file.open("w") as of:
                of.write(rendered)

            if verify_complete(output_file):
                log.success(
                    "Generated IPv{} Prefix Lists for {} at {}",
                    family,
                    participant.pretty,
                    str(output_file),
                )


async def bgp(participant: Participant) -> None:
    """Generate Participant-specific BGP Configs."""
    log.info("Generating BGP Config for {}", participant.pretty)
    create_file_structure()
    max4, max6 = await max_prefixes(participant.asn)
    for rs in params.route_servers:
        output_file = POLICIES_DIR / rs.name / str(participant.asn) / "bgp.ios"
        template = template_env.get_template("participant-bgp.j2")
        result = await template.render_async(p=participant, max4=max4, max6=max6)

        log.debug("BGP Config for {}\n{}", participant.pretty, result)

        with output_file.open("w+") as of:
            of.write(result)

        if verify_complete(output_file):
            log.success(
                "Generated BGP Config for AS{}: {} at {}",
                participant.asn,
                participant.name,
                str(output_file),
            )


async def generate_all() -> None:
    """Generate all templates for all route route servers and participants."""
    coros = (communities, route_map, prefixes, bgp)
    tasks = (c(p) for c in coros for p in params.participants)
    await asyncio.gather(*tasks)
