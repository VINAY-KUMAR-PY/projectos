from app.ai.types import AIRequest


class CostAwareProviderSelector:
    def __init__(
        self,
        registry,
        default_provider: str,
        allowed_providers: list[str],
        max_request_cost_inr: int,
    ):
        self.registry = registry
        self.default_provider = default_provider
        self.allowed_providers = allowed_providers
        self.max_request_cost_inr = max_request_cost_inr

    def select(self, request: AIRequest, preferred_provider: str | None = None):
        if preferred_provider:
            provider = self.registry.get(preferred_provider)
            self._ensure_usable(provider, request)
            return provider

        candidates = []
        ordered_names = [self.default_provider] + [
            name for name in self.allowed_providers if name != self.default_provider
        ]
        for provider_name in ordered_names:
            try:
                provider = self.registry.get(provider_name)
            except ValueError:
                continue
            if provider.info().configured:
                cost = provider.estimate_cost_inr(request)
                if cost <= self.max_request_cost_inr:
                    candidates.append((cost, provider))

        if not candidates:
            raise RuntimeError("No configured AI provider is available within cost limits")

        candidates.sort(key=lambda candidate: (candidate[0], candidate[1].name != self.default_provider))
        return candidates[0][1]

    def _ensure_usable(self, provider, request: AIRequest):
        if provider.name not in self.allowed_providers:
            raise RuntimeError(f"AI provider is not allowed: {provider.name}")
        if not provider.info().configured:
            raise RuntimeError(f"AI provider is not configured: {provider.name}")
        if provider.estimate_cost_inr(request) > self.max_request_cost_inr:
            raise RuntimeError(f"AI provider exceeds request cost limit: {provider.name}")
