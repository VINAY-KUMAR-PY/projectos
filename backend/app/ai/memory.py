from sqlalchemy.orm import Session

from app.repositories import ai_repository
from app.models.workspace import ProjectMemory


class ConversationMemory:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(self, owner_id: int, project_id: int | None, conversation_id: int | None, title: str):
        if conversation_id:
            conversation = ai_repository.get_conversation(self.db, conversation_id, owner_id)
            if conversation:
                return conversation
        conversation = ai_repository.create_conversation(self.db, owner_id, project_id, title)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def append(self, conversation_id: int, owner_id: int, role: str, content: str):
        message = ai_repository.add_message(self.db, conversation_id, owner_id, role, content)
        self.db.commit()
        self.db.refresh(message)
        return message

    def recent_messages(self, conversation_id: int, owner_id: int, limit: int = 12):
        return ai_repository.list_messages(self.db, conversation_id, owner_id, limit)


class ProjectMemoryConnector:
    def __init__(self, db: Session):
        self.db = db

    def load(self, project_id: int, owner_id: int, limit: int = 20):
        memories = ai_repository.list_project_memories(self.db, project_id, owner_id, limit)
        return [{"key": memory.key, "value": memory.value} for memory in memories]

    def save(self, project_id: int, owner_id: int, key: str, value: str):
        memory = ProjectMemory(
            project_id=project_id,
            owner_id=owner_id,
            key=key[:120],
            value=value,
        )
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory
