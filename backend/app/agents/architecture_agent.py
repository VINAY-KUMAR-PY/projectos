from app.core.base_agent import BaseAgent


class ArchitectureAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Architecture Agent",
            role="Design architecture, APIs, modules, database schema, folder structure, and patterns.",
            system_prompt=(
                "You are a senior software architect. Produce clear architecture, modules, "
                "API endpoints, data model, folder structure, deployment shape, and tradeoffs."
            ),
        )

    def run(self, user_input, context=None):
        output = self.call_ai(user_input, context)
        return self.standard_response(user_input, output, {"architecture_markdown": output}, ["Review architecture", "Generate implementation plan"])
