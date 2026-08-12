from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.agents.analytics import GrowthAnalystAgent
from app.agents.content import ContentCreatorAgent, ContentPlannerAgent, QualityAgent
from app.agents.publisher import PublisherAgent
from app.agents.trend import TrendAgent
from app.models import Job
from app.services.retention import clean_expired_user_content


class Orchestrator:
    def __init__(self, db: Session):
        self.db = db

    async def run_daily_content(self, date: datetime | None = None) -> dict:
        date = date or datetime.now(timezone.utc)
        key = f"daily-content:{date.date().isoformat()}"
        job = Job(dedup_key=key, job_type="daily_content", status="running", started_at=datetime.now(timezone.utc))
        self.db.add(job)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return {"status": "already_ran", "dedup_key": key}

        try:
            trend = await TrendAgent(self.db).run({"date": date.date().isoformat()})
            plan = await ContentPlannerAgent(self.db).run({"date": date.isoformat(), "trend": trend.data})
            create = await ContentCreatorAgent(self.db).run(plan.data)
            quality = await QualityAgent(self.db).run(create.data)
            publish = await PublisherAgent(self.db).run({"content_ids": quality.data.get("ready", [])})
            result = {
                "trend": trend.data,
                "plan": plan.data,
                "created": create.data,
                "quality": quality.data,
                "publish": publish.data,
            }
            job.status = "completed"
            job.result = result
            job.finished_at = datetime.now(timezone.utc)
            self.db.commit()
            return result
        except Exception as exc:
            job.status = "failed"
            job.error = str(exc)
            job.finished_at = datetime.now(timezone.utc)
            self.db.commit()
            raise

    async def run_weekly_review(self) -> dict:
        date = datetime.now(timezone.utc)
        key = f"weekly-review:{date.date().isoformat()}"
        job = Job(dedup_key=key, job_type="weekly_review", status="running", started_at=date)
        self.db.add(job)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return {"status": "already_ran", "dedup_key": key}
        result = (await GrowthAnalystAgent(self.db).run({"days": 7})).data
        job.status = "completed"
        job.result = result
        job.finished_at = datetime.now(timezone.utc)
        self.db.commit()
        return result
    async def run_retention_cleanup(self) -> dict:
        date = datetime.now(timezone.utc)
        key = f"retention-cleanup:{date.date().isoformat()}"
        job = Job(dedup_key=key, job_type="retention_cleanup", status="running", started_at=date)
        self.db.add(job)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return {"status": "already_ran", "dedup_key": key}
        result = clean_expired_user_content(self.db)
        job.status = "completed"
        job.result = result
        job.finished_at = datetime.now(timezone.utc)
        self.db.commit()
        return job.result

