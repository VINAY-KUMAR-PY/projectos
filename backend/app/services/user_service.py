from sqlalchemy.orm import Session

from app.repositories.user_repository import (
    get_user_by_email,
    create_user_record
)
from app.auth.hashing import hash_password


def register_user(db: Session, name: str, email: str, password: str):
    existing_user = get_user_by_email(db, email)

    if existing_user:
        return None

    return create_user_record(
        db=db,
        name=name,
        email=email,
        password_hash=hash_password(password)
    )