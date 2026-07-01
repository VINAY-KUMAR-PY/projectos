from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.stage1_schema import RazorpayCheckoutRequest
from app.services import stage1_service

router = APIRouter(prefix="/api/billing", tags=["Billing"])


@router.post("/razorpay/create")
def create_razorpay_checkout(
    request: RazorpayCheckoutRequest,
    current_user: User = Depends(get_current_user),
):
    return stage1_service.create_razorpay_checkout(current_user, request.plan)
