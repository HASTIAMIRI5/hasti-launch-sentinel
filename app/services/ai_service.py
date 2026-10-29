import os
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from app.config import get_settings


def _heuristic_ai_summary(launch: dict[str, Any]) -> dict[str, Any]:
    tasks = launch.get("milestones", [])
    if not tasks:
        return {
            "provider": "heuristic",
            "summary": "No milestone data available; the launch plan should be defined before launch confidence can be assessed.",
            "recommendations": [
                "Create a launch milestone plan with owners and dependencies.",
                "Identify all launch-critical blockers and track them daily.",
            ],
            "risk_score": 72,
        }

    blocked = sum(1 for task in tasks if task.get("status") == "blocked")
    critical_remaining = sum(
        1 for task in tasks if task.get("priority") == "critical" and task.get("status") != "done"
    )
    completion = sum(1 for task in tasks if task.get("status") == "done") / max(len(tasks), 1)
    risk_score = min(100, max(0, round((1 - completion) * 100 + blocked * 12 + critical_remaining * 10)))

    summary = (
        "Launch health is stable but should be actively monitored."
        if risk_score < 45
        else "Launch health is at medium risk and needs executive attention."
        if risk_score < 70
        else "Launch health is high risk and requires immediate intervention."
    )

    recommendations = [
        "Prioritize all blocked critical milestones.",
        "Confirm launch ownership across product, engineering, and go-to-market teams.",
    ]
    if blocked:
        recommendations.append("Remove blockers for all blocked milestones before the launch review.")

    return {
        "provider": "heuristic",
        "summary": summary,
        "recommendations": recommendations,
        "risk_score": risk_score,
    }


async def analyze_launch_with_ai(launch: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()

    if settings.openai_api_key:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are Hasti Launch Sentinel, an AI launch intelligence assistant. Return valid JSON with keys: summary, recommendations, risk_score, provider.",
                            },
                            {
                                "role": "user",
                                "content": f"Analyze this launch plan and return a short executive summary, 3 actionable recommendations, and risk score 0-100. Launch data: {launch}",
                            },
                        ],
                        "temperature": 0.2,
                    },
                )
                response.raise_for_status()
                payload = response.json()
                content = payload["choices"][0]["message"]["content"]
                try:
                    parsed = __import__("json").loads(content)
                    parsed["provider"] = "openai"
                    return parsed
                except Exception:
                    return {"provider": "openai", "summary": content, "recommendations": ["Review the launch plan with owners."], "risk_score": 60}
        except Exception:
            pass

    if settings.anthropic_api_key:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": settings.anthropic_api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 300,
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Analyze this launch plan and return valid JSON with keys summary, recommendations, risk_score, provider. Launch: {launch}",
                            }
                        ],
                    },
                )
                response.raise_for_status()
                payload = response.json()
                text = payload["content"][0]["text"]
                try:
                    parsed = __import__("json").loads(text)
                    parsed["provider"] = "anthropic"
                    return parsed
                except Exception:
                    return {"provider": "anthropic", "summary": text, "recommendations": ["Review with the launch team."], "risk_score": 60}
        except Exception:
            pass

    return _heuristic_ai_summary(launch)
