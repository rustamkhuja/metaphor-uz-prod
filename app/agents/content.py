from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from app.agents.base import AgentResult, BaseAgent
from app.models import ContentItem
from app.services.ai_budget import ensure_budget_available, record_metered_usage
from app.services.media import render_quote_card, render_vertical_video
from app.services.tts import synthesize_xai_speech

ROOT = Path(__file__).resolve().parents[2]


class ContentPlannerAgent(BaseAgent):
    name = "content_planner"

    def _seed_for_day(self, date: datetime) -> dict:
        rows = list(csv.DictReader((ROOT / "content" / "seed_calendar_30d.csv").open(encoding="utf-8")))
        return rows[(date.timetuple().tm_yday - 1) % len(rows)]

    async def run(self, payload: dict) -> AgentResult:
        date = datetime.fromisoformat(payload["date"]) if payload.get("date") else datetime.now()
        seed = self._seed_for_day(date)
        return AgentResult(success=True, data={"date": date.date().isoformat(), "seed": seed, "trend": payload.get("trend", {})})


class ContentCreatorAgent(BaseAgent):
    name = "content_creator"

    async def run(self, payload: dict) -> AgentResult:
        seed = payload["seed"]
        prompt = f"""
Create one useful Metaphor social post in Russian and one in natural Uzbek Latin.
Theme: {seed['theme']}
Audience: {seed['audience']}
Hook: {seed['hook']}
Call to action: {seed['cta']}
Format: {seed['format']}

Rules: show a recognizable bad message and a better alternative; no fake statistics; no invented quotes; no manipulation; no medical or legal claims; each language must sound native. Return strict JSON:
{{"ru":{{"body":"...","card_text":"..."}},"uz":{{"body":"...","card_text":"..."}}}}
""".strip()
        result = await self.generate_ai(
            "You are the senior bilingual editor of Metaphor. Produce practical, humane communication content.",
            prompt,
            purpose="content_create",
        )
        data = self.llm.parse_json(result.text)
        created = []
        for language in ("ru", "uz"):
            item = data.get(language) or {}
            body = str(item.get("body") or "").strip()
            card_text = str(item.get("card_text") or body[:220]).strip()
            if not body:
                continue
            record = ContentItem(
                channel="telegram",
                language=language,
                content_type=seed.get("format", "post"),
                theme=seed.get("theme", ""),
                body=body,
                status="quality_review",
                source_json={"seed": seed, "model": result.model, "provider": result.provider},
            )
            self.db.add(record)
            self.db.flush()
            if seed.get("format") == "reel_script":
                media_path = ROOT / "exports" / f"{record.id}.mp4"
                audio_path = None
                if self.settings.xai_tts_enabled:
                    try:
                        ensure_budget_available(self.db, self.settings)
                        audio_file = ROOT / "exports" / f"{record.id}.mp3"
                        audio_path, tts_cost = await synthesize_xai_speech(
                            card_text,
                            language,
                            str(audio_file),
                            self.settings,
                        )
                        record_metered_usage(
                            self.db,
                            purpose="content_tts",
                            provider="xai",
                            model="text-to-speech",
                            cost_usd=tts_cost,
                            metadata={"language": language, "characters": len(card_text)},
                        )
                    except Exception as exc:
                        record.source_json = {**record.source_json, "tts_warning": str(exc)[:300]}
                render_vertical_video(card_text, str(media_path), audio_path=audio_path)
            else:
                media_path = ROOT / "exports" / f"{record.id}.png"
                render_quote_card(card_text, str(media_path))
            record.media_path = str(media_path)
            created.append(record.id)
        self.db.commit()
        return AgentResult(success=bool(created), data={"content_ids": created})


class QualityAgent(BaseAgent):
    name = "quality"

    async def run(self, payload: dict) -> AgentResult:
        approved, human = [], []
        for content_id in payload.get("content_ids", []):
            item = self.db.get(ContentItem, content_id)
            if not item:
                continue
            prompt = f"""
Assess this social post for Metaphor.
Language: {item.language}
Text: {item.body}
Return strict JSON: {{"score":0-100,"risk":"low|medium|high","issues":["..."],"corrected_body":"..."}}
Reject fabricated facts, author quotations, emotional manipulation, threats, discriminatory language, sexual content involving minors, medical/legal advice, or unnatural Uzbek/Russian.
""".strip()
            result = await self.generate_ai(
                "You are Metaphor's quality and safety reviewer.",
                prompt,
                purpose="content_quality",
            )
            data = self.llm.parse_json(result.text)
            score = float(data.get("score") or 0)
            risk = str(data.get("risk") or "medium")
            corrected = str(data.get("corrected_body") or "").strip()
            if corrected:
                item.body = corrected
            item.quality_score = score
            item.risk_level = risk
            if score >= 85 and risk == "low":
                item.status = "approved" if self.settings.auto_approve_low_risk_content else "ready_for_approval"
                approved.append(content_id)
            else:
                item.status = "needs_human_review"
                human.append(content_id)
        self.db.commit()
        return AgentResult(
            success=True,
            data={"ready": approved, "needs_human": human},
            requires_human=bool(human) or not self.settings.auto_approve_low_risk_content,
            reason="Content remains gated until confidence and brand quality are proven.",
        )
