from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents.orchestrator import Orchestrator
from app.api.deps import require_admin
from app.db import get_db
from app.models import AuditEvent, ContentItem
from app.schemas import ContentApprovalRequest
from app.services.metrics import dashboard_snapshot
from app.services.telegram import TelegramClient

router = APIRouter(prefix="/api/v1/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/dashboard")
def dashboard(days: int = 7, db: Session = Depends(get_db)):
    return dashboard_snapshot(db, max(1, min(days, 90)))


@router.get("/content")
def list_content(status: str | None = None, db: Session = Depends(get_db)):
    query = select(ContentItem).order_by(ContentItem.created_at.desc()).limit(100)
    if status:
        query = query.where(ContentItem.status == status)
    items = db.scalars(query).all()
    return [
        {
            "id": item.id,
            "language": item.language,
            "channel": item.channel,
            "theme": item.theme,
            "body": item.body,
            "status": item.status,
            "quality_score": item.quality_score,
            "risk_level": item.risk_level,
            "media_path": item.media_path,
            "media_url": f"/exports/{Path(item.media_path).name}" if item.media_path else "",
            "created_at": item.created_at,
        }
        for item in items
    ]


@router.post("/content/run")
async def run_content(db: Session = Depends(get_db)):
    return await Orchestrator(db).run_daily_content(datetime.now(timezone.utc))


@router.post("/content/{content_id}/approval")
def approve_content(content_id: str, request: ContentApprovalRequest, db: Session = Depends(get_db)):
    item = db.get(ContentItem, content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content not found")
    item.status = "approved" if request.approved else "rejected"
    db.add(AuditEvent(actor="operator", event_type="content_approval", entity_type="content", entity_id=item.id, payload={"approved": request.approved, "note": request.operator_note}))
    db.commit()
    return {"ok": True, "status": item.status}


@router.post("/content/{content_id}/publish")
async def publish_content(content_id: str, db: Session = Depends(get_db)):
    item = db.get(ContentItem, content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content not found")
    if item.status != "approved":
        raise HTTPException(status_code=409, detail="Content must be approved first")
    client = TelegramClient()
    from app.config import get_settings
    settings = get_settings()
    if not settings.telegram_channel_id:
        raise HTTPException(status_code=503, detail="Telegram channel is not configured")
    response = await client.send_media(settings.telegram_channel_id, item.media_path, item.body)
    item.status = "published"
    item.external_id = str(response.get("message_id") or "")
    item.published_at = datetime.now(timezone.utc)
    db.add(AuditEvent(actor="operator", event_type="content_publish", entity_type="content", entity_id=item.id, payload={"message_id": item.external_id}))
    db.commit()
    return {"ok": True, "message_id": item.external_id}
