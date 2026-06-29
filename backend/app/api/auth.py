from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/ping")
def ping():
    return {
        "status": "success",
        "message": "Authentication API is working"
    }