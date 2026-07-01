from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.stage1_schema import (
    ApprovalDecisionRequest,
    ApprovalRequestCreate,
    CommentCreateRequest,
    TaskAssignRequest,
    TeamInviteRequest,
)
from app.services import stage1_service

router = APIRouter(prefix="/api/collaboration", tags=["Collaboration"])


@router.post("/projects/{project_id}/members")
def invite_member(
    project_id: int,
    request: TeamInviteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.invite_member(db, project_id, current_user, request)


@router.get("/projects/{project_id}/members")
def list_members(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"items": stage1_service.list_members(db, project_id, current_user)}


@router.post("/projects/{project_id}/comments")
def add_comment(
    project_id: int,
    request: CommentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.add_comment(db, project_id, current_user, request)


@router.get("/projects/{project_id}/comments")
def list_comments(
    project_id: int,
    entity_type: str | None = None,
    entity_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {"items": stage1_service.list_comments(db, project_id, current_user, entity_type, entity_id)}


@router.post("/projects/{project_id}/task-assignments")
def assign_task(
    project_id: int,
    request: TaskAssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.assign_task(db, project_id, current_user, request)


@router.post("/projects/{project_id}/approvals")
def request_approval(
    project_id: int,
    request: ApprovalRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.create_approval(db, project_id, current_user, request)


@router.post("/approvals/{approval_id}/decision")
def decide_approval(
    approval_id: int,
    request: ApprovalDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.decide_approval(db, approval_id, current_user, request)
