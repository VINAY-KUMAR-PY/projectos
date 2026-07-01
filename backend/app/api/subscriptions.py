from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.models.workspace import Subscription
from app.schemas.platform_schema import CheckoutRequest

router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

PLANS = [
    {"name": "free", "price_inr": 0, "projects": 2, "agent_runs": 10, "file_upload": "10MB"},
    {"name": "student", "price_inr": 299, "projects": 5, "agent_runs": 50, "file_upload": "50MB"},
    {"name": "pro", "price_inr": 499, "projects": 20, "agent_runs": 200, "file_upload": "200MB"},
    {"name": "team", "price_inr": 999, "projects": "Unlimited", "agent_runs": "Unlimited", "file_upload": "1GB"},
    {"name": "enterprise", "price_inr": 4999, "projects": "Unlimited", "agent_runs": "Unlimited", "file_upload": "10GB"},
]


@router.get("/plans")
def plans():
    return {"items": PLANS}


@router.get("/my-plan")
def my_plan(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = db.scalar(
        select(Subscription)
        .where(Subscription.user_id == current_user.id)
        .order_by(Subscription.id.desc())
    )
    return subscription or {"plan": current_user.subscription_plan, "status": "active"}


@router.post("/create")
def create_checkout(request: CheckoutRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = Subscription(user_id=current_user.id, plan=request.plan, status="pending")
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return {
        "subscription_id": subscription.id,
        "plan": request.plan,
        "checkout_url": None,
        "message": "Stripe checkout is not configured in development",
    }
