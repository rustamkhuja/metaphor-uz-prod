from __future__ import annotations

import base64
import hashlib
import hmac
import secrets


def _sign(value: str, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), value.encode("utf-8"), hashlib.sha256).hexdigest()


def create_session_token(secret: str) -> tuple[str, str]:
    session_id = secrets.token_urlsafe(24)
    signature = _sign(session_id, secret)
    token = base64.urlsafe_b64encode(f"{session_id}.{signature}".encode("utf-8")).decode("ascii")
    return token, session_id


def verify_session_token(token: str | None, secret: str) -> str | None:
    if not token or not secret:
        return None
    try:
        decoded = base64.urlsafe_b64decode(token.encode("ascii")).decode("utf-8")
        session_id, signature = decoded.rsplit(".", 1)
    except Exception:
        return None
    expected = _sign(session_id, secret)
    return session_id if hmac.compare_digest(signature, expected) else None
