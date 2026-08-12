from __future__ import annotations

import httpx

from app.config import Settings, get_settings


class TelegramClient:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    async def send_message(
        self,
        chat_id: str,
        text: str,
        *,
        parse_mode: str | None = None,
        reply_markup: dict | None = None,
    ) -> dict:
        if not self.settings.telegram_bot_token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")
        payload = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if reply_markup:
            payload["reply_markup"] = reply_markup
        endpoint = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(endpoint, json=payload)
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(str(data))
        return data["result"]

    async def set_webhook(self, url: str) -> dict:
        if not self.settings.telegram_bot_token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")
        endpoint = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/setWebhook"
        payload = {"url": url, "secret_token": self.settings.telegram_webhook_secret}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()

    async def send_media(self, chat_id: str, media_path: str, caption: str) -> dict:
        from pathlib import Path
        path = Path(media_path)
        if not path.exists():
            return await self.send_message(chat_id, caption)
        if not self.settings.telegram_bot_token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")
        is_video = path.suffix.lower() == ".mp4"
        method = "sendVideo" if is_video else "sendPhoto"
        field = "video" if is_video else "photo"
        endpoint = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/{method}"
        data = {"chat_id": chat_id, "caption": caption[:1024]}
        async with httpx.AsyncClient(timeout=90) as client:
            with path.open("rb") as file_handle:
                response = await client.post(endpoint, data=data, files={field: (path.name, file_handle)})
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(str(payload))
        return payload["result"]
