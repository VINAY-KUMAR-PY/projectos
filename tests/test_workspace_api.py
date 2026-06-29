from fastapi.testclient import TestClient

from conftest import auth_headers, fresh_app


def create_workspace_and_project(client, headers):
    workspace = client.post(
        "/workspaces",
        json={"name": "Launch Lab", "description": "Student startup workspace"},
        headers=headers,
    )
    project = client.post(
        f"/workspaces/{workspace.json()['id']}/projects",
        json={
            "title": "AI Study Planner",
            "description": "Planner with project memory",
            "status": "active",
        },
        headers=headers,
    )
    return workspace.json(), project.json()


def test_workspace_project_child_resource_crud(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client)
        workspace, project = create_workspace_and_project(client, headers)

        workspace_list = client.get("/workspaces?search=launch", headers=headers)
        project_list = client.get("/projects?status=active&search=study", headers=headers)
        workspace_update = client.patch(
            f"/workspaces/{workspace['id']}",
            json={"description": "Updated workspace"},
            headers=headers,
        )
        project_update = client.patch(
            f"/projects/{project['id']}",
            json={"status": "review"},
            headers=headers,
        )

        task = client.post(
            f"/projects/{project['id']}/tasks",
            json={"title": "Design API", "status": "todo", "priority": "high"},
            headers=headers,
        )
        task_list = client.get(
            f"/projects/{project['id']}/tasks?status=todo&search=design",
            headers=headers,
        )
        task_update = client.patch(
            f"/tasks/{task.json()['id']}",
            json={"status": "done"},
            headers=headers,
        )
        task_get = client.get(f"/tasks/{task.json()['id']}", headers=headers)

        note = client.post(
            f"/projects/{project['id']}/notes",
            json={"title": "MVP Notes", "content": "Keep infra under budget"},
            headers=headers,
        )
        notes = client.get(
            f"/projects/{project['id']}/notes?search=infra",
            headers=headers,
        )
        note_get = client.get(f"/notes/{note.json()['id']}", headers=headers)

        file_record = client.post(
            f"/projects/{project['id']}/files",
            json={
                "file_name": "brief.pdf",
                "file_type": "application/pdf",
                "storage_path": "local/brief.pdf",
                "file_size": 1200,
            },
            headers=headers,
        )
        files = client.get(
            f"/projects/{project['id']}/files?file_type=application/pdf",
            headers=headers,
        )
        file_get = client.get(f"/files/{file_record.json()['id']}", headers=headers)

        memory = client.post(
            f"/projects/{project['id']}/memory",
            json={"key": "business_model", "value": "Stage 1 pricing is 499 INR"},
            headers=headers,
        )
        memories = client.get(
            f"/projects/{project['id']}/memory?search=pricing",
            headers=headers,
        )
        memory_get = client.get(f"/memory/{memory.json()['id']}", headers=headers)

        delete_task = client.delete(f"/tasks/{task.json()['id']}", headers=headers)
        delete_note = client.delete(f"/notes/{note.json()['id']}", headers=headers)
        delete_file = client.delete(f"/files/{file_record.json()['id']}", headers=headers)
        delete_memory = client.delete(f"/memory/{memory.json()['id']}", headers=headers)

    assert workspace["name"] == "Launch Lab"
    assert workspace_list.json()["pagination"]["total"] == 1
    assert workspace_update.json()["description"] == "Updated workspace"
    assert project["workspace_id"] == workspace["id"]
    assert project_list.json()["items"][0]["title"] == "AI Study Planner"
    assert project_update.json()["status"] == "review"
    assert task_update.json()["status"] == "done"
    assert task_get.json()["title"] == "Design API"
    assert task_list.json()["pagination"]["total"] == 1
    assert notes.json()["items"][0]["title"] == "MVP Notes"
    assert note_get.json()["content"] == "Keep infra under budget"
    assert files.json()["items"][0]["file_name"] == "brief.pdf"
    assert file_get.json()["storage_path"] == "local/brief.pdf"
    assert memories.json()["items"][0]["key"] == "business_model"
    assert memory_get.json()["value"] == "Stage 1 pricing is 499 INR"
    assert delete_task.status_code == 204
    assert delete_note.status_code == 204
    assert delete_file.status_code == 204
    assert delete_memory.status_code == 204


def test_project_and_workspace_delete_cascade(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client)
        workspace, project = create_workspace_and_project(client, headers)
        task = client.post(
            f"/projects/{project['id']}/tasks",
            json={"title": "Cascade task"},
            headers=headers,
        )
        delete_project = client.delete(f"/projects/{project['id']}", headers=headers)
        missing_task = client.get(f"/tasks/{task.json()['id']}", headers=headers)
        delete_workspace = client.delete(f"/workspaces/{workspace['id']}", headers=headers)
        missing_workspace = client.get(f"/workspaces/{workspace['id']}", headers=headers)

    assert delete_project.status_code == 204
    assert missing_task.status_code == 404
    assert delete_workspace.status_code == 204
    assert missing_workspace.status_code == 404


def test_workspace_ownership_isolation(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        owner_headers = auth_headers(client, "owner@example.com")
        other_headers = auth_headers(client, "other@example.com")
        workspace, project = create_workspace_and_project(client, owner_headers)

        forbidden_workspace = client.get(
            f"/workspaces/{workspace['id']}",
            headers=other_headers,
        )
        forbidden_project = client.get(
            f"/projects/{project['id']}",
            headers=other_headers,
        )
        forbidden_child_create = client.post(
            f"/projects/{project['id']}/tasks",
            json={"title": "Steal task"},
            headers=other_headers,
        )
        unauthenticated = client.get("/workspaces")

    assert forbidden_workspace.status_code == 404
    assert forbidden_project.status_code == 404
    assert forbidden_child_create.status_code == 404
    assert unauthenticated.status_code == 401
