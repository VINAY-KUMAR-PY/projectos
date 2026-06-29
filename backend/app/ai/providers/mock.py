from app.ai.providers.base import AIProvider, estimate_tokens
from app.ai.types import AIRequest, AIResponse, AIUsage, ProviderInfo


class MockProvider(AIProvider):
    name = "mock"

    def __init__(self, model: str = "mock-model"):
        self.model = model

    def info(self) -> ProviderInfo:
        return ProviderInfo(
            name=self.name,
            model=self.model,
            configured=True,
            cost_per_1k_input_tokens_inr=0,
            cost_per_1k_output_tokens_inr=0,
            supports_local=True,
        )

    def generate(self, request: AIRequest) -> AIResponse:
        content = (
            "Mock AI response: "
            + request.prompt.strip().replace("\n", " ")[:300]
        )
        return AIResponse(
            content=content,
            provider=self.name,
            model=request.model or self.model,
            usage=AIUsage(
                input_tokens=estimate_tokens(request.prompt),
                output_tokens=estimate_tokens(content),
            ),
            estimated_cost_inr=0,
            raw={"mock": True},
        )
