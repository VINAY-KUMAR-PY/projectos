from datetime import datetime
from typing import Any


class MemoryEngine:
    def __init__(self):
        self.projects: dict[str, dict] = {}
        self.chroma_client = None
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings
            from app.config.settings import settings

            self.chroma_client = chromadb.PersistentClient(
                path=settings.chroma_persist_dir,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
        except Exception:
            self.chroma_client = None

    def get_or_create_collection(self, project_id: str):
        if not self.chroma_client:
            return None
        return self.chroma_client.get_or_create_collection(
            name=f"project_{project_id}",
            metadata={"hnsw:space": "cosine"},
        )

    def save_to_memory(
        self,
        project_id: str,
        category: str,
        content: str,
        metadata: dict | None = None,
    ):
        collection = self.get_or_create_collection(project_id)
        if collection:
            collection.upsert(
                ids=[f"{category}_{project_id}_{datetime.now().timestamp()}"],
                documents=[content],
                metadatas=[{"category": category, **(metadata or {})}],
            )
            return
        self.create_project(project_id)
        self.projects[project_id].setdefault("memory", []).append(
            {"category": category, "content": content, "metadata": metadata or {}}
        )

    def search_memory(self, project_id: str, query: str, n_results: int = 5):
        collection = self.get_or_create_collection(project_id)
        if collection:
            return collection.query(query_texts=[query], n_results=n_results)
        memories = self.projects.get(project_id, {}).get("memory", [])
        query_lower = query.lower()
        return [
            memory
            for memory in memories
            if query_lower in memory["content"].lower()
            or query_lower in memory["category"].lower()
        ][:n_results]

    def get_project_context(self, project_id: str) -> dict:
        collection = self.get_or_create_collection(project_id)
        if collection:
            all_data = collection.get()
            context = {}
            for index, doc_id in enumerate(all_data["ids"]):
                category = all_data["metadatas"][index].get("category", "general")
                context[category] = all_data["documents"][index]
            return context
        return self.load(project_id)

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

    def load(self, project_name: str) -> dict:
        return self.projects.get(project_name, {})

    def list_projects(self):
        return list(self.projects.keys())


memory_engine = MemoryEngine()
