from sqlalchemy.orm import Session

from app.ai.memory import ConversationMemory, ProjectMemoryConnector
from app.services.workspace_service import get_project


class ContextBuilder:
    def __init__(self, db: Session):
        self.db = db

    def build(
        self,
        owner_id: int,
        project_id: int | None,
        conversation_id: int | None,
        user_prompt: str,
    ) -> dict:
        sections = []
        if project_id is not None:
            project = get_project(self.db, project_id, owner_id)
            sections.append(
                "Project:\n"
                f"- title: {project.title}\n"
                f"- status: {project.status}\n"
                f"- description: {project.description or ''}"
            )
            memories = ProjectMemoryConnector(self.db).load(project_id, owner_id)
            if memories:
                memory_text = "\n".join(
                    f"- {memory['key']}: {memory['value']}" for memory in memories
                )
                sections.append(f"Project memory:\n{memory_text}")

        if conversation_id is not None:
            messages = ConversationMemory(self.db).recent_messages(conversation_id, owner_id)
            if messages:
                conversation_text = "\n".join(
                    f"{message.role}: {message.content}" for message in messages
                )
                sections.append(f"Recent conversation:\n{conversation_text}")

        sections.append(f"User request:\n{user_prompt}")
        return {
            "context": "\n\n".join(sections),
            "project_id": project_id,
            "conversation_id": conversation_id,
        }
