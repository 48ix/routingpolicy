"""Push & Pull Actions."""

# Standard Library
from typing import Dict
from datetime import datetime

# Third Party
from httpx import AsyncClient

# Project
from routingpolicy.log import log
from routingpolicy.models.switch import Switch


async def get_current_config(switch: Switch) -> Dict:
    """Get the running configuration of an Arista switch via EOS API."""
    async with AsyncClient(
        auth=((switch.username, switch.password.get_secret_value())),
        verify=False,
    ) as client:
        pull_id = f"Get Current Config {datetime.utcnow().isoformat()}"
        res = await client.post(
            f"https://{str(switch.address)}/command-api",
            json={
                "id": pull_id,
                "jsonrpc": "2.0",
                "method": "runCmds",
                "params": {
                    "format": "json",
                    "timestamps": False,
                    "autoComplete": False,
                    "expandAliases": False,
                    "cmds": ["show running-config"],
                    "version": 1,
                },
            },
        )
        data = res.json()

        try:
            commands: Dict = data["result"][0]["cmds"]
            return commands
        except (KeyError, IndexError):
            log.error(data)
            raise RuntimeError(f"Response from {switch.address} was unexpected.")
