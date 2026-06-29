import pytest
from fastapi import HTTPException

from conftest import fresh_app


def test_workspace_service_not_found_raises_404(monkeypatch, tmp_path):
    fresh_app(monkeypatch, tmp_path)

    from app.services.workspace_service import get_workspace
    from app.database.connection import SessionLocal
    from app.database.init_db import init_db

    init_db()

    db = SessionLocal()
    try:
        with pytest.raises(HTTPException) as exc_info:
            get_workspace(db, workspace_id=999, owner_id=1)
    finally:
        db.close()

    assert exc_info.value.status_code == 404
