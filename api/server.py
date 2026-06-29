from fastapi import FastAPI
from config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)


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
