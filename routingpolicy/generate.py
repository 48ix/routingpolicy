"""Generate 48 IX Route Server Configs."""

# Standard Library
from pathlib import Path

# Third Party
from jinja2 import Environment, PackageLoader

# Project
from routingpolicy.irr import render_prefixes
from routingpolicy.log import log
from routingpolicy.config import params
from routingpolicy.config.models.participant import Participant

template_env = Environment(
    loader=PackageLoader("routingpolicy", "templates"),
    enable_async=True,
    trim_blocks=True,
)
TARGET_DIR = Path(__file__).parent.parent / "policies"


def verify_complete(file: Path) -> bool:
    """Verify a template exists and isn't empty."""
    complete = False
    if file.exists() and file.stat().st_size != 0:
        complete = True
    return complete


async def communities(
    participant: Participant,
) -> None:
    """Generate Participant-specific BGP Community Lists."""
    log.info("Generating Communities for AS{}: {}", participant.asn, participant.name)

    participant_comms = template_env.get_template("participant-communities.j2")
    result = await participant_comms.render_async(p=participant)
    output_file = TARGET_DIR / f"communities-{participant.asn}"

    log.debug(result)

    with output_file.open("w+") as of:
        of.write(result)
    if verify_complete(output_file):
        log.success(
            "Generated Communities for AS{}: {} at {}",
            participant.asn,
            participant.name,
            str(output_file),
        )


async def route_map(
    participant: Participant,
    rs_id: int,
    loc_id: int,
    metro_id: int,
) -> None:
    """Generate Participant-specific Route Maps."""
    log.info("Generating Route Maps for AS{}: {}", participant.asn, participant.name)

    participant_route_map = template_env.get_template("participant-route-map.j2")
    result = await participant_route_map.render_async(
        p=participant, rs=rs_id, loc=loc_id, metro=metro_id
    )
    output_file = TARGET_DIR / f"route-map-{participant.asn}"

    log.debug(result)

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
    log.info("Generating Prefix Lists for AS{}: {}", participant.asn, participant.name)

    async for family, rendered in render_prefixes(
        participant,
        max_ipv4=params.max_length.ipv4,
        max_ipv6=params.max_length.ipv6,
        template_env=template_env,
    ):
        output_file = TARGET_DIR / f"prefix-list{family}-{participant.asn}"
        log.debug(rendered)
        with output_file.open("w") as of:
            of.write(await rendered)
        if verify_complete(output_file):
            log.success(
                "Generated Prefix Lists for AS{}: {} at {}",
                participant.asn,
                participant.name,
                str(output_file),
            )