"""Current vs. Target Comparions."""

# Standard Library
from typing import List, AsyncGenerator

# Project
from routingpolicy.log import log
from routingpolicy.arista.acl import parse_acls, generate_acl4, generate_acl6
from routingpolicy.models.switch import Switch
from routingpolicy.arista.actions import get_current_config
from routingpolicy.models.participant import Participant


async def requires_update(  # noqa: C901 your mom's too complex
    switches: List[Switch], participants: List[Participant]
) -> AsyncGenerator[Participant, None]:
    """Determine if an ACL needs to be updated.

    Pull each switch's current running config and extract ACL sections.

    Generate new ACLs based on current policy standard.

    Compare the current configuration state vs. what would be deployed
    and if there are any differences, mark that participant's ACLs for
    the re-deployment.
    """
    requires_update = set()
    for switch in switches:
        # Get current running-configuration.
        current_config = await get_current_config(switch)

        # Parse IPv4 access-lists
        current_acl4 = await parse_acls("ip", current_config)

        # Parse IPv6 access-lists
        current_acl6 = await parse_acls("ipv6", current_config)

        for participant in participants:
            # Generate new IPv4 access-lists based on current policy.
            new_acl4 = await generate_acl4(participant)

            # Generate new IPv6 access-lists based on current policy.
            new_acl6 = await generate_acl6(participant)

            for afi in ((current_acl4, new_acl4), (current_acl6, new_acl6)):
                current_acls, new = afi
                matched = None

                for i, acl in enumerate(current_acls):
                    # Match the current ACL to the new based on the
                    # first line, which contains the participant's ASN.
                    if acl[0] == new[0]:
                        matched = i
                        break

                if matched is None:
                    # If there was no match, this means the ACL doesn't
                    # exist on the switch and should be deployed.
                    log.info(
                        "No ACL for {} exists on {}",
                        participant.pretty,
                        str(switch.address),
                    )
                    requires_update.add(participant)

                else:
                    # Otherwise, confirm the ACL from the switch matches
                    # the ACL generated from policy.
                    for i, new_acl in enumerate(new):

                        # Compare each line for differences.
                        if new_acl != current_acls[matched][i]:
                            log.warning(
                                "New ACL entry '{}' does not match current '{}' for {}",
                                new_acl,
                                acl[i],
                                participant.pretty,
                            )

                            # If there is a difference, mark the
                            # participant for re-generation on first
                            # match.
                            requires_update.add(participant)
                            break

    if len(requires_update) == 0:
        log.info("No particiapant ACLs require updates.")

    for participant in requires_update:
        yield participant
