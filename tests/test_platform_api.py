from fastapi.testclient import TestClient

from conftest import auth_headers, fresh_app


def test_api_prefixed_auth_projects_tasks_outputs_dashboard_and_subscriptions(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "platform@example.com")
        me = client.get("/api/auth/me", headers=headers)
        project = client.post(
            "/api/projects",
            json={"title": "Platform Project", "description": "Full platform smoke"},
            headers=headers,
        )
        project_id = project.json()["id"]
        projects = client.get("/api/projects", headers=headers)
        progress = client.get(f"/api/projects/{project_id}/progress", headers=headers)
        task = client.post(
            f"/api/tasks/{project_id}",
            json={"title": "Build API aliases"},
            headers=headers,
        )
        generated = client.post(f"/api/tasks/generate/{project_id}", headers=headers)
        output = client.post(
            "/api/outputs",
            json={
                "project_id": project_id,
                "output_type": "docs",
                "title": "Readme",
                "content": "Project docs",
            },
            headers=headers,
        )
        outputs = client.get(f"/api/outputs/{project_id}", headers=headers)
        export = client.post(
            f"/api/outputs/{output.json()['id']}/export",
            json={"format": "markdown"},
            headers=headers,
        )
        plans = client.get("/api/subscriptions/plans")
        checkout = client.post(
            "/api/subscriptions/create",
            json={"plan": "pro"},
            headers=headers,
        )
        dashboard = client.get("/api/dashboard", headers=headers)

    assert me.status_code == 200
    assert project.status_code == 201
    assert projects.json()["pagination"]["total"] == 1
    assert progress.json()["completion_status"] == "in_progress"
    assert task.status_code == 201
    assert generated.status_code == 200
    assert outputs.json()["items"][0]["title"] == "Readme"
    assert export.json()["content"] == "Project docs"
    assert plans.json()["items"][2]["name"] == "pro"
    assert checkout.json()["plan"] == "pro"
    assert dashboard.json()["stats"]["total_projects"] == 1


def test_api_agents_run_and_history(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client, "agents-platform@example.com")
        project = client.post(
            "/api/projects",
            json={"title": "Agent Platform"},
            headers=headers,
        )
        project_id = project.json()["id"]
        available = client.get("/api/agents", headers=headers)
        run = client.post(
            "/api/agents/run",
            json={
                "project_id": project_id,
                "agent_type": "requirements",
                "user_input": "Build a student project planner",
            },
            headers=headers,
        )
        history = client.get(f"/api/agents/runs/{project_id}", headers=headers)
        run_detail = client.get(f"/api/agents/run/{run.json()['run_id']}", headers=headers)
        chat = client.post(
            "/api/agents/chat",
            json={"project_id": project_id, "message": "What should I do next?"},
            headers=headers,
        )

    assert available.json()["items"][0] == "requirements"
    assert run.status_code == 200
    assert run.json()["result"]["status"] == "success"
    assert history.json()["items"]
    assert run_detail.json()["id"] == run.json()["run_id"]
    assert chat.status_code == 200


def test_testing_agent_scorecard_is_data_derived(monkeypatch, tmp_path):
    fresh_app(monkeypatch, tmp_path)

    from app.agents.testing_agent import TestingAgent

    agent = TestingAgent()
    sparse = agent.run("ship it", {"description": "", "memory": ""})["data"]["scorecard"]
    rich = agent.run(
        "Create pytest integration tests, documentation, presentation demo, and viva checklist",
        {
            "description": "A documented project workflow with setup, report, and demo details." * 6,
            "memory": "pytest edge cases integration documentation slides demo viva " * 10,
        },
    )["data"]["scorecard"]

    assert sparse != rich
    assert sparse != {
        "code_quality": 80,
        "documentation_completeness": 78,
        "testing_coverage": 70,
        "presentation_readiness": 76,
        "project_improvement_score": 77,
    }
    assert all(0 <= value <= 100 for value in rich.values())
