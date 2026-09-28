from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(min_length=1)
    app_env: str = Field(min_length=1)

    database_url: str = Field(min_length=1)
    document_storage_path: str = Field(min_length=1)
    chroma_path: str = Field(min_length=1)

    llm_model_path: str | None = None
    embedding_model_path: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()