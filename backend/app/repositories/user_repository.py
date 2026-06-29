from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.scalar(select(User).where(User.email == email.lower()))


def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)


def create_user_record(db: Session, name: str, email: str, password_hash: str):
    user = User(
        name=name,
        email=email.lower(),
        password_hash=password_hash
    )

    db.add(user)
    return user
