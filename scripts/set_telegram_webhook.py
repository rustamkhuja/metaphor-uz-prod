from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import asyncio

from app.config import get_settings
from app.services.telegram import TelegramClient


async def main() -> None:
    settings = get_settings()
    url = settings.public_base_url.rstrip("/") + "/api/v1/telegram/webhook"
    result = await TelegramClient(settings).set_webhook(url)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
