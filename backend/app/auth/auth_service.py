from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.repositories.user_repository import create_user_record, get_user_by_email


def create_user(db: Session, name: str, email: str, password: str):
    existing_user = get_user_by_email(db, email)

    if existing_user:
        return None

    new_user = create_user_record(
        db=db,
        name=name,
        email=email,
        password_hash=hash_password(password)
    )

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "subscription_plan": user.subscription_plan
        }
    }
