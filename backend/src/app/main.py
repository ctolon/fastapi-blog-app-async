"""App entry point."""""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.api_v1.api import api_v1_router
from app.api.api_static.api import api_static_router

from app.core.config import settings
from app.core.middleware import middleware_builder

# Set all CORS enabled origins
middleware = None
if settings.BACKEND_CORS_ORIGINS:
    middleware = middleware_builder(settings.BACKEND_CORS_ORIGINS)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.0.1",
    openapi_url=settings.OPENAPI_URL,
    description='Blog app',
    debug=False,
    middleware=middleware
)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)
app.include_router(api_static_router, prefix="/api/static")

app.mount(
    '/api/static/images',
    StaticFiles(directory=settings.MEDIA_DIR.as_posix()),
    name='images'
    )