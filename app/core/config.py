"""Application settings for the MVP."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Static settings used by the local MVP application."""

    app_name: str = "ADAPTY InBody Intelligence System"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./adapty_inbody.db"


settings = Settings()
