from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.models import Launch, LaunchAssessment, Task


def _normalize_task(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": task.get("id") or str(uuid4())[:8],
        "name": task.get("name", "Untitled milestone"),
        "owner": task.get("owner", "Unassigned"),
        "status": task.get("status", "todo"),
        "priority": task.get("priority", "medium"),
        "due_date": task.get("due_date"),
        "dependency_ids": task.get("dependency_ids", []),
    }


def _normalize_launch(raw_launch: dict[str, Any]) -> dict[str, Any]:
    milestones = [
        _normalize_task(task)
        for task in raw_launch.get("milestones", [])
    ]

    launch = {
        "id": raw_launch.get("id") or str(uuid4())[:8],
        "product_name": raw_launch.get("product_name", "New launch"),
        "launch_date": raw_launch.get("launch_date"),
        "market": raw_launch.get("market", "General market"),
        "team": raw_launch.get("team", "Product team"),
        "status": raw_launch.get("status", "planned"),
        "milestones": milestones,
    }
    return launch


def assess_launch(launch: dict[str, Any]) -> LaunchAssessment:
    normalized = _normalize_launch(launch)
    tasks = [Task(**task) for task in normalized["milestones"]]

    if not tasks:
        readiness_score = 50
        findings = [
            {
                "risk_type": "launch plan",
                "severity": "medium",
                "score": 40,
                "message": "No milestone data has been added yet.",
                "recommendation": "Define the launch plan with milestones, owners, and dependencies.",
                "evidence": ["No tasks were provided for the launch."],
            }
        ]
        return LaunchAssessment(
            launch_id=normalized["id"],
            readiness_score=readiness_score,
            risk_level="monitor",
            launch_window=normalized.get("launch_date", "TBD"),
            summary="The launch plan needs structure before confidence can be trusted.",
            findings=findings,
        )

    total = len(tasks)
    done = sum(1 for t in tasks if t.status == "done")
    blocked = sum(1 for t in tasks if t.status == "blocked")
    critical_remaining = sum(1 for t in tasks if t.priority == "critical" and t.status != "done")

    completion_ratio = (done / total) * 100 if total else 0
    blocked_penalty = blocked * 12
    critical_penalty = critical_remaining * 14

    launch_date = normalized.get("launch_date")
    deadline_penalty = 0
    if launch_date:
        from datetime import datetime

        try:
            target = datetime.fromisoformat(launch_date)
            days_to_launch = (target - datetime.now()).days
            if days_to_launch < 14:
                deadline_penalty = 20
            elif days_to_launch < 30:
                deadline_penalty = 10
        except ValueError:
            deadline_penalty = 0

    readiness_score = max(
        0,
        min(
            100,
            round(completion_ratio - blocked_penalty - critical_penalty - deadline_penalty),
        ),
    )

    if readiness_score >= 80:
        risk_level = "healthy"
    elif readiness_score >= 65:
        risk_level = "monitor"
    elif readiness_score >= 45:
        risk_level = "watch"
    else:
        risk_level = "critical"

    findings: list[dict[str, Any]] = []
    if blocked:
        findings.append(
            {
                "risk_type": "blocked work",
                "severity": "high" if blocked > 1 else "medium",
                "score": min(90, blocked * 18),
                "message": f"{blocked} milestone(s) are blocked and could delay the launch.",
                "recommendation": "Assign owners and unblock critical dependencies immediately.",
                "evidence": [f"Blocked milestones: {blocked}"],
            }
        )

    if critical_remaining:
        findings.append(
            {
                "risk_type": "critical path",
                "severity": "critical" if critical_remaining > 1 else "high",
                "score": min(95, critical_remaining * 18),
                "message": f"{critical_remaining} critical milestone(s) still require completion.",
                "recommendation": "Elevate ownership and remove blockers from the launch-critical path.",
                "evidence": [f"Critical tasks remaining: {critical_remaining}"],
            }
        )

    if readiness_score < 60:
        findings.append(
            {
                "risk_type": "launch confidence",
                "severity": "critical",
                "score": 75,
                "message": "The launch is underprepared for a high-confidence release window.",
                "recommendation": "Reduce scope, accelerate the critical path, and re-baseline the launch plan.",
                "evidence": [f"Readiness score: {readiness_score}"],
            }
        )

    if not findings:
        findings.append(
            {
                "risk_type": "launch health",
                "severity": "low",
                "score": 15,
                "message": "The launch appears stable with no major visible blockers.",
                "recommendation": "Protect momentum and maintain close ownership of the launch checklist.",
                "evidence": [f"Completion ratio: {round(completion_ratio)}%"],
            }
        )

    summary = (
        "The launch is in a strong operating position."
        if readiness_score >= 80
        else "The launch is manageable but should be monitored closely."
        if readiness_score >= 60
        else "The launch is at significant risk and needs immediate intervention."
    )

    return LaunchAssessment(
        launch_id=normalized["id"],
        readiness_score=readiness_score,
        risk_level=risk_level,
        launch_window=normalized.get("launch_date", "TBD"),
        summary=summary,
        findings=findings,
    )
