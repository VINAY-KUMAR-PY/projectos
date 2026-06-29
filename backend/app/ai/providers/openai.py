import json
from urllib import request as urlrequest

from app.ai.providers.base import AIProvider, estimate_tokens
from app.ai.types import AIRequest, AIResponse, AIUsage, ProviderInfo


class OpenAIProvider(AIProvider):
    name = "openai"

    def __init__(self, api_key: str | None, model: str):
        self.api_key = api_key
        self.model = model

    def info(self) -> ProviderInfo:
        return ProviderInfo(
            name=self.name,
            model=self.model,
            configured=bool(self.api_key),
            cost_per_1k_input_tokens_inr=0.013,
            cost_per_1k_output_tokens_inr=0.052,
        )

    def generate(self, request: AIRequest) -> AIResponse:
        if not self.api_key:
            raise RuntimeError("OpenAI provider is not configured")

        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.extend({"role": msg.role, "content": msg.content} for msg in request.messages)
        messages.append({"role": "user", "content": request.prompt})

        payload = {
            "model": request.model or self.model,
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        }
        http_request = urlrequest.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlrequest.urlopen(http_request, timeout=30) as response:
            raw = json.loads(response.read().decode("utf-8"))

        content = raw["choices"][0]["message"]["content"]
        usage = raw.get("usage", {})
        return AIResponse(
            content=content,
            provider=self.name,
            model=payload["model"],
            usage=AIUsage(
                input_tokens=usage.get("prompt_tokens", estimate_tokens(request.prompt)),
                output_tokens=usage.get("completion_tokens", estimate_tokens(content)),
            ),
            estimated_cost_inr=self.estimate_cost_inr(request),
            raw=raw,
        )
