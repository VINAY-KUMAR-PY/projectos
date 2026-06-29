from app.ai.providers import (
    AIProvider,
    GeminiProvider,
    MockProvider,
    OllamaProvider,
    OpenAIProvider,
)
from app.config.settings import settings


class ProviderRegistry:
    def __init__(self):
        self._providers: dict[str, AIProvider] = {}

    def register(self, provider: AIProvider):
        self._providers[provider.name] = provider

    def get(self, name: str) -> AIProvider:
        if name not in self._providers:
            raise ValueError(f"Unknown AI provider: {name}")
        return self._providers[name]

    def list(self) -> list[AIProvider]:
        return list(self._providers.values())

    def configured(self) -> list[AIProvider]:
        return [provider for provider in self.list() if provider.info().configured]


def create_provider_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(MockProvider(model=settings.ai_model))
    registry.register(
        OllamaProvider(base_url=settings.ollama_base_url, model=settings.ollama_model)
    )
    registry.register(
        GeminiProvider(api_key=settings.gemini_api_key, model=settings.gemini_model)
    )
    registry.register(
        OpenAIProvider(api_key=settings.openai_api_key, model=settings.openai_model)
    )
    return registry
