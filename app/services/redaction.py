from __future__ import annotations

import base64
import hashlib
import re
from cryptography.fernet import Fernet, InvalidToken


PHONE = re.compile(r"(?<!\d)(?:\+?998[\s-]?)?(?:\d[\s-]?){9}(?!\d)")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
CARD = re.compile(r"(?<!\d)(?:\d[ -]?){16}(?!\d)")
URL = re.compile(r"https?://\S+", re.I)


def redact(text: str) -> str:
    value = text or ""
    value = EMAIL.sub("[EMAIL]", value)
    value = PHONE.sub("[PHONE]", value)
    value = CARD.sub("[CARD]", value)
    value = URL.sub("[URL]", value)
    return value


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class DataProtector:
    def __init__(self, key: str):
        self._fernet = Fernet(key.encode("utf-8")) if key else None

    @staticmethod
    def generate_key() -> str:
        return Fernet.generate_key().decode("utf-8")

    def encrypt(self, value: str) -> str | None:
        if not self._fernet or not value:
            return None
        return self._fernet.encrypt(value.encode("utf-8")).decode("utf-8")

    def decrypt(self, token: str | None) -> str | None:
        if not self._fernet or not token:
            return None
        try:
            return self._fernet.decrypt(token.encode("utf-8")).decode("utf-8")
        except InvalidToken:
            return None
