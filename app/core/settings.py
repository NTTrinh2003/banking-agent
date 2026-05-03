from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_host: str = "127.0.0.1"
    app_port: int = 8080
    app_reload: bool = True

    ollama_url: str = ""
    ollama_model: str = "gpt-oss:20b"
    ollama_timeout: int = 120

    intent_model_path: str = ""
    intent_confidence_threshold: float = 0.6

    min_draft_length: int = 30
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings():
    return Settings()