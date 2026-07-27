from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.exceptions import PredictionError, FeatureEngineeringError, ModelLoadError

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(PredictionError)
async def prediction_error_handler(request: Request, exc: PredictionError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

@app.exception_handler(FeatureEngineeringError)
async def feature_engineering_error_handler(request: Request, exc: FeatureEngineeringError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})

@app.exception_handler(ModelLoadError)
async def model_load_error_handler(request: Request, exc: ModelLoadError):
    return JSONResponse(status_code=503, content={"detail": str(exc)})

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def home():
    return {"message": f"{settings.PROJECT_NAME} is running"}
