from __future__ import annotations

from dataclasses import dataclass
import json
import logging
import re
from typing import Any

import httpx

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


@dataclass
class ProviderConfig:
    name: str
    base_url: str
    api_key: str
    model: str
    input_usd_per_m: float
    output_usd_per_m: float


@dataclass
class LLMResult:
    text: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    citations: list[str] | None = None


class LLMError(RuntimeError):
    pass


class LLMRouter:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.primary = ProviderConfig(
            self.settings.llm_primary_provider,
            self.settings.llm_primary_base_url,
            self.settings.llm_primary_api_key,
            self.settings.llm_primary_model,
            self.settings.llm_primary_input_usd_per_m,
            self.settings.llm_primary_output_usd_per_m,
        )
        self.secondary = ProviderConfig(
            self.settings.llm_secondary_provider,
            self.settings.llm_secondary_base_url,
            self.settings.llm_secondary_api_key,
            self.settings.llm_secondary_model,
            self.settings.llm_secondary_input_usd_per_m,
            self.settings.llm_secondary_output_usd_per_m,
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        web_search: bool = False,
        json_mode: bool | None = None,
    ) -> LLMResult:
        errors: list[str] = []
        for provider in (self.primary, self.secondary):
            if not provider.name:
                continue
            try:
                if provider.name == "mock":
                    return self._mock(user_prompt)
                return await self._responses_api(
                    provider,
                    system_prompt,
                    user_prompt,
                    web_search=web_search,
                    json_mode=self.settings.llm_json_mode if json_mode is None else json_mode,
                )
            except Exception as exc:  # failover is intentional and audited through logs
                logger.exception("LLM provider %s failed", provider.name)
                errors.append(f"{provider.name}: {exc}")
        raise LLMError("All configured LLM providers failed: " + " | ".join(errors))

    async def _responses_api(
        self,
        provider: ProviderConfig,
        system_prompt: str,
        user_prompt: str,
        *,
        web_search: bool,
        json_mode: bool,
    ) -> LLMResult:
        if not provider.api_key:
            raise LLMError(f"API key is missing for provider {provider.name}")
        endpoint = provider.base_url.rstrip("/") + "/responses"
        payload: dict[str, Any] = {
            "model": provider.model,
            "input": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "store": False,
            "max_output_tokens": self.settings.llm_max_output_tokens,
        }
        if json_mode:
            payload["text"] = {"format": {"type": "json_object"}}
        if web_search:
            payload["tools"] = [{"type": "web_search"}]
        if provider.name.lower() == "xai":
            if self.settings.llm_prompt_cache_key:
                payload["prompt_cache_key"] = self.settings.llm_prompt_cache_key
            if self.settings.llm_reasoning_effort:
                payload["reasoning"] = {"effort": self.settings.llm_reasoning_effort}

        async with httpx.AsyncClient(timeout=self.settings.llm_timeout_seconds) as client:
            response = await client.post(
                endpoint,
                headers={"Authorization": f"Bearer {provider.api_key}", "Content-Type": "application/json"},
                json=payload,
            )
        if response.status_code >= 400:
            raise LLMError(f"HTTP {response.status_code}: {response.text[:500]}")
        data = response.json()
        text = self._extract_output_text(data)
        if not text:
            raise LLMError("Provider returned no output text")
        usage = data.get("usage") or {}
        input_tokens = int(usage.get("input_tokens") or usage.get("prompt_tokens") or 0)
        output_tokens = int(usage.get("output_tokens") or usage.get("completion_tokens") or 0)
        ticks = usage.get("cost_in_usd_ticks")
        if ticks is not None:
            cost = float(ticks) / 10_000_000_000
        else:
            cost = (input_tokens / 1_000_000 * provider.input_usd_per_m) + (
                output_tokens / 1_000_000 * provider.output_usd_per_m
            )
        citations: list[str] = []
        for item in data.get("output", []):
            for part in item.get("content", []) if isinstance(item, dict) else []:
                for annotation in part.get("annotations", []) if isinstance(part, dict) else []:
                    url = annotation.get("url")
                    if url:
                        citations.append(str(url))
        return LLMResult(text, provider.name, provider.model, input_tokens, output_tokens, cost, citations)

    @staticmethod
    def _extract_output_text(data: dict[str, Any]) -> str:
        if isinstance(data.get("output_text"), str):
            return data["output_text"]
        chunks: list[str] = []
        for item in data.get("output", []):
            if not isinstance(item, dict):
                continue
            for part in item.get("content", []):
                if not isinstance(part, dict):
                    continue
                if part.get("type") in {"output_text", "text"} and isinstance(part.get("text"), str):
                    chunks.append(part["text"])
        if chunks:
            return "\n".join(chunks)
        choices = data.get("choices") or []
        if choices:
            return str((choices[0].get("message") or {}).get("content") or "")
        return ""

    @staticmethod
    def parse_json(text: str) -> dict[str, Any]:
        value = text.strip()
        value = re.sub(r"^```(?:json)?\s*", "", value, flags=re.I)
        value = re.sub(r"\s*```$", "", value)
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", value, flags=re.S)
            if not match:
                raise LLMError("Model output is not JSON")
            parsed = json.loads(match.group(0))
        if not isinstance(parsed, dict):
            raise LLMError("Model output JSON must be an object")
        return parsed

    @staticmethod
    def _mock(user_prompt: str) -> LLMResult:
        low = user_prompt.lower()
        if "create one useful metaphor social post" in low:
            payload = {
                "ru": {
                    "body": "Фраза «не переживай» редко помогает человеку, которому действительно тяжело. Лучше назвать его усилие и предложить конкретное присутствие: «Я вижу, сколько сил ты вложил. Я рядом и могу просто выслушать». Проверьте свой текст в Metaphor.",
                    "card_text": "Поддержка — это не «не переживай». Это: «Я рядом и могу выслушать».",
                },
                "uz": {
                    "body": "«Xafa bo‘lma» degan gap og‘ir vaziyatda har doim ham yordam bermaydi. Yaxshiroq variant: «Qancha harakat qilganingizni ko‘ryapman. Men yoningizdaman va istasangiz, sizni tinglayman». Matningiz ohangini Metaphor’da tekshiring.",
                    "card_text": "Qo‘llab-quvvatlash — «xafa bo‘lma» emas. «Men yoningizdaman» deyishdir.",
                },
            }
            return LLMResult(json.dumps(payload, ensure_ascii=False), "mock", "mock-v1")
        if "assess this social post" in low:
            body = user_prompt.split("Text:", 1)[-1].split("Return strict JSON", 1)[0].strip()
            payload = {"score": 92, "risk": "low", "issues": [], "corrected_body": body}
            return LLMResult(json.dumps(payload, ensure_ascii=False), "mock", "mock-v1")
        if "review these first-party product metrics" in low:
            payload = {
                "diagnosis": "The main constraint is insufficient send/copy evidence.",
                "bottleneck": "Users generate text but the product has not yet proven repeat use.",
                "experiment": "Show three goal-specific examples on the first screen.",
                "stop_condition": "Stop after 500 eligible sessions if send/copy rate does not improve by 15%.",
                "success_metric": "send_or_copy_events per 100 generations",
            }
            return LLMResult(json.dumps(payload, ensure_ascii=False), "mock", "mock-v1")
        if "find only useful" in low:
            payload = {"signals": [], "note": "Mock mode: no external trend search."}
            return LLMResult(json.dumps(payload, ensure_ascii=False), "mock", "mock-v1")
        language = "uz" if '"language": "uz"' in low else "en" if '"language": "en"' in low else "ru"
        if language == "uz":
            text = "Men bu vaziyat haqida o‘yladim. Sizni xafa qilgan bo‘lsam, uzr so‘rayman. Men uchun munosabatimiz muhim va buni xotirjam gaplashib olishni istayman."
            note = "Hurmatli va tabiiy ohang."
        elif language == "en":
            text = "I have thought about what happened. I am sorry for the part I played. Our relationship matters to me, and I would like us to talk calmly when you are ready."
            note = "Warm, direct and non-manipulative."
        else:
            text = "Я обдумал то, что произошло. Мне жаль, что я вас задел. Для меня важны наши отношения, и я хотел бы спокойно поговорить, когда вы будете готовы."
            note = "Тёплый, прямой и ненавязчивый тон."
        payload = {"variants": [{"label": "Основной", "text": text}], "tone_notes": note, "warnings": []}
        return LLMResult(json.dumps(payload, ensure_ascii=False), "mock", "mock-v1", 0, 0, 0.0, [])
