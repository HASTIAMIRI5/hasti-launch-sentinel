import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    app_title: str = "Hasti Launch Sentinel"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    jwt_secret: str = "dev-secret-change-me"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    database_url: str = "sqlite:///./data/hasti.db"
    redis_url: str = "redis://localhost:6379/0"
    slack_webhook_url: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    admin_email: Optional[str] = None


def get_settings() -> Settings:
    return Settings(
        app_title=os.getenv("APP_TITLE", "Hasti Launch Sentinel"),
        app_env=os.getenv("APP_ENV", "development"),
        app_host=os.getenv("APP_HOST", "0.0.0.0"),
        app_port=int(os.getenv("APP_PORT", "8000")),
        jwt_secret=os.getenv("JWT_SECRET", "dev-secret-change-me"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./data/hasti.db"),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
        smtp_host=os.getenv("SMTP_HOST"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_user=os.getenv("SMTP_USER"),
        smtp_password=os.getenv("SMTP_PASSWORD"),
        admin_email=os.getenv("ADMIN_EMAIL"),
    )
