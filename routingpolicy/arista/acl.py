"""Build and/or Parse Arista ACLs."""

# Standard Library
from typing import Dict, List

# Project
from routingpolicy.models.participant import Participant

DEFAULT4 = [
    "10 deny ospf any any",
    "20 deny 88 any any",
    "30 deny udp any eq rip any",
    "40 deny udp any any eq rip",
    "50 deny icmp any any redirect",
    "60 deny udp any eq bootps any",
    "70 deny udp any eq bootpc any",
    "80 deny udp any any eq bootps",
    "90 deny udp any any eq bootpc",
    "100 deny pim any any",
    "991 deny tcp any eq bgp any",
    "999 permit ip any any",
]

DEFAULT6 = [
    "10 deny ospf any any",
    "20 deny 88 any any",
    "30 deny udp any any eq 521",
    "40 deny udp any eq 521 any",
    "50 deny icmpv6 any any 130",
    "60 deny icmpv6 any any 131",
    "70 deny icmpv6 any any 132",
    "80 deny icmpv6 any any redirect-message",
    "90 deny pim any any",
    "991 deny tcp any eq bgp any",
    "999 permit ipv6 any any",
]


async def generate_acl4(participant: Participant) -> List[str]:
    """Generate a Participant-Specific IPv4 ACL."""
    peer_acl = sorted(DEFAULT4.copy())
    init_lines = (
        f"no ip access-list ipv4-{participant.asn}-in",
        f"ip access-list ipv4-{participant.asn}-in",
    )
    for i, l in enumerate(init_lines):
        peer_acl.insert(i, l)

    for ip in participant.ipv4:
        peer_acl.insert(-2, f"900 permit tcp host {str(ip)} eq bgp any")

    return peer_acl


async def generate_acl6(participant: Participant) -> List[str]:
    """Generate a Participant-Specific IPv6 ACL."""
    peer_acl = sorted(DEFAULT6.copy())
    init_lines = (
        f"no ipv6 access-list ipv6-{participant.asn}-in",
        f"ipv6 access-list ipv6-{participant.asn}-in",
    )
    for i, l in enumerate(init_lines):
        peer_acl.insert(i, l)

    for ip in participant.ipv6:
        peer_acl.insert(-2, f"900 permit tcp host {str(ip)} eq bgp any")

    return peer_acl


async def parse_acls(prefix: str, commands: Dict) -> List[List[str]]:
    """Parse through each command to find access-list statements."""
    acls = []
    for k, v in {
        k: v for k, v in commands.items() if f"{prefix} access-list" in k
    }.items():

        # Sort the entries under each ACL.
        lines = sorted(v.get("cmds", {}).keys())

        # Add the "no" statement at the beginning of the ACL for easy
        # comparison to the newly generated ACLs.
        lines.insert(0, "no " + k)

        # Flatten the list of commands into a single list of commands,
        # which matches how the commands are both generated and
        # consumed by the EOS API.
        lines.insert(1, k)
        acls.append(lines)

    return acls
