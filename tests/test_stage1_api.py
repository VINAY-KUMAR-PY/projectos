from io import BytesIO
from pathlib import Path
import zipfile

from fastapi.testclient import TestClient
from sqlalchemy import select

from conftest import auth_headers, fresh_app


def create_project(client: TestClient, headers: dict, title: str = "Stage 1 Project") -> int:
    response = client.post("/api/projects", json={"title": title, "description": "Stage 1 smoke"}, headers=headers)
    assert response.status_code == 201
    return response.json()["id"]


def test_upload_analyzer_video_and_generation_endpoints(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "stage1-generation@example.com")
        project_id = create_project(client, headers)
        upload = client.post(
            f"/api/files/upload/{project_id}",
            files={"upload": ("notes.txt", BytesIO(b"ProjectOS parses uploaded text."), "text/plain")},
            headers=headers,
        )
        file_id = upload.json()["id"]
        analyze = client.post(f"/api/files/analyze/{file_id}", headers=headers)
        video = client.post(f"/api/files/{file_id}/analyze-video", headers=headers)
        document = client.post(f"/api/projects/{project_id}/generate-document", headers=headers)
        ppt = client.post(f"/api/projects/{project_id}/generate-ppt", headers=headers)
        diagram = client.post(f"/api/projects/{project_id}/generate-diagram?type=architecture", headers=headers)
        code = client.post(f"/api/projects/{project_id}/build-code", json={"action": "generate"}, headers=headers)
        review = client.post(f"/api/projects/{project_id}/review", json={}, headers=headers)
        deploy = client.post(f"/api/projects/{project_id}/generate-deployment?target=railway", headers=headers)

    assert upload.status_code == 201
    assert analyze.status_code == 200
    assert "analysis" in analyze.json()
    assert video.status_code == 200
    assert "viva_questions" in video.json()
    assert document.status_code == 200
    assert document.json()["file_url"].endswith(".docx")
    assert ppt.status_code == 200
    assert diagram.json()["content"].startswith("flowchart")
    assert "zip_url" in code.json()["content"]
    assert review.json()["project_improvement_score"] > 0
    assert "railway" in deploy.json()["content"]


def test_collaboration_learning_marketplace_integrations_security_and_billing(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "stage1-collab@example.com")
        project_id = create_project(client, headers, "Collab Project")
        task = client.post(f"/api/tasks/{project_id}", json={"title": "Ship Stage 1"}, headers=headers)
        output = client.post(
            "/api/outputs",
            json={"project_id": project_id, "output_type": "docs", "title": "Doc", "content": "Content"},
            headers=headers,
        )
        invite = client.post(
            f"/api/collaboration/projects/{project_id}/members",
            json={"email": "friend@example.com", "role": "viewer"},
            headers=headers,
        )
        members = client.get(f"/api/collaboration/projects/{project_id}/members", headers=headers)
        comment = client.post(
            f"/api/collaboration/projects/{project_id}/comments",
            json={"entity_type": "project", "entity_id": project_id, "body": "Looks good"},
            headers=headers,
        )
        assignment = client.post(
            f"/api/collaboration/projects/{project_id}/task-assignments",
            json={"task_id": task.json()["id"], "assignee_email": "friend@example.com"},
            headers=headers,
        )
        approval = client.post(
            f"/api/collaboration/projects/{project_id}/approvals",
            json={"output_id": output.json()["id"], "reviewer_email": "friend@example.com"},
            headers=headers,
        )
        decision = client.post(
            f"/api/collaboration/approvals/{approval.json()['id']}/decision",
            json={"status": "approved"},
            headers=headers,
        )
        learning = client.post(
            "/api/agents/learning/explain_my_project",
            json={"project_id": project_id, "message": "Explain this simply"},
            headers=headers,
        )
        item = client.post(
            "/api/marketplace",
            json={
                "item_type": "template",
                "title": "Student Report Template",
                "description": "Reusable report format",
                "content_ref": "output:1",
            },
            headers=headers,
        )
        marketplace = client.get("/api/marketplace?search=Student")
        integrations = client.get("/api/integrations", headers=headers)
        link = client.post("/api/integrations/link", json={"provider": "github"}, headers=headers)
        github_import = client.post(
            "/api/integrations/github/import",
            json={"repo_url": "https://github.com/example/project"},
            headers=headers,
        )
        github_push = client.post("/api/integrations/github/push-code", headers=headers)
        drive_import = client.post("/api/integrations/google-drive/import", headers=headers)
        drive_export = client.post("/api/integrations/google-drive/export", headers=headers)
        twofa = client.post("/api/users/me/2fa/enable", headers=headers)
        verify = client.post("/api/users/me/2fa/verify", json={"code": "000000"}, headers=headers)
        export = client.get("/api/users/me/export", headers=headers)
        billing = client.post("/api/billing/razorpay/create", json={"plan": "pro"}, headers=headers)

    assert invite.status_code == 200
    assert members.json()["items"][0]["email"] == "friend@example.com"
    assert comment.json()["body"] == "Looks good"
    assert assignment.json()["assignee_email"] == "friend@example.com"
    assert decision.json()["status"] == "approved"
    assert learning.status_code == 200
    assert item.json()["title"] == "Student Report Template"
    assert marketplace.json()["items"]
    assert integrations.json()["items"][0]["provider"] == "github"
    assert link.json()["provider"] == "github"
    assert github_import.status_code == 200
    assert github_import.json()["mode"] == "mock"
    assert github_push.json()["status"] == "mock"
    assert drive_import.json()["mode"] == "mock"
    assert drive_export.json()["mode"] == "mock"
    assert twofa.json()["secret"]
    assert verify.json()["enabled"] is True
    assert export.json()["projects"]
    assert billing.json()["provider"] == "razorpay"


