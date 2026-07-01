from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.ai import router as ai_router
from app.api.agents import router as agents_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.errors import http_exception_handler, validation_exception_handler
from app.api.files import router as files_router
from app.api.outputs import router as outputs_router
from app.api.projects import router as projects_router
from app.api.subscriptions import router as subscriptions_router
from app.api.tasks import router as tasks_router
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
    docs_url="/docs",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(auth_router)
app.include_router(auth_router, prefix="/api")
app.include_router(workspace_router)
app.include_router(workspace_router, prefix="/api")
app.include_router(ai_router)
app.include_router(ai_router, prefix="/api")
app.include_router(projects_router)
app.include_router(agents_router)
app.include_router(files_router)
app.include_router(outputs_router)
app.include_router(tasks_router)
app.include_router(subscriptions_router)
app.include_router(dashboard_router)

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
