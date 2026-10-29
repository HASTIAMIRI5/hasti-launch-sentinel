from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    name: str
    owner: str
    status: str = "todo"
    priority: str = "medium"
    due_date: str | None = None
    dependency_ids: list[str] = Field(default_factory=list)


class Launch(BaseModel):
    id: str
    product_name: str
    launch_date: str | None = None
    market: str = "General market"
    team: str = "Product team"
    status: str = "planned"
    milestones: list[Task] = Field(default_factory=list)


class RiskFinding(BaseModel):
    risk_type: str
    severity: str
    score: int
    message: str
    recommendation: str
    evidence: list[str] = Field(default_factory=list)


class LaunchAssessment(BaseModel):
    launch_id: str
    readiness_score: int
    risk_level: str
    launch_window: str
    summary: str
    findings: list[RiskFinding] = Field(default_factory=list)


class User(BaseModel):
    id: str
    email: str
    name: str
    role: str = "member"


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User


class DashboardSummary(BaseModel):
    active_launches: int
    average_readiness: float
    critical_alerts: int
    risk_distribution: dict[str, int]
    trend: list[dict[str, Any]]


class AIInsight(BaseModel):
    provider: str
    summary: str
    recommendations: list[str]
    risk_score: int
