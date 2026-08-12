from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class SafetyResult:
    level: str
    blocked: bool
    message: str = ""


SELF_HARM = [
    r"\b(хочу|собираюсь)\s+(умереть|покончить с собой)\b",
    r"\bубью себя\b",
    r"\b(o'zimni|oʻzimni)\s+o'ldir",
    r"\bi want to (die|kill myself)\b",
]
THREAT = [
    r"\bя тебя убью\b",
    r"\bубить его\b",
    r"\bseni o'ldiraman\b",
    r"\bi will kill (you|him|her)\b",
]


def classify(text: str) -> SafetyResult:
    normalized = (text or "").lower()
    if any(re.search(p, normalized, flags=re.I) for p in SELF_HARM):
        return SafetyResult(
            level="critical",
            blocked=True,
            message=(
                "Я не буду составлять сообщение, которое помогает причинить вред. "
                "Если опасность непосредственная, свяжитесь с местной экстренной службой или человеком, которому доверяете, и не оставайтесь один." 
            ),
        )
    if any(re.search(p, normalized, flags=re.I) for p in THREAT):
        return SafetyResult(
            level="high",
            blocked=True,
            message="Я не буду усиливать угрозу. Можно сформулировать твёрдую границу без угроз и насилия.",
        )
    return SafetyResult(level="low", blocked=False)
