from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "AI Language Learning Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str
    REDIS_CACHE_TTL: int = 3600

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 2000

    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None

    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "uploads"

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Logging
    LOG_LEVEL: str = "INFO"

    # Spaced Repetition Settings
    FLASHCARD_NEW_CARDS_PER_DAY: int = 20
    FLASHCARD_REVIEW_CARDS_PER_DAY: int = 100

    # Gamification
    XP_PER_FLASHCARD: int = 5
    XP_PER_EXERCISE: int = 10
    XP_PER_SPEAKING_SESSION: int = 20
    XP_PER_READING: int = 15
    XP_PER_WRITING: int = 25

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
