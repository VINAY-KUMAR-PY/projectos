from pydantic import BaseModel, Field


class AIExecuteRequest(BaseModel):
    agent_id: str = Field(default="core_assistant", min_length=1, max_length=120)
    prompt: str = Field(min_length=1, max_length=20000)
    project_id: int | None = None
    conversation_id: int | None = None
    provider: str | None = Field(default=None, max_length=80)
    template_id: str | None = Field(default=None, max_length=120)
    variables: dict | None = None


class AIExecuteResponse(BaseModel):
    agent_run_id: int
    conversation_id: int
    agent_id: str
    provider: str
    model: str
    output: str
    usage: dict
    estimated_cost_inr: int
