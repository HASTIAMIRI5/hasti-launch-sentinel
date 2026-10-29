import os
from typing import Any

import httpx


async def send_email_alert(subject: str, body: str) -> None:
    smtp_host = os.getenv("SMTP_HOST")
    if not smtp_host:
        return
    # Production mail transport can be wired here later.
    # For now this is a safe no-op when SMTP is not configured.
    return


async def send_slack_alert(message: str) -> None:
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        return
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(webhook, json={"text": message})
    except Exception:
        pass


async def send_risk_alert(launch: dict[str, Any], assessment: dict[str, Any]) -> None:
    risk_level = assessment.get("risk_level")
    if risk_level not in {"watch", "critical"}:
        return

    message = (
        f"Launch risk alert: {launch.get('product_name')} is at {risk_level} risk. "
        f"Readiness score: {assessment.get('readiness_score')}"
    )
    await send_email_alert("Launch risk alert", message)
    await send_slack_alert(message)
