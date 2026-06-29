from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user_schema import UserCreate, UserLogin
from app.auth.auth_service import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
def signup(request: UserCreate, db: Session = Depends(get_db)):
    user = create_user(
        db=db,
        name=request.name,
        email=request.email,
        password=request.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return {
        "status": "success",
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "subscription_plan": user.subscription_plan
        }
    }


@router.post("/login")
def login(request: UserLogin, db: Session = Depends(get_db)):
    result = authenticate_user(
        db=db,
        email=request.email,
        password=request.password
    )

    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "status": "success",
        "message": "Login successful",
        "data": result
    }