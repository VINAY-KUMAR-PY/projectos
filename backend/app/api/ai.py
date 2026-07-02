from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.agents.engine import AgentExecutionEngine
from app.ai.agents.registry import create_agent_registry
from app.ai.manager import create_ai_manager
from app.ai.prompts import create_prompt_manager
from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.ai_schema import AIExecuteRequest, AIExecuteResponse
from app.services.workspace_service import get_owned_project

router = APIRouter(prefix="/ai", tags=["AI Core"])


@router.get("/providers")
def list_providers(current_user: User = Depends(get_current_user)):
    return {"items": create_ai_manager().providers()}


@router.get("/agents")
def list_agents(current_user: User = Depends(get_current_user)):
    return {"items": [agent.__dict__ for agent in create_agent_registry().list()]}


@router.post("/execute", response_model=AIExecuteResponse)
def execute_ai(
    request: AIExecuteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if request.project_id is not None:
        get_owned_project(db, request.project_id, current_user.id)
    engine = AgentExecutionEngine(
        db=db,
        ai_manager=create_ai_manager(),
        prompt_manager=create_prompt_manager(),
        agent_registry=create_agent_registry(),
    )
    try:
        return engine.execute(
            owner_id=current_user.id,
            agent_id=request.agent_id,
            user_prompt=request.prompt,
            project_id=request.project_id,
            conversation_id=request.conversation_id,
            provider=request.provider,
            template_id=request.template_id,
            variables=request.variables,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
