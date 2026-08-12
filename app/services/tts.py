from __future__ import annotations

from pathlib import Path

import httpx

from app.config import Settings, get_settings


class TTSError(RuntimeError):
    pass


async def synthesize_xai_speech(
    text: str,
    language: str,
    output_path: str,
    settings: Settings | None = None,
) -> tuple[str, float]:
    settings = settings or get_settings()
    if not settings.xai_tts_enabled:
        raise TTSError("xAI TTS is disabled")
    if not settings.llm_primary_api_key:
        raise TTSError("LLM_PRIMARY_API_KEY is required for xAI TTS")
    clean = " ".join((text or "").split())[:15000]
    if not clean:
        raise TTSError("No text for TTS")
    lang = "ru" if language == "ru" else "en" if language == "en" else "auto"
    endpoint = settings.xai_tts_base_url.rstrip("/") + "/tts"
    payload = {
        "text": clean,
        "voice_id": settings.xai_tts_voice_id,
        "language": lang,
    }
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {settings.llm_primary_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
    if response.status_code >= 400:
        raise TTSError(f"TTS HTTP {response.status_code}: {response.text[:300]}")
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response.content)
    estimated_cost = len(clean) / 1_000_000 * settings.xai_tts_usd_per_m_characters
    return str(target), estimated_cost
