from pydantic import BaseModel, EmailStr, Field


class VideoAnalysisResponse(BaseModel):
    file_id: int
    transcript: str
    key_frames: list[dict]
    summary: str
    action_items: list[str]
    mistakes: list[str]
    viva_questions: list[str]


class GeneratedFileResponse(BaseModel):
    output_id: int
    file_url: str
    title: str
    content: str | None = None
    metadata: dict = Field(default_factory=dict)


class DiagramGenerateRequest(BaseModel):
    diagram_type: str = Field(pattern="^(usecase|er|class|sequence|flowchart|architecture|schema|gantt)$")


class CodeBuildRequest(BaseModel):
    action: str = Field(default="generate", pattern="^(generate|explain|review|fix_bug)$")
    prompt: str | None = Field(default=None, max_length=20000)
    file_id: int | None = None


class ReviewRequest(BaseModel):
    file_id: int | None = None


class DeploymentGenerateRequest(BaseModel):
    target: str = Field(pattern="^(vercel|netlify|railway|render|aws|docker|github-pages)$")


class TeamInviteRequest(BaseModel):
    email: EmailStr
    role: str = Field(default="viewer", pattern="^(owner|editor|viewer)$")


class CommentCreateRequest(BaseModel):
    entity_type: str = Field(pattern="^(task|file|output|project)$")
    entity_id: int
    body: str = Field(min_length=1, max_length=5000)


class TaskAssignRequest(BaseModel):
    task_id: int
    assignee_email: EmailStr
    role: str = Field(default="owner", max_length=50)


class ApprovalRequestCreate(BaseModel):
    output_id: int
    reviewer_email: EmailStr
    note: str | None = Field(default=None, max_length=4000)


class ApprovalDecisionRequest(BaseModel):
    status: str = Field(pattern="^(approved|rejected)$")
    note: str | None = Field(default=None, max_length=4000)


class LearningRequest(BaseModel):
    project_id: int
    message: str = Field(min_length=1, max_length=12000)


class MarketplacePublishRequest(BaseModel):
    item_type: str = Field(pattern="^(template|ui-kit|prompt|workflow|report-format|project-pack)$")
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=4000)
    price_inr: int = Field(default=0, ge=0)
    content_ref: str = Field(min_length=1, max_length=500)


class MarketplaceUseRequest(BaseModel):
    workspace_id: int | None = None


class IntegrationLinkRequest(BaseModel):
    provider: str = Field(pattern="^(github|google-drive|slack|discord|jira|trello|notion|figma|vscode|cursor)$")
    access_token: str | None = Field(default=None, max_length=5000)
    external_account_id: str | None = Field(default=None, max_length=255)


class RepoImportRequest(BaseModel):
    repo_url: str = Field(min_length=1, max_length=1000)
    workspace_id: int | None = None


class TotpVerifyRequest(BaseModel):
    code: str = Field(min_length=6, max_length=8)


class RazorpayCheckoutRequest(BaseModel):
    plan: str = Field(min_length=1, max_length=50)
