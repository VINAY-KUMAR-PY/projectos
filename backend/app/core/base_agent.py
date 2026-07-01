from app.ai.manager import create_ai_manager
from app.ai.types import AIRequest


class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str | None = None):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt or role

    def call_ai(self, user_message: str, context: dict | None = None) -> str:
        context_text = f"Project context:\n{context}\n\n" if context else ""
        response = create_ai_manager().generate(
            AIRequest(
                prompt=f"{context_text}Task:\n{user_message}",
                system_prompt=self.system_prompt,
                max_tokens=1600,
            )
        )
        return response.content

    def standard_response(
        self,
        task: str,
        output: str,
        data: dict | None = None,
        next_steps: list[str] | None = None,
        confidence: float = 0.86,
    ):
        return {
            "status": "success",
            "agent": self.name,
            "task": task,
            "summary": output[:500],
            "data": data or {"output": output},
            "next_steps": next_steps or [],
            "confidence": confidence,
        }

    def run(self, user_input: str, context: dict | None = None) -> dict:
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output)
