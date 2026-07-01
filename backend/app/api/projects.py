from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.platform_schema import ProjectApiCreate
from app.schemas.workspace_schema import ProjectUpdate, WorkspaceCreate
from app.services import workspace_service

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(request: ProjectApiCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workspace_id = request.workspace_id
    if workspace_id is None:
        workspace = workspace_service.create_workspace(
            db,
            current_user.id,
            WorkspaceCreate(name="Default Workspace", description="Auto-created workspace"),
        )
        workspace_id = workspace.id
    return workspace_service.create_project(db, workspace_id, current_user.id, request)


@router.get("")
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), search: str | None = None, status: str | None = None, limit: int = 20, offset: int = 0):
    return workspace_service.list_projects(db, current_user.id, None, search, status, limit, offset)


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workspace_service.get_project(db, project_id, current_user.id)


@router.put("/{project_id}")
def update_project(project_id: int, request: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workspace_service.update_project(db, project_id, current_user.id, request)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workspace_service.delete_project(db, project_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{project_id}/progress")
def get_project_progress(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = workspace_service.get_project(db, project_id, current_user.id)
    return {
        "project_id": project.id,
        "progress_score": project.progress_score or 0,
        "status": project.status,
        "completion_status": "complete" if (project.progress_score or 0) >= 100 else "in_progress",
    }
