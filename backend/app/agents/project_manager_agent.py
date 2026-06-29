from app.agents.requirement_agent import RequirementAgent
from app.core.memory import MemoryEngine
from app.core.router import AgentRouter


class ProjectManagerAgent:
    def __init__(self):
        self.memory = MemoryEngine()
        self.router = AgentRouter()

        self.router.register("requirements", RequirementAgent())

    def run(self, user_input):
        project_name = user_input

        self.memory.create_project(project_name)

        requirements = self.router.route(
            task_type="requirements",
            user_input=user_input
        )

        self.memory.save(
            project_name=project_name,
            category="requirements",
            data=requirements
        )

        project_memory = self.memory.load(project_name)

        return {
            "agent": "Project Manager Agent",
            "message": "ProjectOS plan created using router and saved in memory.",
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
