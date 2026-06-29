from sqlalchemy.orm import Session

from app.ai.context import ContextBuilder
from app.ai.memory import ConversationMemory
from app.ai.types import AIRequest
from app.repositories import ai_repository


class AgentExecutionEngine:
    def __init__(self, db: Session, ai_manager, prompt_manager, agent_registry):
        self.db = db
        self.ai_manager = ai_manager
        self.prompt_manager = prompt_manager
        self.agent_registry = agent_registry

    def execute(
        self,
        owner_id: int,
        agent_id: str,
        user_prompt: str,
        project_id: int | None = None,
        conversation_id: int | None = None,
        provider: str | None = None,
        template_id: str | None = None,
        variables: dict | None = None,
    ) -> dict:
        agent = self.agent_registry.get(agent_id)
        memory = ConversationMemory(self.db)
        conversation = memory.get_or_create(
            owner_id=owner_id,
            project_id=project_id,
            conversation_id=conversation_id,
            title=user_prompt[:80] or "AI conversation",
        )
        context = ContextBuilder(self.db).build(
            owner_id=owner_id,
            project_id=project_id,
            conversation_id=conversation.id,
            user_prompt=user_prompt,
        )
        rendered_prompt = self.prompt_manager.render(
            template_id or agent.prompt_template_id,
            {"input": context["context"], **(variables or {})},
        )
        response = self.ai_manager.generate(
            AIRequest(prompt=rendered_prompt, metadata={"agent_id": agent_id}),
            preferred_provider=provider,
        )

        memory.append(conversation.id, owner_id, "user", user_prompt)
        memory.append(conversation.id, owner_id, "assistant", response.content)

        run = ai_repository.create_agent_run(
            db=self.db,
            owner_id=owner_id,
            project_id=project_id,
            conversation_id=conversation.id,
            agent_id=agent_id,
            provider=response.provider,
            model=response.model,
            prompt=rendered_prompt,
            output=response.content,
            status="success",
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            estimated_cost_inr=response.estimated_cost_inr,
        )
        self.db.commit()
        self.db.refresh(run)

        return {
            "agent_run_id": run.id,
            "conversation_id": conversation.id,
            "agent_id": agent_id,
            "provider": response.provider,
            "model": response.model,
            "output": response.content,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            "estimated_cost_inr": response.estimated_cost_inr,
        }
