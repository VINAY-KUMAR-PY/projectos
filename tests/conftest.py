import importlib
import sys
from pathlib import Path


BACKEND_PATH = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_PATH))


def fresh_app(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")

    for module_name in list(sys.modules):
        if module_name == "app" or module_name.startswith("app."):
            del sys.modules[module_name]

    server = importlib.import_module("app.api.server")
    return server.app


def auth_headers(client, email="user@example.com", password="StrongPass123"):
    client.post(
        "/auth/signup",
        json={"name": "Test User", "email": email, "password": password},
    )
    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
