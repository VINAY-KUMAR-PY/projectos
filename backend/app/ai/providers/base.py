from abc import ABC, abstractmethod

from app.ai.types import AIRequest, AIResponse, ProviderInfo


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


class AIProvider(ABC):
    name: str

    @abstractmethod
    def info(self) -> ProviderInfo:
        raise NotImplementedError

    @abstractmethod
    def generate(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError

    def estimate_cost_inr(self, request: AIRequest) -> int:
        info = self.info()
        input_tokens = estimate_tokens(request.prompt)
        output_tokens = request.max_tokens
        cost = (
            input_tokens * info.cost_per_1k_input_tokens_inr
            + output_tokens * info.cost_per_1k_output_tokens_inr
        ) / 1000
        return int(round(cost))
