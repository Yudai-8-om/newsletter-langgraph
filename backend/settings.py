from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import ValidationError

class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=Path(__file__).parent.parent / '.env')
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    LLM_MODEL_LIGHT: str = "gemma3n:e4b"
    LLM_MODEL: str = "qwen3:8b-q4_K_M"
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "qwen/qwen3-235b-a22b:free"
    NEWS_API_KEY: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL_NO_DOCKER: str
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@postgres_db:5432/{self.POSTGRES_DB}"

try:
    settings = Settings()
except ValidationError as e:
    print(f"Settings error: {e}")
