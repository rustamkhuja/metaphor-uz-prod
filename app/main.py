from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.admin import router as admin_router
from app.api.public import router as public_router
from app.api.telegram import router as telegram_router
from app.config import get_settings
from app.db import get_db, init_db
from app.security import create_session_token, verify_session_token
from sqlalchemy import text
from sqlalchemy.orm import Session

settings = get_settings()
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

def _validate_legal_pages_for_production() -> None:
    if not settings.is_production:
        return
    static_root = Path(__file__).resolve().parents[1] / "app" / "static"
    placeholders = []
    for filename in ("privacy.html", "terms.html"):
        content = (static_root / filename).read_text(encoding="utf-8")
        if "[УКАЗАТЬ" in content or "технический проект" in content.lower():
            placeholders.append(filename)
    if placeholders:
        raise RuntimeError(
            "Unsafe production configuration: legal pages still contain draft placeholders: "
            + ", ".join(placeholders)
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.validate_for_startup()
    _validate_legal_pages_for_production()
    init_db()
    yield


app = FastAPI(
    title="Metaphor AI OS",
    version="0.2.1",
    lifespan=lifespan,
    docs_url="/api/docs" if not settings.is_production else None,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.public_base_url.rstrip("/"), "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"] ,
)

@app.middleware("http")
async def anonymous_session(request: Request, call_next):
    token = request.cookies.get("metaphor_session")
    session_id = verify_session_token(token, settings.session_secret)
    new_token = None
    if not session_id:
        new_token, session_id = create_session_token(settings.session_secret)
    request.state.client_id = f"web:{session_id}"
    response = await call_next(request)
    if new_token:
        response.set_cookie(
            "metaphor_session",
            new_token,
            max_age=31536000,
            httponly=True,
            secure=settings.is_production,
            samesite="lax",
            path="/",
        )
    return response


ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "app" / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")
EXPORTS = ROOT / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)
app.mount("/exports", StaticFiles(directory=EXPORTS), name="exports")
app.include_router(public_router)
app.include_router(admin_router)
app.include_router(telegram_router)


@app.get("/api/v1/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "environment": settings.app_env,
        "provider": settings.llm_primary_provider,
        "model": settings.llm_primary_model,
        "privacy_mode": "no-content-storage" if not settings.store_raw_input and not settings.store_generated_output else "configured-retention",
    }


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/widget")
def widget():
    return FileResponse(STATIC / "widget.html")


@app.get("/operator")
def operator():
    return FileResponse(STATIC / "operator.html")


@app.get("/privacy")
def privacy():
    return FileResponse(STATIC / "privacy.html")


@app.get("/terms")
def terms():
    return FileResponse(STATIC / "terms.html")
