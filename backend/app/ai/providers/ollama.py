import json
from urllib import request as urlrequest

from app.ai.providers.base import AIProvider, estimate_tokens
from app.ai.types import AIRequest, AIResponse, AIUsage, ProviderInfo


class OllamaProvider(AIProvider):
    name = "ollama"

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def info(self) -> ProviderInfo:
        return ProviderInfo(
            name=self.name,
            model=self.model,
            configured=bool(self.base_url),
            cost_per_1k_input_tokens_inr=0,
            cost_per_1k_output_tokens_inr=0,
            supports_local=True,
        )

    def generate(self, request: AIRequest) -> AIResponse:
        prompt = request.prompt
        if request.system_prompt:
            prompt = f"{request.system_prompt}\n\n{prompt}"

        payload = {
            "model": request.model or self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
        }
        http_request = urlrequest.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlrequest.urlopen(http_request, timeout=60) as response:
            raw = json.loads(response.read().decode("utf-8"))

        content = raw.get("response", "")
        return AIResponse(
            content=content,
            provider=self.name,
            model=payload["model"],
            usage=AIUsage(
                input_tokens=estimate_tokens(prompt),
                output_tokens=estimate_tokens(content),
            ),
            estimated_cost_inr=0,
            raw=raw,
        )
