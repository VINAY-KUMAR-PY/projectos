from dataclasses import dataclass


@dataclass(frozen=True)
class AgentDefinition:
    id: str
    name: str
    description: str
    prompt_template_id: str = "project_assistant"


class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, AgentDefinition] = {}

    def register(self, agent: AgentDefinition):
        self._agents[agent.id] = agent

    def get(self, agent_id: str) -> AgentDefinition:
        if agent_id not in self._agents:
            raise ValueError(f"Unknown agent: {agent_id}")
        return self._agents[agent_id]

    def list(self) -> list[AgentDefinition]:
        return list(self._agents.values())


def create_agent_registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(
        AgentDefinition(
            id="core_assistant",
            name="Core Assistant",
            description="Generic AI Core execution entry point for future agents.",
            prompt_template_id="project_assistant",
        )
    )
    return registry