def test_configured_integrations_require_tokens_and_invalid_repo_is_rejected(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "stage1-integrations@example.com")
        invalid = client.post("/api/integrations/github/import", json={"repo_url": "https://example.com/project"}, headers=headers)
        github_link = client.post(
            "/api/integrations/link",
            json={"provider": "github", "access_token": "ghp_test_token"},
            headers=headers,
        )
        drive_link = client.post(
            "/api/integrations/link",
            json={"provider": "google-drive", "access_token": "drive_test_token"},
            headers=headers,
        )
        linked = client.get("/api/integrations/linked", headers=headers)
        github_import = client.post(
            "/api/integrations/github/import",
            json={"repo_url": "https://github.com/example/project.git"},
            headers=headers,
        )
        github_push = client.post("/api/integrations/github/push-code", headers=headers)
        drive_import = client.post("/api/integrations/google-drive/import", headers=headers)
        drive_export = client.post("/api/integrations/google-drive/export", headers=headers)

        from app.database.connection import SessionLocal
        from app.models.stage1 import UserIntegration

        db = SessionLocal()
        try:
            stored_github = db.scalar(
                select(UserIntegration).where(UserIntegration.provider == "github")
            )
        finally:
            db.close()

    assert invalid.status_code == 400
    assert github_link.json()["configured"] is True
    assert drive_link.json()["configured"] is True
    assert "ghp_test_token" not in github_link.text
    assert "drive_test_token" not in drive_link.text
    assert "ghp_test_token" not in linked.text
    assert "drive_test_token" not in linked.text
    assert stored_github.access_token != "ghp_test_token"
    assert stored_github.access_token.startswith("fernet:")
    assert github_import.json()["mode"] == "configured"
    assert github_import.json()["project_id"]
    assert "token" not in github_push.text.lower()
    assert github_push.json()["mode"] == "configured"
    assert drive_import.json()["mode"] == "configured"
    assert drive_export.json()["mode"] == "configured"


def test_review_score_uses_project_data(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "stage1-review@example.com")
        project_id = create_project(client, headers, "Scored Project")
        baseline = client.post(f"/api/projects/{project_id}/review", json={}, headers=headers)
        client.post(
            f"/api/tasks/{project_id}",
            json={"title": "Implement tests", "status": "done"},
            headers=headers,
        )
        client.post(
            f"/api/files/upload/{project_id}",
            files={"upload": ("README.md", BytesIO(b"# Project\n\nDocumented workflow."), "text/markdown")},
            headers=headers,
        )
        client.post(
            "/api/outputs",
            json={"project_id": project_id, "output_type": "document", "title": "Report", "content": "Generated report"},
            headers=headers,
        )
        enriched = client.post(f"/api/projects/{project_id}/review", json={}, headers=headers)

    assert baseline.status_code == 200
    assert enriched.status_code == 200
    assert baseline.json()["inputs"]["files"] == 0
    assert enriched.json()["inputs"]["files"] == 1
    assert enriched.json()["inputs"]["tasks"] == 1
    assert enriched.json()["inputs"]["generated_outputs"] >= 1
    assert enriched.json()["project_improvement_score"] != baseline.json()["project_improvement_score"]


