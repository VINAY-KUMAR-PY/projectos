from agents.requirement_agent import RequirementAgent
from core.memory import MemoryEngine


class ProjectManagerAgent:
    def __init__(self):
        self.requirement_agent = RequirementAgent()
        self.memory = MemoryEngine()

    def run(self, user_input):
        project_name = user_input

        self.memory.create_project(project_name)

        requirements = self.requirement_agent.run(user_input)

        self.memory.save(
            project_name=project_name,
            category="requirements",
            data=requirements
        )

        project_memory = self.memory.load(project_name)

        return {
            "agent": "Project Manager Agent",
            "message": "ProjectOS plan created and saved in memory.",
            "project_name": project_name,
            "requirements": requirements,
            "memory": project_memory,
            "next_steps": [
                "Create architecture plan",
                "Generate documentation",
                "Generate code",
                "Create diagrams",
                "Prepare PPT"
            ]
        }