from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai import AgentRun, Conversation, ConversationMessage
from app.models.workspace import ProjectMemory


def create_conversation(db: Session, owner_id: int, project_id: int | None, title: str):
    conversation = Conversation(owner_id=owner_id, project_id=project_id, title=title)
    db.add(conversation)
    return conversation


def get_conversation(db: Session, conversation_id: int, owner_id: int):
    return db.scalar(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.owner_id == owner_id,
        )
    )


def add_message(db: Session, conversation_id: int, owner_id: int, role: str, content: str):
    message = ConversationMessage(
        conversation_id=conversation_id,
        owner_id=owner_id,
        role=role,
        content=content,
    )
    db.add(message)
    return message


def list_messages(db: Session, conversation_id: int, owner_id: int, limit: int = 12):
    statement = (
        select(ConversationMessage)
        .where(
            ConversationMessage.conversation_id == conversation_id,
            ConversationMessage.owner_id == owner_id,
        )
        .order_by(ConversationMessage.id.desc())
        .limit(limit)
    )
    return list(reversed(db.scalars(statement).all()))


def list_project_memories(db: Session, project_id: int, owner_id: int, limit: int = 20):
    statement = (
        select(ProjectMemory)
        .where(ProjectMemory.project_id == project_id, ProjectMemory.owner_id == owner_id)
        .order_by(ProjectMemory.updated_at.desc(), ProjectMemory.id.desc())
        .limit(limit)
    )
    return db.scalars(statement).all()


def create_agent_run(
    db: Session,
    owner_id: int,
    project_id: int | None,
    conversation_id: int | None,
    agent_id: str,
    provider: str,
    model: str,
    prompt: str,
    output: str,
    status: str,
    input_tokens: int,
    output_tokens: int,
    estimated_cost_inr: int,
    error_message: str | None = None,
    agent_name: str | None = None,
    task_type: str | None = None,
    input_data: str | None = None,
    output_data: str | None = None,
    duration_seconds: int | None = None,
    confidence: int | None = None,
):
    run = AgentRun(
        owner_id=owner_id,
        project_id=project_id,
        conversation_id=conversation_id,
        agent_id=agent_id,
        agent_name=agent_name,
        task_type=task_type,
        provider=provider,
        model=model,
        prompt=prompt,
        input_data=input_data,
        output=output,
        output_data=output_data,
        status=status,
        duration_seconds=duration_seconds,
        confidence=confidence,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost_inr=estimated_cost_inr,
        error_message=error_message,
    )
    db.add(run)
    return run
