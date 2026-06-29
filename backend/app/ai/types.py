from dataclasses import dataclass, field


@dataclass(frozen=True)
class AIMessage:
    role: str
    content: str


@dataclass(frozen=True)
class AIRequest:
    prompt: str
    system_prompt: str | None = None
    messages: list[AIMessage] = field(default_factory=list)
    model: str | None = None
    max_tokens: int = 800
    temperature: float = 0.2
    metadata: dict | None = None


@dataclass(frozen=True)
class AIUsage:
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass(frozen=True)
class AIResponse:
    content: str
    provider: str
    model: str
    usage: AIUsage = field(default_factory=AIUsage)
    estimated_cost_inr: int = 0
    raw: dict | None = None


@dataclass(frozen=True)
class ProviderInfo:
    name: str
    model: str
    configured: bool
    cost_per_1k_input_tokens_inr: float
    cost_per_1k_output_tokens_inr: float
    supports_local: bool = False
