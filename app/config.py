from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    openai_api_key: str = ""
    anthropic_api_key: str = ""

    ollama_base_url: str = "http://localhost:11434"

    redis_url: str = "redis://localhost:6379"

    cache_similarity_threshold: float = 0.70

    embedding_model: str = "all-MiniLM-L6-v2"

    low_complexity_max_tokens: int = 200

    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        protected_namespaces=()
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()