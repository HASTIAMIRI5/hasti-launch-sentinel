from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models import Launch
from app.services.data_store import assess_launch as calculate_assessment
from app.services.data_store import load_launches, save_launches

router = APIRouter(prefix="/api")


@router.get("/health")
def healthcheck():
    return {"status": "ok", "service": "hasti-launch-sentinel"}


@router.get("/launches")
def list_launches():
    launches = load_launches()
    return launches


@router.post("/launches")
def create_launch(payload: dict):
    launch = {
        "id": payload.get("id") or payload.get("product_name", "launch").lower().replace(" ", "-") + "-" + "1",
        "product_name": payload.get("product_name", "Untitled launch"),
        "launch_date": payload.get("launch_date"),
        "market": payload.get("market", "General market"),
        "team": payload.get("team", "Product team"),
        "status": payload.get("status", "planned"),
        "milestones": payload.get("milestones", []),
    }

    assessment = calculate_assessment(launch)
    launch["assessment"] = assessment.model_dump()

    existing = load_launches()
    existing.append(launch)
    save_launches(existing)
    return JSONResponse(content=launch, status_code=201)


@router.get("/launches/{launch_id}")
def get_launch(launch_id: str):
    for launch in load_launches():
        if launch.get("id") == launch_id:
            return launch
    return JSONResponse(content={"detail": "Launch not found"}, status_code=404)


@router.post("/launches/{launch_id}/assess")
def assess_specific_launch(launch_id: str):
    for launch in load_launches():
        if launch.get("id") == launch_id:
            assessment = calculate_assessment(launch)
            launch["assessment"] = assessment.model_dump()
            save_launches([l for l in load_launches() if l.get("id") != launch_id] + [launch])
            return launch
    return JSONResponse(content={"detail": "Launch not found"}, status_code=404)
