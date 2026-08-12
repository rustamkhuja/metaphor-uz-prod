from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.models import Generation
from app.schemas import GenerationRequest, GenerationResponse, RefineRequest, Variant
from app.services.ai_budget import AIBudgetExceeded, ensure_budget_available, record_llm_usage
from app.services.llm import LLMRouter, LLMError
from app.services.prompts import SYSTEM_PROMPT, build_generation_prompt, build_refine_prompt
from app.services.redaction import DataProtector, redact
from app.services.safety import classify


class GenerationService:
    def __init__(self, db: Session, settings: Settings | None = None):
        self.db = db
        self.settings = settings or get_settings()
        self.router = LLMRouter(self.settings)
        self.protector = DataProtector(self.settings.data_encryption_key)

    def _check_daily_limit(self, client_id: str, tier: str) -> None:
        if tier == "premium":
            return
        since = datetime.now(timezone.utc) - timedelta(days=1)
        count = self.db.scalar(
            select(func.count(Generation.id)).where(
                Generation.client_id == client_id,
                Generation.created_at >= since,
            )
        ) or 0
        if count >= self.settings.free_daily_limit:
            raise HTTPException(status_code=429, detail="Дневной бесплатный лимит исчерпан.")

    def _check_daily_budget(self) -> None:
        try:
            ensure_budget_available(self.db, self.settings)
        except AIBudgetExceeded as exc:
            raise HTTPException(status_code=503, detail="Временный лимит расходов достигнут.") from exc

    async def create(self, client_id: str, request: GenerationRequest) -> GenerationResponse:
        if not request.accepted_terms:
            raise HTTPException(status_code=400, detail="Необходимо подтвердить правила обработки текста.")
        combined = (request.context + "\n" + request.source_text).strip()
        if not combined:
            raise HTTPException(status_code=422, detail="Опишите ситуацию или вставьте исходный текст.")
        if len(combined) > self.settings.max_input_characters:
            raise HTTPException(status_code=422, detail="Текст превышает допустимый объём.")

        safety = classify(combined)
        if safety.blocked:
            raise HTTPException(status_code=422, detail=safety.message)
        self._check_daily_limit(client_id, request.tier)
        self._check_daily_budget()

        variants_count = self.settings.premium_variants if request.tier == "premium" else 1
        prompt = build_generation_prompt(request, variants_count)
        try:
            result = await self.router.generate(SYSTEM_PROMPT, prompt, json_mode=True)
            record_llm_usage(
                self.db,
                result,
                "user_generation",
                metadata={"mode": request.mode, "language": request.language, "tier": request.tier},
            )
            parsed = self.router.parse_json(result.text)
        except (LLMError, ValueError, json.JSONDecodeError) as exc:
            raise HTTPException(status_code=502, detail=f"Модель не вернула корректный результат: {exc}") from exc

        variants = []
        for idx, item in enumerate(parsed.get("variants") or []):
            if not isinstance(item, dict):
                continue
            text = str(item.get("text") or "").strip()
            if text:
                variants.append(Variant(label=str(item.get("label") or f"Вариант {idx + 1}"), text=text[:12000]))
        if not variants:
            raise HTTPException(status_code=502, detail="Модель не сформировала сообщение.")

        raw = json.dumps(request.model_dump(), ensure_ascii=False)
        record = Generation(
            client_id=client_id,
            mode=request.mode,
            tier=request.tier,
            source=request.source,
            partner_code=request.partner_code,
            language=request.language,
            relationship=request.relationship,
            goal=request.goal,
            tone=request.tone,
            output_format=request.output_format,
            length=request.length,
            input_redacted=redact(combined)[:6000] if self.settings.store_redacted_input else "",
            input_length=len(combined),
            input_encrypted=self.protector.encrypt(raw) if self.settings.store_raw_input else None,
            output_json=parsed if self.settings.store_generated_output else {},
            provider=result.provider,
            model=result.model,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            cost_usd=result.cost_usd,
            safety_level=safety.level,
            privacy_version=self.settings.privacy_policy_version,
            terms_version=self.settings.terms_version,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return GenerationResponse(
            generation_id=record.id,
            variants=variants,
            tone_notes=str(parsed.get("tone_notes") or "")[:1000],
            warnings=[str(x)[:500] for x in parsed.get("warnings") or []],
            safety_level=safety.level,
            provider=result.provider,
            model=result.model,
            estimated_cost_usd=round(result.cost_usd, 6),
        )

    async def refine(self, client_id: str, generation_id: str, request: RefineRequest) -> GenerationResponse:
        original = self.db.get(Generation, generation_id)
        if not original or original.client_id != client_id:
            raise HTTPException(status_code=404, detail="Результат не найден.")
        safety = classify(request.selected_text)
        if safety.blocked:
            raise HTTPException(status_code=422, detail=safety.message)
        self._check_daily_limit(client_id, original.tier)
        self._check_daily_budget()
        prompt = build_refine_prompt(request.selected_text, request.instruction, original.language)
        try:
            result = await self.router.generate(SYSTEM_PROMPT, prompt, json_mode=True)
            record_llm_usage(
                self.db,
                result,
                "user_refine",
                metadata={"language": original.language, "instruction": request.instruction},
            )
            parsed = self.router.parse_json(result.text)
        except (LLMError, ValueError, json.JSONDecodeError) as exc:
            raise HTTPException(status_code=502, detail=f"Модель не вернула корректный результат: {exc}") from exc
        items = parsed.get("variants") or []
        variants = [
            Variant(label=str(item.get("label") or "Обновлённый"), text=str(item.get("text") or "").strip()[:12000])
            for item in items
            if isinstance(item, dict) and str(item.get("text") or "").strip()
        ]
        if not variants:
            raise HTTPException(status_code=502, detail="Модель не сформировала уточнённый вариант.")
        record = Generation(
            client_id=client_id,
            mode="refine",
            tier=original.tier,
            source=original.source,
            partner_code=original.partner_code,
            language=original.language,
            relationship=original.relationship,
            goal=original.goal,
            tone=original.tone,
            output_format=original.output_format,
            length=original.length,
            input_redacted=redact(request.selected_text)[:6000] if self.settings.store_redacted_input else "",
            input_length=len(request.selected_text),
            output_json=parsed if self.settings.store_generated_output else {},
            provider=result.provider,
            model=result.model,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            cost_usd=result.cost_usd,
            safety_level=safety.level,
            privacy_version=self.settings.privacy_policy_version,
            terms_version=self.settings.terms_version,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return GenerationResponse(
            generation_id=record.id,
            variants=variants,
            tone_notes=str(parsed.get("tone_notes") or "")[:1000],
            warnings=[str(x)[:500] for x in parsed.get("warnings") or []],
            safety_level=safety.level,
            provider=result.provider,
            model=result.model,
            estimated_cost_usd=round(result.cost_usd, 6),
        )
