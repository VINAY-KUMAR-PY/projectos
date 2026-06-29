from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.workspace_schema import (
    FileCreate,
    FileUpdate,
    MemoryCreate,
    MemoryUpdate,
    NoteCreate,
    NoteUpdate,
    ProjectCreate,
    ProjectUpdate,
    TaskCreate,
    TaskUpdate,
    WorkspaceCreate,
    WorkspaceUpdate,
)
from app.services import workspace_service as service

router = APIRouter(tags=["Project Workspace"])


def pagination_params(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return {"limit": limit, "offset": offset}


@router.post("/workspaces", status_code=status.HTTP_201_CREATED)
def create_workspace(
    request: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_workspace(db, current_user.id, request)


@router.get("/workspaces")
def list_workspaces(
    search: str | None = None,
    pagination: dict = Depends(pagination_params),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list_workspaces(db, current_user.id, search, **pagination)


@router.get("/workspaces/{workspace_id}")
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_workspace(db, workspace_id, current_user.id)


@router.patch("/workspaces/{workspace_id}")
def update_workspace(
    workspace_id: int,
    request: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.update_workspace(db, workspace_id, current_user.id, request)


@router.delete("/workspaces/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete_workspace(db, workspace_id, current_user.id)


@router.post("/workspaces/{workspace_id}/projects", status_code=status.HTTP_201_CREATED)
def create_project(
    workspace_id: int,
    request: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_project(db, workspace_id, current_user.id, request)


@router.get("/projects")
def list_projects(
    workspace_id: int | None = None,
    search: str | None = None,
    status: str | None = None,
    pagination: dict = Depends(pagination_params),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list_projects(
        db,
        current_user.id,
        workspace_id,
        search,
        status,
        **pagination,
    )


@router.get("/projects/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_project(db, project_id, current_user.id)


@router.patch("/projects/{project_id}")
def update_project(
    project_id: int,
    request: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.update_project(db, project_id, current_user.id, request)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete_project(db, project_id, current_user.id)


@router.post("/projects/{project_id}/tasks", status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, request: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.create_task(db, project_id, current_user.id, request)


@router.get("/projects/{project_id}/tasks")
def list_tasks(project_id: int, search: str | None = None, status: str | None = None, pagination: dict = Depends(pagination_params), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.list_tasks(db, project_id, current_user.id, search, status, **pagination)


@router.patch("/tasks/{task_id}")
def update_task(task_id: int, request: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.update_task(db, task_id, current_user.id, request)


@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_task(db, task_id, current_user.id)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service.delete_task(db, task_id, current_user.id)


@router.post("/projects/{project_id}/notes", status_code=status.HTTP_201_CREATED)
def create_note(project_id: int, request: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.create_note(db, project_id, current_user.id, request)


@router.get("/projects/{project_id}/notes")
def list_notes(project_id: int, search: str | None = None, pagination: dict = Depends(pagination_params), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.list_notes(db, project_id, current_user.id, search, **pagination)


@router.patch("/notes/{note_id}")
def update_note(note_id: int, request: NoteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.update_note(db, note_id, current_user.id, request)


@router.get("/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_note(db, note_id, current_user.id)


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service.delete_note(db, note_id, current_user.id)


@router.post("/projects/{project_id}/files", status_code=status.HTTP_201_CREATED)
def create_file(project_id: int, request: FileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.create_file(db, project_id, current_user.id, request)


@router.get("/projects/{project_id}/files")
def list_files(project_id: int, search: str | None = None, file_type: str | None = None, pagination: dict = Depends(pagination_params), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.list_files(db, project_id, current_user.id, search, file_type, **pagination)


@router.patch("/files/{file_id}")
def update_file(file_id: int, request: FileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.update_file(db, file_id, current_user.id, request)


@router.get("/files/{file_id}")
def get_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_file(db, file_id, current_user.id)


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service.delete_file(db, file_id, current_user.id)


@router.post("/projects/{project_id}/memory", status_code=status.HTTP_201_CREATED)
def create_memory(project_id: int, request: MemoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.create_memory(db, project_id, current_user.id, request)


@router.get("/projects/{project_id}/memory")
def list_memories(project_id: int, search: str | None = None, pagination: dict = Depends(pagination_params), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.list_memories(db, project_id, current_user.id, search, **pagination)


@router.patch("/memory/{memory_id}")
def update_memory(memory_id: int, request: MemoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.update_memory(db, memory_id, current_user.id, request)


@router.get("/memory/{memory_id}")
def get_memory(memory_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_memory(db, memory_id, current_user.id)


@router.delete("/memory/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(memory_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service.delete_memory(db, memory_id, current_user.id)
