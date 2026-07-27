from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Explainable Loan Approval Engine"
    API_V1_STR: str = "/api/v1"
    
    # CORS setup
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"
    
    # ML settings
    APPROVAL_THRESHOLD: float = 0.65

    # Database settings
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./loan_engine.db"

    # JWT Auth settings
    SECRET_KEY: str = "supersecretkey_please_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
