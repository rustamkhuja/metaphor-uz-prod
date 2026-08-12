from __future__ import annotations

from datetime import datetime, timedelta, timezone
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AIUsage, ContentItem, Feedback, Generation


def dashboard_snapshot(db: Session, days: int = 7) -> dict:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    generations = db.scalar(select(func.count(Generation.id)).where(Generation.created_at >= since)) or 0
    users = db.scalar(select(func.count(func.distinct(Generation.client_id))).where(Generation.created_at >= since)) or 0
    cost = db.scalar(select(func.sum(AIUsage.cost_usd)).where(AIUsage.created_at >= since)) or 0.0
    positive = db.scalar(select(func.count(Feedback.id)).where(Feedback.created_at >= since, Feedback.rating == 1)) or 0
    negative = db.scalar(select(func.count(Feedback.id)).where(Feedback.created_at >= since, Feedback.rating == -1)) or 0
    sent = db.scalar(select(func.count(Feedback.id)).where(Feedback.created_at >= since, Feedback.sent_or_copied.is_(True))) or 0
    published = db.scalar(select(func.count(ContentItem.id)).where(ContentItem.published_at >= since)) or 0
    total_feedback = positive + negative
    purposes = db.execute(
        select(AIUsage.purpose, func.sum(AIUsage.cost_usd))
        .where(AIUsage.created_at >= since)
        .group_by(AIUsage.purpose)
    ).all()
    sources = db.execute(
        select(Generation.source, func.count(Generation.id))
        .where(Generation.created_at >= since)
        .group_by(Generation.source)
    ).all()
    partners = db.execute(
        select(Generation.partner_code, func.count(Generation.id))
        .where(Generation.created_at >= since, Generation.partner_code != "")
        .group_by(Generation.partner_code)
    ).all()
    return {
        "window_days": days,
        "generations": generations,
        "unique_users": users,
        "ai_cost_usd": round(float(cost), 6),
        "ai_cost_by_purpose": {str(name): round(float(value or 0), 6) for name, value in purposes},
        "generations_by_source": {str(name): int(value) for name, value in sources},
        "generations_by_partner": {str(name): int(value) for name, value in partners},
        "positive_feedback_rate": round(positive / total_feedback, 3) if total_feedback else None,
        "send_or_copy_events": sent,
        "send_or_copy_rate": round(sent / generations, 3) if generations else None,
        "published_content_items": published,
        "north_star": "send_or_copy_rate",
    }
