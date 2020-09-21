"""Interact with Slack API."""

# Standard Library
from typing import Dict

# Third Party
from httpx import AsyncClient

# Project
from routingpolicy.log import log
from routingpolicy.config import params
from routingpolicy.models.route_server import RouteServer


def generate_policy_block(route_server: RouteServer, message: str) -> Dict:
    """Generate a Slack message block."""
    return {
        "text": route_server.name,
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Route Policy Updates"},
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{route_server.name}*",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{message}```",
                },
            },
        ],
    }


async def send_webhook(route_server: RouteServer, message: str) -> None:
    """Send a Slack webhook."""

    generated = generate_policy_block(route_server, message)

    log.debug("Generated Slack hook:\n{}", generated)
    try:
        async with AsyncClient(base_url="https://hooks.slack.com") as client:
            await client.post(
                str(params.slack.webhook.path),
                json=generated,
            )
    except Exception as err:
        log.error(str(err))
