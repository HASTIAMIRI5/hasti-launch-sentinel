from __future__ import annotations

from collections import defaultdict
from typing import Any


def calculate_dashboard_summary(launches: list[dict[str, Any]]) -> dict[str, Any]:
    if not launches:
        return {
            "active_launches": 0,
            "average_readiness": 0,
            "critical_alerts": 0,
            "risk_distribution": {"healthy": 0, "monitor": 0, "watch": 0, "critical": 0},
            "trend": [],
        }

    readiness_scores = [
        int(launch.get("assessment", {}).get("readiness_score", 0)) for launch in launches if launch.get("assessment")
    ]
    critical_alerts = sum(
        1 for launch in launches if launch.get("assessment", {}).get("risk_level") == "critical"
    )

    risk_distribution = {"healthy": 0, "monitor": 0, "watch": 0, "critical": 0}
    for launch in launches:
        level = launch.get("assessment", {}).get("risk_level", "monitor")
        if level in risk_distribution:
            risk_distribution[level] += 1

    trend = [
        {
            "label": launch.get("product_name", "Launch"),
            "readiness": int(launch.get("assessment", {}).get("readiness_score", 0)),
        }
        for launch in launches
    ]

    return {
        "active_launches": len(launches),
        "average_readiness": round(sum(readiness_scores) / len(readiness_scores), 1) if readiness_scores else 0,
        "critical_alerts": critical_alerts,
        "risk_distribution": risk_distribution,
        "trend": trend,
    }
