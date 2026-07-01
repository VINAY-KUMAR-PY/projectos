from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.workspace_schema import TaskCreate, TaskUpdate
from app.services import workspace_service

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("/generate/{project_id}")
def generate_tasks(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workspace_service.get_project(db, project_id, current_user.id)
    return {"status": "success", "message": "Task generation is queued for the AI pipeline", "project_id": project_id}


@router.post("/{project_id}", status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, request: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workspace_service.create_task(db, project_id, current_user.id, request)


@router.get("/{project_id}")
def list_tasks(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), status: str | None = None, search: str | None = None, limit: int = 20, offset: int = 0):
    return workspace_service.list_tasks(db, project_id, current_user.id, search, status, limit, offset)


@router.put("/{task_id}")
def update_task(task_id: int, request: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workspace_service.update_task(db, task_id, current_user.id, request)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workspace_service.delete_task(db, task_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
