from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.config.settings import settings
from app.api.ai import router as ai_router
from app.api.auth import router as auth_router
from app.api.errors import http_exception_handler, validation_exception_handler
from app.api.workspaces import router as workspace_router
from app.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.auto_create_tables:
        init_db()
    yield

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(auth_router)
app.include_router(workspace_router)
app.include_router(ai_router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "ProjectOS API is running",
        "version": settings.app_version,
        "environment": settings.environment
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name
    }
