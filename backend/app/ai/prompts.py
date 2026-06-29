from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplate:
    id: str
    name: str
    template: str


class PromptManager:
    def __init__(self):
        self._templates: dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate):
        self._templates[template.id] = template

    def get(self, template_id: str) -> PromptTemplate:
        if template_id not in self._templates:
            raise ValueError(f"Unknown prompt template: {template_id}")
        return self._templates[template_id]

    def render(self, template_id: str, variables: dict | None = None) -> str:
        template = self.get(template_id)
        return template.template.format(**(variables or {}))

    def list(self):
        return list(self._templates.values())


def create_prompt_manager() -> PromptManager:
    manager = PromptManager()
    manager.register(
        PromptTemplate(
            id="default",
            name="Default Assistant",
            template="{input}",
        )
    )
    manager.register(
        PromptTemplate(
            id="project_assistant",
            name="Project Assistant",
            template=(
                "You are ProjectOS AI Core. Help with this project request.\n"
                "Request:\n{input}\n\n"
                "Use project context when available."
            ),
        )
    )
    manager.register(
        PromptTemplate(
            id="memory_summary",
            name="Memory Summary",
            template="Summarize the important project memory from:\n{input}",
        )
    )
    return manager
