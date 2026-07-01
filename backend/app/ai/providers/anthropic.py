import json
from urllib import request as urlrequest

from app.ai.providers.base import AIProvider, estimate_tokens
from app.ai.types import AIRequest, AIResponse, AIUsage, ProviderInfo


class AnthropicProvider(AIProvider):
    name = "anthropic"

    def __init__(self, api_key: str | None, model: str):
        self.api_key = api_key
        self.model = model

    def info(self) -> ProviderInfo:
        return ProviderInfo(
            name=self.name,
            model=self.model,
            configured=bool(self.api_key),
            cost_per_1k_input_tokens_inr=0.25,
            cost_per_1k_output_tokens_inr=1.25,
        )

    def generate(self, request: AIRequest) -> AIResponse:
        if not self.api_key:
            raise RuntimeError("Anthropic provider is not configured")

        payload = {
            "model": request.model or self.model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "system": request.system_prompt or "",
            "messages": [{"role": "user", "content": request.prompt}],
        }
        http_request = urlrequest.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlrequest.urlopen(http_request, timeout=60) as response:
            raw = json.loads(response.read().decode("utf-8"))

        content = raw["content"][0]["text"]
        usage = raw.get("usage", {})
        return AIResponse(
            content=content,
            provider=self.name,
            model=payload["model"],
            usage=AIUsage(
                input_tokens=usage.get("input_tokens", estimate_tokens(request.prompt)),
                output_tokens=usage.get("output_tokens", estimate_tokens(content)),
            ),
            estimated_cost_inr=self.estimate_cost_inr(request),
            raw=raw,
        )
