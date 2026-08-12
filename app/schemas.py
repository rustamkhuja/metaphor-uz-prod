from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, field_validator

Mode = Literal["write", "reply", "improve", "tone_check"]
Language = Literal["ru", "uz", "en"]
Length = Literal["short", "medium", "long"]
Tier = Literal["free", "premium"]


class GenerationRequest(BaseModel):
    mode: Mode = "write"
    language: Language = "ru"
    relationship: str = Field(default="", max_length=80)
    goal: str = Field(default="", max_length=100)
    tone: str = Field(default="warm", max_length=80)
    output_format: str = Field(default="message", max_length=80)
    length: Length = "medium"
    context: str = Field(default="", max_length=6000)
    source_text: str = Field(default="", max_length=6000)
    recipient_name: str = Field(default="", max_length=80)
    address_form: Literal["informal", "formal", "auto"] = "auto"
    source: Literal["web", "widget", "telegram", "api"] = "web"
    partner_code: str = Field(default="", max_length=40, pattern=r"^[A-Za-z0-9_-]*$")
    tier: Tier = "free"
    accepted_terms: bool = False

    @field_validator("context", "source_text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class Variant(BaseModel):
    label: str
    text: str


class GenerationResponse(BaseModel):
    generation_id: str
    variants: list[Variant]
    tone_notes: str = ""
    warnings: list[str] = Field(default_factory=list)
    safety_level: str = "low"
    provider: str
    model: str
    estimated_cost_usd: float = 0.0


class RefineRequest(BaseModel):
    instruction: Literal["shorter", "warmer", "firmer", "formal", "natural", "more_metaphorical"]
    selected_text: str = Field(min_length=1, max_length=6000)


class FeedbackRequest(BaseModel):
    generation_id: str
    rating: Literal[-1, 0, 1]
    reason: str = Field(default="", max_length=128)
    comment: str = Field(default="", max_length=1000)
    sent_or_copied: bool = False


class ContentApprovalRequest(BaseModel):
    approved: bool
    operator_note: str = Field(default="", max_length=1000)
