from agents.requirement_agent import RequirementAgent

class ProjectManagerAgent:
    def __init__(self):
        self.requirement_agent = RequirementAgent()

    def run(self, user_input):
        requirements = self.requirement_agent.run(user_input)

        return {
            "agent": "Project Manager Agent",
            "message": "ProjectOS plan created successfully.",
            "requirements": requirements,
            "next_steps": [
                "Create architecture plan",
                "Generate documentation",
                "Generate code",
                "Create diagrams",
                "Prepare PPT"
            ]
        }