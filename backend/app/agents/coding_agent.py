from app.core.base_agent import BaseAgent


class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Coding Agent",
            role="Generate source code, README, setup steps, and code review guidance.",
            system_prompt=(
                "You are a senior coding assistant. Generate practical module-by-module "
                "code plans, file structures, README content, setup instructions, and bug review notes. "
                "Respect any language/framework in context."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output, {"code_plan_markdown": output}, ["Implement modules", "Run tests"])
