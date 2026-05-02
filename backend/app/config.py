import os

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_DEFAULT_DB = os.path.join(_BACKEND_ROOT, "data", "risk_intel.db")
os.makedirs(os.path.dirname(_DEFAULT_DB), exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = f"sqlite:///{_DEFAULT_DB.replace(os.sep, '/')}"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    reliefweb_rss_url: str = "https://reliefweb.int/updates/rss.xml"
    scheduler_enabled: bool = True
    jwt_secret: str = "dev-CHANGE-ME-use-long-random-string-in-production"
    jwt_expire_minutes: int = 60 * 24 * 7
    demo_upgrade_secret: str = ""


settings = Settings()
