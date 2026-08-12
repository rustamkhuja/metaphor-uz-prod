from __future__ import annotations

import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DB_PATH = ROOT / "smoke_metaphor.db"
DB_PATH.unlink(missing_ok=True)

# Isolated smoke test: never touches a developer or production database.
os.environ["APP_ENV"] = "test"
os.environ["LLM_PRIMARY_PROVIDER"] = "mock"
os.environ["DATABASE_URL"] = f"sqlite:///{DB_PATH}"
os.environ["FREE_DAILY_LIMIT"] = "100"

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402

payload = {
    "mode": "write",
    "language": "ru",
    "relationship": "друг",
    "goal": "извиниться",
    "tone": "спокойный",
    "output_format": "message",
    "length": "short",
    "context": "Мы поссорились. Хочу извиниться без пафоса.",
    "source_text": "",
    "recipient_name": "",
    "address_form": "informal",
    "tier": "free",
    "accepted_terms": True,
}

try:
    with TestClient(app) as client:
        health = client.get("/api/v1/health")
        assert health.status_code == 200, health.text
        response = client.post("/api/v1/generate", json=payload)
        assert response.status_code == 200, response.text
        assert response.json()["variants"], response.text
        assert client.cookies.get("metaphor_session")
        print("Smoke test passed:", response.json()["variants"][0]["text"])
finally:
    DB_PATH.unlink(missing_ok=True)
