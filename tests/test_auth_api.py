from fastapi.testclient import TestClient

from conftest import fresh_app


def test_auth_signup_login_me_and_duplicate_email(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        signup = client.post(
            "/auth/signup",
            json={
                "name": "Auth User",
                "email": "auth@example.com",
                "password": "StrongPass123",
            },
        )
        duplicate = client.post(
            "/auth/signup",
            json={
                "name": "Auth User",
                "email": "auth@example.com",
                "password": "StrongPass123",
            },
        )
        invalid = client.post(
            "/auth/login",
            json={"email": "auth@example.com", "password": "wrong-password"},
        )
        login = client.post(
            "/auth/login",
            json={"email": "auth@example.com", "password": "StrongPass123"},
        )
        me = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {login.json()['data']['access_token']}"},
        )

    assert signup.status_code == 200
    assert duplicate.status_code == 400
    assert invalid.status_code == 401
    assert login.status_code == 200
    assert me.status_code == 200
    assert me.json()["email"] == "auth@example.com"
