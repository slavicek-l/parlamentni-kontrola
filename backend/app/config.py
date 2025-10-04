from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    ENV: str = "dev"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = "app"
    POSTGRES_DB: str = "pkontrola"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    REDIS_URL: str = "redis://redis:6379/0"

    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"
    CELERY_BEAT_ENABLED: bool = True

    CORS_ORIGINS: str = "http://localhost:8080,http://localhost:5173"

    API_RATE_LIMIT_PER_MIN: int = 120
    API_AUTH_MODE: str = "none"  # none|apikey|jwt
    API_KEYS: str = "devkey1,devkey2"
    JWT_SECRET: str = "devsecret"
    JWT_ALG: str = "HS256"
    JWT_ACCESS_TTL: int = 3600

    PSP_DATA_BASE: str = "https://www.psp.cz/eknih/cdrom/opendata"
    ETL_DOWNLOAD_DIR: str = "/data/downloads"
    ETL_WORK_DIR: str = "/data/work"
    ETL_USER_AGENT: str = "ParlamentniKontrola/1.0"
    ETL_AUDIT_ALERT_THRESHOLD: float = 0.02

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
