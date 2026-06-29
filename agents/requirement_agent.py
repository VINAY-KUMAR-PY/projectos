from core.base_agent import BaseAgent

class RequirementAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Requirement Analyzer Agent",
            role="Extract project requirements, features, and constraints."
        )

    def run(self, user_input, context=None):
        return {
            "agent": self.name,
            "features": [
                "Project workspace",
                "AI agents",
                "File upload analysis",
                "Documentation generation",
                "Code generation",
                "PPT generation"
            ],
            "constraints": [
                "Low initial cost",
                "Cloud-based",
                "Scalable for global users"
            ]
        }