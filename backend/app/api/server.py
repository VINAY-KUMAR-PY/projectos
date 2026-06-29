from fastapi import FastAPI
from app.config.settings import settings
from app.api.auth import router as auth_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)
app.include_router(auth_router)

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
