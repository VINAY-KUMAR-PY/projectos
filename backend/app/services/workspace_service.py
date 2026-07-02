from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.stage1 import TeamMember
from app.models.user import User
from app.models.workspace import Project
from app.repositories import workspace_repository as repo
from app.services import usage_service


def commit_and_refresh(db: Session, entity):
    db.commit()
    db.refresh(entity)
    return entity


def apply_updates(entity, values: dict):
    for field, value in values.items():
        if value is not None:
            setattr(entity, field, value)
    return entity


def not_found(resource: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found",
    )


def paginated(items, total: int, limit: int, offset: int):
    return {
        "items": items,
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
        },
    }


def create_workspace(db: Session, owner_id: int, data):
    workspace = repo.create_workspace(db, owner_id, data.name, data.description)
    return commit_and_refresh(db, workspace)


def list_workspaces(db: Session, owner_id: int, search: str | None, limit: int, offset: int):
    items, total = repo.list_workspaces(db, owner_id, search, limit, offset)
    return paginated(items, total, limit, offset)


def get_workspace(db: Session, workspace_id: int, owner_id: int):
    workspace = repo.get_workspace(db, workspace_id, owner_id)
    if not workspace:
        not_found("Workspace")
    return workspace


def update_workspace(db: Session, workspace_id: int, owner_id: int, data):
    workspace = get_workspace(db, workspace_id, owner_id)
    apply_updates(workspace, data.model_dump(exclude_unset=True))
    return commit_and_refresh(db, workspace)


def delete_workspace(db: Session, workspace_id: int, owner_id: int):
    workspace = get_workspace(db, workspace_id, owner_id)
    db.delete(workspace)
    db.commit()


def create_project(db: Session, workspace_id: int, owner_id: int, data):
    get_workspace(db, workspace_id, owner_id)
    user = db.get(User, owner_id)
    if user:
        usage_service.assert_project_limit(db, user)
    project = repo.create_project(
        db,
        workspace_id=workspace_id,
        owner_id=owner_id,
        title=data.title,
        description=data.description,
        status=data.status,
    )
    return commit_and_refresh(db, project)


def list_projects(db, owner_id, workspace_id, search, status, limit, offset):
    if workspace_id is not None:
        get_workspace(db, workspace_id, owner_id)
    items, total = repo.list_projects(
        db, owner_id, workspace_id, search, status, limit, offset
    )
    return paginated(items, total, limit, offset)


def get_project(db: Session, project_id: int, owner_id: int):
    project = repo.get_project(db, project_id, owner_id)
    if not project:
        project = db.scalar(
            select(Project)
            .join(TeamMember, TeamMember.project_id == Project.id)
            .where(
                Project.id == project_id,
                TeamMember.user_id == owner_id,
                TeamMember.status == "active",
            )
        )
    if not project:
        not_found("Project")
    return project


def get_owned_project(db: Session, project_id: int, owner_id: int):
    project = repo.get_project(db, project_id, owner_id)
    if not project:
        not_found("Project")
    return project


def update_project(db: Session, project_id: int, owner_id: int, data):
    project = get_owned_project(db, project_id, owner_id)
    apply_updates(project, data.model_dump(exclude_unset=True))
    return commit_and_refresh(db, project)


def delete_project(db: Session, project_id: int, owner_id: int):
    project = get_owned_project(db, project_id, owner_id)
    db.delete(project)
    db.commit()


def create_task(db, project_id, owner_id, data):
    get_owned_project(db, project_id, owner_id)
    task = repo.create_task(db, project_id, owner_id, **data.model_dump())
    return commit_and_refresh(db, task)


def list_tasks(db, project_id, owner_id, search, status, limit, offset):
    get_project(db, project_id, owner_id)
    items, total = repo.list_tasks(db, project_id, owner_id, search, status, limit, offset)
    return paginated(items, total, limit, offset)


def get_task(db, task_id, owner_id):
    task = repo.get_task(db, task_id, owner_id)
    if not task:
        not_found("Task")
    return task


def update_task(db, task_id, owner_id, data):
    task = get_task(db, task_id, owner_id)
    apply_updates(task, data.model_dump(exclude_unset=True))
    return commit_and_refresh(db, task)


def delete_task(db, task_id, owner_id):
    task = get_task(db, task_id, owner_id)
    db.delete(task)
    db.commit()


def create_note(db, project_id, owner_id, data):
    get_owned_project(db, project_id, owner_id)
    note = repo.create_note(db, project_id, owner_id, **data.model_dump())
    return commit_and_refresh(db, note)


def list_notes(db, project_id, owner_id, search, limit, offset):
    get_project(db, project_id, owner_id)
    items, total = repo.list_notes(db, project_id, owner_id, search, limit, offset)
    return paginated(items, total, limit, offset)


def get_note(db, note_id, owner_id):
    note = repo.get_note(db, note_id, owner_id)
    if not note:
        not_found("Note")
    return note


def update_note(db, note_id, owner_id, data):
    note = get_note(db, note_id, owner_id)
    apply_updates(note, data.model_dump(exclude_unset=True))
    return commit_and_refresh(db, note)


def delete_note(db, note_id, owner_id):
    note = get_note(db, note_id, owner_id)
    db.delete(note)
    db.commit()


def create_file(db, project_id, owner_id, data):
    get_owned_project(db, project_id, owner_id)
    file_record = repo.create_file(db, project_id, owner_id, **data.model_dump())
    return commit_and_refresh(db, file_record)


def list_files(db, project_id, owner_id, search, file_type, limit, offset):
    get_project(db, project_id, owner_id)
    items, total = repo.list_files(
        db, project_id, owner_id, search, file_type, limit, offset
    )
    return paginated(items, total, limit, offset)


def get_file(db, file_id, owner_id):
    file_record = repo.get_file(db, file_id, owner_id)
    if not file_record:
        not_found("File")
    return file_record


def update_file(db, file_id, owner_id, data):
    file_record = get_file(db, file_id, owner_id)
    apply_updates(file_record, data.model_dump(exclude_unset=True))
    return commit_and_refresh(db, file_record)


def delete_file(db, file_id, owner_id):
    file_record = get_file(db, file_id, owner_id)
    delete_owned_upload(file_record.storage_path)
    db.delete(file_record)
    db.commit()


def create_memory(db, project_id, owner_id, data):
    get_owned_project(db, project_id, owner_id)
    memory = repo.create_memory(db, project_id, owner_id, **data.model_dump())
    return commit_and_refresh(db, memory)


def list_memories(db, project_id, owner_id, search, limit, offset):
    get_project(db, project_id, owner_id)
    items, total = repo.list_memories(db, project_id, owner_id, search, limit, offset)
    return paginated(items, total, limit, offset)


def get_memory(db, memory_id, owner_id):
    memory = repo.get_memory(db, memory_id, owner_id)
    if not memory:
        not_found("Project memory")
    return memory


def update_memory(db, memory_id, owner_id, data):
    memory = get_memory(db, memory_id, owner_id)
    apply_updates(memory, data.model_dump(exclude_unset=True))
    return commit_and_refresh(db, memory)


def delete_memory(db, memory_id, owner_id):
    memory = get_memory(db, memory_id, owner_id)
    db.delete(memory)
    db.commit()


def delete_owned_upload(storage_path: str | None):
    if not storage_path:
        return
    upload_root = Path(settings.upload_dir).resolve()
    target = Path(storage_path).resolve()
    if upload_root == target or upload_root not in target.parents:
        return
    target.unlink(missing_ok=True)
