from app.agents.architecture_agent import ArchitectureAgent
from app.agents.coding_agent import CodingAgent
from app.agents.deployment_agent import DeploymentAgent
from app.agents.diagram_agent import DiagramAgent
from app.agents.documentation_agent import DocumentationAgent
from app.agents.file_video_agent import FileVideoAgent
from app.agents.learning_viva_agent import LearningVivaAgent
from app.agents.presentation_agent import PresentationAgent
from app.agents.requirement_agent import RequirementAgent
from app.agents.research_agent import ResearchAgent
from app.agents.testing_agent import TestingAgent


class AgentRouter:
    def __init__(self):
        self.routes = {
            "requirements": RequirementAgent(),
            "research": ResearchAgent(),
            "architecture": ArchitectureAgent(),
            "coding": CodingAgent(),
            "documentation": DocumentationAgent(),
            "diagrams": DiagramAgent(),
            "presentation": PresentationAgent(),
            "testing": TestingAgent(),
            "deployment": DeploymentAgent(),
            "learning": LearningVivaAgent(),
            "file_analysis": FileVideoAgent(),
        }

    def register(self, task_type, agent):
        self.routes[task_type] = agent

    def route(self, task_type, user_input, context=None):
        agent = self.routes.get(task_type)

        if not agent:
            return {
                "status": "error",
                "message": f"No agent found for task type: {task_type}"
            }

        return agent.run(user_input, context)

    def get_available_agents(self):
        return list(self.routes.keys())


agent_router = AgentRouter()
