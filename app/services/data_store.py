from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.models import LaunchAssessment, RiskFinding, Task

BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_PATH = BASE_DIR / "data" / "launches.json"


def ensure_store() -> Path:
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not STORAGE_PATH.exists():
        STORAGE_PATH.write_text("[]", encoding="utf-8")
    return STORAGE_PATH


def load_launches() -> list[dict[str, Any]]:
    try:
        text = ensure_store().read_text(encoding="utf-8")
        if not text.strip():
            return []
        payload = json.loads(text)
        return payload if isinstance(payload, list) else []
    except json.JSONDecodeError:
        return []


def save_launches(launches: list[dict[str, Any]]) -> None:
    ensure_store().write_text(json.dumps(launches, indent=2), encoding="utf-8")


def _normalize_task(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(task.get("id") or task.get("name", "task").lower().replace(" ", "-") + "-1"),
        "name": task.get("name", "Untitled milestone"),
        "owner": task.get("owner", "Unassigned"),
        "status": task.get("status", "todo"),
        "priority": task.get("priority", "medium"),
        "due_date": task.get("due_date"),
        "dependency_ids": task.get("dependency_ids", []),
    }


def _normalize_launch(raw: dict[str, Any]) -> dict[str, Any]:
    milestones = [_normalize_task(task) for task in raw.get("milestones", [])]
    return {
        "id": raw.get("id") or raw.get("product_name", "launch").lower().replace(" ", "-") + "-1",
        "product_name": raw.get("product_name", "Untitled launch"),
        "launch_date": raw.get("launch_date"),
        "market": raw.get("market", "General market"),
        "team": raw.get("team", "Product team"),
        "status": raw.get("status", "planned"),
        "milestones": milestones,
    }


def assess_launch(launch: dict[str, Any]) -> LaunchAssessment:
    normalized = _normalize_launch(launch)
    tasks = [Task(**task) for task in normalized["milestones"]]

    if not tasks:
        return LaunchAssessment(
            launch_id=normalized["id"],
            readiness_score=50,
            risk_level="monitor",
            launch_window=normalized.get("launch_date") or "TBD",
            summary="The launch plan needs a defined milestone checklist before confidence can be trusted.",
            findings=[
                RiskFinding(
                    risk_type="launch plan",
                    severity="medium",
                    score=40,
                    message="No milestone data is available yet.",
                    recommendation="Define the launch plan with objectives, owners, and dependencies.",
                    evidence=["No tasks were provided for the launch."],
                )
            ],
        )

    total = len(tasks)
    done = sum(1 for task in tasks if task.status == "done")
    blocked = sum(1 for task in tasks if task.status == "blocked")
    critical_remaining = sum(1 for task in tasks if task.priority == "critical" and task.status != "done")
    completion_ratio = (done / total) * 100 if total else 0

    blocked_penalty = blocked * 12
    critical_penalty = critical_remaining * 14
    deadline_penalty = 0

    if normalized.get("launch_date"):
        try:
            target = datetime.fromisoformat(normalized["launch_date"])
            days_to_launch = (target - datetime.now()).days
            if days_to_launch < 14:
                deadline_penalty = 20
            elif days_to_launch < 30:
                deadline_penalty = 10
        except ValueError:
            deadline_penalty = 0

    readiness = max(
        0,
        min(100, round(completion_ratio - blocked_penalty - critical_penalty - deadline_penalty)),
    )

    if readiness >= 80:
        risk_level = "healthy"
    elif readiness >= 65:
        risk_level = "monitor"
    elif readiness >= 45:
        risk_level = "watch"
    else:
        risk_level = "critical"

    findings: list[RiskFinding] = []
    if blocked:
        findings.append(
            RiskFinding(
                risk_type="blocked work",
                severity="high" if blocked > 1 else "medium",
                score=min(90, blocked * 18),
                message=f"{blocked} milestone(s) are blocked and may delay launch execution.",
                recommendation="Assign owners, remove blockers, and escalate critical dependency issues immediately.",
                evidence=[f"Blocked milestones: {blocked}"],
            )
        )

    if critical_remaining:
        findings.append(
            RiskFinding(
                risk_type="critical path",
                severity="critical" if critical_remaining > 1 else "high",
                score=min(95, critical_remaining * 18),
                message=f"{critical_remaining} critical milestone(s) remain incomplete.",
                recommendation="Prioritize the launch-critical path and reduce scope where needed.",
                evidence=[f"Critical tasks remaining: {critical_remaining}"],
            )
        )

    if readiness < 60:
        findings.append(
            RiskFinding(
                risk_type="launch confidence",
                severity="critical",
                score=75,
                message="Launch confidence is too low for a smooth rollout.",
                recommendation="Re-baseline the launch plan, remove non-essential scope, and assign executive ownership.",
                evidence=[f"Readiness score: {readiness}"],
            )
        )

    if not findings:
        findings.append(
            RiskFinding(
                risk_type="launch health",
                severity="low",
                score=15,
                message="The launch appears stable with no major blockers currently visible.",
                recommendation="Maintain momentum and keep launch owners aligned on the checklist.",
                evidence=[f"Completion ratio: {round(completion_ratio)}%"],
            )
        )

    summary = (
        "The launch is strong and progressing with low risk."
        if readiness >= 80
        else "The launch is manageable, but it should be monitored closely."
        if readiness >= 60
        else "The launch is at significant risk and needs immediate intervention."
    )

    return LaunchAssessment(
        launch_id=normalized["id"],
        readiness_score=readiness,
        risk_level=risk_level,
        launch_window=normalized.get("launch_date") or "TBD",
        summary=summary,
        findings=findings,
    )
