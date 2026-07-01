from sqlalchemy.orm import Session

from app.models.user import User
from app.services import stage1_service


def generate_project_diagram(db: Session, project_id: int, user: User, diagram_type: str):
    """Generate Mermaid syntax for a project diagram."""
    return stage1_service.generate_diagram(db, project_id, user, diagram_type)
