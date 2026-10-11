"""Email OTP verification for signup.

Flow: register creates an unverified user and issues a 6-digit code,
``verify-otp`` checks it and activates the account, ``resend-otp`` issues a
fresh code. Codes are stored as SHA-256 hashes, expire after 10 minutes, die
after 5 wrong guesses, and resends are throttled to one per minute.

Delivery mirrors the forgot-password pattern: real SMTP when configured,
otherwise (local development) the code is printed to the server log and
returned in the ``dev_otp`` response field.
"""
from __future__ import annotations

import hashlib
import secrets
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

from sqlalchemy import func, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import EmailOTP, User
from app.services.common import naive_utc_now

OTP_TTL_MINUTES = 10
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_COOLDOWN_SECONDS = 60


class OtpError(ValueError):
    """User-facing OTP failure with a stable, matchable message."""


def hash_otp(code: str) -> str:
    return hashlib.sha256(code.strip().encode("utf-8")).hexdigest()


def _as_naive(value: datetime) -> datetime:
    # SQLite returns naive datetimes, Postgres aware ones; stored instants are UTC.
    if value.tzinfo is not None:
        return value.replace(tzinfo=None)
    return value


def ensure_user_columns(engine: Engine) -> int:
    """Add ``users.is_verified`` to databases created before this feature.

    Existing accounts predate verification, so they are grandfathered as
    verified instead of being locked out. Returns rows backfilled.
    """
    from sqlalchemy import inspect, text

    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    backfilled = 0
    with engine.begin() as connection:
        if "is_verified" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE"))
            # The column is brand new, so every row predates verification.
            backfilled = connection.execute(text("UPDATE users SET is_verified = TRUE")).rowcount or 0
        else:
            backfilled = connection.execute(
                text("UPDATE users SET is_verified = TRUE WHERE is_verified IS NULL")
            ).rowcount or 0
    return backfilled


def _latest_otp(db: Session, user_id: int) -> EmailOTP | None:
    return db.scalar(
        select(EmailOTP)
        .where(EmailOTP.user_id == user_id, EmailOTP.purpose == "signup")
        .order_by(EmailOTP.id.desc())
        .limit(1)
    )


def issue_signup_otp(db: Session, user: User) -> tuple[str, EmailOTP]:
    """Create a fresh code, invalidating any previous ones. Returns (plain, row)."""
    now = naive_utc_now()
    latest = _latest_otp(db, user.id)
    if latest is not None:
        elapsed = (now - _as_naive(latest.created_at)).total_seconds()
        if elapsed < OTP_RESEND_COOLDOWN_SECONDS:
            wait = int(OTP_RESEND_COOLDOWN_SECONDS - elapsed) + 1
            raise OtpError(f"An OTP was just sent - please wait {wait}s before requesting a new one.")
    db.query(EmailOTP).filter(
        EmailOTP.user_id == user.id,
        EmailOTP.purpose == "signup",
        EmailOTP.consumed.is_(False),
    ).update({"consumed": True})
    plain = f"{secrets.randbelow(1_000_000):06d}"
    row = EmailOTP(
        user_id=user.id,
        otp_hash=hash_otp(plain),
        purpose="signup",
        expires_at=now + timedelta(minutes=OTP_TTL_MINUTES),
        attempts=0,
        consumed=False,
    )
    db.add(row)
    db.commit()
    return plain, row


def verify_signup_otp(db: Session, email: str, code: str) -> User:
    """Check a code; on success the account is verified. Raises OtpError."""
    user = db.scalar(select(User).where(func.lower(User.email) == email.strip().lower()))
    if user is None:
        raise OtpError("Invalid code - check it and try again.")
    if user.is_verified:
        raise OtpError("This email is already verified - please log in.")
    row = _latest_otp(db, user.id)
    if row is None or row.consumed:
        raise OtpError("No active code for this email - request a new one.")
    if _as_naive(row.expires_at) <= naive_utc_now():
        raise OtpError("This code has expired - request a new one.")
    if row.attempts >= OTP_MAX_ATTEMPTS:
        raise OtpError("Too many wrong attempts - request a new code.")
    if row.otp_hash != hash_otp(code):
        row.attempts += 1
        db.commit()
        left = OTP_MAX_ATTEMPTS - row.attempts
        raise OtpError(
            f"Invalid code - {left} attempt{'s' if left != 1 else ''} left." if left > 0
            else "Too many wrong attempts - request a new code."
        )
    row.consumed = True
    user.is_verified = True
    db.commit()
    return user


def _send_email(to: str, subject: str, body: str) -> None:
    from fastapi import HTTPException, status

    message = EmailMessage()
    message["From"] = settings.email_from
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
            server.starttls()
            if settings.smtp_user:
                server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(message)
    except (smtplib.SMTPException, OSError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email",
        )


def send_signup_otp(user: User, plain: str) -> bool:
    """Deliver the code. Returns True when a real email went out (False = dev mode)."""
    if not settings.smtp_host and settings.environment == "development":
        print(f"[otp] verification code for {user.email}: {plain}", flush=True)
        return False
    _send_email(
        user.email,
        "CareerPrep Hub - your verification code",
        f"Hi {user.full_name},\n\nYour CareerPrep Hub verification code is:\n\n{plain}\n\n"
        f"It expires in {OTP_TTL_MINUTES} minutes. If you did not sign up, ignore this email.",
    )
    return True
