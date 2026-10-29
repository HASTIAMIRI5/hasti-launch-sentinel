from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="Hasti Launch Sentinel",
    description="AI product launch tracker and risk detector.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
app.include_router(api_router)


@app.get("/")
def root() -> FileResponse:
    return FileResponse(str(BASE_DIR / "app" / "static" / "index.html"))
