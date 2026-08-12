from __future__ import annotations

from datetime import datetime, timezone

from app.agents.base import AgentResult, BaseAgent
from app.models import ContentItem
from app.services.telegram import TelegramClient


class PublisherAgent(BaseAgent):
    name = "publisher"

    async def run(self, payload: dict) -> AgentResult:
        if not self.settings.auto_publish_telegram:
            return AgentResult(True, {"published": []}, True, "AUTO_PUBLISH_TELEGRAM is disabled")
        if not self.settings.telegram_channel_id:
            return AgentResult(False, {"published": []}, True, "TELEGRAM_CHANNEL_ID is missing")
        client = TelegramClient(self.settings)
        published = []
        for content_id in payload.get("content_ids", []):
            item = self.db.get(ContentItem, content_id)
            if not item or item.status != "approved":
                continue
            response = await client.send_media(self.settings.telegram_channel_id, item.media_path, item.body)
            item.status = "published"
            item.external_id = str(response.get("message_id") or "")
            item.published_at = datetime.now(timezone.utc)
            published.append(content_id)
        self.db.commit()
        return AgentResult(True, {"published": published})
