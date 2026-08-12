from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import client_id
from app.config import get_settings
from app.db import get_db
from app.models import Feedback, Generation
from app.schemas import FeedbackRequest, GenerationRequest, GenerationResponse, RefineRequest
from app.services.generation import GenerationService

router = APIRouter(prefix="/api/v1", tags=["public"])


@router.post("/generate", response_model=GenerationResponse)
async def generate(
    request: GenerationRequest,
    cid: str = Depends(client_id),
    x_premium_key: str = Header(default=""),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    if request.tier == "premium":
        if (
            not settings.enable_premium_pilot
            or not settings.premium_access_key
            or x_premium_key != settings.premium_access_key
        ):
            raise HTTPException(status_code=403, detail="Premium entitlement is not active.")
    return await GenerationService(db).create(cid, request)


@router.post("/generate/{generation_id}/refine", response_model=GenerationResponse)
async def refine(
    generation_id: str,
    request: RefineRequest,
    cid: str = Depends(client_id),
    db: Session = Depends(get_db),
):
    return await GenerationService(db).refine(cid, generation_id, request)


@router.post("/feedback")
def feedback(
    request: FeedbackRequest,
    cid: str = Depends(client_id),
    db: Session = Depends(get_db),
):
    generation = db.get(Generation, request.generation_id)
    if not generation or generation.client_id != cid:
        raise HTTPException(status_code=404, detail="Результат не найден.")
    record = db.scalar(
        select(Feedback).where(
            Feedback.generation_id == request.generation_id,
            Feedback.client_id == cid,
        )
    )
    if record:
        if request.rating != 0 or record.rating == 0:
            record.rating = request.rating
        record.reason = request.reason
        record.comment = request.comment
        record.sent_or_copied = request.sent_or_copied or record.sent_or_copied
    else:
        record = Feedback(
            generation_id=request.generation_id,
            client_id=cid,
            rating=request.rating,
            reason=request.reason,
            comment=request.comment,
            sent_or_copied=request.sent_or_copied,
        )
        db.add(record)
    db.commit()
    return {"ok": True}
