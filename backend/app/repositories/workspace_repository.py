from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.workspace import (
    Note,
    Project,
    ProjectFile,
    ProjectMemory,
    Task,
    Workspace,
)


def paginate_query(db: Session, statement, limit: int, offset: int):
    total_statement = select(func.count()).select_from(statement.subquery())
    total = db.scalar(total_statement) or 0
    items = db.scalars(statement.limit(limit).offset(offset)).all()
    return items, total


def create_workspace(db: Session, owner_id: int, name: str, description: str | None):
    workspace = Workspace(owner_id=owner_id, name=name, description=description)
    db.add(workspace)
    return workspace


def list_workspaces(db: Session, owner_id: int, search: str | None, limit: int, offset: int):
    statement = select(Workspace).where(Workspace.owner_id == owner_id)
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(Workspace.name.ilike(pattern), Workspace.description.ilike(pattern))
        )
    statement = statement.order_by(Workspace.updated_at.desc(), Workspace.id.desc())
    return paginate_query(db, statement, limit, offset)


def get_workspace(db: Session, workspace_id: int, owner_id: int):
    return db.scalar(
        select(Workspace).where(
            Workspace.id == workspace_id,
            Workspace.owner_id == owner_id,
        )
    )


def create_project(
    db: Session,
    workspace_id: int,
    owner_id: int,
    title: str,
    description: str | None,
    status: str,
):
    project = Project(
        workspace_id=workspace_id,
        owner_id=owner_id,
        title=title,
        description=description,
        status=status,
    )
    db.add(project)
    return project


def list_projects(
    db: Session,
    owner_id: int,
    workspace_id: int | None,
    search: str | None,
    status: str | None,
    limit: int,
    offset: int,
):
    statement = select(Project).where(Project.owner_id == owner_id)
    if workspace_id is not None:
        statement = statement.where(Project.workspace_id == workspace_id)
    if status:
        statement = statement.where(Project.status == status)
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(Project.title.ilike(pattern), Project.description.ilike(pattern))
        )
    statement = statement.order_by(Project.updated_at.desc(), Project.id.desc())
    return paginate_query(db, statement, limit, offset)


def get_project(db: Session, project_id: int, owner_id: int):
    return db.scalar(
        select(Project).where(Project.id == project_id, Project.owner_id == owner_id)
    )


def create_task(db: Session, project_id: int, owner_id: int, **values):
    task = Task(project_id=project_id, owner_id=owner_id, **values)
    db.add(task)
    return task


def list_tasks(db: Session, project_id: int, owner_id: int, search, status, limit, offset):
    statement = select(Task).where(Task.project_id == project_id, Task.owner_id == owner_id)
    if status:
        statement = statement.where(Task.status == status)
    if search:
        pattern = f"%{search}%"
        statement = statement.where(or_(Task.title.ilike(pattern), Task.description.ilike(pattern)))
    statement = statement.order_by(Task.updated_at.desc(), Task.id.desc())
    return paginate_query(db, statement, limit, offset)


def get_task(db: Session, task_id: int, owner_id: int):
    return db.scalar(select(Task).where(Task.id == task_id, Task.owner_id == owner_id))


def create_note(db: Session, project_id: int, owner_id: int, **values):
    note = Note(project_id=project_id, owner_id=owner_id, **values)
    db.add(note)
    return note


def list_notes(db: Session, project_id: int, owner_id: int, search, limit, offset):
    statement = select(Note).where(Note.project_id == project_id, Note.owner_id == owner_id)
    if search:
        pattern = f"%{search}%"
        statement = statement.where(or_(Note.title.ilike(pattern), Note.content.ilike(pattern)))
    statement = statement.order_by(Note.updated_at.desc(), Note.id.desc())
    return paginate_query(db, statement, limit, offset)


def get_note(db: Session, note_id: int, owner_id: int):
    return db.scalar(select(Note).where(Note.id == note_id, Note.owner_id == owner_id))


def create_file(db: Session, project_id: int, owner_id: int, **values):
    file_record = ProjectFile(project_id=project_id, owner_id=owner_id, **values)
    db.add(file_record)
    return file_record


def list_files(db: Session, project_id: int, owner_id: int, search, file_type, limit, offset):
    statement = select(ProjectFile).where(
        ProjectFile.project_id == project_id,
        ProjectFile.owner_id == owner_id,
    )
    if file_type:
        statement = statement.where(ProjectFile.file_type == file_type)
    if search:
        statement = statement.where(ProjectFile.file_name.ilike(f"%{search}%"))
    statement = statement.order_by(ProjectFile.updated_at.desc(), ProjectFile.id.desc())
    return paginate_query(db, statement, limit, offset)


def get_file(db: Session, file_id: int, owner_id: int):
    return db.scalar(select(ProjectFile).where(ProjectFile.id == file_id, ProjectFile.owner_id == owner_id))


def create_memory(db: Session, project_id: int, owner_id: int, **values):
    memory = ProjectMemory(project_id=project_id, owner_id=owner_id, **values)
    db.add(memory)
    return memory


def list_memories(db: Session, project_id: int, owner_id: int, search, limit, offset):
    statement = select(ProjectMemory).where(
        ProjectMemory.project_id == project_id,
        ProjectMemory.owner_id == owner_id,
    )
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(ProjectMemory.key.ilike(pattern), ProjectMemory.value.ilike(pattern))
        )
    statement = statement.order_by(ProjectMemory.updated_at.desc(), ProjectMemory.id.desc())
    return paginate_query(db, statement, limit, offset)


def get_memory(db: Session, memory_id: int, owner_id: int):
    return db.scalar(
        select(ProjectMemory).where(
            ProjectMemory.id == memory_id,
            ProjectMemory.owner_id == owner_id,
        )
    )
