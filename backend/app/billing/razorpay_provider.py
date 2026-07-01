class RazorpayProvider:
    """Stage 1 billing seam: mock by default, real SDK can replace this later."""

    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode

    def create_checkout(self, plan: str, amount_inr: int, user_email: str):
        return {
            "provider": "razorpay",
            "mode": "mock" if self.mock_mode else "live",
            "plan": plan,
            "amount_inr": amount_inr,
            "user_email": user_email,
            "checkout_url": None,
        }
