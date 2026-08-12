from fastapi.testclient import TestClient
from app.main import app


def test_generate_with_mock_provider():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/generate",
            headers={"X-Client-Id": "pytest-user"},
            json={
                "mode": "write",
                "language": "ru",
                "relationship": "коллега",
                "goal": "поблагодарить",
                "tone": "warm",
                "output_format": "message",
                "length": "short",
                "context": "Хочу поблагодарить за помощь.",
                "source_text": "",
                "recipient_name": "",
                "address_form": "formal",
                "tier": "free",
                "accepted_terms": True,
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data["variants"]
    assert data["provider"] == "mock"
