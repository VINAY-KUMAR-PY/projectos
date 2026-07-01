from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.stage1_schema import MarketplacePublishRequest, MarketplaceUseRequest
from app.services import stage1_service

router = APIRouter(prefix="/api/marketplace", tags=["Marketplace"])


@router.get("")
def list_marketplace(search: str | None = None, item_type: str | None = None, db: Session = Depends(get_db)):
    return {"items": stage1_service.list_marketplace(db, search, item_type)}


@router.post("")
def publish_item(
    request: MarketplacePublishRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.publish_marketplace_item(db, current_user, request)


@router.post("/{item_id}/use")
def use_item(
    item_id: int,
    request: MarketplaceUseRequest | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return stage1_service.use_marketplace_item(db, item_id, current_user, request or MarketplaceUseRequest())
