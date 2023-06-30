from fastapi import APIRouter
from app.api.api_v1.endpoints import posts, images


api_v1_router = APIRouter()
api_v1_router.include_router(posts.router, prefix="/post", tags=["post"])
api_v1_router.include_router(images.router, prefix="/image", tags=["image"])