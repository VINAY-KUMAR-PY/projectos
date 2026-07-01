from io import BytesIO

from fastapi.testclient import TestClient

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
    assert twofa.json()["secret"]
    assert verify.json()["enabled"] is True
    assert export.json()["projects"]
    assert billing.json()["provider"] == "razorpay"


def test_free_plan_project_limit_returns_upgrade_message(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "stage1-limit@example.com")
        create_project(client, headers, "First")
        create_project(client, headers, "Second")
        denied = client.post("/api/projects", json={"title": "Third"}, headers=headers)

    assert denied.status_code == 402
    assert "project limit reached" in denied.json()["message"]
