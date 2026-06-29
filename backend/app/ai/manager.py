from app.ai.cost import CostAwareProviderSelector
from app.ai.registry import ProviderRegistry, create_provider_registry
from app.ai.types import AIRequest, AIResponse
from app.config.settings import settings


class AIManager:
    def __init__(self, registry: ProviderRegistry, selector: CostAwareProviderSelector):
        self.registry = registry
        self.selector = selector

    def generate(
        self,
        request: AIRequest,
        preferred_provider: str | None = None,
    ) -> AIResponse:
        provider = self.selector.select(request, preferred_provider)
        return provider.generate(request)

    def providers(self):
        return [
            {
                "name": provider.info().name,
                "model": provider.info().model,
                "configured": provider.info().configured,
                "supports_local": provider.info().supports_local,
            }
            for provider in self.registry.list()
        ]


def create_ai_manager() -> AIManager:
    registry = create_provider_registry()
    selector = CostAwareProviderSelector(
        registry=registry,
        default_provider=settings.ai_provider,
        allowed_providers=[
            provider.strip()
            for provider in settings.ai_allowed_providers.split(",")
            if provider.strip()
        ],
        max_request_cost_inr=settings.ai_max_request_cost_inr,
    )
    return AIManager(registry, selector)
