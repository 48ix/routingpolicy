"""Send commands to Arista switches."""

# Standard Library
import json
from typing import List, Tuple
from datetime import datetime

# Third Party
from httpx import AsyncClient

# Project
from routingpolicy.log import log
from routingpolicy.arista.acl import generate_acl4, generate_acl6
from routingpolicy.models.switch import Switch
from routingpolicy.arista.compare import requires_update
from routingpolicy.models.participant import Participant


async def send_acls(  # noqa: C901 your mom's too complex
    switches: List[Switch], participants: List[Participant]
) -> str:
    """Send ACLs to IX switches, only if updates are required."""
    messages: Tuple[str, ...] = ()
    # Determine if an ACL push is required.
    async for participant in requires_update(switches, participants):

        for switch in switches:

            async with AsyncClient(
                auth=((switch.username, switch.password.get_secret_value())),
                verify=False,
            ) as client:
                p_messages: Tuple[str, ...] = ()
                p_errors: Tuple[str, ...] = ()
                acl4 = await generate_acl4(participant)
                acl6 = await generate_acl6(participant)
                push_id = (
                    f"{participant.pretty} ACL Push {datetime.utcnow().isoformat()}"
                )
                data = {
                    "id": push_id,
                    "jsonrpc": "2.0",
                    "method": "runCmds",
                    "params": {
                        "version": 1,
                        "format": "json",
                        "timestamps": False,
                        "autoComplete": False,
                        "expandAliases": False,
                        "cmds": [
                            "configure",
                            *acl4,
                            *acl6,
                        ],
                    },
                }
                log.info("Sending {} ACLs to {}", participant.pretty, switch.name)
                log.debug(json.dumps(data, indent=2))

                res = await client.post(
                    f"https://{str(switch.address)}/command-api", json=data
                )
                res_json = res.json()

                # Handle errors returned from the switch.
                if "error" in res_json:
                    res_error: Tuple[str, ...] = ()
                    error_data = [
                        d for d in res_json["error"].get("data", []) if "errors" in d
                    ]

                    for d in error_data:
                        for e in d.get("errors", []):
                            res_error += (e,)

                    if "message" in res_json["error"]:
                        res_error += (res_json["error"]["message"],)

                    p_errors += (", ".join(res_error),)

                # Handle non-error messages returned from the switch.
                elif "result" in res_json:
                    for d in [d for d in res_json["result"] if d]:
                        p_messages += (d,)

                if len(p_errors) == 0:
                    messages += (
                        "{} ACLs updated on {}".format(
                            participant.pretty, str(switch.address)
                        ),
                    )

                for err in p_errors:
                    msg = "Error while sending {} ACLs to {}:\n{}".format(
                        participant.pretty, str(switch.address), err
                    )
                    log.error(msg)
                    messages += (msg,)

                for m in p_messages:
                    msg = "Response while sending {} ACLs to {}:\n{}".format(
                        participant.pretty,
                        str(switch.address),
                        m,
                    )
                    log.info(msg)
                    messages += (msg,)

    if len(messages) == 0:
        message = "No particiapant ACLs require updates."
    else:
        message = ", ".join(messages)

    return message
