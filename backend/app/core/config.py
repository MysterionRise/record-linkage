"""Application configuration."""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Record Linkage API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "ML-powered record linkage with explainability"

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://localhost:8000",
    ]

    # Model Settings
    MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    MODEL_PATH: str = "./models_saved"
    SIMILARITY_THRESHOLD: float = 0.75

    # Data Settings
    DATA_DIR: str = "./data"
    RAW_DATA_DIR: str = "./data/raw"
    PROCESSED_DATA_DIR: str = "./data/processed"

    # ML Settings
    MAX_SEQ_LENGTH: int = 128
    BATCH_SIZE: int = 32
    DEVICE: str = "cpu"  # Will auto-detect CUDA if available

    # Explainability Settings
    SHAP_MAX_SAMPLES: int = 100
    LIME_NUM_FEATURES: int = 10

    class Config:
        """Pydantic config."""

        case_sensitive = True
        env_file = ".env"


settings = Settings()
