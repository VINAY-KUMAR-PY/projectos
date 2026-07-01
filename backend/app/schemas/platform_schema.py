from pydantic import BaseModel, Field


class ProjectApiCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: str = "draft"
    workspace_id: int | None = None


class AgentRunRequest(BaseModel):
    project_id: int
    agent_type: str = Field(min_length=1, max_length=120)
    user_input: str = Field(min_length=1, max_length=20000)


class AgentRunAllRequest(BaseModel):
    project_id: int
    user_input: str = Field(default="Run the full ProjectOS planning pipeline", min_length=1, max_length=20000)


class AgentChatRequest(BaseModel):
    project_id: int
    message: str = Field(min_length=1, max_length=20000)


class OutputCreate(BaseModel):
    project_id: int
    output_type: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=500)
    content: str = Field(min_length=1)
    format: str = "markdown"


class OutputExportRequest(BaseModel):
    format: str = Field(pattern="^(markdown|txt|pdf|docx|pptx)$")


class CheckoutRequest(BaseModel):
    plan: str = Field(min_length=1, max_length=50)
