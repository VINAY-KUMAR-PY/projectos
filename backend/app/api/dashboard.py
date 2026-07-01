from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.ai import AgentRun
from app.models.user import User
from app.models.workspace import Project, ProjectFile, Task

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("")
def dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_projects = db.scalar(select(func.count()).select_from(Project).where(Project.owner_id == current_user.id)) or 0
    agent_runs = db.scalar(select(func.count()).select_from(AgentRun).where(AgentRun.owner_id == current_user.id)) or 0
    files = db.scalar(select(func.count()).select_from(ProjectFile).where(ProjectFile.owner_id == current_user.id)) or 0
    completed_tasks = db.scalar(
        select(func.count()).select_from(Task).where(Task.owner_id == current_user.id, Task.status == "done")
    ) or 0
    recent_projects = db.scalars(
        select(Project).where(Project.owner_id == current_user.id).order_by(Project.updated_at.desc()).limit(5)
    ).all()
    return {
        "stats": {
            "total_projects": total_projects,
            "agent_runs": agent_runs,
            "files_uploaded": files,
            "tasks_completed": completed_tasks,
            "subscription_plan": current_user.subscription_plan,
        },
        "recent_projects": recent_projects,
    }
