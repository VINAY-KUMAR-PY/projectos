from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.integrations.base import IntegrationCapability
from app.models.user import User
from app.schemas.stage1_schema import IntegrationLinkRequest, RepoImportRequest
from app.services import stage1_service

router = APIRouter(prefix="/api/integrations", tags=["Integrations"])


@router.get("")
def capabilities():
    providers = [
        IntegrationCapability("github", True, True, "oauth-ready"),
        IntegrationCapability("google-drive", True, True, "oauth-ready"),
        IntegrationCapability("slack", False, False, "placeholder"),
        IntegrationCapability("discord", False, False, "placeholder"),
        IntegrationCapability("jira", False, False, "placeholder"),
        IntegrationCapability("trello", False, False, "placeholder"),
        IntegrationCapability("notion", False, False, "placeholder"),
        IntegrationCapability("figma", False, False, "placeholder"),
        IntegrationCapability("vscode", False, False, "placeholder"),
        IntegrationCapability("cursor", False, False, "placeholder"),
    ]
    return {"items": [item.__dict__ for item in providers]}


@router.get("/github/oauth-url")
def github_oauth_url(current_user: User = Depends(get_current_user)):
    return stage1_service.github_oauth_url()


@router.get("/google-drive/oauth-url")
def drive_oauth_url(current_user: User = Depends(get_current_user)):
    return stage1_service.drive_oauth_url()


@router.post("/link")
def link_integration(
    request: IntegrationLinkRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.link_integration(db, current_user, request)


@router.get("/linked")
def linked_integrations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"items": stage1_service.list_integrations(db, current_user)}


@router.post("/github/import")
def import_github_repo(
    request: RepoImportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.import_repo(db, current_user, request)


@router.post("/github/push-code")
def push_generated_code(current_user: User = Depends(get_current_user)):
    return {"status": "ready", "message": "GitHub push uses linked OAuth token in production; no cloud call is made in Stage 1 mock mode."}


@router.post("/google-drive/import")
def import_drive_file(current_user: User = Depends(get_current_user)):
    return {"status": "ready", "message": "Google Drive import is OAuth-ready; file fetch is enabled when credentials are configured."}


@router.post("/google-drive/export")
def export_drive_file(current_user: User = Depends(get_current_user)):
    return {"status": "ready", "message": "Google Drive export is OAuth-ready; upload is enabled when credentials are configured."}
