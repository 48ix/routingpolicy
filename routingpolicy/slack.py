"""Interact with Slack API."""

# Standard Library
from typing import Dict

# Third Party
from httpx import AsyncClient

# Project
from routingpolicy.log import log
from routingpolicy.config import params


def generate_policy_block(title: str, summary: str, message: str) -> Dict:
    """Generate a Slack message block."""
    return {
        "text": summary,
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": summary},
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{title}*",
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


async def send_webhook(title: str, summary: str, message: str) -> None:
    """Send a Slack webhook."""

    generated = generate_policy_block(title, summary, message)

    log.debug("Generated Slack hook:\n{}", generated)
    try:
        async with AsyncClient(base_url="https://hooks.slack.com") as client:
            await client.post(
                str(params.slack.webhook.path),
                json=generated,
            )
    except Exception as err:
        log.error(str(err))
