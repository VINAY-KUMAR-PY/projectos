from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrationCapability:
    provider: str
    supports_import: bool
    supports_export: bool
    status: str


class IntegrationProvider:
    """Small interface for Stage 1 integrations."""

    name = "base"

    def capability(self) -> IntegrationCapability:
        return IntegrationCapability(self.name, False, False, "placeholder")
