from sqlalchemy.orm import Session

from app.models.user import User
from app.services import stage1_service


def generate_project_document(db: Session, project_id: int, user: User):
    """Generate and persist a downloadable project report."""
    return stage1_service.generate_document(db, project_id, user)
