from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.stage1_schema import (
    CodeBuildRequest,
    DeploymentGenerateRequest,
    DiagramGenerateRequest,
    ReviewRequest,
)
from app.services import stage1_service

router = APIRouter(prefix="/api/projects", tags=["Stage 1 Generation"])


@router.post("/{project_id}/generate-document")
def generate_document(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return stage1_service.generate_document(db, project_id, current_user)


@router.post("/{project_id}/generate-ppt")
def generate_ppt(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return stage1_service.generate_ppt(db, project_id, current_user)


@router.post("/{project_id}/generate-diagram")
def generate_diagram(
    project_id: int,
    diagram_type: str = Query(alias="type", pattern="^(usecase|er|class|sequence|flowchart|architecture|schema|gantt)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    request = DiagramGenerateRequest(diagram_type=diagram_type)
    return stage1_service.generate_diagram(db, project_id, current_user, request.diagram_type)


@router.post("/{project_id}/build-code")
def build_code(
    project_id: int,
    request: CodeBuildRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.build_code(db, project_id, current_user, request)


@router.post("/{project_id}/review")
def review_project(
    project_id: int,
    request: ReviewRequest | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.review_project(db, project_id, current_user, request or ReviewRequest())


@router.post("/{project_id}/generate-deployment")
def generate_deployment(
    project_id: int,
    target: str = Query(pattern="^(vercel|netlify|railway|render|aws|docker|github-pages)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    request = DeploymentGenerateRequest(target=target)
    return stage1_service.generate_deployment(db, project_id, current_user, request)
