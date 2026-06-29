from fastapi.testclient import TestClient

from conftest import auth_headers, fresh_app


def create_project_with_memory(client, headers):
    workspace = client.post(
        "/workspaces",
        json={"name": "AI Core Workspace"},
        headers=headers,
    ).json()
    project = client.post(
        f"/workspaces/{workspace['id']}/projects",
        json={"title": "AI Core Project", "status": "active"},
        headers=headers,
    ).json()
    client.post(
        f"/projects/{project['id']}/memory",
        json={"key": "budget", "value": "Keep monthly infra below 2000 INR"},
        headers=headers,
    )
    return project


def test_prompt_registry_and_cost_selector(monkeypatch, tmp_path):
    fresh_app(monkeypatch, tmp_path)

    from app.ai.manager import create_ai_manager
    from app.ai.prompts import create_prompt_manager
    from app.ai.types import AIRequest

    prompt_manager = create_prompt_manager()
    rendered = prompt_manager.render("project_assistant", {"input": "Build MVP"})
    ai_manager = create_ai_manager()
    response = ai_manager.generate(AIRequest(prompt=rendered))

    assert "Build MVP" in rendered
    assert response.provider == "mock"
    assert response.estimated_cost_inr == 0
    assert any(provider["name"] == "mock" for provider in ai_manager.providers())


def test_ai_execute_api_persists_conversation_and_agent_run(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        headers = auth_headers(client)
        project = create_project_with_memory(client, headers)

        providers = client.get("/ai/providers", headers=headers)
        agents = client.get("/ai/agents", headers=headers)
        execute = client.post(
            "/ai/execute",
            json={
                "agent_id": "core_assistant",
                "project_id": project["id"],
                "prompt": "Plan the next step with budget context",
            },
            headers=headers,
        )
        body = execute.json()
        second_execute = client.post(
            "/ai/execute",
            json={
                "agent_id": "core_assistant",
                "project_id": project["id"],
                "conversation_id": body["conversation_id"],
                "prompt": "Continue the same conversation",
            },
            headers=headers,
        )

        from app.database.connection import SessionLocal
        from app.models.ai import AgentRun, ConversationMessage
        from sqlalchemy import select

        db = SessionLocal()
        try:
            runs = db.scalars(select(AgentRun)).all()
            messages = db.scalars(select(ConversationMessage)).all()
        finally:
            db.close()

    assert providers.status_code == 200
    assert providers.json()["items"][0]["name"] == "mock"
    assert agents.status_code == 200
    assert agents.json()["items"][0]["id"] == "core_assistant"
    assert execute.status_code == 200
    assert body["provider"] == "mock"
    assert "budget" in body["output"].lower()
    assert second_execute.json()["conversation_id"] == body["conversation_id"]
    assert len(runs) == 2
    assert len(messages) == 4


def test_ai_execute_rejects_unknown_agent_and_unauthorized_project(monkeypatch, tmp_path):
    app = fresh_app(monkeypatch, tmp_path)

    with TestClient(app) as client:
        owner_headers = auth_headers(client, "ai-owner@example.com")
        other_headers = auth_headers(client, "ai-other@example.com")
        project = create_project_with_memory(client, owner_headers)

        unknown_agent = client.post(
            "/ai/execute",
            json={"agent_id": "missing", "prompt": "Hello"},
            headers=owner_headers,
        )
        unauthorized_project = client.post(
            "/ai/execute",
            json={
                "agent_id": "core_assistant",
                "project_id": project["id"],
                "prompt": "Should not access this project",
            },
            headers=other_headers,
        )
        no_auth = client.get("/ai/providers")

    assert unknown_agent.status_code == 400
    assert unauthorized_project.status_code == 404
    assert no_auth.status_code == 401
