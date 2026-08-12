from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import secrets
from app.services.redaction import DataProtector

print(f"ADMIN_API_KEY={secrets.token_urlsafe(32)}")
print(f"SESSION_SECRET={secrets.token_urlsafe(48)}")
print(f"PREMIUM_ACCESS_KEY={secrets.token_urlsafe(32)}")
print(f"TELEGRAM_WEBHOOK_SECRET={secrets.token_urlsafe(32)}")
print(f"DATA_ENCRYPTION_KEY={DataProtector.generate_key()}")
print(f"POSTGRES_PASSWORD={secrets.token_urlsafe(32)}")
