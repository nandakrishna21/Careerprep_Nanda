from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _env_file() -> str:
    """Locate `.env` regardless of the working directory uvicorn was started from."""
    for candidate in (_PROJECT_ROOT / ".env", _PROJECT_ROOT / "backend" / ".env", Path.cwd() / ".env"):
        if candidate.is_file():
            return str(candidate)
    return str(_PROJECT_ROOT / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_env_file(), env_file_encoding="utf-8", extra="ignore")

    app_name: str = "CareerPrep Hub"
    environment: str = "development"

    database_url: str = "sqlite:///./careerprep.db"

    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    apify_token: str = ""
    apify_max_items: int = 25
    apify_run_timeout_seconds: int = 420

    admin_email: str = "admin@careerprep.com"
    admin_password: str = "Admin@12345"

    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "noreply@careerprep.local"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
