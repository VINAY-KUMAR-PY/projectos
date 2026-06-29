import json
from urllib import request as urlrequest

from app.ai.providers.base import AIProvider, estimate_tokens
from app.ai.types import AIRequest, AIResponse, AIUsage, ProviderInfo


class GeminiProvider(AIProvider):
    name = "gemini"

    def __init__(self, api_key: str | None, model: str):
        self.api_key = api_key
        self.model = model

    def info(self) -> ProviderInfo:
        return ProviderInfo(
            name=self.name,
            model=self.model,
            configured=bool(self.api_key),
            cost_per_1k_input_tokens_inr=0.003,
            cost_per_1k_output_tokens_inr=0.012,
        )

    def generate(self, request: AIRequest) -> AIResponse:
        if not self.api_key:
            raise RuntimeError("Gemini provider is not configured")

        prompt = request.prompt
        if request.system_prompt:
            prompt = f"{request.system_prompt}\n\n{prompt}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": request.max_tokens,
                "temperature": request.temperature,
            },
        }
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{request.model or self.model}:generateContent?key={self.api_key}"
        )
        http_request = urlrequest.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlrequest.urlopen(http_request, timeout=30) as response:
            raw = json.loads(response.read().decode("utf-8"))

        content = raw["candidates"][0]["content"]["parts"][0]["text"]
        return AIResponse(
            content=content,
            provider=self.name,
            model=request.model or self.model,
            usage=AIUsage(
                input_tokens=estimate_tokens(prompt),
                output_tokens=estimate_tokens(content),
            ),
            estimated_cost_inr=self.estimate_cost_inr(request),
            raw=raw,
        )
