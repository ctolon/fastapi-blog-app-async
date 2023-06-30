"""Base middleware for the application."""
from typing import List

# FastAPI middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

# Starlette middleware
# from starlette.middleware.cors import CORSMiddleware
# from starlette.middleware import Middleware

from app.core.config import settings
    
def middleware_builder(
    middleware_list: List[str] = settings.BACKEND_CORS_ORIGINS
    ) -> List[Middleware]:
    """Builds a middleware stack."""
    
    middleware = []
    if middleware_list:
        middleware.append(
            Middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in middleware_list],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
                expose_headers=["*"]
            )
        )
    return middleware