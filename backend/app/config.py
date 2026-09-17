"""Application configuration (12-factor, env-driven with sane dev defaults)."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="EASEUR_", extra="ignore")

    app_name: str = "Easeur Exercise Knowledge Base"
    environment: str = "development"
    database_url: str = "postgresql+psycopg2://easeur:easeur@127.0.0.1:5432/easeur"

    # Admin API key for protected (review/admin) endpoints. Rotate in production.
    admin_api_key: str = "dev-admin-key"

    # CORS origins for the research UI (Next.js dev server).
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # ---- Crawler policy ----
    crawler_user_agent: str = (
        "EaseurExerciseBot/0.1 (+https://workout.easeur.com/bot; "
        "research aggregation crawler; contact=dev@easeur.com)"
    )
    crawler_min_delay_seconds: float = 3.0   # per-domain politeness delay
    crawler_max_concurrency: int = 4
    crawler_timeout_seconds: float = 20.0
    crawler_max_redirects: int = 3
    crawler_max_pages_per_job: int = 60
    crawler_max_depth: int = 2
    crawler_cache_dir: str = ".crawl_cache"
    crawler_cache_ttl_seconds: int = 86400

    # ---- Selective AI enrichment (optional; disabled unless configured) ----
    ai_api_base: str | None = None          # OpenAI-compatible endpoint
    ai_api_key: str | None = None
    ai_model: str = "gpt-4o-mini"
    ai_prompt_version: str = "2026-09-v1"
    ai_max_candidates_per_run: int = 25     # hard cap: AI is enrichment, not the default parser

    # Review auto-queue thresholds
    low_confidence_threshold: float = 0.55
    high_confidence_threshold: float = 0.85
    duplicate_auto_merge_threshold: float = 0.99  # only near-exact matches auto-merge

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
