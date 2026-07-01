from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.stage1_schema import LearningRequest
from app.services import stage1_service

router = APIRouter(prefix="/api/agents/learning", tags=["Learning Mode"])


@router.post("/{action}")
def learning_action(
    action: str,
    request: LearningRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.run_learning_action(db, action, current_user, request)
