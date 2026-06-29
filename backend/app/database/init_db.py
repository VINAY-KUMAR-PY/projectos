from app.database.connection import engine, Base
from app.database import models
from app.models import user


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")