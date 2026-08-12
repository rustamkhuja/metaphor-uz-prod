from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.models import AIUsage
from app.services.llm import LLMResult


class AIBudgetExceeded(RuntimeError):
    pass


def spent_last_24_hours(db: Session) -> float:
    since = datetime.now(timezone.utc) - timedelta(days=1)
    value = db.scalar(select(func.sum(AIUsage.cost_usd)).where(AIUsage.created_at >= since)) or 0.0
    return float(value)


def ensure_budget_available(db: Session, settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    spent = spent_last_24_hours(db)
    if spent >= settings.daily_ai_budget_usd:
        raise AIBudgetExceeded(
            f"Daily AI budget reached: ${spent:.4f} / ${settings.daily_ai_budget_usd:.2f}"
        )


def record_llm_usage(db: Session, result: LLMResult, purpose: str, *, metadata: dict | None = None) -> AIUsage:
    record = AIUsage(
        purpose=purpose[:80],
        provider=result.provider[:32],
        model=result.model[:128],
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        cost_usd=float(result.cost_usd),
        metadata_json=metadata or {},
    )
    db.add(record)
    db.commit()
    return record


def record_metered_usage(
    db: Session,
    *,
    purpose: str,
    provider: str,
    model: str,
    cost_usd: float,
    metadata: dict | None = None,
) -> AIUsage:
    record = AIUsage(
        purpose=purpose[:80],
        provider=provider[:32],
        model=model[:128],
        cost_usd=float(cost_usd),
        metadata_json=metadata or {},
    )
    db.add(record)
    db.commit()
    return record
