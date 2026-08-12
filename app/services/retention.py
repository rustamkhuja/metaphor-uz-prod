from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.models import Generation


def clean_expired_user_content(db: Session, settings: Settings | None = None) -> dict[str, int]:
    settings = settings or get_settings()
    now = datetime.now(timezone.utc)
    raw_cutoff = now - timedelta(hours=settings.raw_input_retention_hours)
    output_cutoff = now - timedelta(hours=settings.output_retention_hours)

    raw = db.execute(
        update(Generation)
        .where(
            Generation.created_at < raw_cutoff,
            (Generation.input_encrypted.is_not(None)) | (Generation.input_redacted != ""),
        )
        .values(input_encrypted=None, input_redacted="")
    )
    output = db.execute(
        update(Generation)
        .where(Generation.created_at < output_cutoff, Generation.output_json != {})
        .values(output_json={})
    )
    db.commit()
    return {"raw_inputs_cleaned": int(raw.rowcount or 0), "outputs_cleaned": int(output.rowcount or 0)}


def clean_expired_raw_inputs(db: Session, settings: Settings | None = None) -> int:
    """Backward-compatible wrapper used by older scripts."""
    return clean_expired_user_content(db, settings)["raw_inputs_cleaned"]
