from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_name: str = "Metaphor AI OS"
    public_base_url: str = "http://localhost:8000"
    database_url: str = "sqlite:///./metaphor.db"
    timezone: str = "Asia/Tashkent"
    log_level: str = "INFO"

    llm_primary_provider: str = "mock"
    llm_primary_base_url: str = "https://api.x.ai/v1"
    llm_primary_api_key: str = ""
    llm_primary_model: str = "grok-4.3"
    llm_primary_input_usd_per_m: float = 1.25
    llm_primary_output_usd_per_m: float = 2.50

    llm_secondary_provider: str = ""
    llm_secondary_base_url: str = ""
    llm_secondary_api_key: str = ""
    llm_secondary_model: str = ""
    llm_secondary_input_usd_per_m: float = 0.0
    llm_secondary_output_usd_per_m: float = 0.0
    llm_timeout_seconds: int = 60
    llm_max_output_tokens: int = 1200
    llm_enable_web_search: bool = False
    llm_json_mode: bool = True
    llm_reasoning_effort: str = "low"
    llm_prompt_cache_key: str = "metaphor-v1"

    free_daily_limit: int = 3
    daily_ai_budget_usd: float = 3.0
    max_input_characters: int = 6000
    premium_variants: int = 3

    # Privacy-by-default: product inputs and generated messages are not persisted.
    store_raw_input: bool = False
    store_redacted_input: bool = False
    store_generated_output: bool = False
    raw_input_retention_hours: int = 24
    output_retention_hours: int = 168
    data_encryption_key: str = ""
    privacy_policy_version: str = "2026-08-draft"
    terms_version: str = "2026-08-draft"
    legal_launch_approved: bool = False

    admin_api_key: str = "change-me-before-production"
    session_secret: str = "change-me-with-generated-secret"
    enable_premium_pilot: bool = False
    premium_access_key: str = ""
    auto_approve_low_risk_content: bool = False
    auto_publish_telegram: bool = False
    daily_content_hour: int = 9
    weekly_review_weekday: int = 1

    telegram_bot_token: str = ""
    telegram_bot_username: str = ""
    telegram_channel_id: str = ""
    telegram_operator_chat_id: str = ""
    telegram_webhook_secret: str = ""

    # Optional low-cost narration for generated vertical videos.
    xai_tts_enabled: bool = False
    xai_tts_base_url: str = "https://api.x.ai/v1"
    xai_tts_voice_id: str = "carina"
    xai_tts_usd_per_m_characters: float = 15.0

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    def validate_for_startup(self) -> None:
        """Fail closed instead of starting production with public/default secrets."""
        if not self.is_production:
            return
        errors: list[str] = []
        if not self.public_base_url.startswith("https://"):
            errors.append("PUBLIC_BASE_URL must use HTTPS")
        if self.database_url.startswith("sqlite"):
            errors.append("production DATABASE_URL must use PostgreSQL")
        if self.llm_primary_provider == "mock":
            errors.append("LLM_PRIMARY_PROVIDER cannot be mock in production")
        if self.llm_primary_provider != "mock" and not self.llm_primary_api_key:
            errors.append("LLM_PRIMARY_API_KEY is required")
        if len(self.session_secret) < 32 or self.session_secret.startswith("change-me"):
            errors.append("SESSION_SECRET must be a generated secret of at least 32 characters")
        if len(self.admin_api_key) < 24 or self.admin_api_key.startswith("change-me"):
            errors.append("ADMIN_API_KEY must be a generated secret of at least 24 characters")
        if self.enable_premium_pilot and len(self.premium_access_key) < 24:
            errors.append("PREMIUM_ACCESS_KEY is required when ENABLE_PREMIUM_PILOT=true")
        if self.telegram_bot_token and len(self.telegram_webhook_secret) < 24:
            errors.append("TELEGRAM_WEBHOOK_SECRET is required when Telegram bot is enabled")
        if self.store_raw_input and not self.data_encryption_key:
            errors.append("DATA_ENCRYPTION_KEY is required when STORE_RAW_INPUT=true")
        if not self.legal_launch_approved:
            errors.append("LEGAL_LAUNCH_APPROVED must be true after legal review")
        if "draft" in self.privacy_policy_version.lower() or "draft" in self.terms_version.lower():
            errors.append("PRIVACY_POLICY_VERSION and TERMS_VERSION must be final versions")
        if errors:
            raise RuntimeError("Unsafe production configuration: " + "; ".join(errors))


@lru_cache
def get_settings() -> Settings:
    return Settings()
