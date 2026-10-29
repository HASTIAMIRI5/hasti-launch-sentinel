from typing import Literal, Optional, List

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    name: str
    owner: str
    status: Literal["todo", "in_progress", "done", "blocked"]
    priority: Literal["low", "medium", "high", "critical"]
    due_date: Optional[str] = None
    dependency_ids: List[str] = Field(default_factory=list)


class Launch(BaseModel):
    id: str
    product_name: str
    launch_date: Optional[str] = None
    market: str = "General market"
    team: str = "Product team"
    status: Literal["planned", "active", "at_risk", "launched"] = "planned"
    milestones: List[Task] = Field(default_factory=list)


class RiskFinding(BaseModel):
    risk_type: str
    severity: Literal["low", "medium", "high", "critical"]
    score: int
    message: str
    recommendation: str
    evidence: List[str] = Field(default_factory=list)


class LaunchAssessment(BaseModel):
    launch_id: str
    readiness_score: int
    risk_level: Literal["healthy", "monitor", "watch", "critical"]
    launch_window: str
    summary: str
    findings: List[RiskFinding] = Field(default_factory=list)
