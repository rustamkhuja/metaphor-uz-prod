from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from app.agents.orchestrator import Orchestrator
from app.config import get_settings
from app.db import SessionLocal, init_db
from app.services.telegram import TelegramClient


async def main() -> None:
    settings = get_settings()
    tz = ZoneInfo(settings.timezone)
    init_db()
    while True:
        now = datetime.now(tz)
        try:
            if now.hour == 2 and now.minute < 5:
                with SessionLocal() as db:
                    await Orchestrator(db).run_retention_cleanup()
            if now.hour == settings.daily_content_hour and now.minute < 5:
                with SessionLocal() as db:
                    await Orchestrator(db).run_daily_content(now)
            if now.weekday() == settings.weekly_review_weekday and now.hour == 10 and now.minute < 5:
                with SessionLocal() as db:
                    await Orchestrator(db).run_weekly_review()
        except Exception as exc:
            print(f"scheduler error: {exc}", flush=True)
            if settings.telegram_bot_token and settings.telegram_operator_chat_id:
                try:
                    await TelegramClient(settings).send_message(
                        settings.telegram_operator_chat_id,
                        f"Metaphor worker error: {type(exc).__name__}: {str(exc)[:600]}",
                    )
                except Exception as notify_exc:
                    print(f"operator notification error: {notify_exc}", flush=True)
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
