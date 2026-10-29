from __future__ import annotations

import hashlib
import os
from datetime import datetime, timedelta
from typing import Any

import jwt

from app.config import get_settings

_USERS: dict[str, dict[str, Any]] = {}


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(email: str, password: str, name: str) -> dict[str, Any]:
    if email in _USERS:
        raise ValueError("User already exists")
    user = {
        "id": f"user-{len(_USERS) + 1}",
        "email": email,
        "name": name,
        "password_hash": _hash_password(password),
        "role": "member",
    }
    _USERS[email] = user
    return {"id": user["id"], "email": user["email"], "name": user["name"], "role": user["role"]}


def authenticate_user(email: str, password: str) -> dict[str, Any] | None:
    user = _USERS.get(email)
    if not user:
        return None
    if user["password_hash"] != _hash_password(password):
        return None
    return {"id": user["id"], "email": user["email"], "name": user["name"], "role": user["role"]}


def create_access_token(user: dict[str, Any]) -> str:
    settings = get_settings()
    payload = {
        "sub": user["email"],
        "user_id": user["id"],
        "exp": datetime.utcnow() + timedelta(hours=12),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
