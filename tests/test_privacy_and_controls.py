from fastapi.testclient import TestClient

from app.config import Settings
from app.db import SessionLocal
from app.main import app
from app.models import Generation


def payload(**overrides):
    value = {
        "mode": "write",
        "language": "ru",
        "relationship": "friend",
        "goal": "apologize",
        "tone": "calm",
        "output_format": "message",
        "length": "short",
        "context": "Мы резко поговорили. Хочу спокойно извиниться.",
        "source_text": "",
        "recipient_name": "",
        "address_form": "informal",
        "source": "web",
        "partner_code": "",
        "tier": "free",
        "accepted_terms": True,
    }
    value.update(overrides)
    return value


def test_premium_is_fail_closed_by_default():
    with TestClient(app) as client:
        response = client.post("/api/v1/generate", json=payload(tier="premium"))
    assert response.status_code == 403


def test_default_mode_does_not_store_user_text_or_output():
    with TestClient(app) as client:
        response = client.post("/api/v1/generate", json=payload())
        assert response.status_code == 200
        generation_id = response.json()["generation_id"]
    with SessionLocal() as db:
        record = db.get(Generation, generation_id)
        assert record is not None
        assert record.input_redacted == ""
        assert record.input_encrypted is None
        assert record.output_json == {}
        assert record.input_length > 0


def test_feedback_must_belong_to_current_session():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/feedback",
            json={
                "generation_id": "00000000-0000-0000-0000-000000000000",
                "rating": 1,
                "reason": "test",
                "comment": "",
                "sent_or_copied": False,
            },
        )
    assert response.status_code == 404


def test_production_configuration_fails_closed():
    settings = Settings(app_env="production")
    try:
        settings.validate_for_startup()
    except RuntimeError as exc:
        assert "Unsafe production configuration" in str(exc)
    else:
        raise AssertionError("unsafe production defaults must not be accepted")


def test_copy_event_does_not_count_as_positive_or_overwrite_explicit_rating():
    from app.models import Feedback

    with TestClient(app) as client:
        generated = client.post("/api/v1/generate", json=payload())
        assert generated.status_code == 200
        generation_id = generated.json()["generation_id"]

        copied = client.post(
            "/api/v1/feedback",
            json={
                "generation_id": generation_id,
                "rating": 0,
                "reason": "copied",
                "comment": "",
                "sent_or_copied": True,
            },
        )
        assert copied.status_code == 200

        explicit = client.post(
            "/api/v1/feedback",
            json={
                "generation_id": generation_id,
                "rating": -1,
                "reason": "explicit",
                "comment": "",
                "sent_or_copied": False,
            },
        )
        assert explicit.status_code == 200

        copied_again = client.post(
            "/api/v1/feedback",
            json={
                "generation_id": generation_id,
                "rating": 0,
                "reason": "copied",
                "comment": "",
                "sent_or_copied": True,
            },
        )
        assert copied_again.status_code == 200

    with SessionLocal() as db:
        record = db.query(Feedback).filter(Feedback.generation_id == generation_id).one()
        assert record.rating == -1
        assert record.sent_or_copied is True
