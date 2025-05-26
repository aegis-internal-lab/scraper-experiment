from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    """Database configuration"""

    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    url: str = Field(default="sqlite://db.sqlite3")


class LoggingConfig(BaseSettings):
    """Logging configuration"""

    model_config = SettingsConfigDict(env_prefix="LOGGING_")

    level: str = Field(default="INFO")
    file_name: str = Field(default="news_scraper.log")


class ScraperConfig(BaseSettings):
    """Scraper configuration"""

    model_config = SettingsConfigDict(env_prefix="SCRAPER_")

    interval_time: int = Field(default=5)
    max_results: int = Field(default=3)
    news_period: str = Field(default="7d")
    https_proxy: Optional[str] = Field(default=None)


class AIConfig(BaseSettings):
    """AI/Analysis configuration"""

    model_config = SettingsConfigDict(env_prefix="AI_")

    model: str = Field(default="gemini-2.0-flash")
    gemini_api_key: str = Field(default="", description="Gemini API key from environment")
    rc_analysis_prompt: Optional[str] = Field(default=None)
    sentiment_analysis_prompt: Optional[str] = Field(default=None)
    prominent_analysis_prompt: Optional[str] = Field(default=None)
    extracting_prompt: Optional[str] = Field(default=None)


class ServerConfig(BaseSettings):
    """Server configuration"""

    model_config = SettingsConfigDict(env_prefix="SERVER_")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=5000)
    reload: bool = Field(default=False)
    log_level: str = Field(default="info")


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database: DatabaseConfig = DatabaseConfig()
    logging: LoggingConfig = LoggingConfig()
    scraper: ScraperConfig = ScraperConfig()
    ai: AIConfig = AIConfig()
    server: ServerConfig = ServerConfig()


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
