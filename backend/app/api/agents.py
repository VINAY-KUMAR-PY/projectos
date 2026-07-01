import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.memory import memory_engine
from app.core.router import agent_router
from app.database.connection import get_db
from app.models.ai import AgentRun
from app.models.user import User
from app.models.workspace import GeneratedOutput
from app.repositories.ai_repository import create_agent_run
from app.schemas.platform_schema import AgentChatRequest, AgentRunAllRequest, AgentRunRequest
from app.services.workspace_service import get_project

router = APIRouter(prefix="/api/agents", tags=["AI Agents"])


def run_agent_and_persist(db: Session, owner_id: int, project_id: int, agent_type: str, user_input: str):
    project = get_project(db, project_id, owner_id)
    context = {
        "project_id": project.id,
        "title": project.title,
        "description": project.description,
        "status": project.status,
        "memory": memory_engine.get_project_context(str(project.id)),
    }
    result = agent_router.route(agent_type, user_input, context)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message", "Agent failed"))

    output_text = json.dumps(result, ensure_ascii=True)
    memory_engine.save_to_memory(str(project.id), agent_type, output_text)
    run = create_agent_run(
        db=db,
        owner_id=owner_id,
        project_id=project.id,
        conversation_id=None,
        agent_id=agent_type,
        agent_name=result.get("agent", agent_type),
        task_type=agent_type,
        provider="ai_manager",
        model="configured",
        prompt=user_input,
        input_data=user_input,
        output=output_text,
        output_data=output_text,
        status="success",
        input_tokens=0,
        output_tokens=0,
        estimated_cost_inr=0,
        confidence=int(float(result.get("confidence", 0.85)) * 100),
    )
    generated = GeneratedOutput(
        owner_id=owner_id,
        project_id=project.id,
        output_type=agent_type,
        title=f"{agent_type.title()} Output",
        content=output_text,
        format="json",
    )
    db.add(generated)
    db.commit()
    db.refresh(run)
    return {"run_id": run.id, "result": result}


@router.get("")
def available_agents(current_user: User = Depends(get_current_user)):
    return {"items": agent_router.get_available_agents()}


@router.post("/run")
def run_agent(request: AgentRunRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return run_agent_and_persist(db, current_user.id, request.project_id, request.agent_type, request.user_input)


@router.post("/run-all")
def run_all_agents(request: AgentRunAllRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sequence = [
        "requirements",
        "research",
        "architecture",
        "coding",
        "documentation",
        "diagrams",
        "presentation",
        "testing",
        "deployment",
    ]
    results = [
        run_agent_and_persist(db, current_user.id, request.project_id, agent_type, request.user_input)
        for agent_type in sequence
    ]
    return {"project_id": request.project_id, "runs": results}


@router.get("/runs/{project_id}")
def list_agent_runs(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_project(db, project_id, current_user.id)
    runs = db.scalars(
        select(AgentRun)
        .where(AgentRun.project_id == project_id, AgentRun.owner_id == current_user.id)
        .order_by(AgentRun.id.desc())
    ).all()
    return {"items": runs}


@router.get("/run/{run_id}")
def get_agent_run(run_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    run = db.scalar(select(AgentRun).where(AgentRun.id == run_id, AgentRun.owner_id == current_user.id))
    if not run:
        raise HTTPException(status_code=404, detail="Agent run not found")
    return run


@router.post("/chat")
def chat(request: AgentChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return run_agent_and_persist(db, current_user.id, request.project_id, "requirements", request.message)
