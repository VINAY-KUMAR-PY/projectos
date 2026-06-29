from datetime import datetime
from typing import Dict, Any


class MemoryEngine:
    """
    Stores and retrieves project information.
    """

    def __init__(self):
        self.projects = {}

    def create_project(self, project_name: str):
        if project_name not in self.projects:
            self.projects[project_name] = {
                "created_at": datetime.now().isoformat(),
                "requirements": {},
                "documents": {},
                "code": {},
                "diagrams": {},
                "files": [],
                "videos": [],
                "tasks": [],
                "logs": []
            }

    def save(self, project_name: str, category: str, data: Any):
        self.create_project(project_name)

        self.projects[project_name][category] = data

    def load(self, project_name: str) -> Dict:
        return self.projects.get(project_name, {})

    def list_projects(self):
        return list(self.projects.keys())
