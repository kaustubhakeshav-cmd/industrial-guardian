from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Industrial Guardian SCADA"
    API_V1_STR: str = "/api/v1"
    
    # Security parameters loaded from .env
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Database connection loaded from .env
    DATABASE_URL: str
    
    # Data Stream Settings loaded from .env
    DATASET_PATH: str
    REDIS_HOST: str
    REDIS_PORT: int
    USE_MOCK_STREAM: bool
    STREAM_FREQUENCY_HZ: float
    DEFAULT_ANOMALY_THRESHOLD: float
    CRITICAL_ANOMALY_THRESHOLD: float
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()