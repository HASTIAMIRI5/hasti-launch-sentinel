from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_PATH = BASE_DIR / "data" / "launches.json"


def ensure_store() -> Path:
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not STORAGE_PATH.exists():
        STORAGE_PATH.write_text("[]", encoding="utf-8")
    return STORAGE_PATH


def load_launches() -> list[dict]:
    try:
        data = ensure_store().read_text(encoding="utf-8")
        if not data.strip():
            return []
        return json.loads(data)
    except json.JSONDecodeError:
        return []


def save_launches(launches: list[dict]) -> None:
    ensure_store().write_text(json.dumps(launches, indent=2), encoding="utf-8")