def test_uploads_are_unique_and_deleted_with_record(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "stage1-files@example.com")
        project_id = create_project(client, headers, "Upload Lifecycle")
        first = client.post(
            f"/api/files/upload/{project_id}",
            files={"upload": ("notes.txt", BytesIO(b"first"), "text/plain")},
            headers=headers,
        )
        second = client.post(
            f"/api/files/upload/{project_id}",
            files={"upload": ("notes.txt", BytesIO(b"second"), "text/plain")},
            headers=headers,
        )
        from app.database.connection import SessionLocal
        from app.models.workspace import ProjectFile

        db = SessionLocal()
        try:
            first_record = db.get(ProjectFile, first.json()["id"])
            second_record = db.get(ProjectFile, second.json()["id"])
            first_path = Path(first_record.storage_path)
            second_path = Path(second_record.storage_path)
        finally:
            db.close()
        delete_first = client.delete(f"/api/files/{first.json()['id']}", headers=headers)

    assert first.status_code == 201
    assert second.status_code == 201
    assert "storage_path" not in first.json()
    assert first.json()["file_name"] == "notes.txt"
    assert second.json()["file_name"] == "notes.txt"
    assert first_path != second_path
    assert delete_first.status_code == 204
    assert not first_path.exists()
    assert second_path.exists()


def test_code_builder_rejects_cross_project_file_ids(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        owner_headers = auth_headers(client, "file-owner@example.com")
        other_headers = auth_headers(client, "file-other@example.com")
        owner_project = create_project(client, owner_headers, "Owner Project")
        other_project = create_project(client, other_headers, "Other Project")
        upload = client.post(
            f"/api/files/upload/{owner_project}",
            files={"upload": ("secret.py", BytesIO(b"api_key = 'abc'"), "text/x-python")},
            headers=owner_headers,
        )
        cross_project = client.post(
            f"/api/projects/{other_project}/build-code",
            json={"action": "review", "file_id": upload.json()["id"]},
            headers=other_headers,
        )

    assert cross_project.status_code == 404


def test_optional_file_parser_fallbacks_do_not_crash(tmp_path):
    from app.utils.file_processing import extract_key_frames, extract_video_transcript, parse_uploaded_file

    docx = tmp_path / "broken.docx"
    pptx = tmp_path / "broken.pptx"
    image = tmp_path / "image.png"
    video = tmp_path / "demo.mp4"
    archive = tmp_path / "source.zip"
    for path in [docx, pptx, image, video]:
        path.write_bytes(b"not a real optional file")
    with zipfile.ZipFile(archive, "w") as package:
        package.writestr("package.json", "{}")
        package.writestr("src/main.py", "print('hello')")

    assert "unavailable" in parse_uploaded_file(str(docx), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")["text"].lower()
    assert "unavailable" in parse_uploaded_file(str(pptx), "application/vnd.openxmlformats-officedocument.presentationml.presentation")["text"].lower()
    image_result = parse_uploaded_file(str(image), "image/png")
    assert image_result["metadata"]["parser"] in {"ocr-unavailable", "pytesseract"}
    zip_result = parse_uploaded_file(str(archive), "application/zip")
    assert {"Node.js", "Python"}.issubset(set(zip_result["metadata"]["tech_stack"]))
    assert extract_video_transcript(str(video))
    assert isinstance(extract_key_frames(str(video)), list)


def test_production_settings_fail_closed(monkeypatch, tmp_path):
    fresh_app(monkeypatch, tmp_path)

    from app.config.settings import Settings
    import pytest

    with pytest.raises(ValueError):
        Settings(environment="production", secret_key="real-secret", database_url="sqlite:///prod.db")
    with pytest.raises(ValueError):
        Settings(
            environment="production",
            secret_key="real-secret",
            database_url="postgresql://user:pass@localhost/db",
            cors_origins=["*"],
        )


def test_free_plan_project_limit_returns_upgrade_message(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "stage1-limit@example.com")
        create_project(client, headers, "First")
        create_project(client, headers, "Second")
        denied = client.post("/api/projects", json={"title": "Third"}, headers=headers)

    assert denied.status_code == 402
    assert "project limit reached" in denied.json()["message"]
