from sqlalchemy.orm import Session

from app.models.user import User
from app.services import stage1_service


def generate_project_ppt(db: Session, project_id: int, user: User):
    """Generate and persist a downloadable project presentation."""
    return stage1_service.generate_ppt(db, project_id, user)
