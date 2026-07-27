from typing import Generator
from app.db.session import SessionLocal
from app.services.model_repository import ModelRepository
from app.services.prediction_service import PredictionService

# Singleton repository instantiation
_model_repository = ModelRepository()

def get_prediction_service() -> PredictionService:
    """
    Dependency injection provider for PredictionService.
    Allows easy mocking of the service during unit tests.
    """
    return PredictionService(model_repo=_model_repository)

def get_db() -> Generator:
    """
    Dependency to get a database session.
    Closes the session automatically after the request.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
