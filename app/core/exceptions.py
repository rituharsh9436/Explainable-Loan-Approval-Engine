from fastapi import HTTPException, status

class ModelLoadError(Exception):
    """Raised when an ML model fails to load from disk."""
    pass

class FeatureEngineeringError(Exception):
    """Raised when input data cannot be transformed into model features."""
    pass

class PredictionError(Exception):
    """Raised when the ML model fails to generate a prediction."""
    pass

# FastAPI specific exceptions
def get_validation_exception(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

def get_server_exception(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
