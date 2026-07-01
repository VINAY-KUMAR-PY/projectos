from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.auth.auth_service import create_user, authenticate_user
from app.auth.dependencies import get_current_user
from app.repositories.user_repository import get_user_by_email
from app.services.stage1_service import log_audit

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

    log_audit(db, user.id, "auth.signup", "user", user.id)
    db.commit()

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


@router.post("/register")
def register(request: UserCreate, db: Session = Depends(get_db)):
    return signup(request, db)


@router.post("/login")
def login(request: UserLogin, db: Session = Depends(get_db)):
    result = authenticate_user(
        db=db,
        email=request.email,
        password=request.password
    )

    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = get_user_by_email(db, request.email)
    log_audit(db, user.id if user else None, "auth.login", "user", user.id if user else None)
    db.commit()

    return {
        "status": "success",
        "message": "Login successful",
        "data": result
    }


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
