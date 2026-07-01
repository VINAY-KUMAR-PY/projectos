from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.stage1_schema import TotpVerifyRequest
from app.services import stage1_service

router = APIRouter(prefix="/api/users/me", tags=["Security"])


@router.post("/2fa/enable")
def enable_2fa(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return stage1_service.enable_2fa(db, current_user)


@router.post("/2fa/verify")
def verify_2fa(
    request: TotpVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.verify_2fa(db, current_user, request.code)


@router.post("/2fa/disable")
def disable_2fa(
    request: TotpVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.disable_2fa(db, current_user, request.code)


@router.get("/export")
def export_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return stage1_service.export_user_data(db, current_user)


@router.delete("")
def delete_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return stage1_service.delete_user_data(db, current_user)
