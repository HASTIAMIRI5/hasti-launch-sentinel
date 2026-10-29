from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models import AuthToken, LoginRequest, User, UserCreate
from app.services.ai_service import analyze_launch_with_ai
from app.services.analytics import calculate_dashboard_summary
from app.services.data_store import assess_launch, load_launches, save_launches

router = APIRouter(prefix="/api")


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": "hasti-launch-sentinel"}


@router.get("/launches")
def list_launches() -> list[dict]:
    return load_launches()


@router.post("/launches")
async def create_launch(payload: dict) -> dict:
    launch = {
        "id": payload.get("id") or payload.get("product_name", "launch").lower().replace(" ", "-") + "-1",
        "product_name": payload.get("product_name", "Untitled launch"),
        "launch_date": payload.get("launch_date"),
        "market": payload.get("market", "General market"),
        "team": payload.get("team", "Product team"),
        "status": payload.get("status", "planned"),
        "milestones": payload.get("milestones", []),
    }
    assessment = assess_launch(launch)
    launch["assessment"] = assessment.model_dump()

    launches = load_launches()
    launches.append(launch)
    save_launches(launches)
    return launch


@router.get("/launches/{launch_id}")
def get_launch(launch_id: str) -> dict:
    for launch in load_launches():
        if launch.get("id") == launch_id:
            return launch
    raise HTTPException(status_code=404, detail="Launch not found")


@router.post("/launches/{launch_id}/assess")
async def assess_specific_launch(launch_id: str) -> dict:
    launches = load_launches()
    for launch in launches:
        if launch.get("id") == launch_id:
            assessment = assess_launch(launch)
            launch["assessment"] = assessment.model_dump()
            save_launches(launches)
            return launch
    raise HTTPException(status_code=404, detail="Launch not found")


@router.get("/launches/{launch_id}/ai")
async def launch_ai_insight(launch_id: str) -> dict:
    for launch in load_launches():
        if launch.get("id") == launch_id:
            insight = await analyze_launch_with_ai(launch)
            return {"launch_id": launch_id, "insight": insight}
    raise HTTPException(status_code=404, detail="Launch not found")


@router.get("/dashboard")
async def dashboard() -> dict:
    launches = load_launches()
    summary = calculate_dashboard_summary(launches)
    return {"summary": summary, "launches": launches}


@router.post("/auth/register")
async def register_user(payload: UserCreate) -> AuthToken:
    user = User(id="demo-user-1", email=payload.email, name=payload.name, role="admin")
    return AuthToken(access_token="demo-token", user=user)


@router.post("/auth/login")
async def login_user(payload: LoginRequest) -> AuthToken:
    if not payload.email or not payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = User(id="demo-user-1", email=payload.email, name="Demo User", role="member")
    return AuthToken(access_token="demo-token", user=user)


@router.get("/projects")
def list_projects() -> list[str]:
    return [launch.get("product_name", "Untitled launch") for launch in load_launches()]
