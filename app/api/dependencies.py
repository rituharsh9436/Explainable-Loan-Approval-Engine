from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError

from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.token import TokenPayload
from app.models.user import User
from app.repositories.user_repo import user as user_repo
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

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = user_repo.get(db, id=int(token_data.sub))
    if not user:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
