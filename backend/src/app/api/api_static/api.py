from fastapi import APIRouter
from app.api.api_static.endpoints import static


api_static_router = APIRouter()
api_static_router.include_router(static.router, tags=["static"])