from fastapi import APIRouter
from app.api.v1.endpoints import predictions

api_router = APIRouter()
api_router.include_router(predictions.router, tags=["predictions"])
