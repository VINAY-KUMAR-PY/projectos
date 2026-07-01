from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.stage1 import UsageRecord
from app.models.user import User
from app.models.workspace import Project, ProjectFile, Subscription


PLAN_LIMITS = {
    "free": {"projects": 2, "agent_runs": 10, "storage_mb": 10},
    "student": {"projects": 5, "agent_runs": 50, "storage_mb": 50},
    "pro": {"projects": 20, "agent_runs": 200, "storage_mb": 200},
    "team": {"projects": None, "agent_runs": None, "storage_mb": 1024},
    "enterprise": {"projects": None, "agent_runs": None, "storage_mb": 10240},
}


def current_cycle() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def get_active_plan(db: Session, user: User) -> str:
    subscription = db.scalar(
        select(Subscription)
        .where(Subscription.user_id == user.id, Subscription.status.in_(["active", "pending"]))
        .order_by(Subscription.id.desc())
    )
    return (subscription.plan if subscription else user.subscription_plan) or "free"


def _limit_response(plan: str, metric: str, limit):
    raise HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail=f"{metric} limit reached for {plan} plan. Upgrade to continue. Limit: {limit}",
    )


def assert_project_limit(db: Session, user: User):
    plan = get_active_plan(db, user)
    limit = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])["projects"]
    if limit is None:
        return
    count = db.scalar(select(func.count()).select_from(Project).where(Project.owner_id == user.id)) or 0
    if count >= limit:
        _limit_response(plan, "project", limit)


def assert_agent_run_limit(db: Session, user: User):
    plan = get_active_plan(db, user)
    limit = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])["agent_runs"]
    if limit is None:
        return
    used = (
        db.scalar(
            select(func.coalesce(func.sum(UsageRecord.amount), 0)).where(
                UsageRecord.user_id == user.id,
                UsageRecord.metric == "agent_run",
                UsageRecord.cycle == current_cycle(),
            )
        )
        or 0
    )
    if used >= limit:
        _limit_response(plan, "agent run", limit)


def assert_storage_limit(db: Session, user: User, additional_bytes: int = 0):
    plan = get_active_plan(db, user)
    limit_mb = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])["storage_mb"]
    if limit_mb is None:
        return
    used_bytes = (
        db.scalar(
            select(func.coalesce(func.sum(ProjectFile.file_size), 0)).where(
                ProjectFile.owner_id == user.id,
            )
        )
        or 0
    )
    if used_bytes + additional_bytes > limit_mb * 1024 * 1024:
        _limit_response(plan, "storage", f"{limit_mb}MB")


def record_usage(db: Session, user_id: int, metric: str, amount: int = 1, project_id: int | None = None):
    record = UsageRecord(
        user_id=user_id,
        project_id=project_id,
        metric=metric,
        amount=amount,
        cycle=current_cycle(),
    )
    db.add(record)
    return record
