from __future__ import annotations

from fastapi import Header, HTTPException, Request

from app.config import get_settings


def client_id(request: Request) -> str:
    value = getattr(request.state, "client_id", None)
    return str(value or "anonymous")[:128]


def require_admin(x_admin_key: str = Header(default="")) -> None:
    settings = get_settings()
    if not settings.admin_api_key or x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Invalid admin key")
