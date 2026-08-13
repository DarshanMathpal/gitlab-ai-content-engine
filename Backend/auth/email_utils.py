"""
auth/email_utils.py
---------------------
Sends signup verification emails using Resend.
"""

import os
import resend

from database.audit_log import log_event


RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# For initial testing, Resend provides onboarding@resend.dev.
# Later we can replace this with your verified project sender.
RESEND_FROM = os.getenv("RESEND_FROM", "onboarding@resend.dev")


def send_verification_code(email: str, code: str) -> None:
    if not RESEND_API_KEY:
        # Local development fallback
        print(f"[DEV EMAIL] Verification code for {email}: {code}")
        log_event(
            "verification_code_logged_dev_mode",
            job_id=None,
            email=email,
        )
        return

    resend.api_key = RESEND_API_KEY

    resend.Emails.send(
        {
            "from": RESEND_FROM,
            "to": [email],
            "subject": "Your verification code",
            "text": (
                f"Your verification code is: {code}\n\n"
                "This code expires in 15 minutes."
            ),
        }
    )

    print(f"SUCCESS: Verification email sent to {email}")