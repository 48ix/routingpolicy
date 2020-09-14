"""Combine generated configuration files.

Generates a combined config file per route server containing global
configurations and all participant configurations.
"""

# Standard Library
from typing import Generator

from routingpolicy.log import log
from routingpolicy.config import params
from routingpolicy.rendering import template_env, POLICIES_DIR, GLOBALS_DIR

FILE_NAMES = (
    "communities.ios",
    "prefix-list-ipv4.ios",
    "prefix-list-ipv6.ios",
    "route-map.ios",
)


def global_policies() -> Generator[str, None, None]:
    """Read global config files."""
    global_file_names = (
        "aspaths.ios",
        "communities.ios",
        "prefix-list-ipv4.ios",
        "prefix-list-ipv6.ios",
    )
    for file_name in global_file_names:
        file_path = GLOBALS_DIR / file_name
        with file_path.open("r") as f:
            yield f.read()


async def generate_combined() -> None:
    """Combine generated per-participant configs into a single file per route server."""
    combined_template = template_env.get_template("combined.j2")
    g_aspaths, g_communities, g_prefixes4, g_prefixes6 = global_policies()

    for rs in params.route_servers:
        log.info("Generating combined config file for {}", rs.name)
        items = ["" for _ in FILE_NAMES]
        rs_path = POLICIES_DIR / rs.name
        output_file = rs_path / "_all.ios"
        for participant in params.participants:
            participant_path = rs_path / str(participant.asn)
            for i, file_name in enumerate(FILE_NAMES):
                file = participant_path / file_name
                with file.open("r") as f:
                    items[i] += "\n" + f.read()
        communities, prefixes4, prefixes6, route_maps = items
        output = await combined_template.render_async(
            rs=rs,
            communities="\n".join((g_communities, communities)),
            aspaths=g_aspaths,
            prefixes4="\n".join((g_prefixes4, prefixes4)),
            prefixes6="\n".join((g_prefixes6, prefixes6)),
        )
        with output_file.open("w") as of:
            of.write(output)
