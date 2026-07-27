import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        
        # Bind the request ID to this execution context for logs
        log = logger.bind(request_id=request_id)
        
        start_time = time.perf_counter()
        
        try:
            response = await call_next(request)
            process_time = (time.perf_counter() - start_time) * 1000
            
            log.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=round(process_time, 2),
            )
            return response
        except Exception as e:
            process_time = (time.perf_counter() - start_time) * 1000
            log.error(
                "request_failed",
                method=request.method,
                path=request.url.path,
                duration_ms=round(process_time, 2),
                error=str(e),
                exc_info=True
            )
            raise e
