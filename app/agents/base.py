from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.services.ai_budget import ensure_budget_available, record_llm_usage
from app.services.llm import LLMResult, LLMRouter


@dataclass
class AgentResult:
    success: bool
    data: dict[str, Any]
    requires_human: bool = False
    reason: str = ""


class BaseAgent(ABC):
    name: str = "base"

    def __init__(self, db: Session, settings: Settings | None = None):
        self.db = db
        self.settings = settings or get_settings()
        self.llm = LLMRouter(self.settings)

    async def generate_ai(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        purpose: str,
        web_search: bool = False,
        json_mode: bool = True,
    ) -> LLMResult:
        ensure_budget_available(self.db, self.settings)
        result = await self.llm.generate(
            system_prompt,
            user_prompt,
            web_search=web_search,
            json_mode=json_mode,
        )
        record_llm_usage(self.db, result, purpose, metadata={"agent": self.name})
        return result

    @abstractmethod
    async def run(self, payload: dict[str, Any]) -> AgentResult:
        raise NotImplementedError
